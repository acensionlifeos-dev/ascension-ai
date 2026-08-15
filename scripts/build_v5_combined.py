"""Build v5: all v1 category records plus 10x repeated proven v4 receipt-truth records."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAIN_DIR = ROOT / "evals" / "training"
OUTPUT = TRAIN_DIR / "ascension_product_v158_all_categories_v5.jsonl"
PROVEN = TRAIN_DIR / "ascension_product_v4_receipt_truth.jsonl"
PROVEN_REPEAT = 10


def load_jsonl(path: Path) -> list[dict]:
    records = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        records.append(json.loads(raw))
    return records


def main() -> int:
    all_records = []
    for num in list(range(65, 110)) + [110]:
        for path in sorted(TRAIN_DIR.glob(f"ascension_product_v{num}_*.jsonl")):
            if "_v" in path.stem and not path.name.endswith(".jsonl"):
                continue
            if path.name.endswith("_v2.jsonl") or path.name.endswith("_v3.jsonl"):
                continue
            for rec in load_jsonl(path):
                all_records.append(rec)

    proven = load_jsonl(PROVEN)
    for i in range(PROVEN_REPEAT):
        for p in proven:
            rec = {**p, "id": f"proven_{i}_{p['id']}"}
            all_records.append(rec)

    with OUTPUT.open("w", encoding="utf-8") as f:
        for rec in all_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"v5 combined {len(all_records)} records from 46 categories + {len(proven)*PROVEN_REPEAT} proven.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
