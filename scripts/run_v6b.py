"""Train a single v6b adapter on the de-duplicated full curriculum."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    args = ["python", "scripts/run_qwen_growth_experiment.py",
            "--run-id", "grow161_all_v6b",
            "--parent-adapter", str(ROOT / "checkpoints" / "proven_parent_grow018_v7_a"),
            "--curriculum", "evals/training/ascension_product_v161_all_v6b.jsonl",
            "--gpu-indices", "0,1",
            "--learning-rates", "1e-5,5e-6",
            "--seeds", "9980,9981",
            "--epochs", "1.0",
            "--max-length", "768",
            "--tokens", "160",
            "--report", "evals/results/grow161_all_v6b_comparison.json"]
    return subprocess.run(args, cwd=ROOT).returncode


if __name__ == "__main__":
    raise SystemExit(main())
