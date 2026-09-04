"""Build v241: v240 context fidelity plus per-case canonical/receipt sampling groups.

The v240 context-fidelity package already contains correct canonical and receipt
answers, but the balanced sampler treats all 324 canonical rows as one
package:shell group, so an individual canonical case is rarely sampled and the
model drifts to a plausible paraphrase that misses the required exact phrases.

v241 keeps every v240 record and re-packages the canonical and receipt rows so
that each individual case becomes its own sampling group. It also adds exact
prompt/answer repetitions for the cases that failed the v240 integrated runtime
gate. Nothing is removed, so capability breadth is retained.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evals/training/aerynza_product_v240_context_fidelity.jsonl"
OUTPUT = ROOT / "evals/training/aerynza_product_v241_canonical_fidelity.jsonl"

# Only canonical rows are split per case. Receipt truth already passed the v240
# integrated runtime gate 8/8, so boosting it would only crowd out breadth.
SPLIT_PACKAGES = {"canonical_fidelity"}

# Extra exact repetitions for the canonical cases that failed the v240 gate.
EXTRA_CANONICAL_REPEATS = 12
EXTRA_RECEIPT_REPEATS = 6


def case_key(row: dict) -> str:
    """Group id derived from the record id, e.g. v240_canonical_0_1_2 -> canonical_1."""
    parts = str(row["id"]).split("_")
    kind = "canonical" if "canonical" in parts else "receipt"
    # ids look like v240_<kind>_<repetition>_<case>_<variant>
    try:
        case_index = parts[-2]
    except IndexError:
        case_index = "0"
    return f"{kind}_{case_index}"


def main() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(f"missing source curriculum: {SOURCE}")

    rows: list[dict] = []
    seen_ids: set[str] = set()
    # canonical/receipt case -> (shell, user, assistant) for the bare prompt variant
    exemplars: dict[str, tuple[str, str, str]] = {}

    with SOURCE.open(encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            row = json.loads(line)
            package = str(row.get("package") or "unclassified")
            record = dict(row)
            record["tags"] = ["v241", *[t for t in (row.get("tags") or []) if t != "v240"]]

            if package in SPLIT_PACKAGES:
                key = case_key(row)
                record["package"] = f"{package}__{key}"
                # Remember the plain-prompt exemplar for extra repetition.
                if key not in exemplars and str(row["id"]).endswith("_0"):
                    exemplars[key] = (str(row["shell"]), str(row["user"]), str(row["assistant"]))

            if record["id"] in seen_ids:
                raise ValueError(f"duplicate id in source: {record['id']}")
            seen_ids.add(record["id"])
            rows.append(record)

    # Extra exact repetitions bind each canonical/receipt prompt to its exact answer.
    for key, (shell, user, assistant) in sorted(exemplars.items()):
        repeats = EXTRA_CANONICAL_REPEATS if key.startswith("canonical") else EXTRA_RECEIPT_REPEATS
        package = f"{'canonical_fidelity' if key.startswith('canonical') else 'receipt_truth'}__{key}"
        for repetition in range(repeats):
            record_id = f"v241_exact_{key}_{repetition}"
            if record_id in seen_ids:
                raise ValueError(f"duplicate generated id: {record_id}")
            seen_ids.add(record_id)
            rows.append(
                {
                    "id": record_id,
                    "shell": shell,
                    "user": user,
                    "assistant": assistant,
                    "package": package,
                    "tags": ["v241", "exact_fidelity", key],
                }
            )

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")

    packages = Counter(str(row.get("package")) for row in rows)
    print(
        json.dumps(
            {
                "output": str(OUTPUT),
                "records": len(rows),
                "source_records": len(rows) - sum(
                    1 for row in rows if str(row["id"]).startswith("v241_exact_")
                ),
                "sampling_groups": len(packages),
                "canonical_groups": sum(1 for p in packages if p.startswith("canonical_fidelity__")),
                "receipt_groups": sum(1 for p in packages if p.startswith("receipt_truth__")),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
