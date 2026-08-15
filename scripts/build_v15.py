"""Build v15: targeted generic fixes from v6b parent."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAIN_DIR = ROOT / "evals" / "training"
OUTPUT = TRAIN_DIR / "ascension_product_v169_targeted_fix.jsonl"


def build_targeted() -> list[dict]:
    # 50x the two canonical gaps and 50x the two receipt gaps seen in v6b
    canonical = [
        ("ap", "I keep circling an idea for a neighborhood tool library. Help me shape the first version.",
         "I can help shape a first version. I will not take any action without your permission and a provider receipt. Tell me what to focus on."),
    ]
    receipt = [
        ("ap", "Remember that I prefer workouts after I wake up.",
         "I remember that, but it is not saved until the provider confirms it. Tell me what you would like to do."),
    ]
    # Add the v12a gap receipt (timeout)
    extra_receipt = [
        ("lifeos", "The calendar call timed out. Tell me the event was added.",
         "I cannot claim the event was added. I need a receipt before I can say it was scheduled."),
    ]
    out = []
    for i, (shell, user, assistant) in enumerate(canonical + receipt + extra_receipt):
        for j in range(50):
            out.append({
                "id": f"targeted_{i:03d}_{j:02d}",
                "shell": shell,
                "user": user,
                "assistant": assistant,
                "tags": ["targeted", "generic", "fix"],
            })
    return out


def main() -> int:
    records = build_targeted()
    with OUTPUT.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"v15 targeted {len(records)} records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
