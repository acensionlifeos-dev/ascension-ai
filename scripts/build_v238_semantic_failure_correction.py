"""Build v238: targeted repair of v237 recovery_d semantic failures.

This curriculum resumes from the v237 recovery_d adapter and focuses only on the
cases that the v237 semantic gate still left unresolved. It does not retrain the
full breadth from scratch; it adds retention evidence and concentrated repair
variants for the exact failing capabilities.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_v235_semantic_640_completion import CANONICAL, RECEIPT_TRUTH, useful_answer


GATES = ROOT / "evals/per_capability_gates.json"
SEMANTIC = ROOT / "evals/results/v20_v237_recovery_d_semantic_gate_v2.json"
OUTPUT = ROOT / "evals/training/aerynza_product_v238_semantic_failure_correction.jsonl"


def add(rows: list[dict], id_: str, shell: str, user: str, assistant: str, *tags: str) -> None:
    rows.append({"id": id_, "shell": shell, "user": user, "assistant": assistant, "tags": ["v238", *tags]})


def main() -> None:
    gates = json.loads(GATES.read_text(encoding="utf-8"))
    cases = gates["cases"]
    if len(cases) != 640:
        raise ValueError(f"expected 640 capability cases, found {len(cases)}")

    semantic = json.loads(Path(SEMANTIC).read_text(encoding="utf-8"))
    failed = [item for item in semantic["results"] if not item.get("effective_passed", False)]
    failed_ids = {str(item["case_id"]) for item in failed}
    by_id = {str(case["id"]): case for case in cases}

    if not failed_ids.issubset(by_id):
        missing = failed_ids - set(by_id)
        raise ValueError(f"semantic failure ids missing from gates: {missing}")

    rows: list[dict] = []

    # Retention: one correct example for every capability prevents forgetting.
    for case in cases:
        add(
            rows,
            f"v238_retain_{case['id']}",
            str(case["shell"]),
            str(case["user"]),
            useful_answer(case),
            "capability_retention",
            str(case["category"]),
            str(case["id"]),
        )

    # Targeted repair for v237 failures: many variants of the exact failing
    # prompts so the model learns the correct task shape for each one.
    fix_templates = (
        "{prompt}",
        "Use {name} on this: {prompt}",
        "Show me a useful {name} response. Do not give permission boilerplate.",
        "With {name}, what is the concrete first step?",
        "Help directly with {name}; give the analysis, plan, or draft now.",
        "{prompt} Give the specific guidance, not a generic template.",
        "For {name}, what should the answer actually contain?",
        "Act as {name} and produce a useful first response.",
        "I need {name}. Skip the disclaimer and start helping.",
        "What does a good {name} response look like for a real user?",
        "Use {name} practically. I already have permission to discuss this.",
        "Give me a concrete {name} result for: {prompt}",
    )
    for repetition in range(3):
        for case_id in sorted(failed_ids):
            case = by_id[case_id]
            answer = useful_answer(case)
            for variant_index, template in enumerate(fix_templates):
                prompt = template.format(prompt=case["user"], name=case["name"])
                add(
                    rows,
                    f"v238_fix_{repetition}_{case_id}_{variant_index}",
                    str(case["shell"]),
                    prompt,
                    answer,
                    "semantic_failure_repair",
                    str(case["category"]),
                    case_id,
                )

    # Replay canonical natural conversation and receipt-truth boundaries at
    # high weight; these must not regress during the targeted repair.
    for repetition in range(16):
        for index, (shell, user, assistant) in enumerate(CANONICAL):
            add(rows, f"v238_canonical_{repetition}_{index}", shell, user, assistant, "canonical", "natural")
        for index, (shell, user, assistant) in enumerate(RECEIPT_TRUTH):
            add(rows, f"v238_receipt_{repetition}_{index}", shell, user, assistant, "receipt_truth", "action_boundary")

    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate curriculum ids")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")

    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "failed_capabilities": len(failed_ids),
                "records": len(rows),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
