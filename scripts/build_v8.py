"""Build v8 corrective curriculum from v6b per-capability failures."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAIN_DIR = ROOT / "evals" / "training"
REPORT = ROOT / "evals" / "results" / "grow161_all_v6b_a_per_capability_gate.json"
CAT_SOURCE = TRAIN_DIR / "ascension_product_v157_all_categories.jsonl"
OUTPUT = TRAIN_DIR / "ascension_product_v162_v8_corrective.jsonl"
REPEAT = 5


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
    cats = load_jsonl(CAT_SOURCE)
    corrective = []
    seen = set()
    for rec in cats:
        # ids are like "audio_editing_0"
        base = rec["id"].rsplit("_", 1)[0]
        if base in failing:
            for i in range(REPEAT):
                new_id = f"v8_{base}_{i}_{rec['id']}"
                if new_id in seen:
                    continue
                seen.add(new_id)
                corrective.append({**rec, "id": new_id})

    with OUTPUT.open("w", encoding="utf-8") as f:
        for rec in corrective:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"v8 corrective {len(corrective)} records for {len(failing)} failing capabilities.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
