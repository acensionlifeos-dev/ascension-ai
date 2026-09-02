"""Reproducible product gap: all Qwen-supported shells must exist in the canonical Shell contract."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.contracts import SHELL_CONTRACTS, Shell


def supported_shells_from_curriculum() -> set[str]:
    """Shells used by the reviewed product curriculum trainer."""
    from scripts.train_qwen_ascension_lora import SUPPORTED_SHELLS

    return set(SUPPORTED_SHELLS)


def main() -> int:
    shells = {member.value for member in Shell}
    supported = supported_shells_from_curriculum()
    missing = supported - shells
    if missing:
        raise AssertionError(f"Shells used in training missing from contracts.Shell: {sorted(missing)}")

    missing_contracts = supported - {member.value for member in SHELL_CONTRACTS}
    if missing_contracts:
        raise AssertionError(f"Shells missing from SHELL_CONTRACTS: {sorted(missing_contracts)}")

    print("PASS: all curriculum shells have enum members and contracts")
    print(f"shells: {sorted(shells)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
