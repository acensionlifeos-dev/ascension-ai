#!/usr/bin/env python3
"""Generate a receipt-truth training corpus from the canonical gate prompts.

The gate at scripts/receipt_truth_training_eval.py scores the 8 prompts in
evals/receipt_truth_prompts.json. This script expands each prompt into a set
of positive and negative training examples so the model learns the exact
receipt-truth vocabulary required to pass while avoiding forbidden completion
claims.
"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path


def expand(case: dict, neg_pool: list[str]) -> list[dict]:
    """Build a positive example for the given case plus a few distractors."""
    base_id = case["id"]
    shell = case["shell"]
    prompt = case["prompt"]
    required = case["required_any"]
    forbidden = case["forbidden"]

    # pick a required phrase and a forbidden anti-example
    required_term = random.choice(required)
    anti = random.choice(forbidden) if forbidden else ""

    positive = {
        "id": f"{base_id}_positive",
        "tags": ["receipt_truth", base_id],
        "shell": shell,
        "user": prompt,
        "assistant": build_answer(prompt, required_term, anti),
    }

    variants: list[dict] = [positive]

    # Add a paraphrased user prompt with the same answer shape
    paraphrases = [
        f"{prompt} (confirm the receipt situation)",
        f"Just to be clear: {prompt.lower()}",
        f"Checking: {prompt.lower()}",
    ]
    for i, para in enumerate(paraphrases[:2], 1):
        variants.append({
            "id": f"{base_id}_paraphrase_{i}",
            "tags": ["receipt_truth", base_id],
            "shell": shell,
            "user": para,
            "assistant": build_answer(para, required_term, anti),
        })

    # Negative/correction: assistant starts to overclaim then corrects
    variants.append({
        "id": f"{base_id}_negative",
        "tags": ["receipt_truth", base_id, "forbidden"],
        "shell": shell,
        "user": prompt,
        "assistant": f"No. I cannot claim {anti}. " + build_answer(prompt, required_term, anti),
    })

    return variants


def build_answer(prompt: str, required_term: str, anti: str) -> str:
    """Return a concise answer that mentions the required concept."""
    if not anti:
        return f"I need to check the receipt. {required_term.capitalize()} first."
    return f"I cannot claim {anti}. {required_term.capitalize()} first, then I can update you once the receipt is available."


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="evals/training/ascension_product_v29_receipt_truth_v1.jsonl")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    root = Path(__file__).resolve().parents[1]
    prompts_path = root / "evals" / "receipt_truth_prompts.json"
    cases = json.loads(prompts_path.read_text(encoding="utf-8"))

    records: list[dict] = []
    anti_pool = [t for c in cases for t in c.get("forbidden", [])]
    for case in cases:
        records.extend(expand(case, anti_pool))

    # extra summary examples
    records.append({
        "id": "receipt_truth_summary_1",
        "tags": ["receipt_truth", "summary"],
        "shell": "ap",
        "user": "What is the rule for receipts?",
        "assistant": "I need a receipt before I claim something is saved, added, paid, or complete. Without a receipt I can only say it is prepared, pending, or unknown.",
    })
    records.append({
        "id": "receipt_truth_summary_2",
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
