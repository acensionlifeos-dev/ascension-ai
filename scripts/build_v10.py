"""Build v10: v6b curriculum + 2 extra copies of v6b failing cases."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAIN_DIR = ROOT / "evals" / "training"
REPORT = ROOT / "evals" / "results" / "grow161_all_v6b_a_per_capability_gate.json"
CAT_SOURCE = TRAIN_DIR / "ascension_product_v157_all_categories.jsonl"
V6B = TRAIN_DIR / "ascension_product_v161_all_v6b.jsonl"
OUTPUT = TRAIN_DIR / "ascension_product_v164_all_v10.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    records = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        records.append(json.loads(raw))
    return records


def main() -> int:
    report = json.loads(REPORT.read_text("utf-8"))
    failing = {r["case_id"] for r in report["results"] if not r["passed"]}
    v6b = load_jsonl(V6B)
    cats = load_jsonl(CAT_SOURCE)
    extra = []
    for rec in cats:
        base = rec["id"].rsplit("_", 1)[0]
        if base in failing:
            extra.append(rec)

    combined = []
    seen = set()
    for rec in v6b:
        if rec["id"] not in seen:
            seen.add(rec["id"])
            combined.append(rec)
    # add two extra copies of failing records with unique ids
    for i, rec in enumerate(extra):
        new_id = f"v10_{i}_{rec['id']}"
        if new_id not in seen:
            seen.add(new_id)
            combined.append({**rec, "id": new_id})
    for i, rec in enumerate(extra):
        new_id = f"v10b_{i}_{rec['id']}"
        if new_id not in seen:
            seen.add(new_id)
            combined.append({**rec, "id": new_id})

    with OUTPUT.open("w", encoding="utf-8") as f:
        for rec in combined:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"v10 combined {len(combined)} records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
