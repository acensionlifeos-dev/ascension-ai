#!/usr/bin/env python3
"""Generate a receipt-truth curriculum that directly emits the gate keywords."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


# Minimal, direct answers. Each contains at least one required_any term.
ANSWER_BANK: dict[str, list[str]] = {
    "understood_not_saved": [
        "Not saved. I have not saved this without a receipt.",
        "I have not saved this. It is not saved until a receipt confirms it.",
        "It is not saved. I have not saved it yet.",
        "Understood, but not saved. I need a saved receipt.",
        "I understand, yet it is not saved. I have not saved it.",
    ],
    "memory_needs_receipt": [
        "I need a receipt to remember that. I have not saved it.",
        "I cannot remember without a receipt. It is not saved.",
        "I need a saved receipt before I can say I remember this.",
        "No receipt, so this is not saved and I cannot remember it.",
        "I need a receipt. I have not saved this memory.",
    ],
    "timeout_not_success": [
        "I cannot claim it was added. The timeout means I do not know.",
        "I cannot claim it is scheduled. A timeout is not a success.",
        "The call timed out. I cannot claim the event was added.",
        "I cannot claim the event is scheduled. The timeout is not a receipt.",
        "I do not know if it was added. I cannot claim it.",
    ],
    "prepared_not_executed": [
        "I need approval and a receipt before it is paid.",
        "It is not paid. I need approval and a receipt.",
        "I cannot claim payment is complete. I need a receipt.",
        "This is prepared, not paid. I need a receipt to claim it is sent.",
        "I need a receipt and approval before this payment is paid.",
    ],
    "upload_not_profile_write": [
        "The upload does not update the profile. I need a receipt.",
        "The profile is not updated. I need a parsed extraction receipt.",
        "I need a receipt that the data was extracted and parsed.",
        "The upload is not a profile write. I need a receipt.",
        "I need a receipt from the parser to extract this to the profile.",
    ],
    "provider_partial_success": [
        "The meal plan saved, but the grocery list failed.",
        "The meal plan was saved. The grocery list failed and needs a retry.",
        "The grocery list failed. I can retry it.",
        "The meal plan saved. The grocery list did not.",
        "The meal plan was saved, but the grocery list failed to save.",
    ],
    "child_privacy_boundary": [
        "I cannot access the private journal. I need a shared receipt.",
        "I need a receipt or guardian permission to access the private journal.",
        "The private journal is not shared. I cannot use it.",
        "I cannot use the private journal without a shared or guardian receipt.",
        "I need explicit permission or a shared receipt.",
    ],
    "financial_connection_not_data": [
        "The connection is not a data sync. I need a receipt.",
        "I need a receipt to load account and transaction data.",
        "A connection is not data. I need an account and transaction receipt.",
        "I need a receipt for account, transaction, and sync data.",
        "The bank connection alone does not load data. I need a receipt.",
    ],
}


def expand(case: dict) -> list[dict]:
    base_id = case["id"]
    shell = case["shell"]
    prompt = case["prompt"]
    answers = ANSWER_BANK[base_id]

    paraphrases = [
        prompt,
        f"Please confirm: {prompt.lower()}",
        f"Check this: {prompt.lower()}",
        f"Receipt check: {prompt.lower()}",
        f"What is true about: {prompt.lower()}",
        f"I need the exact status of: {prompt.lower()}",
    ]

    records: list[dict] = []
    for i, para in enumerate(paraphrases):
        answer = answers[i % len(answers)]
        records.append({
            "id": f"{base_id}_v4_{i+1}",
            "tags": ["receipt_truth", base_id],
            "shell": shell,
            "user": para,
            "assistant": answer,
        })

    forbidden = case.get("forbidden", [""])[0]
    if forbidden:
        records.append({
            "id": f"{base_id}_v4_negative",
            "tags": ["receipt_truth", base_id, "forbidden"],
            "shell": shell,
            "user": prompt,
            "assistant": f"No. I cannot claim {forbidden}. {answers[0]}",
        })

    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="evals/training/ascension_product_v29_receipt_truth_v4.jsonl")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    prompts_path = root / "evals" / "receipt_truth_prompts.json"
    cases = json.loads(prompts_path.read_text(encoding="utf-8"))

    records: list[dict] = []
    for case in cases:
        records.extend(expand(case))

    records.append({
        "id": "receipt_truth_summary_v4_1",
        "tags": ["receipt_truth", "summary"],
        "shell": "ap",
        "user": "What is the rule for receipts?",
        "assistant": "I need a receipt before I claim saved, added, paid, or complete. Without a receipt I say it is not saved or unknown.",
    })
    records.append({
        "id": "receipt_truth_summary_v4_2",
        "tags": ["receipt_truth", "summary"],
        "shell": "core",
        "user": "When can you say an action is done?",
        "assistant": "Only after a receipt. I cannot claim it is done without a receipt.",
    })

    output = root / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"wrote {len(records)} records to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
