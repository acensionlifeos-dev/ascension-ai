"""Runtime-backed capability-surface evidence collector.

Reads the static capability-surface audit, calls the actual native handlers for
each surface, and writes a machine-readable evidence report.  A surface is only
marked *proven* when the handler produces real, canary-driven, permission-aware
output; it is never marked proven from registration, static declarations,
outside-provider HTTP 200, or mocked inference.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.contracts import Shell, Tier
from src.core.model_runtime import runtime
from src.core.orchestrator import surface_plan


REPORT_PATH = Path(
    os.getenv("ASCENSION_SURFACE_EVIDENCE_PATH", str(ROOT / "evals" / "capability_surface_runtime_evidence.json"))
)
STATIC_REPORT_PATH = ROOT / "evals" / "capability_surface_report.json"
SOURCE_FILES = (
    "src/core/cognition.py",
    "src/core/orchestrator.py",
    "src/core/model_runtime.py",
    "src/serving/api.py",
)

RISK_ORDER = {"none": -1, "low": 0, "high": 1, "critical": 2}


class EvidenceCollectionError(Exception):
    """Raised when a surface cannot be evaluated honestly."""


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def compute_source_hashes() -> dict[str, str]:
    hashes: dict[str, str] = {}
    for rel in SOURCE_FILES:
        full = ROOT / rel
        hashes[rel] = _sha256_file(full) if full.is_file() else ""
    return hashes


def _runtime_identity() -> dict:
    status = runtime.status()
    return {
        "ready": status.get("ready"),
        "model": status.get("model"),
        "profile": status.get("profile"),
        "repo_id": status.get("repo_id"),
        "inference": status.get("inference"),
        "outside_provider": status.get("outside_provider"),
        "replacement_ready": False,
    }


def _runtime_queue() -> dict:
    return runtime.status().get("queue", {})


def _try_native_chat() -> dict:
    """Attempt one real native chat; only succeeds with a loaded ascension-native model."""
    if not runtime.status().get("ready"):
        return {"class": "unavailable", "reason": "Native model is not loaded; no runtime inference evidence available."}
    messages = [{"role": "system", "content": "You are Ascension AI."}, {"role": "user", "content": "Hello, can you respond with one natural sentence?"}]
    started = time.perf_counter()
    try:
        result = runtime.chat(messages, 0.65, 32)
        latency_ms = round((time.perf_counter() - started) * 1000)
        if result.get("provider") != "ascension-native" or result.get("outside_provider") is not False:
            return {"class": "failed", "reason": "Native chat returned a non-native or fallback provider."}
        content = str(result.get("content") or "").strip()
        if not content:
            return {"class": "failed", "reason": "Native chat returned empty content."}
        return {
            "class": "proven",
            "reason": None,
            "latency_ms": latency_ms,
            "model": result.get("model"),
            "content_preview": content[:120],
            "usage": result.get("usage"),
        }
    except Exception as exc:
        return {"class": "failed", "reason": f"Native chat raised an exception: {exc}"}


def _surface_plan_evidence(
    *,
    trigger: str,
    shell: Shell,
    allowed_capabilities: list[str],
    available_actions: list[str],
) -> dict:
    started = time.perf_counter()
    try:
        plan = surface_plan(
            shell=shell,
            tier=Tier.LIFE_OS,
            trigger=trigger,
            context={"surface": "runtime_evidence"},
            available_actions=available_actions,
            allowed_capabilities=allowed_capabilities,
        )
        latency_ms = round((time.perf_counter() - started) * 1000)
        contract = plan.get("execution_contract") or {}
        return {
            "latency_ms": latency_ms,
            "execution_contract": contract,
            "error": None,
        }
    except Exception as exc:
        return {
            "latency_ms": round((time.perf_counter() - started) * 1000),
            "execution_contract": {},
            "error": str(exc),
        }


def _proposed_action(contract: dict, action_id: str) -> dict | None:
    for action in contract.get("proposed_actions", []):
        if action.get("action") == action_id:
            return action
    return None


SURFACE_CASES: dict[str, dict] = {
    "natural conversation": {
        "handler": "native_chat",
        "trigger": "Hello, how are you today?",
    },
    "persistent memory / corrections": {
        "handler": "surface_plan",
        "trigger": "My preferred name is Brandon",
        "shell": Shell.AP,
        "allowed_capabilities": ["identity"],
        "available_actions": [],
        "expect_memory": "preferred_name",
        "expect_persistence_condition": "shell_authority_and_guardian_when_minor",
    },
    "schedule / calendar": {
        "handler": "surface_plan",
        "trigger": "I work 10 pm-6 am Wed-Sun",
        "shell": Shell.AP,
        "allowed_capabilities": ["schedule"],
        "available_actions": ["schedule.upsert_recurring_work"],
        "expect_action": "schedule.upsert_recurring_work",
        "expect_risk": "low",
        "expect_approval": "safe_internal_auto",
    },
    "finance / budget / grocery": {
        "handler": "surface_plan",
        "trigger": "I'm short on cash and need to pay my landlord",
        "shell": Shell.AP,
        "allowed_capabilities": ["finance"],
        "available_actions": ["finance.prepare_budget", "finance.payment"],
        "expect_action": "finance.payment",
        "expect_risk": "critical",
        "expect_approval": "explicit_confirmation",
    },
    "nutrition": {
        "handler": "surface_plan",
        "trigger": "I need a meal plan for the week",
        "shell": Shell.AP,
        "allowed_capabilities": ["health"],
        "available_actions": ["nutrition.prepare_meal_plan"],
        "expect_action": "nutrition.prepare_meal_plan",
        "expect_risk": "low",
        "expect_approval": "safe_internal_auto",
    },
    "learning / course generation": {
        "handler": "surface_plan",
        "trigger": "Teach me Spanish",
        "shell": Shell.AP,
        "allowed_capabilities": ["learning"],
        "available_actions": ["learning.prepare_course"],
        "expect_action": "learning.prepare_course",
        "expect_risk": "low",
        "expect_approval": "safe_internal_auto",
    },
    "career": {
        "handler": "surface_plan",
        "trigger": "I want a new job",
        "shell": Shell.AP,
        "allowed_capabilities": ["career"],
        "available_actions": ["career.research_jobs"],
        "expect_action": "career.research_jobs",
        "expect_risk": "low",
        "expect_approval": "safe_research",
    },
    "creation / project workspaces": {
        "handler": "surface_plan",
        "trigger": "I have an idea for a video",
        "shell": Shell.AP,
        "allowed_capabilities": ["creation"],
        "available_actions": ["creation.save_seed"],
        "expect_action": "creation.save_seed",
        "expect_risk": "low",
        "expect_approval": "safe_internal_auto",
    },
    "relationships": {
        "handler": "surface_plan",
        "trigger": "Send a message to my friend",
        "shell": Shell.AP,
        "allowed_capabilities": ["relationships"],
        "available_actions": ["messages.send"],
        "expect_action": "messages.send",
        "expect_risk": "high",
        "expect_approval": "explicit_confirmation",
    },
    "FamilyOS / Sprout / Nexus permission boundaries": {
        "handler": "surface_plan",
        "trigger": "Schedule a dentist appointment for my toddler on Tuesday at 3 pm",
        "shell": Shell.NEXUS_HOME,
        "allowed_capabilities": ["schedule", "home", "sprout"],
        "available_actions": ["calendar.external_write"],
        "expect_action": "calendar.external_write",
        "expect_risk": "high",
        "expect_approval": "explicit_confirmation",
        "expect_guardian": True,
    },
    "browser / web research": {
        "handler": "outside_fallback",
        "trigger": "Search the web for apartments",
    },
}


def _classify_surface(surface: str, case: dict, evidence: dict) -> tuple[str, str | None, dict]:
    """Return (class, reason, permission_receipt_evidence)."""
    if case.get("handler") == "native_chat":
        chat = _try_native_chat()
        return (
            str(chat.get("class")),
            chat.get("reason"),
            {
                "model": chat.get("model"),
                "content_preview": chat.get("content_preview"),
                "usage": chat.get("usage"),
            },
        )

    if case.get("handler") == "outside_fallback":
        return (
            "unavailable",
            "Native runtime has no handler for this surface; outside-provider fallback remains the active route.",
            {"routed_provider": "outside-provider-fallback"},
        )

    contract = evidence.get("execution_contract", {})
    if evidence.get("error"):
        return "failed", f"Handler raised an exception: {evidence['error']}", {}

    if case.get("expect_memory"):
        signals = contract.get("memory_update_signals", [])
        if any(s.get("key") == case["expect_memory"] for s in signals):
            signal = next(s for s in signals if s.get("key") == case["expect_memory"])
            if case.get("expect_persistence_condition") and signal.get("persistence_condition") != case["expect_persistence_condition"]:
                return "failed", "Memory signal did not include the expected fail-closed persistence condition.", {}
            return "proven", None, {
                "memory_signal": signal,
                "permission_approval_gate": contract.get("permission_approval_gate"),
            }
        return "unimplemented", "No runtime memory signal was generated for the expected candidate.", {}

    if case.get("expect_action"):
        action = _proposed_action(contract, case["expect_action"])
        if action is None:
            return "unimplemented", f"Expected action {case['expect_action']} was not proposed by the runtime handler.", {}
        if case.get("expect_risk") and action.get("risk") != case["expect_risk"]:
            return "failed", f"Expected risk {case['expect_risk']}, got {action.get('risk')}.", {}
        if case.get("expect_approval") and action.get("approval") != case["expect_approval"]:
            return "failed", f"Expected approval {case['expect_approval']}, got {action.get('approval')}.", {}
        if case.get("expect_guardian") and not action.get("guardian_required"):
            return "failed", "Expected guardian requirement was not enforced for this Sprout/family action.", {}
        if not action.get("receipt_fields"):
            return "failed", "Proposed action is missing the required execution-receipt spec.", {}
        return "proven", None, {
            "proposed_action": action,
            "permission_approval_gate": contract.get("permission_approval_gate"),
            "child_safe_guardian_boundaries": contract.get("child_safe_guardian_boundaries"),
            "execution_receipt": contract.get("execution_receipt"),
        }

    return "unimplemented", "No runtime test case expected a specific action or memory signal for this surface.", {}


def _evidence_for_surface(surface: str, ids: list[str]) -> dict:
    timestamp = datetime.now(timezone.utc).isoformat()
    queue = _runtime_queue()
    case = SURFACE_CASES.get(surface)

    if case is None:
        return {
            "surface": surface,
            "ids": ids,
            "class": "unimplemented",
            "timestamp_utc": timestamp,
            "unix_timestamp": time.time(),
            "latency_ms": 0,
            "queue": queue,
            "reason": "No runtime test case is defined for this surface in the native core.",
            "permission_receipt_evidence": None,
            "provenance": "no_handler",
        }

    if case.get("handler") == "native_chat":
        started = time.perf_counter()
        chat = _try_native_chat()
        latency_ms = round((time.perf_counter() - started) * 1000)
        return {
            "surface": surface,
            "ids": ids,
            "class": chat.get("class"),
            "timestamp_utc": timestamp,
            "unix_timestamp": time.time(),
            "latency_ms": chat.get("latency_ms", latency_ms),
            "queue": queue,
            "reason": chat.get("reason"),
            "permission_receipt_evidence": {
                "model": chat.get("model"),
                "content_preview": chat.get("content_preview"),
                "usage": chat.get("usage"),
            },
            "provenance": "native_model",
        }

    if case.get("handler") == "outside_fallback":
        class_, reason, pr_evidence = _classify_surface(surface, case, {})
        return {
            "surface": surface,
            "ids": ids,
            "class": class_,
            "timestamp_utc": timestamp,
            "unix_timestamp": time.time(),
            "latency_ms": 0,
            "queue": queue,
            "reason": reason,
            "permission_receipt_evidence": pr_evidence,
            "provenance": "outside_fallback",
        }

    evidence = _surface_plan_evidence(
        trigger=case["trigger"],
        shell=case["shell"],
        allowed_capabilities=case.get("allowed_capabilities", []),
        available_actions=case.get("available_actions", []),
    )
    class_, reason, pr_evidence = _classify_surface(surface, case, evidence)
    return {
        "surface": surface,
        "ids": ids,
        "class": class_,
        "timestamp_utc": timestamp,
        "unix_timestamp": time.time(),
        "latency_ms": evidence["latency_ms"],
        "queue": queue,
        "reason": reason,
        "permission_receipt_evidence": pr_evidence,
        "provenance": "runtime_handler",
    }


def build_report() -> dict:
    if STATIC_REPORT_PATH.is_file():
        static = json.loads(STATIC_REPORT_PATH.read_text(encoding="utf-8"))
        static_surfaces = static.get("per_surface", {})
    else:
        static_surfaces = {}

    per_surface: dict[str, dict] = {}
    for surface, detail in static_surfaces.items():
        ids = detail.get("ids", [])
        per_surface[surface] = _evidence_for_surface(surface, ids)

    by_class: dict[str, list[str]] = {"proven": [], "failed": [], "unavailable": [], "unimplemented": []}
    for surface, record in per_surface.items():
        by_class.setdefault(record["class"], []).append(surface)

    return {
        "schema_version": "1.1",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "unix_timestamp": time.time(),
        "source_hashes": compute_source_hashes(),
        "runtime_identity": _runtime_identity(),
        "per_surface": per_surface,
        "proven_surfaces": sorted(by_class.get("proven", [])),
        "failed_surfaces": sorted(by_class.get("failed", [])),
        "unavailable_surfaces": sorted(by_class.get("unavailable", [])),
        "unimplemented_surfaces": sorted(by_class.get("unimplemented", [])),
        "replacement_ready": False,
        "outside_provider": False,
        "report_rule": "A surface is proven only when a real native handler produced a canary-driven, permission-aware, receipt-gated output. Registration, static declarations, HTTP 200, and mocks do not count.",
    }


def write_report(report: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")


def main() -> None:
    report = build_report()
    write_report(report, REPORT_PATH)
    summary = {
        "proven": len(report["proven_surfaces"]),
        "failed": len(report["failed_surfaces"]),
        "unavailable": len(report["unavailable_surfaces"]),
        "unimplemented": len(report["unimplemented_surfaces"]),
        "path": str(REPORT_PATH),
    }
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
