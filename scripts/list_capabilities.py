import re
from collections import defaultdict
from pathlib import Path

text = Path("src/services/capability-registry.ts").read_text(encoding="utf-8")
objects = re.findall(r"\{([^{}]*?)\}", text, re.DOTALL)
caps = []
for obj in objects:
    m_id = re.search(r"id:\s*'([^']+)'", obj)
    m_name = re.search(r"name:\s*'([^']+)'", obj)
    m_cat = re.search(r"category:\s*'([^']+)'", obj)
    if m_id and m_name and m_cat:
        caps.append((m_id.group(1), m_name.group(1), m_cat.group(1)))

by_cat = defaultdict(list)
for c in caps:
    by_cat[c[2]].append((c[0], c[1]))

print(f"TOTAL: {len(caps)} capabilities")
for cat in sorted(by_cat):
    print(f"\n{cat.upper()} ({len(by_cat[cat])}):")
    for cid, name in by_cat[cat]:
        print(f"  {cid} - {name}")
