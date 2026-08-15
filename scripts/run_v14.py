"""Train v14 from v12a on extra generic gate reinforcement."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    args = ["python", "scripts/run_qwen_growth_experiment.py",
            "--run-id", "grow168_generic_blast",
            "--parent-adapter", str(ROOT / "checkpoints" / "grow166_reinforced_a"),
            "--curriculum", "evals/training/ascension_product_v168_generic_blast.jsonl",
            "--gpu-indices", "0,1",
            "--learning-rates", "2e-6,1e-6",
            "--seeds", "10001,10002",
            "--epochs", "0.5",
            "--max-length", "768",
            "--tokens", "160",
            "--report", "evals/results/grow168_generic_blast_comparison.json"]
    return subprocess.run(args, cwd=ROOT).returncode


if __name__ == "__main__":
    raise SystemExit(main())
