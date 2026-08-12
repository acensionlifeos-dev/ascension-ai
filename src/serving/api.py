"""Standalone self-contained Ascension AI service."""

from __future__ import annotations

import asyncio
import hmac
import json
import os
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, field_validator

from src.core.capabilities import CAPABILITIES
from src.core.cognition import TALENTS, build_cognitive_packet, extract_memory_candidates, hybrid_retrieve
from src.core.contracts import Shell, Tier
from src.core.model_runtime import NativeInferenceQueueTimeout, runtime
from src.core.orchestrator import prepare_inference, respond, surface_plan


ROOT = Path(__file__).resolve().parents[2]
PUBLIC = ROOT / "public"
APP_VERSION = "2.3.1-native-alpha"
MAX_MESSAGES = 24
MAX_MESSAGE_LENGTH = 12_000


@asynccontextmanager
async def lifespan(_: FastAPI):
    try:
        await asyncio.to_thread(runtime.load)
    except Exception as error:
        print(f"Ascension native model did not load: {error}")
    yield


app = FastAPI(title="Ascension AI Native Core", version=APP_VERSION, lifespan=lifespan)
allowed_origins = [value.strip() for value in os.getenv("ASCENSION_AI_ALLOWED_ORIGINS", "").split(",") if value.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
app.mount("/static", StaticFiles(directory=str(PUBLIC)), name="static")


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=(), payment=()"
    response.headers["Cache-Control"] = "no-store" if request.url.path.startswith("/v1") or request.url.path in {"/chat", "/model/info"} else "public, max-age=300"
    return response


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=MAX_MESSAGE_LENGTH)

    @field_validator("content")
    @classmethod
    def clean_content(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("message cannot be empty")
        return cleaned


class IntelligenceRequest(BaseModel):
    shell: Shell = Shell.AP
    tier: Tier = Tier.LIFE_OS
    messages: list[ChatMessage] = Field(min_length=1, max_length=MAX_MESSAGES)
    context: dict = Field(default_factory=dict)
    surface: str = Field(default="chat", max_length=100)
    mode: Literal["conversation", "analysis", "planning", "proactive", "background"] = "conversation"
    allowed_capabilities: list[str] = Field(default_factory=list, max_length=100)
    temperature: float = Field(default=0.65, ge=0.0, le=1.2)
    max_tokens: int = Field(default=500, ge=32, le=1600)

    @field_validator("messages")
    @classmethod
    def require_user_turn(cls, value: list[ChatMessage]) -> list[ChatMessage]:
        if value[-1].role != "user":
            raise ValueError("the final message must be from the user")
        return value

    @field_validator("context")
    @classmethod
    def bound_context(cls, value: dict) -> dict:
        if len(json.dumps(value, default=str)) > 50_000:
            raise ValueError("context packet is too large")
        return value

    @field_validator("allowed_capabilities")
    @classmethod
    def validate_capabilities(cls, value: list[str]) -> list[str]:
        cleaned = list(dict.fromkeys(item.strip().lower() for item in value if item.strip()))
        unknown = [item for item in cleaned if item not in CAPABILITIES]
        if unknown:
            raise ValueError(f"unknown capabilities: {', '.join(unknown)}")
        return cleaned


class SurfacePlanRequest(BaseModel):
    shell: Shell = Shell.LIFE_OS
    tier: Tier = Tier.LIFE_OS
    trigger: str = Field(min_length=1, max_length=MAX_MESSAGE_LENGTH)
    context: dict = Field(default_factory=dict)
    available_actions: list[str] = Field(default_factory=list, max_length=100)
    allowed_capabilities: list[str] = Field(default_factory=list, max_length=100)


class CognitionRequest(SurfacePlanRequest):
    pass


class RetrievalRequest(BaseModel):
    query: str = Field(min_length=1, max_length=MAX_MESSAGE_LENGTH)
    context: dict = Field(default_factory=dict)
    top_k: int = Field(default=6, ge=1, le=10)


class MemoryCandidateRequest(BaseModel):
    text: str = Field(min_length=1, max_length=MAX_MESSAGE_LENGTH)


class LegacyGenerationRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=MAX_MESSAGE_LENGTH)
    max_new_tokens: int = Field(default=300, ge=32, le=1000)
    temperature: float = Field(default=0.65, ge=0.0, le=1.2)


def _authorized_token(authorization: str | None) -> bool:
    supplied = ""
    if authorization and authorization.lower().startswith("bearer "):
        supplied = authorization[7:].strip()
    expected = [
        os.getenv("ASCENSION_AI_TEST_TOKEN", "").strip(),
        os.getenv("ASCENSION_AI_SERVICE_TOKEN", "").strip(),
    ]
    return bool(supplied) and any(token and hmac.compare_digest(supplied, token) for token in expected)


