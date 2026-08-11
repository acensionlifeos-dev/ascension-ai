"""Thirty-prompt native shell smoke evaluation with no hosted AI calls."""

from __future__ import annotations

import json
import os
import statistics
import sys
from pathlib import Path

from fastapi.testclient import TestClient


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
PROMPTS = json.loads((ROOT / "evals" / "native_smoke_prompts.json").read_text(encoding="utf-8"))
FORBIDDEN = ("openai", "gemini", "anthropic", "claude", "as an ai language model", "<|im_")


def main() -> None:
    os.environ.setdefault("ASCENSION_AI_TEST_TOKEN", "local-native-eval")
    os.environ.setdefault("ASCENSION_MODEL_PROFILE", "starter")
    from src.serving.api import app

    results = []
    headers = {"Authorization": f"Bearer {os.environ['ASCENSION_AI_TEST_TOKEN']}"}
    with TestClient(app) as client:
        health = client.get("/health").json()
        if not health.get("candidate_ready"):
            raise SystemExit(f"Native model unavailable: {health}")
        for index, case in enumerate(PROMPTS, start=1):
            response = client.post("/chat", headers=headers, json={
                "shell": case["shell"],
                "messages": [{"role": "user", "content": case["prompt"]}],
                "surface": "native_regression",
                "mode": "conversation",
                "max_tokens": 48,
            })
            payload = response.json()
            content = str(payload.get("content") or "").strip()
            failures = []
            if response.status_code != 200:
                failures.append(f"http_{response.status_code}")
            if len(content) < 8:
                failures.append("empty_or_too_short")
            lowered = content.lower()
            if any(marker in lowered for marker in FORBIDDEN):
                failures.append("outside_provider_or_raw_token_leak")
            if payload.get("provider") not in {None, "ascension-native"}:
                failures.append("wrong_provider")
            results.append({
                "index": index,
                "shell": case["shell"],
                "passed": not failures,
                "failures": failures,
                "latency_ms": payload.get("latency_ms", 0),
                "response_preview": content[:180].replace("\n", " "),
            })
            print(f"{index:02d}/30 {'PASS' if not failures else 'FAIL'} {case['shell']} {payload.get('latency_ms', 0)}ms", flush=True)

    passed = sum(1 for result in results if result["passed"])
    latencies = [int(result["latency_ms"] or 0) for result in results]
    summary = {
        "passed": passed,
        "total": len(results),
        "pass_rate": round(passed / len(results), 3),
        "median_latency_ms": int(statistics.median(latencies)),
        "p95_latency_ms": sorted(latencies)[max(0, round(len(latencies) * 0.95) - 1)],
        "profile": os.environ["ASCENSION_MODEL_PROFILE"],
        "outside_provider": False,
    }
    print(json.dumps(summary, indent=2))
    if passed != len(results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
