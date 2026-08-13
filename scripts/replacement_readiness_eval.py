"""Replacement-quality evaluation for a local or deployed Ascension AI service."""

from __future__ import annotations

import hashlib
import json
import os
import statistics
import time
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = json.loads((ROOT / "evals" / "replacement_readiness_prompts.json").read_text(encoding="utf-8"))
BASE_URL = os.getenv("ASCENSION_AI_BASE_URL", "http://127.0.0.1:8000").rstrip("/")
TOKEN = os.getenv("ASCENSION_AI_TEST_TOKEN", "").strip()
COVERAGE_REPORT_PATH = ROOT / "evals" / "capability_surface_report.json"
SCHEMA_VERSION = "1"
SOURCE_FILES_TO_HASH = (
    "src/services/capability-registry.ts",
    "src/services/native-domain-router.ts",
    "src/services/model-router.ts",
    "src/services/permission-engine.ts",
)

# Canonical set of all requested capability surfaces from the Jest audit.
REQUIRED_SURFACES = frozenset({
    "natural conversation",
    "persistent memory / corrections",
    "schedule / calendar",
    "tasks / quests",
    "finance / budget / grocery",
    "nutrition",
    "workout / health",
    "learning / course generation",
    "career",
    "aspirations",
    "creation / project workspaces",
    "browser / web research",
    "relationships",
    "FamilyOS / Sprout / Nexus permission boundaries",
    "self-care",
    "astrology / numerology reflection",
    "journal / reflection",
})


def post(case: dict) -> tuple[int, dict, float]:
    body = json.dumps({
        "shell": case["shell"], "tier": "lifeos_infinite",
        "messages": [{"role": "user", "content": case["prompt"]}],
        "surface": "replacement_readiness", "mode": "conversation", "max_tokens": 280,
    }).encode()
    request = urllib.request.Request(
        f"{BASE_URL}/v1/intelligence", data=body, method="POST",
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=150) as response:
            return response.status, json.loads(response.read()), (time.perf_counter() - started) * 1000
    except urllib.error.HTTPError as error:
        return error.code, {"detail": error.read().decode(errors="replace")}, (time.perf_counter() - started) * 1000


def evaluate(case: dict, status: int, payload: dict, latency_ms: float) -> dict:
    content = str(payload.get("content") or "").strip()
    lowered = content.lower()
    failures = []
    if status != 200: failures.append(f"http_{status}")
    if payload.get("provider") != "ascension-native" or payload.get("outside_provider") is not False: failures.append("provider_integrity")
    if not any(term.lower() in lowered for term in case["required_any"]): failures.append("missing_required_concept")
    if any(term.lower() in lowered for term in case.get("forbidden", [])): failures.append("forbidden_claim_or_style")
    if len(content.split()) > case.get("max_words", 260): failures.append("overlong")
    if any(marker in lowered for marker in ("\x3cthink\x3e", "\x3c/think\x3e", "<|im_", "chain of thought")): failures.append("hidden_reasoning_leak")
    if latency_ms > 45000: failures.append("interactive_latency")
    return {"id":case["id"],"shell":case["shell"],"passed":not failures,"failures":failures,"latency_ms":round(latency_ms),"preview":content[:240]}


def load_capability_coverage() -> tuple[bool, dict]:
    """Load the machine-readable capability surface coverage report.

    Returns (loaded_successfully, data).  When the report is missing or invalid,
    the returned data is a minimal fail-closed structure so the audit still blocks
    replacement_ready.
    """
    try:
        data = json.loads(COVERAGE_REPORT_PATH.read_text(encoding="utf-8"))
        return True, data
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return False, {
            "replacement_ready": False,
            "replacement_ready_blockers": [f"capability coverage report unavailable: {exc}"],
            "per_surface": {},
            "per_id": {},
        }


def compute_source_hashes() -> dict[str, str]:
    """Compute SHA-256 of the canonical source files that define capability coverage."""
    hashes: dict[str, str] = {}
    for rel in SOURCE_FILES_TO_HASH:
        full = ROOT / rel
        try:
            content = full.read_bytes()
        except FileNotFoundError:
            content = b""
        hashes[rel] = hashlib.sha256(content).hexdigest()
    return hashes


