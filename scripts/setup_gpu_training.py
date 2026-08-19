"""One-command GPU training setup and launcher for Ascension AI.

This script checks for a CUDA-capable environment, installs the training
requirements, builds the product corpus if needed, and launches the v6
product trainer with GPU-friendly defaults. It never reads production
conversations or private user data.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parents[1]
CORPUS_PATH = ROOT / "data" / "ascension_product_v6.txt"
TRAINER = ROOT / "scripts" / "train_ascension_product_v6.py"
BUILDER = ROOT / "scripts" / "build_ascension_product_corpus.py"
REQUIREMENTS = ROOT / "requirements-training.txt"


def log(message: str) -> None:
    print(f"[GPU Setup] {message}", flush=True)


def run(cmd: list[str], **kwargs) -> int:
    log(" ".join(cmd))
    return subprocess.run(cmd, cwd=ROOT, check=False, **kwargs).returncode


def install_requirements() -> int:
    if not REQUIREMENTS.exists():
        log(f"Missing {REQUIREMENTS}; cannot install training dependencies.")
        return 1
    return run([sys.executable, "-m", "pip", "install", "-q", "-r", str(REQUIREMENTS)])


def build_corpus(product_repeats: int) -> int:
    log("Building Ascension product training corpus...")
    return run([
        sys.executable,
        str(BUILDER),
        "--output",
        str(CORPUS_PATH),
        "--product-repeats",
        str(product_repeats),
    ])


def launch_training(args: argparse.Namespace) -> int:
    cmd = [
        sys.executable,
        str(TRAINER),
        "--version",
        args.version,
        "--steps",
        str(args.steps),
        "--batch-size",
        str(args.batch_size),
        "--learning-rate",
        str(args.learning_rate),
        "--product-repeats",
        str(args.product_repeats),
        "--general-replay-ratio",
        str(args.general_replay_ratio),
        "--save-every",
        str(args.save_every),
        "--print-every",
        str(args.print_every),
    ]
    if args.initialization:
        cmd.extend(["--initialization", args.initialization])
    if args.resume_latest:
        cmd.append("--resume-latest")
    if args.assistant_only_loss:
        cmd.append("--assistant-only-loss")
    if args.human_review_approved:
        cmd.append("--human-review-approved")
    if args.gate_result:
        cmd.extend(["--gate-result", args.gate_result])
    return run(cmd)


def main() -> int:
    parser = argparse.ArgumentParser(description="Set up and launch Ascension AI GPU training")
    parser.add_argument("--skip-install", action="store_true", help="skip pip install step")
    parser.add_argument("--skip-corpus", action="store_true", help="skip corpus build if it exists")
    parser.add_argument("--version", default="ascension_product_v6")
    parser.add_argument("--initialization", choices=("resume", "transplant", "fresh"))
    parser.add_argument("--steps", type=int, default=20000)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--product-repeats", type=int, default=12)
    parser.add_argument("--general-replay-ratio", type=float, default=0.2)
    parser.add_argument("--save-every", type=int, default=2500)
    parser.add_argument("--print-every", type=int, default=250)
    parser.add_argument("--resume-latest", action="store_true")
    parser.add_argument("--assistant-only-loss", action="store_true")
    parser.add_argument("--human-review-approved", action="store_true")
    parser.add_argument("--gate-result", help="JSON receipt from evaluate_native_checkpoint.py")
    args = parser.parse_args()

    log(f"PyTorch {torch.__version__}; CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        log(f"CUDA device count: {torch.cuda.device_count()}")
        for i in range(torch.cuda.device_count()):
            log(f"  GPU {i}: {torch.cuda.get_device_name(i)}")
    else:
        log("WARNING: no CUDA device detected; training will use CPU.")

    if not args.skip_install:
        if install_requirements() != 0:
            log("Dependency install failed; aborting.")
            return 1

    if not args.skip_corpus or not CORPUS_PATH.exists():
        if build_corpus(args.product_repeats) != 0:
            log("Corpus build failed; aborting.")
            return 1

    if not CORPUS_PATH.exists():
        log(f"Corpus still missing after build: {CORPUS_PATH}")
        return 1

    log("Launching GPU training...")
    return launch_training(args)


if __name__ == "__main__":
    raise SystemExit(main())
