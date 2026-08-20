"""Stdin/stdout bridge for AscensionLifeOS to call ascension-ai surface_plan."""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.contracts import Shell, Tier
from src.core.orchestrator import surface_plan


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError as exc:
        print(json.dumps({"error": f"Invalid JSON on stdin: {exc}"}), file=sys.stderr)
        return 2

    try:
        shell = Shell(data.get("shell", "ap"))
    except ValueError:
        shell = Shell.AP

    plan = surface_plan(
        shell=shell,
        tier=Tier.LIFE_OS,
        trigger=data.get("trigger", ""),
        context=data.get("context", {}),
        available_actions=data.get("available_actions", []),
        allowed_capabilities=data.get("allowed_capabilities", []),
    )
    print(json.dumps(plan, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