def require_access(authorization: str | None = Header(default=None)) -> None:
    if not any(os.getenv(name, "").strip() for name in ("ASCENSION_AI_TEST_TOKEN", "ASCENSION_AI_SERVICE_TOKEN")):
        raise HTTPException(status_code=503, detail="Private Ascension AI access is not configured.")
    if not _authorized_token(authorization):
        raise HTTPException(status_code=401, detail="Invalid Ascension AI access code.")


def require_native_ready() -> None:
    if not runtime.status()["ready"]:
        raise HTTPException(status_code=503, detail=runtime.status()["error"] or "Ascension native model is not ready.")


def effective_max_tokens(requested: int, mode: str = "conversation") -> int:
    """Bound interactive latency while preserving deeper queued reasoning."""
    profile_limits = {"starter": 72, "standard": 420, "pro": 1200, "candidate": 1200, "deep": 1400}
    mode_limits = {"conversation": 160, "proactive": 240, "planning": 420, "analysis": 680, "background": 1200}
    return min(requested, profile_limits.get(runtime.profile_name, requested), mode_limits.get(mode, 240))


@app.get("/")
async def root() -> FileResponse:
    return FileResponse(PUBLIC / "index.html")


@app.get("/health")
async def health() -> dict:
    model = runtime.status()
    return {
        "status": "healthy" if model["ready"] else "loading_or_degraded",
        "version": APP_VERSION,
        "mode": "ascension_native_local",
        "candidate_ready": model["ready"],
        "replacement_ready": False,
        "provider": "ascension-native" if model["ready"] else None,
        "model": model["model"],
        "outside_provider": False,
        "test_access_configured": bool(os.getenv("ASCENSION_AI_TEST_TOKEN", "").strip()),
        "service_access_configured": bool(os.getenv("ASCENSION_AI_SERVICE_TOKEN", "").strip()),
        "runtime": model,
    }


@app.get("/v1/readiness")
async def replacement_readiness(_: None = Depends(require_access)) -> dict:
    required_gates = [
        "conversation_quality", "shell_isolation", "action_integrity",
        "domain_reasoning", "safety_privacy", "interactive_latency",
        "concurrency_recovery", "native_primary_canary",
    ]
    return {
        "candidate_ready": runtime.status()["ready"],
        "replacement_ready": False,
        "evaluation_suite": "replacement_readiness_prompts_v1",
        "evaluation_cases": 20,
        "required_gates": required_gates,
        "gates": {gate: False for gate in required_gates},
        "promotion_rule": "Every gate must pass before outside-model fallback is removed.",
        "runtime": runtime.status(),
    }


@app.get("/model/info")
async def model_info(_: None = Depends(require_access)) -> dict:
    return {
        "name": "Ascension AI Native Core",
        "version": APP_VERSION,
        "runtime": runtime.status(),
        "shells": [shell.value for shell in Shell],
        "tiers": [tier.value for tier in Tier],
        "capability_domains": list(CAPABILITIES),
        "outside_provider": False,
        "production_replacement_enabled": False,
        "promotion_rule": "Enable production replacement only after shell-specific evaluation gates pass.",
    }


@app.get("/v1/capabilities")
async def capabilities(_: None = Depends(require_access)) -> dict:
    return {
        "capabilities": CAPABILITIES,
        "shells": [shell.value for shell in Shell],
        "tiers": [tier.value for tier in Tier],
        "tier_scope": "all_ascension_tiers",
        "entitlement_rule": "The authenticated calling shell supplies and enforces tier permissions; the shared native core retains one capability model.",
    }


@app.get("/capabilities")
async def capabilities_compat(access: None = Depends(require_access)) -> dict:
    """Compatibility alias retained for Devin's original SDK consumers."""
    return await capabilities(access)


@app.get("/v1/talents")
async def talents(_: None = Depends(require_access)) -> dict:
    active = [key for key, value in TALENTS.items() if value["state"] == "active"]
    shell_required = [key for key, value in TALENTS.items() if value["state"] == "shell_required"]
    return {
        "talents": TALENTS,
        "counts": {"active": len(active), "shell_required": len(shell_required)},
        "active": active,
        "shell_required": shell_required,
        "truth_rule": "A talent is active only when this service can produce its structured intelligence now; shell-required talents depend on permissioned LifeOS integrations.",
    }


@app.post("/v1/cognition")
async def cognition(request: CognitionRequest, _: None = Depends(require_access)) -> dict:
    packet = build_cognitive_packet(
        request.trigger,
        request.context,
        request.allowed_capabilities,
        request.available_actions,
    )
    return {
        "shell": request.shell.value,
        "tier": request.tier.value,
        "surface": request.context.get("surface", "chat"),
        **packet,
        "outside_provider": False,
    }


