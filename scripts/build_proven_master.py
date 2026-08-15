"""Build a master proven curriculum from all non-category product JSONL files."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAIN_DIR = ROOT / "evals" / "training"
OUTPUT = TRAIN_DIR / "ascension_product_v159_proven_master.jsonl"
EXCLUDED_PREFIX = [f"ascension_product_v{n}_" for n in list(range(65, 110)) + [110]]


def is_category(name: str) -> bool:
    return any(name.startswith(p) for p in EXCLUDED_PREFIX)


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
    for path in sorted(TRAIN_DIR.glob("ascension_product_v*.jsonl")):
        if is_category(path.name):
            continue
        # also skip v2/v3 category variants if any slipped through
        if "_v2" in path.name or "_v3" in path.name or "_v4" in path.name or "_v5" in path.name:
            continue
        for rec in load_jsonl(path):
            all_records.append(rec)

    # deduplicate by id, then re-id to avoid collisions
    seen = set()
    unique = []
    for rec in all_records:
        if rec["id"] in seen:
            continue
        seen.add(rec["id"])
        unique.append(rec)

    with OUTPUT.open("w", encoding="utf-8") as f:
        for rec in unique:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Built proven master with {len(unique)} records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
