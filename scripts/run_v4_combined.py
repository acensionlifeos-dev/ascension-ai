"""Train a single v4 adapter on the combined all-category curriculum."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    args = ["python", "scripts/run_qwen_growth_experiment.py",
            "--run-id", "grow157_all_categories_v4",
            "--parent-adapter", str(ROOT / "checkpoints" / "proven_parent_grow018_v7_a"),
            "--curriculum", "evals/training/ascension_product_v157_all_categories.jsonl",
            "--gpu-indices", "0,1",
            "--learning-rates", "1e-5,5e-6",
            "--seeds", "9950,9951",
            "--epochs", "3.0",
            "--max-length", "768",
            "--tokens", "160",
            "--report", "evals/results/grow157_all_categories_v4_comparison.json"]
    return subprocess.run(args, cwd=ROOT).returncode


if __name__ == "__main__":
    raise SystemExit(main())
