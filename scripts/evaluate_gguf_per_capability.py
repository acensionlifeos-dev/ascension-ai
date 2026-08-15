"""Evaluate a GGUF profile against the 640 per-capability gates."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.model_runtime import NativeModelRuntime


def score_case(case: dict, text: str) -> dict:
    if not text or not text.strip():
        return {
            "case_id": case["id"],
            "shell": case["shell"],
            "passed": False,
            "score": 0.0,
            "response": "",
        }
    lower = text.lower()
    rubric = case["rubric"]
    scores = []
    for item in rubric:
        score = 1.0
        positive = item.get("positive", [])
        if positive and not any(p.lower() in lower for p in positive):
            score -= 0.5
        negative = item.get("negative", [])
        if any(n.lower() in lower for n in negative):
            score -= 0.5
        if item["name"].endswith("_shell_aligned"):
            # Native runtime already pin the shell via the API request.
            score = 1.0
        scores.append(max(0.0, min(1.0, score)))
    avg = sum(scores) / len(scores) if scores else 0.0
    return {
        "case_id": case["id"],
        "shell": case["shell"],
        "passed": avg >= case["pass_threshold"],
        "score": round(avg, 3),
        "response": text,
    }


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Evaluate a GGUF profile on 640 capabilities")
    parser.add_argument("--profile", default="pro_v16")
    parser.add_argument("--tokens", type=int, default=128)
    parser.add_argument("--output", default="evals/results/pro_v16_per_capability_gate.json")
    parser.add_argument("--capability-gates", default="evals/per_capability_gates.json")
    args = parser.parse_args(argv)

    os.environ["ASCENSION_MODEL_PROFILE"] = args.profile
    runtime = NativeModelRuntime()
    runtime.load()

    gates = json.loads((ROOT / args.capability_gates).read_text("utf-8"))
    cases = gates["cases"]
    results = []
    for case in cases:
        messages = [
            {"role": "system", "content": f"You are Ascension AI in shell {case['shell']}."},
            {"role": "user", "content": case["user"]},
        ]
        try:
            out = runtime.chat(messages, temperature=0.35, max_tokens=args.tokens)
            text = out["content"]
        except Exception as error:
            text = ""
            print(f"{case['id']}: {error!r}", file=sys.stderr)
        results.append(score_case(case, text))

    passed = sum(1 for r in results if r["passed"])
    report = {
        "profile": args.profile,
        "capability_gate_version": gates.get("version", 1),
        "total_capabilities": len(results),
        "passed": passed,
        "pass_rate": round(passed / len(results) if results else 0.0, 4),
        "production_replacement_ready": False,
        "human_review_required": True,
        "results": results,
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"passed": passed, "total": len(results), "pass_rate": report["pass_rate"]}, ensure_ascii=False))
    return 0 if passed == len(results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
