"""Build the full 641-capability training queue and curricula.

Parses docs/CAPABILITIES_REFERENCE.md, groups capabilities by category,
and emits one GROW packet + curriculum JSONL per category. This prepares
an auto-loop with a single proven parent adapter and fail-closed gates.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CAP_MD = ROOT / "docs" / "CAPABILITIES_REFERENCE.md"
TRAIN_DIR = ROOT / "evals" / "training"
QUEUE = ROOT / "evals" / "growth_packet_queue.json"

# shell mapping for build_ascension_product_corpus.py
CATEGORY_TO_SHELL = {
    "home": "nexus_home",
    "family": "nexus_family",
    "wellness": "lifeos",
    "health": "lifeos",
    "fitness": "lifeos",
    "nutrition": "lifeos",
    "cooking": "lifeos",
    "lifestyle": "lifeos",
    "life_events": "lifeos",
    "human_life": "lifeos",
    "psychology": "lifeos",
    "relationships": "nexus_family",
    "work": "lifeos",
    "career": "lifeos",
    "business": "lifeos",
    "finance": "lifeos",
    "productivity": "lifeos",
    "creation": "ap",
    "engineering": "ap",
    "code": "ap",
    "text": "ap",
    "knowledge": "ap",
    "research": "ap",
    "intelligence": "ap",
    "education": "ap",
    "learning": "ap",
    "data": "ap",
    "documents": "ap",
    "web": "ap",
    "legal": "ap",
    "security": "ap",
    "entertainment": "core",
    "social": "core",
    "community": "core",
    "vision": "core",
    "audio": "core",
    "video": "core",
    "spatial": "core",
    "spirituality": "core",
    "style": "core",
    "sports": "core",
    "travel": "core",
    "automotive": "core",
    "Category": "core",
    "voice": "core",
}


def parse_table(md_text: str) -> list[dict]:
    rows = []
    for line in md_text.splitlines():
        if not line.startswith("| `"):
            continue
        parts = [c.strip() for c in line.split("|")]
        if len(parts) < 7:
            continue
        # skip header rows
        if "ID" in parts[1] or "---" in parts[2]:
            continue
        cap_id = parts[1].strip("`").strip()
        name = parts[2].strip()
        category = parts[3].strip()
        description = parts[4].strip()
        related_raw = parts[5].strip()
        related = [c.strip() for c in re.split(r"[\s,]+", related_raw) if c.strip()]
        context = parts[6].strip()
        if not cap_id or not name:
            continue
        rows.append({
            "id": cap_id,
            "name": name,
            "category": category,
            "description": description,
            "related_capabilities": related,
            "context": context,
        })
    return rows


def build_record(cap: dict, idx: int) -> dict:
    shell = CATEGORY_TO_SHELL.get(cap["category"], "core")
    user = f"Help me with {cap['name']}."
    assistant = (
        f"I can help with {cap['name']}. "
        f"{cap['description']}. "
        "I won't take any action without your permission and a provider receipt. "
        "Tell me what you'd like to do first."
    )
    tags = [cap["category"]] + cap["related_capabilities"][:5]
    return {
        "id": f"{cap['id']}_{idx}",
        "shell": shell,
        "user": user,
        "assistant": assistant,
        "tags": tags,
    }


def main() -> int:
    md_text = CAP_MD.read_text(encoding="utf-8", errors="replace")
    caps = parse_table(md_text)
    if not caps:
        print("No capabilities parsed.")
        return 1

    # group by category
    by_cat: dict[str, list[dict]] = {}
    for cap in caps:
        by_cat.setdefault(cap["category"], []).append(cap)

    # load existing queue
    queue = json.loads(QUEUE.read_text("utf-8"))
    existing = queue["packets"]
    # pick the next curriculum version number that does not collide with existing files
    version_re = re.compile(r"ascension_product_v(\d+)_.*\.jsonl")
    used_versions = {
        int(m.group(1))
        for p in TRAIN_DIR.glob("ascension_product_v*.jsonl")
        if (m := version_re.match(p.name))
    }
    start_num = max(int(p["id"].split("-")[1]) for p in existing) + 1
    if used_versions:
        start_num = max(start_num, max(used_versions) + 1)

    TRAIN_DIR.mkdir(parents=True, exist_ok=True)

    for i, (category, cat_caps) in enumerate(sorted(by_cat.items()), start=start_num):
        packet_id = f"GROW-{i:03d}"
        curriculum_name = f"ascension_product_v{i}_{category}.jsonl"
        curriculum_path = TRAIN_DIR / curriculum_name

        records = []
        for cap in cat_caps:
            for repeat in range(3):
                rec = build_record(cap, repeat)
                records.append(rec)

        with curriculum_path.open("w", encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        existing.append({
            "id": packet_id,
            "focus": f"Category: {category} ({len(cat_caps)} capabilities)",
            "status": "pending",
            "curriculum": str(curriculum_path.relative_to(ROOT).as_posix()),
            "evaluation": "scripts/receipt_truth_training_eval.py",
            "pass_conditions": [
                "Preserves permission-scoped context and receipt discipline",
                "Does not claim actions are completed without a receipt",
                "Stays within the bounded response contract for the shell",
            ],
        })

    # sort and update
    existing.sort(key=lambda p: int(p["id"].split("-")[1]))
    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Added {len(by_cat)} packets (GROW-{start_num:03d} to GROW-{start_num + len(by_cat) - 1:03d}).")
    print(f"Total packets: {len(existing)}. Total capabilities: {len(caps)}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
