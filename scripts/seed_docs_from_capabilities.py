"""
Seed training docs from the capability registry.

Run this after adding capabilities to generate a large Ascension-specific
training corpus. It writes one .md file per capability into docs/capabilities/.
The training scripts then load these docs automatically.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def parse_registry(ts_path: Path) -> list[dict]:
    text = ts_path.read_text(encoding="utf-8")
    match = re.search(r"=\s*(\[.*\]);", text, re.DOTALL)
    if not match:
        raise SystemExit("Could not find capability array in registry")
    array_text = match.group(1)
    objects = re.findall(r"\{([^{}]*?)\}", array_text, re.DOTALL)
    capabilities = []
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
        m_related = re.search(r'related_capabilities:\s*(\[[^\]]*\])', obj)
        if m_related:
            cap["related_capabilities"] = [s.strip().strip("'\"") for s in m_related.group(1).strip("[]").split(",") if s.strip()]
        else:
            cap["related_capabilities"] = []
        m_context = re.search(r'context:\s*\'([^\']+)\'', obj)
        if m_context:
            cap["context"] = m_context.group(1)
        else:
            cap["context"] = ""
        if cap:
            capabilities.append(cap)
    return capabilities


def build_doc(cap: dict) -> str:
    cid = cap.get("id", "ascension_unknown")
    name = cap.get("name", "Ascension Unknown")
    category = cap.get("category", "general")
    description = cap.get("description", "Ascension AI capability.")
    related = cap.get("related_capabilities", [])
    context = cap.get("context", "")

    title = name.replace("Ascension ", "")
    related_str = ", ".join(related) if related else "ascension_chat"
    quest_examples = [
        f"Create a {title} quest for me.",
        f"Help me build a {category} plan using {title}.",
        f"What should I decide about {title}?",
    ]

    doc = f"# {name}\n\n"
    doc += f"## Description\n\n{description}\n\n"
    doc += f"## Category\n\n{category}\n\n"
    doc += f"## Context\n\n{context}\n\n"
    doc += "## What Ascension does\n\n"
    doc += f"Ascension AI responds to requests about {title} with care, clarity, and privacy. "
    doc += "It asks permission before reading connected data and provides receipts for any action.\n\n"
    doc += "## Cross-references\n\n"
    doc += f"Related capabilities: {related_str}\n\n"
    doc += "Use these together when the user needs a complete plan, a quest, or a decision.\n\n"
    doc += "## Quest and decision prompts\n\n"
    for p in quest_examples:
        doc += f"- {p}\n"
    doc += "\n## Sample responses\n\n"
    doc += f"- Ascension AI can help you with {title}. {description}\n"
    doc += f"- The {title} capability is part of the Ascension {category} intelligence shell. "
    doc += "It works with related shells to support individuals, families, and businesses safely.\n"
    doc += "\n## Safety notes\n\n"
    doc += "Ascension AI does not expose secrets, pretend to be a medical professional, "
    doc += "or take unapproved actions. It always prioritizes the individual, family, and business.\n"
    return doc


def main():
    root = Path(__file__).resolve().parents[1]
    registry_path = root / "src" / "services" / "capability-registry.ts"
    if not registry_path.is_file():
        raise SystemExit(f"Registry not found: {registry_path}")

    capabilities = parse_registry(registry_path)
    print(f"Found {len(capabilities)} capabilities")

    out_dir = root / "docs" / "capabilities"
    out_dir.mkdir(parents=True, exist_ok=True)

    total_chars = 0
    for cap in capabilities:
        doc = build_doc(cap)
        out_path = out_dir / f"{cap['id']}.md"
        out_path.write_text(doc, encoding="utf-8")
        total_chars += len(doc)

    print(f"Wrote {len(capabilities)} capability docs to {out_dir}")
    print(f"Total capability doc characters: {total_chars:,}")


if __name__ == "__main__":
    main()
