import re
from collections import defaultdict
from pathlib import Path


def parse_registry(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"=\s*(\[.*\]);", text, re.DOTALL)
    if not match:
        raise SystemExit("Could not find capability array")
    array_text = match.group(1)
    objects = re.findall(r"\{([^{}]*?)\}", array_text, re.DOTALL)
    caps = []
    for obj in objects:
        cap = {}
        for key in ("id", "name", "category", "description", "default_provider", "requires_tier", "executor"):
            m = re.search(rf'{key}:\s*\'([^\']+)\'', obj)
            if m:
                cap[key] = m.group(1)
        m_cost = re.search(r'cost_per_1k_tokens:\s*([0-9.]+)', obj)
        if m_cost:
            cap["cost_per_1k_tokens"] = float(m_cost.group(1)) if "." in m_cost.group(1) else int(m_cost.group(1))
        m_providers = re.search(r'providers:\s*(\[[^\]]*\])', obj)
        if m_providers:
            cap["providers"] = [s.strip().strip("'\"") for s in m_providers.group(1).strip("[]").split(",") if s.strip()]
        else:
            cap["providers"] = [cap.get("default_provider", "ascension-native")]
        caps.append(cap)
    return caps


def format_cap(cap: dict) -> str:
    by_cat = by_category[cap["category"]]
    related = [c["id"] for c in by_cat if c["id"] != cap["id"]][:5]
    if not related:
        related = ["ascension_chat"]
    related_str = "[\n    " + ",\n    ".join(f"'{r}'" for r in related) + "\n  ]"

    clean_name = cap["name"].replace("Ascension ", "")
    related_text = ", ".join(related)
    context = (
        f"Triggers: user asks about {clean_name}, starts a {cap['category']}-domain quest, "
        f"or needs a decision in this area. Cross-references: {related_text}. "
        f"Use with permission-scoped context and a receipt for any action."
    )

    return f"""  {{
    id: '{cap['id']}',
    name: '{cap['name']}',
    category: '{cap['category']}',
    description: '{cap['description']}',
    providers: {cap['providers']},
    default_provider: '{cap['default_provider']}',
    cost_per_1k_tokens: {cap['cost_per_1k_tokens']},
    requires_tier: '{cap['requires_tier']}',
    executor: '{cap['executor']}',
    related_capabilities: {related_str},
    context: '{context}'
  }}"""


def main():
    global by_category
    root = Path(__file__).resolve().parents[1]
    path = root / "src" / "services" / "capability-registry.ts"

    caps = parse_registry(path)
    by_category = defaultdict(list)
    for c in caps:
        by_category[c["category"]].append(c)

    text = path.read_text(encoding="utf-8")
    prefix_match = re.search(r"^(.*?=\s*)\[", text, re.DOTALL)
    if not prefix_match:
        raise SystemExit("Could not find array start")
    prefix = prefix_match.group(1)
    suffix_match = re.search(r"\];\s*(\n.*)$", text, re.DOTALL)
    if not suffix_match:
        raise SystemExit("Could not find array end")
    suffix = suffix_match.group(1)

    array = ",\n".join(format_cap(c) for c in caps)
    new_text = prefix + "[\n" + array + "\n];" + suffix

    path.write_text(new_text, encoding="utf-8")
    print(f"Enriched {len(caps)} capabilities with cross-references")


if __name__ == "__main__":
    main()
