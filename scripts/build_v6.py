"""Build v6: all proven master records + all category records, 1 epoch."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAIN_DIR = ROOT / "evals" / "training"
OUTPUT = TRAIN_DIR / "ascension_product_v160_all_v6.jsonl"


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
    combined = proven + cats
    with OUTPUT.open("w", encoding="utf-8") as f:
        for rec in combined:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"v6 combined {len(combined)} records ({len(proven)} proven + {len(cats)} category).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
