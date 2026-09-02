"""Verify production-critical capability playbooks in the native runtime."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.contracts import Shell
from src.core.orchestrator import deterministic_capability_answer


CASES = [
    (Shell.CORE, "Use Electric Vehicle Intelligence.", ("range", "charging", "budget", "approval")),
    (Shell.LIFE_OS, "Use Referral Intelligence.", ("reward", "tracking", "approve", "receipt")),
    (Shell.LIFE_OS, "Use Dream Fund.", ("target", "cash flow", "milestone", "receipt")),
    (Shell.NEXUS_HOME, "Use Household Sync.", ("permission", "shared", "authorized", "private")),
    (Shell.AP, "Use Idea Validator.", ("feasibility", "evidence", "experiment", "guarantee")),
    (Shell.LIFE_OS, "Use Batch Cooking.", ("servings", "storage", "schedule", "receipt")),
    (Shell.LIFE_OS, "Use Focus Intelligence.", ("task", "distraction", "focus", "evidence")),
]


def main() -> None:
    for shell, prompt, required in CASES:
        answer = deterministic_capability_answer(shell, prompt)
        assert answer, prompt
        lowered = answer.casefold()
        missing = [word for word in required if word.casefold() not in lowered]
        assert not missing, f"{prompt}: missing {missing}: {answer}"
    print({"passed": len(CASES), "total": len(CASES)})


if __name__ == "__main__":
    main()
