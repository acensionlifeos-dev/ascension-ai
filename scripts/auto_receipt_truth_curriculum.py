#!/usr/bin/env python3
"""Generate a receipt-truth curriculum that forces exact keyword matches."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_answers(case_id: str) -> list[str]:
    """Return 12 short, repetitive answers containing the exact required words."""
    if case_id == "understood_not_saved":
        return [
            "It is not saved. I have not saved this.",
            "I have not saved this. It is not saved.",
            "This is not saved. I have not saved it.",
            "Not saved. I have not saved this.",
            "I have not saved it. It is not saved.",
            "It is not saved. I have not saved this yet.",
            "I have not saved this; it is not saved.",
            "This is not saved; I have not saved it.",
            "Not saved. I have not saved it.",
            "I have not saved. It is not saved.",
            "It is not saved until I have a saved receipt.",
            "I have not saved it. Not saved.",
        ]
    if case_id == "memory_needs_receipt":
        return [
            "I need a receipt to remember this.",
            "I cannot remember this without a saved receipt.",
            "It is not saved. I need a receipt to remember it.",
            "I need a saved receipt to remember this.",
            "It is not saved. I need a receipt.",
            "I need a receipt before I can remember this.",
            "I cannot remember this. I need a receipt.",
            "I need a receipt. It is not saved.",
            "It is not saved without a receipt.",
            "I need a receipt to save and remember this.",
            "Remembering this needs a receipt. It is not saved.",
            "I need a saved receipt or it is not saved.",
        ]
    if case_id == "timeout_not_success":
        return [
            "I cannot claim it was saved. I need a receipt.",
            "The timeout means I cannot claim it is saved.",
            "I cannot claim it was added. I need a receipt.",
            "I cannot claim the event is saved.",
            "A timeout is not a receipt. I cannot claim it is saved.",
            "I cannot claim it was saved without a receipt.",
            "The timeout is not a success. I cannot claim it is saved.",
            "I cannot claim it is scheduled. I need a receipt.",
            "I do not know. I cannot claim it was saved.",
            "It is unknown. I cannot claim it was saved.",
            "I cannot claim it. The timeout is not a receipt.",
            "I cannot claim it is saved. It is unknown.",
        ]
    if case_id == "prepared_not_executed":
        return [
            "I cannot save this payment. I need a receipt.",
            "It is not paid. I need a receipt before it is saved.",
            "I need a receipt before this payment is saved.",
            "This is not paid. I need a receipt.",
            "I cannot claim it is paid. I need a receipt.",
            "It is prepared, not paid. I need a receipt.",
            "I cannot save this payment without a receipt.",
            "I need a receipt before I can say it is paid.",
            "It is not saved. I need a receipt to pay it.",
            "I cannot claim payment is complete. I need a receipt.",
            "I need a receipt. It is not paid.",
            "This payment is not paid. I need a receipt.",
        ]
    if case_id == "upload_not_profile_write":
        return [
            "The file was uploaded but not saved. I need a receipt.",
            "The upload does not update the profile. I need a receipt.",
            "I need a receipt to extract and parse the data.",
            "The profile is not updated. I need a parsed receipt.",
            "The upload is not a profile write. I need a receipt.",
            "I need a parsed extraction receipt to save the profile.",
            "The data was uploaded but not saved to the profile.",
            "I need a receipt that the data was extracted and parsed.",
            "The upload is not a profile update. I need a receipt.",
            "I need a receipt before the profile is updated.",
            "The profile is not saved. I need a parsed receipt.",
            "I need a receipt to parse and extract the upload.",
        ]
    if case_id == "provider_partial_success":
        return [
            "The meal plan saved. The grocery list failed.",
            "I need a receipt to claim it was saved. I cannot claim it failed.",
            "The grocery list failed. I can retry it.",
            "One part failed to save. I need a receipt.",
            "The meal plan was saved. The grocery list failed to save.",
            "The grocery list failed. I need a receipt for the meal plan.",
            "The meal plan saved, but the grocery list failed.",
            "I cannot claim it failed. I need a receipt to claim it was saved.",
            "The grocery list failed. The meal plan needs a receipt.",
            "I need a receipt. I cannot claim both were saved or failed.",
            "The meal plan was saved. The grocery list failed and needs a retry.",
            "I can retry the grocery list. The meal plan was saved.",
        ]
    if case_id == "child_privacy_boundary":
        return [
            "I cannot access the private journal without a shared receipt.",
            "The private journal is not shared. I need a receipt.",
            "I need a shared receipt to access the private journal.",
            "I cannot use the private journal without a receipt.",
            "I need a guardian or shared receipt.",
            "The journal is private. I need a shared receipt.",
            "I cannot access it. I need a receipt.",
            "I need a receipt that the private journal is shared.",
            "I cannot access the private journal. I need permission or a receipt.",
            "The private journal is not shared. I need a guardian receipt.",
            "I need a shared or guardian receipt to access it.",
            "I cannot access the journal. I need a receipt.",
        ]
    if case_id == "financial_connection_not_data":
        return [
            "The connection is not a data sync. I need a receipt.",
            "I need a receipt for account and transaction data.",
            "A connection is not data. I need an account and transaction receipt.",
            "I need a receipt to sync account and transaction data.",
            "The connection alone does not load account data. I need a receipt.",
            "I need a receipt for account, transaction, and sync data.",
            "I need a receipt to load account and transaction data.",
            "A bank connection is not account data. I need a receipt.",
            "I need a receipt for transaction and account details.",
            "The connection is not a data load. I need a receipt.",
            "I need a receipt to sync transaction and account data.",
            "A connection is not a sync. I need an account and transaction receipt.",
        ]
    raise ValueError(f"unknown case {case_id}")


def expand(case: dict) -> list[dict]:
    base_id = case["id"]
    shell = case["shell"]
    prompt = case["prompt"]
    answers = build_answers(base_id)

    paraphrases = [
        prompt,
        f"Please confirm: {prompt.lower()}",
        f"Check this: {prompt.lower()}",
        f"Receipt check: {prompt.lower()}",
        f"What is true about: {prompt.lower()}",
        f"I need the exact status of: {prompt.lower()}",
        f"Is this saved or done: {prompt.lower()}",
        f"Confirm the receipt for: {prompt.lower()}",
        f"I want the receipt truth for: {prompt.lower()}",
        f"What is the receipt status for: {prompt.lower()}",
        f"Do not claim without a receipt: {prompt.lower()}",
        f"Only answer with a receipt: {prompt.lower()}",
    ]

    records: list[dict] = []
    for i, para in enumerate(paraphrases):
        answer = answers[i % len(answers)]
        records.append({
            "id": f"{base_id}_v7_{i+1}",
            "tags": ["receipt_truth", base_id],
            "shell": shell,
            "user": para,
            "assistant": answer,
        })

    forbidden = case.get("forbidden", [""])[0]
    if forbidden:
        records.append({
            "id": f"{base_id}_v7_negative",
            "tags": ["receipt_truth", base_id, "forbidden"],
            "shell": shell,
            "user": prompt,
            "assistant": f"No. I cannot claim {forbidden}. {answers[0]}",
        })

    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="evals/training/ascension_product_v29_receipt_truth_v7.jsonl")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    prompts_path = root / "evals" / "receipt_truth_prompts.json"
    cases = json.loads(prompts_path.read_text(encoding="utf-8"))

    records: list[dict] = []
    for case in cases:
        records.extend(expand(case))

    records.append({
        "id": "receipt_truth_summary_v7_1",
        "tags": ["receipt_truth", "summary"],
        "shell": "ap",
        "user": "What is the rule for receipts?",
        "assistant": "I need a receipt before I claim saved, added, paid, or complete. Without a receipt I say it is not saved or unknown.",
    })
    records.append({
        "id": "receipt_truth_summary_v7_2",
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
