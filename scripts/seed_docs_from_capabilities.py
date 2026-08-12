"""
Seed training docs from the capability registry.

Run this after adding capabilities to generate a large Ascension-specific
training corpus. It writes one .md file per capability into docs/capabilities/.
The training scripts then load these docs automatically.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def parse_registry(ts_path: Path) -> list[dict]:
    text = ts_path.read_text(encoding="utf-8")
    # Find the array between the last '=' and the final '];'
    match = re.search(r"=\s*(\[.*?\]);", text, re.DOTALL)
    if not match:
        raise SystemExit("Could not find capability array in registry")
    array_text = match.group(1)

    # Extract object blocks with id, name, category, description
    objects = re.findall(r"\{(.*?)\},", array_text, re.DOTALL)
    capabilities = []
    for obj in objects:
        cap = {}
        for line in obj.split("\n"):
            line = line.strip()
            for key in ("id", "name", "category", "description"):
                if line.startswith(f"{key}:"):
                    value = ":".join(line.split(":", 1)[1:]).strip().rstrip(",")
                    value = value.strip("'\"")
                    cap[key] = value
        if cap:
            capabilities.append(cap)
    return capabilities


def build_doc(cap: dict) -> str:
    cid = cap.get("id", "ascension_unknown")
    name = cap.get("name", "Ascension Unknown")
    category = cap.get("category", "general")
    description = cap.get("description", "Ascension AI capability.")

    title = name.replace("Ascension ", "")
    prompts = [
        f"Tell me about {title}.",
        f"How can Ascension help with {title}?",
        f"I need help with {title}.",
        f"What is the {title} capability?",
    ]
    responses = [
        f"Ascension AI can help you with {title}. {description}",
        f"When you ask about {title}, Ascension will guide you carefully. "
        f"It protects your personal information and never takes action without your permission.",
        f"The {title} capability is part of the Ascension {category} intelligence shell. "
        f"Ascension uses this to support individuals, families, and businesses safely.",
    ]

    doc = f"# {name}\n\n"
    doc += f"## Description\n\n{description}\n\n"
    doc += f"## Category\n\n{category}\n\n"
    doc += "## What Ascension does\n\n"
    doc += f"Ascension AI responds to requests about {title} with care, clarity, and privacy. "
    doc += "It asks permission before reading connected data and provides receipts for any action.\n\n"
    doc += "## Sample prompts\n\n"
    for p in prompts:
        doc += f"- {p}\n"
    doc += "\n## Sample responses\n\n"
    for r in responses:
        doc += f"- {r}\n"
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
