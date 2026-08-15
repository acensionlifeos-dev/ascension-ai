"""Train v10 from proven parent on full+emphasis-failures curriculum."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    args = ["python", "scripts/run_qwen_growth_experiment.py",
            "--run-id", "grow164_all_v10",
            "--parent-adapter", str(ROOT / "checkpoints" / "proven_parent_grow018_v7_a"),
            "--curriculum", "evals/training/ascension_product_v164_all_v10.jsonl",
            "--gpu-indices", "0,1",
            "--learning-rates", "1e-5,5e-6",
            "--seeds", "9999,10000",
            "--epochs", "1.0",
            "--max-length", "768",
            "--tokens", "160",
            "--report", "evals/results/grow164_all_v10_comparison.json"]
    return subprocess.run(args, cwd=ROOT).returncode


if __name__ == "__main__":
    raise SystemExit(main())
