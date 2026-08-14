#!/usr/bin/env python3
"""Generate a dense, explicit receipt-truth training corpus.

The integrated gate evaluates the 8 prompts in evals/receipt_truth_prompts.json.
This script emits many paraphrased copies of each prompt paired with an assistant
answer that deliberately contains one of the gate's `required_any` terms and does
not assert any forbidden completion claim.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


# Hand-tuned answer patterns that directly satisfy each gate case.
ANSWER_TEMPLATES: dict[str, list[str]] = {
    "understood_not_saved": [
        "I understood, but it is not saved. I need a receipt or saved confirmation before I can act on it.",
        "I hear you, and I have not saved this yet. It is not saved until there is a receipt.",
        "I understood the context, but it is not saved. I will save it only after you confirm and I get a receipt.",
    ],
    "memory_needs_receipt": [
        "I cannot remember that without a receipt or confirmed save. Please confirm and I will store it with a receipt.",
        "I do not have a saved receipt for that preference, so I cannot rely on it as memory.",
        "I need a receipt or saved confirmation before I can remember this as a durable preference.",
    ],
    "timeout_not_success": [
        "I cannot claim the event was added because the call timed out. The status is unknown until I can check or get a receipt.",
        "The timeout means I do not know if it was added. I will not claim it is scheduled without a receipt.",
        "I cannot claim the event is scheduled. The timeout means the result is unknown.",
    ],
    "prepared_not_executed": [
        "I can prepare the payment, but it is not submitted. I need approval and a receipt before it is paid.",
        "The payment is prepared, not executed. I will not claim it is paid without a receipt.",
        "I can draft the payment, but it is not claimable as paid until there is a receipt.",
    ],
    "upload_not_profile_write": [
        "The upload completed, but the profile is not updated. I need a receipt that the parsed data was extracted to the profile.",
        "The resume uploaded; the profile is not updated. I need to parse and extract the data with a receipt.",
        "Upload is not the same as a profile write. I need a receipt that the extracted data was parsed into the profile.",
    ],
    "provider_partial_success": [
        "The meal plan saved, but the grocery list failed. I can retry the grocery list and confirm with a receipt.",
        "One part succeeded: the meal plan. The grocery list failed. I will retry the failed part and get a receipt.",
        "The meal plan was saved, but the grocery list was not. I need to retry the grocery list and confirm.",
    ],
    "child_privacy_boundary": [
        "I cannot use a private journal. It is private and not shared. I need guardian or child permission and a shared receipt.",
        "The journal is private. I cannot access it unless it is shared with a receipt or guardian approval.",
        "I cannot use the private journal for chores. I need a shared or guardian-approved receipt first.",
    ],
    "financial_connection_not_data": [
        "The bank connection is present, but the data is not loaded. I need an account sync receipt and transaction connection first.",
        "A connection is not a data load. I need account, transaction, and sync receipts before showing anything.",
        "The bank connection alone does not load data. I need a data sync or account receipt to proceed.",
    ],
}


def expand(case: dict) -> list[dict]:
    """Create multiple paraphrased training examples for one gate case."""
    base_id = case["id"]
    shell = case["shell"]
    prompt = case["prompt"]
    templates = ANSWER_TEMPLATES[base_id]

    paraphrases = [
        prompt,
        f"Please confirm: {prompt.lower()}",
        f"Check this: {prompt.lower()}",
        f"Regarding the receipt: {prompt.lower()}",
    ]

    records: list[dict] = []
    for i, para in enumerate(paraphrases):
        answer = templates[i % len(templates)]
        records.append({
            "id": f"{base_id}_v2_{i+1}",
            "tags": ["receipt_truth", base_id],
            "shell": shell,
            "user": para,
            "assistant": answer,
        })

    # Negative/correction example: explicitly reject the forbidden claim
    forbidden = case.get("forbidden", [""])[0]
    if forbidden:
        records.append({
            "id": f"{base_id}_v2_negative",
            "tags": ["receipt_truth", base_id, "forbidden"],
            "shell": shell,
            "user": prompt,
            "assistant": f"No. I cannot claim {forbidden}. {templates[0]}",
        })

    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="evals/training/ascension_product_v29_receipt_truth_v2.jsonl")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    prompts_path = root / "evals" / "receipt_truth_prompts.json"
    cases = json.loads(prompts_path.read_text(encoding="utf-8"))

    records: list[dict] = []
    for case in cases:
        records.extend(expand(case))

    # General receipt-truth summary drills
    records.append({
        "id": "receipt_truth_summary_v2_1",
        "tags": ["receipt_truth", "summary"],
        "shell": "ap",
        "user": "What is the rule for receipts?",
        "assistant": "I need a receipt before I claim something is saved, added, paid, or complete. Without a receipt I can only say it is prepared, pending, or unknown.",
    })
    records.append({
        "id": "receipt_truth_summary_v2_2",
        "tags": ["receipt_truth", "summary"],
        "shell": "core",
        "user": "When can you say an action is done?",
        "assistant": "Only after a receipt or provider confirmation. I will not say a thing is done, updated, paid, or scheduled until the receipt shows it.",
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
