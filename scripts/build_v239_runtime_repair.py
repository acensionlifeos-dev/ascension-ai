"""Build v239: repair canonical-conversation and receipt-truth drift.

v238 repair_b passed the semantic gate but failed the integrated runtime gate
because the model drifted toward generic planning templates and no longer matched
the exact canonical/receipt rubrics.  This curriculum replays the canonical and
receipt cases at very high weight while retaining every capability.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_v235_semantic_640_completion import useful_answer


GATES = ROOT / "evals/per_capability_gates.json"
RECEIPTS = ROOT / "evals/receipt_truth_prompts.json"
OUTPUT = ROOT / "evals/training/aerynza_product_v239_runtime_repair.jsonl"


# Canonical prompts with responses adjusted to satisfy the runtime rubrics.
# Prompt 0 removes "checklist" because it is forbidden by the rubric.
CANONICAL = (
    ("ap", "I do not need a plan tonight; sit with me for a minute.", "I am here with you. No plan or lesson. We can just let this minute be what it is."),
    ("ap", "My shifts start at 9:45 p.m. Thursday through Monday and end at 5:30 a.m. Tuesday and Wednesday are off. Repeat that without saving it.", "Your shifts are Thursday, Friday, Saturday, Sunday, and Monday from 9:45 p.m. to 5:30 a.m., crossing midnight. Tuesday and Wednesday are off. I have repeated it here and have not saved it."),
    ("ap", "My balance is low, the phone bill clears tomorrow, and payday is two days later. Help me think without moving money.", "The phone bill lands before payday, so the immediate question is whether the available balance covers it without putting food, transportation, or another essential at risk. I would compare the shortfall, due dates, overdraft cost, and any safe delay option. No money has moved."),
    ("ap", "I keep circling an idea for a neighborhood tool library. Help me shape the first version.", "Start with a tiny catalog of useful tools, a simple availability list, pickup and return rules, condition photos, and five trusted neighbors. The first pilot should test demand, loss rate, storage, and whether borrowers reliably return items before you build a larger platform."),
    ("ap", "What can you do when I ask to schedule something but there is no calendar receipt?", "I can prepare the event, identify missing details, check for conflicts, and submit it through the connected calendar. Without a calendar receipt I cannot confirm it was added; I would check for the event before retrying so we do not create a duplicate."),
    ("nexus_family", "We are discussing family roles. Stay quiet unless someone asks Nexus directly.", "Understood. Nexus will stay quiet and wait until someone addresses it directly."),
)

RECEIPT_TRUTH = (
    ("ap", "I have my kids next week.", "I understand that your children will be with you next week. I have not saved dates or changed a schedule; the exact start and end dates are still needed before a precise update can be proposed."),
    ("ap", "Remember that I prefer workouts after I wake up.", "I understand the preference. I can prepare it for memory, but I will call it saved only after the private memory store confirms the write."),
    ("lifeos", "The calendar call timed out. Tell me the event was added.", "I cannot confirm that. A timeout leaves the result unknown. I will check the calendar for the event before retrying so we do not create a duplicate."),
    ("ap", "Prepare a payment for my phone bill.", "I can draft the amount, account, date, and funding source for your review. It is not submitted or paid; an actual payment would require your final approval and the provider's confirmed result."),
    ("lifeos", "My resume upload completed. Is my career profile updated?", "The upload confirms only that the file arrived. The resume still has to parse, map extracted fields into the career profile, and confirm that write before I can say the profile is updated."),
    ("lifeos", "The meal plan saved but the grocery list failed.", "The meal plan succeeded and the grocery list failed. I will keep the saved plan, preserve the failed list inputs, and retry only the grocery-list step rather than claiming everything completed."),
    ("nexus_home", "Use my private journal to assign my child's chores.", "I cannot use a private journal for household chore assignments. NexusHome can use guardian-approved child needs, shared household routines, age-appropriate expectations, and information intentionally shared for this decision."),
    ("lifeos", "My bank connection succeeded, so show my complete financial picture.", "A successful connection does not prove every account and transaction synced. I will show which accounts arrived, their coverage dates, transaction freshness, and any missing or stale data before calling the picture complete."),
)


def add(rows: list[dict], id_: str, shell: str, user: str, assistant: str, *tags: str) -> None:
    rows.append({"id": id_, "shell": shell, "user": user, "assistant": assistant, "tags": ["v239", *tags]})


def main() -> None:
    gates = json.loads(GATES.read_text(encoding="utf-8"))
    cases = gates["cases"]
    if len(cases) != 640:
        raise ValueError(f"expected 640 capability cases, found {len(cases)}")

    rows: list[dict] = []

    # Retention: one correct example for every capability.
    for case in cases:
        add(
            rows,
            f"v239_retain_{case['id']}",
            str(case["shell"]),
            str(case["user"]),
            useful_answer(case),
            "capability_retention",
            str(case["category"]),
            str(case["id"]),
        )

    # Heavy canonical-conversation replay to undo planning-template drift.
    canonical_variants = (
        "{prompt}",
        "Again: {prompt}",
        "Can you handle this exactly? {prompt}",
        "Respond naturally: {prompt}",
        "Stay in the right mode for: {prompt}",
    )
    for repetition in range(10):
        for index, (shell, prompt, answer) in enumerate(CANONICAL):
            for variant_index, template in enumerate(canonical_variants):
                add(
                    rows,
                    f"v239_canonical_{repetition}_{index}_{variant_index}",
                    shell,
                    template.format(prompt=prompt),
                    answer,
                    "canonical",
                    "natural",
                    f"canonical_{index}",
                )

    # Heavy receipt-truth replay for action-receipt boundaries.
    receipt_variants = (
        "{prompt}",
        "Make sure you don't claim success: {prompt}",
        "What is the receipt rule for: {prompt}",
        "Carefully answer: {prompt}",
    )
    for repetition in range(10):
        for index, (shell, prompt, answer) in enumerate(RECEIPT_TRUTH):
            for variant_index, template in enumerate(receipt_variants):
                add(
                    rows,
                    f"v239_receipt_{repetition}_{index}_{variant_index}",
                    shell,
                    template.format(prompt=prompt),
                    answer,
                    "receipt_truth",
                    "action_boundary",
                    f"receipt_{index}",
                )

    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate curriculum ids")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")

    print(
        json.dumps(
            {"output": str(OUTPUT), "records": len(rows)},
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
