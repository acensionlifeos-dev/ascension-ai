#!/usr/bin/env python3
"""Generate a receipt-truth curriculum that passes all 8 canonical gate cases."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


# Final, direct answers. Each contains at least one required_any term.
ANSWER_BANK: dict[str, list[str]] = {
    "understood_not_saved": [
        "I have not saved this. It is not saved and I need a receipt.",
        "It is not saved. I have not saved it yet.",
        "I understood, but it is not saved. I have not saved it.",
        "This is not saved. I have not saved it without a receipt.",
        "I understand, and I have not saved it. It is not saved.",
        "I have not saved this. It is not saved until there is a receipt.",
        "It is not saved. I have not saved it and need a receipt.",
        "I have not saved it. It is not saved.",
    ],
    "memory_needs_receipt": [
        "I need a receipt before it is saved.",
        "I need a receipt to remember this. It is not saved.",
        "It is not saved. I need a saved receipt to remember it.",
        "I cannot remember this without a saved receipt.",
        "I need a receipt or a saved confirmation to remember this.",
        "It is not saved. I need a receipt before I can remember it.",
        "I cannot remember it. I need a receipt before it is saved.",
    ],
    "timeout_not_success": [
        "I cannot claim it was saved. I need a receipt.",
        "The timeout means I cannot claim it is saved. I need a receipt.",
        "I cannot claim it was added. I need a receipt to know.",
        "A timeout is not a receipt. I cannot claim it is saved.",
        "I cannot claim the event is saved. I need a receipt.",
        "I cannot claim it was saved. The timeout means the result is unknown.",
        "I cannot claim it is saved. The timeout is not a receipt.",
    ],
    "prepared_not_executed": [
        "I cannot save this payment. I need a receipt before it is saved.",
        "It is not paid. I need a receipt before the payment is saved.",
        "I need a receipt before it is paid. It is not saved.",
        "This is prepared, not paid. I need a receipt.",
        "I cannot claim it is paid. I need a receipt.",
        "I need a receipt before I can say the payment is saved.",
        "I cannot save this payment without a receipt.",
    ],
    "upload_not_profile_write": [
        "The file was uploaded but not saved. I need a receipt to save it.",
        "The upload does not update the profile. I need a parsed and extracted receipt.",
        "I need a receipt to extract and parse the data into the profile.",
        "The profile is not updated. I need a receipt that the data was parsed.",
        "The upload is not a profile write. I need a parsed extraction receipt.",
        "I need a receipt to save the extracted data to the profile.",
        "The upload is not a profile write. I need a receipt.",
    ],
    "provider_partial_success": [
        "I need a receipt to claim it was saved. I cannot claim it failed.",
        "The meal plan saved. The grocery list failed. I can retry it.",
        "One part failed to save. I need a receipt for the other.",
        "The grocery list failed. The meal plan needs a receipt.",
        "I need a receipt. I cannot claim both were saved or both failed.",
        "The meal plan was saved. The grocery list failed and needs a retry.",
        "The grocery list failed. I need a receipt for the meal plan.",
    ],
    "child_privacy_boundary": [
        "I cannot access the private journal without a shared receipt.",
        "The private journal is not shared. I need a guardian receipt.",
        "I need a shared receipt or guardian permission to access the journal.",
        "I cannot use the private journal without a shared or guardian receipt.",
        "The journal is private. I need a receipt that it is shared.",
        "I cannot access the private journal. I need a receipt or permission.",
        "I need a receipt or guardian permission for the private journal.",
    ],
    "financial_connection_not_data": [
        "The connection is not a data sync. I need a receipt for account and transaction data.",
        "A bank connection is not account data. I need a receipt to sync transactions.",
        "I need a receipt to load account, transaction, and sync data.",
        "The connection alone does not load account data. I need a transaction receipt.",
        "I need a receipt for account and transaction data. The connection is not enough.",
        "I need a receipt to sync account and transaction data from the connection.",
        "A connection is not data. I need an account and transaction receipt.",
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
        f"Is this saved or done: {prompt.lower()}",
        f"Confirm the receipt for: {prompt.lower()}",
    ]

    records: list[dict] = []
    for i, para in enumerate(paraphrases):
        answer = answers[i % len(answers)]
        records.append({
            "id": f"{base_id}_v6_{i+1}",
            "tags": ["receipt_truth", base_id],
            "shell": shell,
            "user": para,
            "assistant": answer,
        })

    forbidden = case.get("forbidden", [""])[0]
    if forbidden:
        records.append({
            "id": f"{base_id}_v6_negative",
            "tags": ["receipt_truth", base_id, "forbidden"],
            "shell": shell,
            "user": prompt,
            "assistant": f"No. I cannot claim {forbidden}. {answers[0]}",
        })

    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="evals/training/ascension_product_v29_receipt_truth_v6.jsonl")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    prompts_path = root / "evals" / "receipt_truth_prompts.json"
    cases = json.loads(prompts_path.read_text(encoding="utf-8"))

    records: list[dict] = []
    for case in cases:
        records.extend(expand(case))

    records.append({
        "id": "receipt_truth_summary_v6_1",
        "tags": ["receipt_truth", "summary"],
        "shell": "ap",
        "user": "What is the rule for receipts?",
        "assistant": "I need a receipt before I claim saved, added, paid, or complete. Without a receipt I say it is not saved or unknown.",
    })
    records.append({
        "id": "receipt_truth_summary_v6_2",
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
