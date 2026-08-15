"""Combine all 46 v1 category curricula into a single curriculum for v4."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAIN_DIR = ROOT / "evals" / "training"
OUTPUT = TRAIN_DIR / "ascension_product_v157_all_categories.jsonl"


def main() -> int:
    all_records = []
    for num in list(range(65, 110)) + [110]:
        files = sorted(TRAIN_DIR.glob(f"ascension_product_v{num}_*.jsonl"))
        for path in files:
            if "_v" in path.stem and not path.stem.endswith("_v1"):
                # Prefer v1; skip v2/v3 if v1 exists
                v1 = TRAIN_DIR / (path.stem.rsplit("_", 1)[0] + ".jsonl")
                if v1.exists():
                    continue
            for raw in path.read_text(encoding="utf-8").splitlines():
                raw = raw.strip()
                if not raw:
                    continue
                all_records.append(json.loads(raw))
    with OUTPUT.open("w", encoding="utf-8") as f:
        for rec in all_records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Combined {len(all_records)} records from {len(list(range(65,110))+[110])} categories into {OUTPUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
