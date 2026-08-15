"""Train a single v7 adapter on v6b curriculum with lower learning rates."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    args = ["python", "scripts/run_qwen_growth_experiment.py",
            "--run-id", "grow162_all_v7",
            "--parent-adapter", str(ROOT / "checkpoints" / "proven_parent_grow018_v7_a"),
            "--curriculum", "evals/training/ascension_product_v161_all_v6b.jsonl",
            "--gpu-indices", "0,1",
            "--learning-rates", "5e-6,2e-6",
            "--seeds", "9990,9991",
            "--epochs", "1.0",
            "--max-length", "768",
            "--tokens", "160",
            "--report", "evals/results/grow162_all_v7_comparison.json"]
    return subprocess.run(args, cwd=ROOT).returncode


if __name__ == "__main__":
    raise SystemExit(main())
