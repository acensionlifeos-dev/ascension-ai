"""Ensure the legacy Render candidate setting resolves to the approved profile."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.model_runtime import resolve_profile_name


def main() -> None:
    assert resolve_profile_name("candidate") == "pro_v231"
    assert resolve_profile_name("pro_v19") == "pro_v19"
    assert resolve_profile_name(" PRO_V231 ") == "pro_v231"
    print("PASS production profile alias")


if __name__ == "__main__":
    main()
