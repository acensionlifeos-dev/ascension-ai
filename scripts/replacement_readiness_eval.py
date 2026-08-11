"""Replacement-quality evaluation for a local or deployed Ascension AI service."""

from __future__ import annotations

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
    if any(marker in lowered for marker in ("<think>", "</think>", "<|im_", "chain of thought")): failures.append("hidden_reasoning_leak")
    if latency_ms > 45000: failures.append("interactive_latency")
    return {"id":case["id"],"shell":case["shell"],"passed":not failures,"failures":failures,"latency_ms":round(latency_ms),"preview":content[:240]}


def main() -> None:
    if not TOKEN:
        raise SystemExit("ASCENSION_AI_TEST_TOKEN is required; never put it in source control.")
    results = []
    for index, case in enumerate(CASES, 1):
        status, payload, latency = post(case)
        result = evaluate(case, status, payload, latency)
        results.append(result)
        print(f"{index:02d}/{len(CASES)} {'PASS' if result['passed'] else 'FAIL'} {case['id']} {result['latency_ms']}ms", flush=True)
    latencies = [item["latency_ms"] for item in results]
    passed = sum(item["passed"] for item in results)
    summary = {
        "service": BASE_URL, "passed": passed, "total": len(results),
        "pass_rate": round(passed / len(results), 3),
        "median_latency_ms": int(statistics.median(latencies)),
        "p95_latency_ms": sorted(latencies)[max(0, round(len(latencies) * .95) - 1)],
        "replacement_ready": passed == len(results), "outside_provider": False,
        "results": results,
    }
    print(json.dumps(summary, indent=2))
    if not summary["replacement_ready"]: raise SystemExit(1)


if __name__ == "__main__":
    main()
