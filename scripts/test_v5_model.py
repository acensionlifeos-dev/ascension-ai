"""
Quick test for an Ascension Elite v5 checkpoint.

Usage:
    python -u scripts/test_v5_model.py --version ascension_elite_general_v5_4h
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.architecture.inference import EliteInference


def main():
    parser = argparse.ArgumentParser(description="Test Ascension Elite v5")
    parser.add_argument("--version", default="ascension_elite_general_v5_4h", help="checkpoint version")
    parser.add_argument("--temperature", type=float, default=0.9, help="sampling temperature")
    parser.add_argument("--tokens", type=int, default=80, help="max new tokens")
    args = parser.parse_args()

    try:
        inference = EliteInference("checkpoints", prefix=args.version)
    except FileNotFoundError as exc:
        print(f"Checkpoint not found: {exc}")
        return 1

    print("Status:", inference.status())
    prompts = [
        "The future of AI is",
        "To make money with twenty dollars",
        "The best way to improve your life is",
        "Ascension AI can",
    ]

    for prompt in prompts:
        print("\n" + "=" * 60)
        print("Prompt:", prompt)
        generated = inference.generate(prompt, max_new_tokens=args.tokens, temperature=args.temperature)
        print("Generated:", generated)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
