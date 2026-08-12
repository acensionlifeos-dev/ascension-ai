import re
from pathlib import Path

text = Path("src/services/capability-registry.ts").read_text(encoding="utf-8")
objects = re.findall(r"\{([^{}]*?)\}", text, re.DOTALL)

caps = []
for obj in objects:
    m_id = re.search(r"id:\s*'([^']+)'", obj)
    m_name = re.search(r"name:\s*'([^']+)'", obj)
    m_cat = re.search(r"category:\s*'([^']+)'", obj)
    m_desc = re.search(r"description:\s*'([^']+)'", obj)
    m_related = re.search(r"related_capabilities:\s*(\[[^\]]*\])", obj)
    m_context = re.search(r"context:\s*'([^']+)'", obj)
    if m_id and m_name and m_cat and m_desc:
        related = ""
        if m_related:
            related = m_related.group(1).replace("'", "").replace("[", "").replace("]", "").replace("\n", " ").strip()
        context = m_context.group(1) if m_context else ""
        caps.append((m_id.group(1), m_name.group(1), m_cat.group(1), m_desc.group(1), related, context))

lines = ["# Ascension AI - Complete Capability Reference", ""]
lines.append(f"**Total capabilities:** {len(caps)}")
lines.append("")
lines.append("This is the single source of truth for the native capability surface. "
             "Each capability has a registered `id`, `name`, `category`, `description`, "
             "`related_capabilities`, and `context`. "
             "The native chat router uses `id` to route to the matching handler in "
             "`src/services/native-domain-router.ts`.")
lines.append("")
lines.append("| ID | Name | Category | Description | Related Capabilities | Context |")
lines.append("|---|---|---|---|---|---|")

for cid, name, cat, desc, related, context in sorted(caps, key=lambda x: x[2] + x[1]):
    desc = desc.replace("|", "\\|")
    context = context.replace("|", "\\|")
    lines.append(f"| `{cid}` | {name} | {cat} | {desc} | {related} | {context} |")

Path("docs/CAPABILITIES_REFERENCE.md").write_text("\n".join(lines), encoding="utf-8")
print(f"Wrote {len(caps)} capabilities to docs/CAPABILITIES_REFERENCE.md")
