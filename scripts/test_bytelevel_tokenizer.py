"""Fast contract test for the reversible tokenizer required by native training."""

from __future__ import annotations

import tempfile
from pathlib import Path

from train_ascension_general_v5 import build_bpe_tokenizer, validate_tokenizer_roundtrip


def main() -> int:
    corpus = (
        "AP understands a night-shift schedule. "
        "Nexus coordinates a family without exposing private LifeOS data. "
        "The user's words, punctuation, and spacing must survive exactly.\n"
    ) * 40
    with tempfile.TemporaryDirectory(prefix="ascension-tokenizer-") as directory:
        tokenizer = build_bpe_tokenizer(corpus, 512, "roundtrip", Path(directory))
        validate_tokenizer_roundtrip(tokenizer)
        probe = "We can talk casually—without turning every sentence into a task."
        if tokenizer.decode(tokenizer.encode(probe).ids) != probe:
            raise AssertionError("byte-level BPE did not preserve natural text")
    print("PASS byte-level tokenizer preserves text and word boundaries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
