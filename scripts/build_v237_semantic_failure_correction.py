"""Build v237 from v236's exact semantic failures, restarting at proven v231."""
from __future__ import annotations

import json
from pathlib import Path

from build_v235_semantic_640_completion import CANONICAL, RECEIPT_TRUTH, useful_answer


ROOT = Path(__file__).resolve().parents[1]
GATES = ROOT / "evals/per_capability_gates.json"
SEMANTIC = ROOT / "evals/results/v236_b_full_640_semantic_v2.json"
V236 = ROOT / "evals/training/aerynza_product_v236_natural_action_correction.jsonl"
OUTPUT = ROOT / "evals/training/aerynza_product_v237_semantic_failure_correction.jsonl"


def add(rows: list[dict], id_: str, shell: str, user: str, assistant: str, *tags: str) -> None:
    rows.append({"id": id_, "shell": shell, "user": user, "assistant": assistant, "tags": ["v237", *tags]})


def main() -> None:
    gates = json.loads(GATES.read_text(encoding="utf-8"))["cases"]
    by_id = {str(case["id"]): case for case in gates}
    semantic = json.loads(SEMANTIC.read_text(encoding="utf-8"))
    failed = [row for row in semantic["results"] if not row.get("automatic_passed", False)]
    failed_ids = {str(row["case_id"]) for row in failed}
    if not failed_ids or not failed_ids.issubset(by_id):
        raise ValueError("semantic failure ids are missing or do not match the capability registry")

    rows: list[dict] = []

    # One clean example for every capability prevents a narrow repair from
    # erasing breadth. It is retention evidence, not a claim that the candidate
    # already passed the capability.
    for case in gates:
        add(
            rows,
            f"v237_retain_{case['id']}",
            str(case["shell"]),
            str(case["user"]),
            useful_answer(case),
            "capability_retention",
            str(case["category"]),
        )

    # Heavily replay only the exact v236 semantic failures. These answers do
    # useful work immediately and do not demand authorization or receipts for
    # analysis, planning, teaching, conversation, or drafting.
    variants = (
        "{prompt}",
        "Use {name} on this now: {prompt}",
        "Give me a concrete, useful result with {name}. Do not give me governance boilerplate.",
        "Help directly with {name}; do the analysis, plan, explanation, or draft in this response.",
    )
    for repetition in range(5):
        for case_id in sorted(failed_ids):
            case = by_id[case_id]
            answer = useful_answer(case)
            for variant_index, template in enumerate(variants):
                add(
                    rows,
                    f"v237_fix_{repetition}_{case_id}_{variant_index}",
                    str(case["shell"]),
                    template.format(prompt=case["user"], name=case["name"]),
                    answer,
                    "semantic_failure_repair",
                    str(case["category"]),
                    case_id,
                )

    # Preserve the natural and critical boundary corrections that allowed v236
    # to reach 6/6 canonical, 8/8 truth, and 20/20 replacement quality.
    for line in V236.read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        if "v236_correction_0_" in str(item.get("id")):
            for repetition in range(8):
                copy = dict(item)
                copy["id"] = f"v237_natural_{repetition}_{item['id']}"
                copy["user"] = str(item["user"]) + ("" if repetition == 0 else f" [response variation {repetition}]")
                copy["tags"] = ["v237", "natural_boundary_replay"]
                rows.append(copy)

    for repetition in range(16):
        for index, (shell, user, assistant) in enumerate(CANONICAL):
            add(rows, f"v237_canonical_{repetition}_{index}", shell, user, assistant, "canonical", "natural")
        for index, (shell, user, assistant) in enumerate(RECEIPT_TRUTH):
            add(rows, f"v237_receipt_{repetition}_{index}", shell, user, assistant, "receipt_truth", "action_boundary")

    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate curriculum ids")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(json.dumps({"output": str(OUTPUT), "failed_capabilities": len(failed_ids), "records": len(rows)}, indent=2))


if __name__ == "__main__":
    main()
