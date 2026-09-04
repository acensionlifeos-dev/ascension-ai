"""
Extend native-domain-router.ts with missing capability handlers and a full map.
Preserves existing hand-written handlers.
"""

from __future__ import annotations

import re
from pathlib import Path


def parse_registry(ts_path: Path) -> list[dict]:
    text = ts_path.read_text(encoding="utf-8")
    match = re.search(r"=\s*(\[.*?\]);", text, re.DOTALL)
    if not match:
        raise SystemExit("Could not find capability array in registry")
    array_text = match.group(1)
    objects = re.findall(r"\{([^{}]*?)\}", array_text, re.DOTALL)
    capabilities = []
    for obj in objects:
        cap = {}
        for line in obj.split("\n"):
            line = line.strip()
            for key in ("id", "name", "description"):
                if line.startswith(f"{key}:"):
                    value = ":".join(line.split(":", 1)[1:]).strip().rstrip(",")
                    value = value.strip("'\"")
                    cap[key] = value
        if cap:
            capabilities.append(cap)
    # dedupe by id, keep first
    seen = set()
    unique = []
    for c in capabilities:
        if c["id"] not in seen:
            seen.add(c["id"])
            unique.append(c)
    return unique


def parse_existing_handlers(router_path: Path) -> set[str]:
    text = router_path.read_text(encoding="utf-8")
    return set(re.findall(r"function\s+(\w+)Response\s*\(", text))


def missing_handler_block(cap: dict) -> str:
    cid = cap["id"]
    name = cap["name"]
    desc = cap["description"]
    func_name = f"{cid}Response"
    return f"""\nfunction {func_name}(message: string): NativeResponse {{
  return {{
    content: `I can help with {name}. {desc} What do you need?`,
    model: '{name}',
    provider: 'Aerynza-Native',
    tokensUsed: 0,
    capability: '{cid}',
    data: {{ question: null }}
  }};
}}"""


def main():
    root = Path(__file__).resolve().parents[1]
    registry_path = root / "src" / "services" / "capability-registry.ts"
    router_path = root / "src" / "services" / "native-domain-router.ts"

    capabilities = parse_registry(registry_path)
    existing = parse_existing_handlers(router_path)
    missing = [c for c in capabilities if f"{c['id']}Response" not in existing]

    print(f"Registry: {len(capabilities)}")
    print(f"Existing handlers: {len(existing)}")
    print(f"Missing to add: {len(missing)}")

    if missing:
        blocks = "\n".join(missing_handler_block(c) for c in missing)
        with open(router_path, "a", encoding="utf-8") as f:
            f.write(blocks)
            f.write("\n")

    text = router_path.read_text(encoding="utf-8")
    # Replace the DOMAIN_HANDLERS map content
    map_content = ",\n  ".join(f"'{c['id']}': {c['id']}Response" for c in capabilities)
    new_text = re.sub(
        r"const DOMAIN_HANDLERS: Record<string, \(message: string\) => NativeResponse> = \{[^}]*\};",
        f"const DOMAIN_HANDLERS: Record<string, (message: string) => NativeResponse> = {{\n  {map_content}\n}};",
        text,
        flags=re.DOTALL,
    )

    router_path.write_text(new_text, encoding="utf-8")
    print(f"Updated {router_path}")


if __name__ == "__main__":
    main()
