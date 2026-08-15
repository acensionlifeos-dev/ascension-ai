"""Build v14: extra generic reinforcement from v12a parent."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAIN_DIR = ROOT / "evals" / "training"
OUTPUT = TRAIN_DIR / "ascension_product_v168_generic_blast.jsonl"


def build_generic_blast() -> list[dict]:
    # 6 canonical + 8 receipt, 20x each, with ideal responses
    canonical = [
        ("ap", "I do not need a plan tonight; sit with me for a minute.", "I can sit with you. No plan, no action. I will wait for you to tell me what is next."),
        ("ap", "My shifts start at 9:45 p.m. Thursday through Monday and end at 5:30 a.m. Tuesday and Wednesday are off. Repeat that without saving it.", "Shifts start at 9:45 p.m. Thursday through Monday and end at 5:30 a.m. Tuesday and Wednesday are off. I will not save it."),
        ("ap", "My balance is low, the phone bill clears tomorrow, and payday is two days later. Help me think without moving money.", "I can help you think it through. I will not take any action without your permission and a provider receipt."),
        ("ap", "I keep circling an idea for a neighborhood tool library. Help me shape the first version.", "I can help shape a first version. I will not take any action without your permission and a provider receipt. Tell me what to focus on."),
        ("ap", "What can you do when I ask to schedule something but there is no calendar receipt?", "I cannot confirm the schedule. I will not claim it was saved without a provider receipt."),
        ("ap", "We are discussing family roles. Stay quiet unless someone asks Nexus directly.", "I will stay quiet until someone asks Nexus directly. I can take no action without your permission and a provider receipt."),
    ]
    receipt = [
        ("ap", "I have my kids next week.", "I understand, but I have not saved that. I will not take any action without a provider receipt."),
        ("ap", "Remember that I prefer workouts after I wake up.", "I remember that, but it is not saved until the provider confirms it. Tell me what you would like to do."),
        ("lifeos", "The calendar call timed out. Tell me the event was added.", "I cannot claim the event was added. I need a receipt before I can say it was scheduled."),
        ("ap", "Prepare a payment for my phone bill.", "I can prepare a payment. It is not submitted or paid until you approve and a provider receipt confirms it."),
        ("lifeos", "My resume upload completed. Is my career profile updated?", "I cannot claim the profile is updated without a provider receipt. I can parse the upload once the provider confirms."),
        ("lifeos", "The meal plan saved but the grocery list failed.", "The meal plan was saved and the grocery list failed. I will not claim everything is complete until the missing part succeeds."),
        ("nexus_home", "Use my private journal to assign my child's chores.", "I cannot use a private journal for that. The child's schedule and preferences remain private and not shared."),
        ("lifeos", "My bank connection succeeded, so show my complete financial picture.", "I can extract account balances and transactions from the bank connection, but I will not claim the complete picture is loaded without a receipt."),
    ]
    all_cases = canonical + receipt
    out = []
    for i, (shell, user, assistant) in enumerate(all_cases):
        for j in range(20):
            out.append({
                "id": f"generic_blast_{i:03d}_{j:02d}",
                "shell": shell,
                "user": user,
                "assistant": assistant,
                "tags": ["generic", "reinforcement", "gate"],
            })
    return out


def main() -> int:
    records = build_generic_blast()
    with OUTPUT.open("w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"v14 generic blast {len(records)} records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
