"""Train v17 support adapter from v6b."""
from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    args = ["python", "scripts/run_qwen_growth_experiment.py",
            "--run-id", "grow170_support_v17",
            "--parent-adapter", str(ROOT / "checkpoints" / "grow161_all_v6b_a"),
            "--curriculum", "evals/training/ascension_product_v170_support.jsonl",
            "--gpu-indices", "0,1",
            "--learning-rates", "2e-4,1e-4",
            "--seeds", "20001,20002",
            "--epochs", "0.5",
            "--max-length", "768",
            "--tokens", "160",
            "--report", "evals/results/grow170_support_v17_comparison.json"]
    return subprocess.run(args, cwd=ROOT).returncode


if __name__ == "__main__":
    raise SystemExit(main())
