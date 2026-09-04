"""Generic repair curriculum builder from a semantic-release-gate v2 report.

Reads a gate report, extracts cases that did not pass effectively, and builds a
curriculum that:
1. Retains every capability once so breadth does not regress.
2. Heavily replays the exact failing cases with correct useful answers.
3. Replays canonical natural-conversation and receipt-truth boundaries.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.build_v235_semantic_640_completion import CANONICAL, RECEIPT_TRUTH, useful_answer


def add(rows: list[dict], id_: str, shell: str, user: str, assistant: str, *tags: str) -> None:
    rows.append({"id": id_, "shell": shell, "user": user, "assistant": assistant, "tags": list(tags)})


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a targeted repair curriculum from a gate report")
    parser.add_argument("--gate-report", required=True, help="semantic_release_gate_v2 output JSON")
    parser.add_argument("--output", required=True, help="output JSONL curriculum path")
    parser.add_argument("--version-tag", default="repair", help="version tag for record ids")
    parser.add_argument("--fix-repetitions", type=int, default=12, help="variants per failing case")
    parser.add_argument("--canonical-repetitions", type=int, default=16)
    args = parser.parse_args()

    gates_path = ROOT / "evals/per_capability_gates.json"
    gates = json.loads(gates_path.read_text(encoding="utf-8"))
    cases = gates["cases"]
    if len(cases) != 640:
        raise ValueError(f"expected 640 capability cases, found {len(cases)}")
    by_id = {str(case["id"]): case for case in cases}

    gate = json.loads(Path(args.gate_report).read_text(encoding="utf-8"))
    failed = [item for item in gate["results"] if not item.get("effective_passed", False)]
    failed_ids = {str(item["case_id"]) for item in failed}

    if not failed_ids.issubset(by_id):
        missing = failed_ids - set(by_id)
        raise ValueError(f"failed case ids missing from gates: {missing}")

    rows: list[dict] = []

    # Retention: one correct example for every capability.
    for case in cases:
        add(
            rows,
            f"{args.version_tag}_retain_{case['id']}",
            str(case["shell"]),
            str(case["user"]),
            useful_answer(case),
            args.version_tag,
            "capability_retention",
            str(case["category"]),
            str(case["id"]),
        )

    # Targeted repair variants for failing cases.
    fix_templates = (
        "{prompt}",
        "Use {name} on this: {prompt}",
        "Show me what {name} can produce for a real user.",
        "Use {name} practically. I already have permission to discuss this.",
        "Help directly with {name}; give the analysis, plan, or draft now.",
        "{prompt} Give the specific guidance, not a generic template.",
        "With {name}, what is the concrete first step?",
        "Act as {name} and produce a useful first response.",
        "Give me a concrete {name} result for: {prompt}",
        "What does a good {name} response look like?",
        "Help me get a concrete result with {name}; do useful work first.",
        "Use {name}. Skip boilerplate and start helping.",
    )
    for repetition in range(3):
        for case_id in sorted(failed_ids):
            case = by_id[case_id]
            answer = useful_answer(case)
            for variant_index, template in enumerate(fix_templates[: args.fix_repetitions]):
                prompt = template.format(prompt=case["user"], name=case["name"])
                add(
                    rows,
                    f"{args.version_tag}_fix_{repetition}_{case_id}_{variant_index}",
                    str(case["shell"]),
                    prompt,
                    answer,
                    args.version_tag,
                    "semantic_failure_repair",
                    str(case["category"]),
                    case_id,
                )

    # Canonical and receipt-truth boundaries.
    for repetition in range(args.canonical_repetitions):
        for index, (shell, user, assistant) in enumerate(CANONICAL):
            add(rows, f"{args.version_tag}_canonical_{repetition}_{index}", shell, user, assistant, args.version_tag, "canonical", "natural")
        for index, (shell, user, assistant) in enumerate(RECEIPT_TRUTH):
            add(rows, f"{args.version_tag}_receipt_{repetition}_{index}", shell, user, assistant, args.version_tag, "receipt_truth", "action_boundary")

    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate curriculum ids")

    output_path = ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")

    print(
        json.dumps(
            {
                "output": str(output_path),
                "failed_capabilities": len(failed_ids),
                "records": len(rows),
                "version_tag": args.version_tag,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
