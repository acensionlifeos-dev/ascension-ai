"""Train v15 from v6b on targeted generic fixes."""
from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main(argv: list[str] | None = None) -> int:
    args = ["python", "scripts/run_qwen_growth_experiment.py",
            "--run-id", "grow169_targeted_fix",
            "--parent-adapter", str(ROOT / "checkpoints" / "grow161_all_v6b_a"),
            "--curriculum", "evals/training/ascension_product_v169_targeted_fix.jsonl",
            "--gpu-indices", "0,1",
            "--learning-rates", "1e-5,5e-6",
            "--seeds", "10001,10002",
            "--epochs", "0.3",
            "--max-length", "768",
            "--tokens", "160",
            "--report", "evals/results/grow169_targeted_fix_comparison.json"]
    return subprocess.run(args, cwd=ROOT).returncode


if __name__ == "__main__":
    raise SystemExit(main())
