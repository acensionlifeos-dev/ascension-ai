"""Collect fail-closed evidence from a live Ascension native runtime.

The collector records only hashes, bounded metrics, and model identity. It never
marks mock/fallback responses as proof and never changes replacement readiness.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.model_runtime import NativeModelRuntime


BASE_URL = os.getenv("ASCENSION_AI_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
TOKEN = os.getenv("ASCENSION_AI_TEST_TOKEN", "").strip()
PROMPT = os.getenv(
    "ASCENSION_EVIDENCE_PROMPT",
    "Hello. Please answer naturally with one friendly sentence.",
)
TIMEOUT = float(os.getenv("ASCENSION_EVIDENCE_TIMEOUT", "150"))
REPORT_PATH = Path(
    os.getenv(
        "ASCENSION_EVIDENCE_REPORT_PATH",
        str(ROOT / "evals" / "runtime_evidence_report.json"),
    )
)
SOURCE_FILES = (
    "src/serving/api.py",
    "src/core/orchestrator.py",
    "src/core/model_runtime.py",
)


class EvidenceCollectionError(RuntimeError):
    """Raised when evidence is incomplete or not from a live native run."""


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compute_source_hashes() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for relative in SOURCE_FILES:
        path = ROOT / relative
        hashes[relative] = _sha256_file(path) if path.is_file() else ""
    return hashes


def _request_json(request: urllib.request.Request, timeout: float) -> tuple[int, dict, float]:
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return response.status, payload if isinstance(payload, dict) else {}, (
                time.perf_counter() - started
            ) * 1000
    except urllib.error.HTTPError as error:
        return error.code, {"error": "http_error"}, (time.perf_counter() - started) * 1000
    except Exception as error:
        return 0, {"error": type(error).__name__}, (time.perf_counter() - started) * 1000


def get_health() -> tuple[int, dict, float]:
    return _request_json(
        urllib.request.Request(
            f"{BASE_URL}/health", method="GET", headers={"Accept": "application/json"}
        ),
        15,
    )


def post_intelligence() -> tuple[int, dict, float]:
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    body = json.dumps(
        {
            "shell": "ap",
            "tier": "lifeos",
            "messages": [{"role": "user", "content": PROMPT}],
            "context": {},
            "surface": "runtime_evidence",
            "mode": "conversation",
            "allowed_capabilities": [],
            "temperature": 0.65,
            "max_tokens": 160,
        }
    ).encode("utf-8")
    return _request_json(
        urllib.request.Request(
            f"{BASE_URL}/v1/intelligence", data=body, method="POST", headers=headers
        ),
        TIMEOUT,
    )


def build_report(
    *,
    intelligence_status: int,
    payload: dict,
    client_latency_ms: float,
    health_status: int,
    health: dict,
    provenance: str,
    source_hashes: dict[str, str],
) -> dict:
    raw_content = str(payload.get("content") or "")
    content = NativeModelRuntime._clean_content(raw_content)
    runtime = health.get("runtime") if isinstance(health.get("runtime"), dict) else {}
    queue = runtime.get("queue") if isinstance(runtime.get("queue"), dict) else None

    blockers: list[str] = []
    checks = (
        (intelligence_status == 200, "intelligence_http_status_not_200"),
        (health_status == 200, "health_http_status_not_200"),
        (payload.get("provider") == "ascension-native", "provider_not_ascension_native"),
        (payload.get("outside_provider") is False, "outside_provider_not_false"),
        (
            payload.get("production_replacement_enabled") is False,
            "production_replacement_enabled_not_false",
        ),
        (bool(content), "cleaned_content_empty"),
        (bool(payload.get("model")), "model_identity_missing"),
        (isinstance(payload.get("latency_ms"), (int, float)), "server_latency_missing"),
        (isinstance(payload.get("queue_wait_ms"), (int, float)), "queue_wait_missing"),
        (isinstance(payload.get("inference_ms"), (int, float)), "inference_time_missing"),
        (health.get("provider") == "ascension-native", "health_provider_not_ascension_native"),
        (health.get("outside_provider") is False, "health_outside_provider_not_false"),
        (health.get("replacement_ready") is False, "health_replacement_ready_not_false"),
        (queue is not None, "runtime_queue_missing"),
        (
            all(len(source_hashes.get(path, "")) == 64 for path in SOURCE_FILES),
            "source_hash_evidence_missing",
        ),
    )
    blockers.extend(reason for passed, reason in checks if not passed)
    proven = provenance == "live" and not blockers

    return {
        "schema_version": "1.0",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "provenance": provenance,
        "proven": proven,
        "replacement_ready": False,
        "gated_reasons": blockers,
        "endpoint_fingerprint": _sha256_bytes(
            f"{BASE_URL}/v1/intelligence".encode("utf-8")
        ),
        "prompt_fingerprint": _sha256_bytes(PROMPT.encode("utf-8")),
        "source_hashes": source_hashes,
        "model_identity": {
            "model": payload.get("model") or runtime.get("model"),
            "profile": runtime.get("profile"),
            "repo_id": runtime.get("repo_id"),
            "filename": runtime.get("filename"),
            "inference": runtime.get("inference"),
        },
        "response_evidence": {
            "content_hash": _sha256_bytes(content.encode("utf-8")) if content else None,
            "character_count": len(content),
            "word_count": len(content.split()),
        },
        "latency_and_queue": {
            "client_latency_ms": round(client_latency_ms, 3),
            "server_latency_ms": payload.get("latency_ms"),
            "queue_wait_ms": payload.get("queue_wait_ms"),
            "inference_ms": payload.get("inference_ms"),
            "runtime_queue": queue or {},
        },
    }


def write_report(report: dict, path: Path = REPORT_PATH) -> None:
    if report.get("provenance") != "live" or report.get("proven") is not True:
        raise EvidenceCollectionError("refusing to write unproven runtime evidence")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    if not TOKEN:
        raise SystemExit("ASCENSION_AI_TEST_TOKEN is required; never commit it")
    health_status, health, _ = get_health()
    intelligence_status, payload, latency = post_intelligence()
    report = build_report(
        intelligence_status=intelligence_status,
        payload=payload,
        client_latency_ms=latency,
        health_status=health_status,
        health=health,
        provenance="live",
        source_hashes=compute_source_hashes(),
    )
    print(json.dumps({"proven": report["proven"], "gated_reasons": report["gated_reasons"]}, indent=2))
    if not report["proven"]:
        return 1
    write_report(report)
    print(f"Wrote evidence report: {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
