"""Build v13: triple proven master + 107 capability fills."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAIN_DIR = ROOT / "evals" / "training"
PROVEN = TRAIN_DIR / "ascension_product_v159_proven_master.jsonl"
CAT_SOURCE = TRAIN_DIR / "ascension_product_v157_all_categories.jsonl"
REPORT = ROOT / "evals" / "results" / "proven_parent_per_capability_gate.json"
OUTPUT = TRAIN_DIR / "ascension_product_v167_triple_proven.jsonl"


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
    proven = load_jsonl(PROVEN)
    cats = load_jsonl(CAT_SOURCE)

    combined = []
    seen = set()
    for _ in range(3):
        for rec in proven:
            key = f"triple_{_}_{rec['id']}"
            if key not in seen:
                seen.add(key)
                combined.append({**rec, "id": key})
    for i, rec in enumerate(cats):
        base = rec["id"].rsplit("_", 1)[0]
        if base in failing:
            new_id = f"v13_{i}_{rec['id']}"
            if new_id not in seen:
                seen.add(new_id)
                combined.append({**rec, "id": new_id})

    with OUTPUT.open("w", encoding="utf-8") as f:
        for rec in combined:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"v13 combined {len(combined)} records (proven x3 {len(proven)*3} + fills for {len(failing)} capabilities).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
