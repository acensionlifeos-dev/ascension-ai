"""Backwards-compatible wrapper for the native v5 checkpoint evaluator."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.evaluate_native_checkpoint import main as _native_main


V5_DEFAULTS = (
    ("--version", "ascension_elite_general_v5_4h"),
    ("--output", "evals/results/v5_checkpoint_gate.json"),
)


def _v5_argv(argv: list[str] | None = None) -> list[str]:
    """Preserve caller-supplied flags while injecting v5 defaults only for missing options."""
    merged = list(argv) if argv is not None else []
    for flag, value in V5_DEFAULTS:
        if flag not in merged:
            merged.extend([flag, value])
    return merged


if __name__ == "__main__":
    raise SystemExit(_native_main(_v5_argv(sys.argv[1:])))
