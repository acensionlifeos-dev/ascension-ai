"""Reset the 46 category packets to use v1 curricula and start a v3 pass."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "evals" / "growth_packet_queue.json"
TRAIN_DIR = ROOT / "evals" / "training"


def main() -> int:
    queue = json.loads(QUEUE.read_text("utf-8"))
    for p in queue["packets"]:
        num = int(p["id"].split("-")[1])
        if num < 19:
            continue
        m = re.match(r"Category:\s*([\w_]+)", p.get("focus", ""))
        if not m:
            continue
        category = m.group(1)
        v1 = TRAIN_DIR / f"ascension_product_v{num}_{category}.jsonl"
        p["curriculum"] = str(v1.relative_to(ROOT).as_posix())
        p["status"] = "pending"
        p.pop("blocked_by", None)
        p["focus"] = f"Category: {category} (v3 from v1 curriculum)"

    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Queue reset for v3 using v1 curricula.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
