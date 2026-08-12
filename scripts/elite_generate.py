"""Generate text from the Ascension Elite native checkpoint.

This is a proof-of-concept for the end-to-end native pipeline. The current
4-layer/128-dim seed is tiny and will be scaled up with more data and compute.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.architecture.inference import EliteInference


def main():
    parser = argparse.ArgumentParser(description="Generate from Ascension Elite")
    parser.add_argument("--checkpoint", default="checkpoints", help="checkpoint directory")
    parser.add_argument("--version", default="ascension_elite", help="checkpoint name prefix (ascension_elite, ascension_elite_v2, etc.)")
    parser.add_argument("--prompt", default="Ascension AI is", help="prompt")
    parser.add_argument("--tokens", type=int, default=80, help="max new tokens")
    parser.add_argument("--temperature", type=float, default=0.9, help="sampling temperature")
    args = parser.parse_args()

    inference = EliteInference(args.checkpoint, prefix=args.version)
    print("Elite model status:", inference.status())
    print("Prompt:", args.prompt)
    print("Generated:", inference.generate(args.prompt, max_new_tokens=args.tokens, temperature=args.temperature))


if __name__ == "__main__":
    main()
