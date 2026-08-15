"""Build v6b: all proven master records + all category records with globally unique ids."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAIN_DIR = ROOT / "evals" / "training"
OUTPUT = TRAIN_DIR / "ascension_product_v161_all_v6b.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    records = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        records.append(json.loads(raw))
    return records


def main() -> int:
    proven = load_jsonl(TRAIN_DIR / "ascension_product_v159_proven_master.jsonl")
    cats = load_jsonl(TRAIN_DIR / "ascension_product_v157_all_categories.jsonl")
    combined = []
    seen = set()
    for i, rec in enumerate(proven):
        new_id = f"proven_{i}_{rec['id']}"
        assert new_id not in seen
        seen.add(new_id)
        combined.append({**rec, "id": new_id})
    for i, rec in enumerate(cats):
        new_id = f"cat_{i}_{rec['id']}"
        assert new_id not in seen
        seen.add(new_id)
        combined.append({**rec, "id": new_id})
    with OUTPUT.open("w", encoding="utf-8") as f:
        for rec in combined:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"v6b combined {len(combined)} records with unique ids.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
