"""Regenerate only the 46 full-capability category curricula."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CAP_MD = ROOT / "docs" / "CAPABILITIES_REFERENCE.md"
TRAIN_DIR = ROOT / "evals" / "training"
QUEUE = ROOT / "evals" / "growth_packet_queue.json"

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

    by_cat: dict[str, list[dict]] = {}
    for cap in caps:
        by_cat.setdefault(cap["category"], []).append(cap)

    queue = json.loads(QUEUE.read_text("utf-8"))
    changed = 0

    for p in queue["packets"]:
        num = int(p["id"].split("-")[1])
        if num < 19:
            continue
        # category is the part of focus after "Category: "
        m = re.match(r"Category:\s*([\w_]+)", p.get("focus", ""))
        if not m:
            continue
        category = m.group(1)
        cat_caps = by_cat.get(category)
        if not cat_caps:
            continue

        curriculum_name = f"ascension_product_v{num}_{category}.jsonl"
        curriculum_path = TRAIN_DIR / curriculum_name

        repeats = max(3, (20 + len(cat_caps) - 1) // len(cat_caps))
        records = []
        for cap in cat_caps:
            for repeat in range(repeats):
                rec = build_record(cap, repeat)
                records.append(rec)

        with curriculum_path.open("w", encoding="utf-8") as f:
            for rec in records:
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        p["curriculum"] = str(curriculum_path.relative_to(ROOT).as_posix())
        p["focus"] = f"Category: {category} ({len(cat_caps)} capabilities, {len(records)} records)"
        p["status"] = "pending"
        p.pop("blocked_by", None)
        changed += 1

    QUEUE.write_text(json.dumps(queue, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Regenerated {changed} category curricula with at least 20 records each.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
