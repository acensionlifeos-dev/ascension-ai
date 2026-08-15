"""Build v2 mixed curricula for the 46 category packets.

Each v2 curriculum combines the category-specific examples with a
reinforced set of proven receipt-truth/product examples. This helps the
fine-tuned model retain the Ascension shell gates while learning the
category surface.
"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAIN_DIR = ROOT / "evals" / "training"
QUEUE = ROOT / "evals" / "growth_packet_queue.json"
PROVEN = ROOT / "evals" / "training" / "ascension_product_v4_receipt_truth.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    records = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        raw = raw.strip()
        if not raw:
            continue
        records.append(json.loads(raw))
    return records


def main() -> int:
    queue = json.loads(QUEUE.read_text("utf-8"))
    proven = load_jsonl(PROVEN)
    changed = 0

    for p in queue["packets"]:
        num = int(p["id"].split("-")[1])
        if num < 19:
            continue
        # derive category from current curriculum name
        old = Path(p["curriculum"])
        category = old.stem.split("_", 3)[-1]  # ascension_product_v65_audio -> audio
        v2_path = TRAIN_DIR / f"{old.stem}_v2.jsonl"

        cat_records = load_jsonl(old)
        # prefix proven ids to avoid collisions
        proven_prefix = [
            {**r, "id": f"proven_{r['id']}"}
            for r in proven
        ]
        mixed = cat_records + proven_prefix

        with v2_path.open("w", encoding="utf-8") as f:
            for rec in mixed:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        p["curriculum"] = str(v2_path.relative_to(ROOT).as_posix())
        p["status"] = "pending"
        p.pop("blocked_by", None)
        p["focus"] = p["focus"].split(",")[0] + f", {len(mixed)} records (v2)"
        changed += 1

    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Built {changed} v2 mixed curricula.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
