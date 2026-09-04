"""Pick the best of two semantic-gate candidates for the repair loop."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load(name: str, results_dir: Path) -> dict | None:
    p = results_dir / f"{name}_semantic_gate_v2.json"
    if not p.exists():
        return None
    data = json.loads(p.read_text(encoding="utf-8"))
    s = data["summary"]
    return {
        "name": name,
        "effective_passed": s["effective_passed"],
        "effective_rate": s["effective_pass_rate"],
        "hard_blocks": s["hard_block_count"],
        "failed_domains": s["failed_domains"],
        "gate_passed": s["semantic_release_gate_passed"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Pick best semantic gate candidate")
    parser.add_argument("candidate_a")
    parser.add_argument("candidate_b")
    parser.add_argument("--results-dir", default="evals/results", type=Path)
    args = parser.parse_args()

    a = load(args.candidate_a, args.results_dir)
    b = load(args.candidate_b, args.results_dir)

    if a is None or b is None:
        print("MISSING", file=sys.stderr)
        return 1

    def score(x: dict) -> tuple:
        return (x["effective_passed"], -x["hard_blocks"], -len(x["failed_domains"]))

    best = a if score(a) >= score(b) else b
    print(json.dumps(best))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
