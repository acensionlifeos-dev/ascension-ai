"""
Generate native-domain-router.ts from the capability registry.
Creates a handler function and map entry for every registered capability.
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
    return capabilities


def handler_function(cap: dict) -> str:
    cid = cap["id"]
    name = cap["name"]
    desc = cap["description"]
    return f"""function {cid}Response(message: string): NativeResponse {{
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
    print(f"Found {len(capabilities)} capabilities")

    functions = "\n\n".join(handler_function(c) for c in capabilities)
    map_entries = ",\n  ".join(f"'{c['id']}': {c['id']}Response" for c in capabilities)

    router = f"""// Auto-generated from capability-registry.ts by scripts/sync_domain_handlers.py

import {{ NativeResponse }} from '../models/native';
import {{ PermissionStatus, permissionMessage }} from './permission-engine';

{functions}

const DOMAIN_HANDLERS: Record<string, (message: string) => NativeResponse> = {{
  {map_entries}
}};

export function routeNativeDomain(
  capabilityId: string,
  message: string,
  permissions: Record<string, PermissionStatus>
): NativeResponse {{
  const permissionMsg = permissionMessage(capabilityId, permissions);
  if (permissionMsg) {{
    return {{
      content: permissionMsg.content,
      model: 'Aerynza Permission Gate',
      provider: 'Aerynza-Native',
      tokensUsed: 0,
      capability: capabilityId
    }};
  }}

  const handler = DOMAIN_HANDLERS[capabilityId];
  if (handler) {{
    return handler(message);
  }}

  return {{
    content: `Aerynza native response for ${{capabilityId}} (stub: domain handler not yet specialized).`,
    model: 'Aerynza AI',
    provider: 'Aerynza-Native',
    tokensUsed: 0,
    capability: capabilityId
  }};
}}
"""

    router_path.write_text(router, encoding="utf-8")
    print(f"Wrote {len(capabilities)} handlers to {router_path}")


if __name__ == "__main__":
    main()
