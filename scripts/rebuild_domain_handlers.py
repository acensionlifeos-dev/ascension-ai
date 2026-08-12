"""
Rebuild native-domain-router.ts from scratch using the capability registry.
Creates one handler function and map entry for every registered capability.
Includes custom overrides for high-stakes capabilities.
"""

from __future__ import annotations

import re
from pathlib import Path

OVERRIDES = {
    'ascension_fast_turn': """I can map fast, legal, survival-first cash strategies (sell unused items, gig work, micro-flipping, paid tasks, food banks, emergency aid) but I will not recommend risking money needed for food or rent. How much time, skills, and items do you have right now?""",
    'ascension_wallet_automation': """I can connect to a wallet and run rule-based automation. Tell me your balance, income dates, bills, and risk tolerance, and I will build a permissioned automation plan.""",
    'ascension_income_split': """I can split deposits into spending, bill savings, emergency savings, quick investment, long-term investment, aspiration/dream board, and giving buckets. Share the deposit amount and due dates to set percentages.""",
    'ascension_inventor_lab': """I am your co-inventor and lab partner. I can model designs, list materials, find cost-efficient suppliers, build a step-by-step prototype path, and help run experiments. What are you building?""",
    'ascension_hardware_prototyping': """I can design a build path for hardware like AP Frames, recommend materials, estimate costs, and suggest the cheapest/fastest prototyping order. What is the device and the first version goal?""",
    'ascension_youtube_automation': """I can build a YouTube channel plan: niche, 3 AI-generated videos per day, titles/thumbnails, upload schedule, comment interaction, and a path to monetization/affiliates. What niche and budget?""",
    'ascension_tiktok_automation': """I can build a TikTok growth engine: 3 short videos per day, trend riding, hashtag strategy, comment engagement, and a path to paid partnerships. What niche and budget?""",
    'ascension_amsr_studio': """I can set up an ASMR channel, script/audio prompts, generate video ideas, schedule daily uploads, and plan monetization. What ASMR themes and equipment do you have?""",
    'ascension_affiliate_automation': """I can find affiliate programs, track links, suggest products to promote, and plan content that converts. What niche and audience size?""",
    'ascension_streaming_channel': """I can build a live gaming channel: overlays, alerts, schedule, best-traffic time slots, and growth strategy. What game, time zone, and streaming platform?""",
    'ascension_streaming_moderator': """I can act as a live moderator, manage chat rules, answer common questions, flag problems, and keep the stream safe. What rules and platform?""",
    'ascension_overlay_design': """I can design stream overlays, scenes, alerts, and panels that fit your brand. What game, colors, and layout do you want?""",
    'ascension_research_assistant': """I can research patents, papers, competitors, and materials, then organize everything into a decision-ready report with citations. What do you need to know?""",
    'ascension_design_assistant': """I can help design products, interfaces, and experiences, from sketch to spec, with user flow and cost-aware decisions. What are you designing?""",
    'ascension_crowdfunding_product': """I can plan a crowdfunding campaign for an invention, set reward tiers, write the story, and list launch tasks. What is the product and target?""",
    'ascension_dream_fund': """I can connect dream-board goals to automated savings buckets and milestone plans. What is the dream, the cost, and the deadline?""",
    'ascension_content_workspace': """I can create a content workspace with folders, briefs, brand kit, and project boards for any channel or campaign. What project or channel is this for?""",
    'ascension_content_analytics': """I can wire analytics from YouTube, TikTok, Twitch, and social accounts into one dashboard and explain what is working. What platforms do you want connected?""",
    'ascension_growth_tracker': """I can track followers, views, subscribers, watch time, and growth rate across platforms and flag trends. Which accounts do you want to monitor?""",
    'ascension_revenue_tracker': """I can track ad, affiliate, sponsorship, and product revenue from content and streams and map it to goals. What income sources do you have?""",
    'ascension_content_calendar': """I can build a cross-platform content calendar with release dates, themes, and best-traffic time slots. What channels and posting cadence do you want?""",
}


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
        for key in ("id", "name", "category", "description"):
            m = re.search(rf'{key}:\s*\'([^\']+)\'', obj)
            if m:
                cap[key] = m.group(1)
        if cap:
            capabilities.append(cap)
    return capabilities


def handler_function(cap: dict) -> str:
    cid = cap["id"]
    name = cap["name"]
    content = OVERRIDES.get(cid, f"I can help with {name}. {cap['description']} What do you need?")
    return f"""function {cid}Response(message: string): NativeResponse {{
  return {{
    content: `{content}`,
    model: '{name}',
    provider: 'ascension-native',
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

    router = f"""/**
 * Native Domain Router
 *
 * Provides structured, deterministic responses for each native overlay capability
 * while the generative model is still in training. This keeps the API useful,
 * fast, and safe across all registered native domains.
 */

import {{ requestPermissions, PermissionStatus }} from './permission-engine';

export interface NativeResponse {{
  content: string;
  model: string;
  provider: 'ascension-native';
  tokensUsed: number;
  capability: string;
  data?: Record<string, any>;
}}

function permissionMessage(capability: string, permissions: Record<string, PermissionStatus>): {{ content: string }} | null {{
  const request = requestPermissions(capability, permissions);
  if (!request.can_execute) {{
    return {{ content: request.message }};
  }}
  return null;
}}

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
      model: 'Ascension Permission Gate',
      provider: 'ascension-native',
      tokensUsed: 0,
      capability: capabilityId
    }};
  }}

  const handler = DOMAIN_HANDLERS[capabilityId];
  if (handler) {{
    return handler(message);
  }}

  return {{
    content: `Ascension native response for ${{capabilityId}} (stub: domain handler not yet specialized).`,
    model: 'Ascension Candidate 3B',
    provider: 'ascension-native',
    tokensUsed: 0,
    capability: capabilityId
  }};
}}
"""

    router_path.write_text(router, encoding="utf-8")
    print(f"Wrote {len(capabilities)} handlers to {router_path}")


if __name__ == "__main__":
    main()