@app.post("/v1/agent/plan")
async def agent_plan(request: CognitionRequest, access: None = Depends(require_access)) -> dict:
    """Plan but never silently execute; the authenticated product shell owns execution."""
    return await cognition(request, access)


@app.post("/v1/retrieve")
async def retrieve(request: RetrievalRequest, _: None = Depends(require_access)) -> dict:
    return {
        "query": request.query,
        "results": hybrid_retrieve(request.query, request.context, request.top_k),
        "scope": "request_supplied_permissioned_context",
        "outside_provider": False,
    }


@app.post("/v1/memory/candidates")
async def memory_candidates(request: MemoryCandidateRequest, _: None = Depends(require_access)) -> dict:
    return {
        "candidates": extract_memory_candidates(request.text),
        "persistence": "calling_shell_validates_and_persists",
        "outside_provider": False,
    }


@app.post("/v1/surface-plan")
async def plan_surfaces(request: SurfacePlanRequest, _: None = Depends(require_access)) -> dict:
    return surface_plan(
        shell=request.shell,
        tier=request.tier,
        trigger=request.trigger,
        context=request.context,
        available_actions=request.available_actions,
        allowed_capabilities=request.allowed_capabilities,
    )


@app.post("/v1/intelligence")
async def intelligence(request: IntelligenceRequest, _: None = Depends(require_access)) -> dict:
    require_native_ready()
    try:
        return await asyncio.to_thread(
            respond,
            shell=request.shell,
            tier=request.tier,
            messages=[message.model_dump() for message in request.messages],
            context=request.context,
            surface=request.surface,
            mode=request.mode,
            allowed_capabilities=request.allowed_capabilities,
            temperature=request.temperature,
            max_tokens=effective_max_tokens(request.max_tokens, request.mode),
        )
    except NativeInferenceQueueTimeout as error:
        raise HTTPException(status_code=504, detail=str(error)) from error
    except RuntimeError as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=502, detail=str(error)) from error


@app.post("/chat")
async def chat(request: IntelligenceRequest, access: None = Depends(require_access)) -> dict:
    return await intelligence(request, access)


@app.post("/v1/stream")
async def stream_intelligence(request: IntelligenceRequest, _: None = Depends(require_access)):
    require_native_ready()
    prepared = prepare_inference(
        shell=request.shell,
        tier=request.tier,
        messages=[message.model_dump() for message in request.messages],
        context=request.context,
        surface=request.surface,
        mode=request.mode,
        allowed_capabilities=request.allowed_capabilities,
    )

    def events():
        started = time.perf_counter()
        cognition_meta = prepared.get("cognition", {})
        meta = {
            key: value for key, value in prepared.items()
            if key not in {"messages", "cognition"}
        }
        meta["cognition"] = {
            "domains": cognition_meta.get("domains", []),
            "talents": [item.get("key") for item in cognition_meta.get("talents", [])],
            "memory_candidates": cognition_meta.get("memory_candidates", []),
            "action_proposals": cognition_meta.get("action_proposals", []),
            "surface_recommendations": cognition_meta.get("surface_recommendations", []),
        }
        meta.update({"model": runtime.status()["model"], "provider": "ascension-native", "outside_provider": False})
        yield f"event: meta\ndata: {json.dumps(meta, separators=(',', ':'))}\n\n"
        try:
            for token in runtime.stream_chat(prepared["messages"], request.temperature, effective_max_tokens(request.max_tokens, request.mode)):
                yield f"event: token\ndata: {json.dumps({'token': token}, ensure_ascii=False)}\n\n"
            done = {"latency_ms": round((time.perf_counter() - started) * 1000), "production_replacement_enabled": False}
            yield f"event: done\ndata: {json.dumps(done, separators=(',', ':'))}\n\n"
        except Exception as error:
            yield f"event: error\ndata: {json.dumps({'message': str(error)})}\n\n"

    return StreamingResponse(events(), media_type="text/event-stream", headers={"X-Accel-Buffering": "no", "Cache-Control": "no-store"})


@app.post("/generate")
async def generate(request: LegacyGenerationRequest, access: None = Depends(require_access)) -> dict:
    result = await intelligence(
        IntelligenceRequest(
            shell=Shell.CORE,
            messages=[ChatMessage(role="user", content=request.prompt)],
            surface="legacy_generate",
            mode="analysis",
            max_tokens=request.max_new_tokens,
            temperature=request.temperature,
        ),
        access,
    )
    return {
        "content": result["content"],
        "model": result["model"],
        "provider": result["provider"],
        "tokens_generated": result.get("usage", {}).get("completion_tokens", 0),
        "generation_time_ms": result["latency_ms"],
        "mode": "ascension_native_local",
    }
