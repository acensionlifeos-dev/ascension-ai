"""Train v18 creative/ideation adapter from v6b."""
from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    args = ["python", "scripts/run_qwen_growth_experiment.py",
            "--run-id", "grow171_creative_v18",
            "--parent-adapter", str(ROOT / "checkpoints" / "grow161_all_v6b_a"),
            "--curriculum", "evals/training/ascension_product_v171_creative.jsonl",
            "--gpu-indices", "0,1",
            "--learning-rates", "2e-4,1e-4",
            "--seeds", "30001,30002",
            "--epochs", "0.5",
            "--max-length", "768",
            "--tokens", "160",
            "--report", "evals/results/grow171_creative_v18_comparison.json"]
    return subprocess.run(args, cwd=ROOT).returncode


if __name__ == "__main__":
    raise SystemExit(main())
