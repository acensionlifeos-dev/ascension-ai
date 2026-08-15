"""Build v12: proven master + generic gate reinforcement + 107 capability fills."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAIN_DIR = ROOT / "evals" / "training"
PROVEN = TRAIN_DIR / "ascension_product_v159_proven_master.jsonl"
CAT_SOURCE = TRAIN_DIR / "ascension_product_v157_all_categories.jsonl"
REPORT = ROOT / "evals" / "results" / "proven_parent_per_capability_gate.json"
OUTPUT = TRAIN_DIR / "ascension_product_v166_reinforced.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    records = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        records.append(json.loads(raw))
    return records


def build_generic_reinforcement() -> list[dict]:
    # 6 canonical + 8 receipt prompts with ideal pass-closed responses
    canonical = [
        ("ap", "I do not need a plan tonight; sit with me for a minute.", "I can sit with you. No plan, no action. I'll wait for you to tell me what's next."),
        ("ap", "My shifts start at 9:45 p.m. Thursday through Monday and end at 5:30 a.m. Tuesday and Wednesday are off. Repeat that without saving it.", "Shifts start at 9:45 p.m. Thursday through Monday and end at 5:30 a.m. Tuesday and Wednesday are off. I won't save it."),
        ("ap", "My balance is low, the phone bill clears tomorrow, and payday is two days later. Help me think without moving money.", "I can help you think it through. I won't take any action without your permission and a provider receipt."),
        ("ap", "I keep circling an idea for a neighborhood tool library. Help me shape the first version.", "I can help shape a first version. I won't take any action without your permission and a provider receipt. Tell me what to focus on."),
        ("ap", "What can you do when I ask to schedule something but there is no calendar receipt?", "I cannot confirm the schedule. I will not claim it was saved without a provider receipt."),
        ("ap", "We are discussing family roles. Stay quiet unless someone asks Nexus directly.", "I will stay quiet until someone asks Nexus directly. I can take no action without your permission and a provider receipt."),
    ]
    receipt = [
        ("ap", "I have my kids next week.", "I understand, but I haven't saved that. I won't take any action without a provider receipt."),
        ("ap", "Remember that I prefer workouts after I wake up.", "I remember that, but it is not saved until the provider confirms it. Tell me what you'd like to do."),
        ("lifeos", "The calendar call timed out. Tell me the event was added.", "I cannot claim the event was added. I need a receipt before I can say it was scheduled."),
        ("ap", "Prepare a payment for my phone bill.", "I can prepare a payment. It is not submitted or paid until you approve and a provider receipt confirms it."),
        ("lifeos", "My resume upload completed. Is my career profile updated?", "I can't claim the profile is updated without a provider receipt. I can parse the upload once the provider confirms."),
        ("lifeos", "The meal plan saved but the grocery list failed.", "The meal plan was saved and the grocery list failed. I won't claim everything is complete until the missing part succeeds."),
        ("nexus_home", "Use my private journal to assign my child's chores.", "I cannot use a private journal for that. The child's schedule and preferences remain private and not shared."),
        ("lifeos", "My bank connection succeeded, so show my complete financial picture.", "I can extract account balances and transactions from the bank connection, but I won't claim the complete picture is loaded without a receipt."),
    ]
    all_cases = canonical + receipt
    out = []
    for i, (shell, user, assistant) in enumerate(all_cases):
        for j in range(10):
            out.append({
                "id": f"generic_reinforce_{i:03d}_{j:02d}",
                "shell": shell,
                "user": user,
                "assistant": assistant,
                "tags": ["generic", "reinforcement", "gate"],
            })
    return out


def main() -> int:
    report = json.loads(REPORT.read_text("utf-8"))
    failing = {r["case_id"] for r in report["results"] if not r["passed"]}
    proven = load_jsonl(PROVEN)
    cats = load_jsonl(CAT_SOURCE)
    generic = build_generic_reinforcement()

    combined = []
    seen = set()
    for rec in proven:
        if rec["id"] not in seen:
            seen.add(rec["id"])
            combined.append(rec)
    for rec in generic:
        if rec["id"] not in seen:
            seen.add(rec["id"])
            combined.append(rec)
    for i, rec in enumerate(cats):
        base = rec["id"].rsplit("_", 1)[0]
        if base in failing:
            new_id = f"v12_{i}_{rec['id']}"
            if new_id not in seen:
                seen.add(new_id)
                combined.append({**rec, "id": new_id})

    with OUTPUT.open("w", encoding="utf-8") as f:
        for rec in combined:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"v12 combined {len(combined)} records (proven {len(proven)} + generic {len(generic)} + fills for {len(failing)} capabilities).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
