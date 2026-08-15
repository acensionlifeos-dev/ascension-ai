"""Build v9: v6b full curriculum + another full category repeat."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAIN_DIR = ROOT / "evals" / "training"
OUTPUT = TRAIN_DIR / "ascension_product_v163_all_v9.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    records = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        records.append(json.loads(raw))
    return records


def main() -> int:
    v6b = load_jsonl(TRAIN_DIR / "ascension_product_v161_all_v6b.jsonl")
    cats = load_jsonl(TRAIN_DIR / "ascension_product_v157_all_categories.jsonl")
    combined = []
    seen = set()
    for rec in v6b:
        if rec["id"] not in seen:
            seen.add(rec["id"])
            combined.append(rec)
    for i, rec in enumerate(cats):
        new_id = f"v9_{i}_{rec['id']}"
        if new_id in seen:
            continue
        seen.add(new_id)
        combined.append({**rec, "id": new_id})
    with OUTPUT.open("w", encoding="utf-8") as f:
        for rec in combined:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"v9 combined {len(combined)} records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