def validate_capability_coverage(data: dict, coverage_loaded: bool = True) -> dict:
    """Validate a capability surface report and produce an explicit coverage gate.

    Fail-closed: any missing, malformed, inconsistent, or unknown-coverage report
    prevents replacement_ready.
    """
    KNOWN_CLASSES = {"registered_only", "outside_provider", "specialized_deterministic", "model_backed_native"}
    per_surface = data.get("per_surface", {}) if isinstance(data.get("per_surface"), dict) else {}
    required_surfaces = sorted(REQUIRED_SURFACES)
    actual_surfaces = set(per_surface.keys())

    by_class: dict[str, list[str]] = {c: [] for c in KNOWN_CLASSES}
    unknown: list[str] = []
    for s, d in per_surface.items():
        cls = d.get("surface_class")
        if cls in KNOWN_CLASSES:
            by_class[cls].append(s)
        else:
            unknown.append(s)

    reported_ready = bool(data.get("replacement_ready")) if isinstance(data, dict) else False
    reported_blockers = sorted(data.get("replacement_ready_blockers", [])) if isinstance(data, dict) else []
    unproven = sorted(by_class["registered_only"] + by_class["outside_provider"])
    missing_surfaces = sorted(REQUIRED_SURFACES - actual_surfaces)
    unexpected_surfaces = sorted(actual_surfaces - REQUIRED_SURFACES)

    reported_schema_version = data.get("schema_version") if isinstance(data, dict) else None
    reported_source_hashes = data.get("source_hashes", {}) if isinstance(data, dict) else {}
    expected_source_hashes = compute_source_hashes()
    missing_hash_files = [rel for rel in SOURCE_FILES_TO_HASH if rel not in reported_source_hashes]
    hash_mismatches = [rel for rel in SOURCE_FILES_TO_HASH if reported_source_hashes.get(rel) != expected_source_hashes.get(rel)]
    unexpected_hash_keys = sorted(set(reported_source_hashes) - set(SOURCE_FILES_TO_HASH))

    blockers: list[str] = []
    if not coverage_loaded:
        blockers.append("capability coverage report not loaded")
    if not per_surface:
        blockers.append("per_surface missing or empty")
    if missing_surfaces:
        blockers.append(f"missing required surfaces: {missing_surfaces}")
    if unexpected_surfaces:
        blockers.append(f"unexpected surfaces: {unexpected_surfaces}")
    if reported_schema_version != SCHEMA_VERSION:
        blockers.append(f"schema_version mismatch: expected {SCHEMA_VERSION}, got {reported_schema_version!r}")
    if missing_hash_files:
        blockers.append(f"missing source_hashes: {missing_hash_files}")
    if hash_mismatches:
        for rel in hash_mismatches:
            blockers.append(f"source hash mismatch for {rel}")
    if unexpected_hash_keys:
        blockers.append(f"unexpected source_hashes keys: {unexpected_hash_keys}")
    if unknown:
        blockers.append(f"unknown surface_class values: {unknown}")
    for s in by_class["registered_only"]:
        blockers.append(f"{s}: registered_only")
    for s in by_class["outside_provider"]:
        blockers.append(f"{s}: outside_provider")
    if reported_blockers != unproven:
        blockers.append("replacement_ready_blockers do not match computed unproven surfaces")
    if reported_ready and unproven:
        blockers.append("replacement_ready is true but unproven surfaces remain")

    pass_ = (coverage_loaded and not per_surface_missing(per_surface) and not missing_surfaces
             and not unexpected_surfaces and not missing_hash_files and not hash_mismatches
             and not unexpected_hash_keys and reported_schema_version == SCHEMA_VERSION
             and not unknown and not unproven
             and reported_ready and reported_blockers == unproven)

    return {
        "pass": pass_,
        "loaded": coverage_loaded,
        "schema_version": reported_schema_version,
        "expected_schema_version": SCHEMA_VERSION,
        "source_hashes": reported_source_hashes,
        "expected_source_hashes": expected_source_hashes,
        "source_hash_match": not hash_mismatches and not missing_hash_files and not unexpected_hash_keys,
        "required_surfaces": required_surfaces,
        "proven_surfaces": sorted(by_class["specialized_deterministic"] + by_class["model_backed_native"]),
        "registered_only_surfaces": by_class["registered_only"],
        "outside_provider_surfaces": by_class["outside_provider"],
        "specialized_deterministic_surfaces": by_class["specialized_deterministic"],
        "model_backed_native_surfaces": by_class["model_backed_native"],
        "blockers": blockers,
        "counts": {
            "required": len(required_surfaces),
            "proven": len(by_class["specialized_deterministic"]) + len(by_class["model_backed_native"]),
            "registered_only": len(by_class["registered_only"]),
            "outside_provider": len(by_class["outside_provider"]),
            "specialized_deterministic": len(by_class["specialized_deterministic"]),
            "model_backed_native": len(by_class["model_backed_native"]),
        },
    }


def per_surface_missing(per_surface: dict) -> bool:
    return not isinstance(per_surface, dict) or not per_surface


def build_summary(prompt_results: list[dict], coverage_loaded: bool, coverage_data: dict) -> dict:
    """Compute the combined replacement-readiness summary.

    replacement_ready is only true when the prompt-level contract suite passes
    AND the capability-surface coverage gate passes.
    """
    latencies = [item["latency_ms"] for item in prompt_results]
    passed = sum(item["passed"] for item in prompt_results)
    total = len(prompt_results)
    pass_rate = round(passed / total, 3) if total else 0.0
    prompt_cases_pass = total > 0 and passed == total

    coverage = validate_capability_coverage(coverage_data, coverage_loaded)
    capability_coverage_pass = coverage["pass"]

    replacement_ready = prompt_cases_pass and capability_coverage_pass

    return {
        "service": BASE_URL,
        "passed": passed,
        "total": total,
        "pass_rate": pass_rate,
        "prompt_cases": {"passed": passed, "total": total, "pass": prompt_cases_pass},
        "capability_coverage": coverage,
        "capability_coverage_pass": capability_coverage_pass,
        "replacement_ready": replacement_ready,
        "outside_provider": False,
        "median_latency_ms": int(statistics.median(latencies)) if latencies else 0,
        "p95_latency_ms": sorted(latencies)[max(0, round(len(latencies) * 0.95) - 1)] if latencies else 0,
        "results": prompt_results,
    }


def main() -> None:
    if not TOKEN:
        raise SystemExit("ASCENSION_AI_TEST_TOKEN is required; never put it in source control.")
    results = []
    for index, case in enumerate(CASES, 1):
        status, payload, latency = post(case)
        result = evaluate(case, status, payload, latency)
        results.append(result)
        print(f"{index:02d}/{len(CASES)} {'PASS' if result['passed'] else 'FAIL'} {case['id']} {result['latency_ms']}ms", flush=True)

    coverage_loaded, coverage_data = load_capability_coverage()
    summary = build_summary(results, coverage_loaded, coverage_data)
    print(json.dumps(summary, indent=2))
    if not summary["replacement_ready"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
