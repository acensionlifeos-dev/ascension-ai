"""
Rebuild native-domain-router.ts from scratch using the capability registry.
Creates one handler function and map entry for every registered capability.
Includes custom overrides for high-stakes capabilities.
"""

from __future__ import annotations

import re
from pathlib import Path

OVERRIDES = {
    'phone_os': """I can help design a custom mobile operating system from the kernel up. Tell me the target phone (SoC, storage, screen, radios) and I will produce a build plan, toolchain, driver list, and partition layout. Real flashing to a device requires explicit device.flash permission and a verified receipt.""",
    'phone_drivers': """I can help map the driver layer for a phone OS: USB, fastboot, ADB, display, touch, audio, modem, Wi-Fi, Bluetooth, camera, and SoC power management. I will generate the driver matrix, source locations, and build order.""",
    'phone_flash': """I can prepare a flashable OS image and a safe flashing procedure, but I will not write to a phone over USB until I have the device.flash permission, a verified device ID, and an explicit one-time approval. I will also require a recovery image and a brick-recovery path before starting.""",
    'phone_recovery': """I can design the bootloader, recovery partition, and fail-safe images for a phone OS. This includes fastboot/Odin-style recovery, A/B partitions, rollback protection, and an unbrick path.""",
    'universal_os': """I can architect Universal OS: one kernel and userspace design that targets phones, laptops, desktops, and smart devices. Tell me the device classes and I will produce a common HAL, build matrix, and IP-safe source layout.""",
    'laptop_os': """I can adapt Aerynza OS for laptops: x86/ARM64 SoC selection, power management, keyboard/trackpad, display, sleep states, and docking. I will produce a port plan and driver list.""",
    'desktop_os': """I can adapt Aerynza OS for desktops: multi-monitor, discrete GPU, fast storage, expansion slots, peripherals, and networking. I will produce a port plan and driver list.""",
    'smart_device_os': """I can adapt Aerynza OS for smart home, wearables, and embedded IoT devices: low-power ARM/RISC-V, sensors, BLE, Thread, and Matter. I will produce a board port plan and minimal image spec.""",
    'device_drivers': """I can design the unified HAL and device-driver catalog for Universal OS. I will generate a device-class matrix, driver source mapping, and a build order that works across phones, laptops, desktops, and smart devices.""",
    'device_flash': """I can prepare a flashable image for any connected phone, laptop, desktop, or smart device, but I will not write to the device until I have device.read and device.flash permissions, a verified device ID, an explicit one-time approval, and a brick-recovery image.""",
    'ip_guard': """I can design the IP protection layer for Aerynza: license files, watermarking, signed binaries, source access tiers, audit logging, and enforcement. I will not emit or sign any protected material without ip.control approval and a verified receipt.""",
    'code_guardian': """I can design the source vault and code-guardian pipeline for Aerynza: encryption at rest, commit signing, artifact hashes, exfiltration checks, and release attestation. I will not package or release any code without ip.control approval and a verified receipt.""",
    'ar_assistant': """I can be a walking AR companion: seeing what you see, understanding where you are, and giving you glanceable answers, navigation, translations, and reminders. This requires camera.read, location.read, microphone.read, and ar.overlay permissions. I will not record or identify bystanders without their explicit consent.""",
    'ar_environment_scan': """I can build a real-time spatial map of your surroundings for safe AR: doors, walls, obstacles, surfaces, and open paths. Requires camera.read, ar.read, and location.read permissions. I will not store or transmit the mesh without your approval.""",
    'ar_object_recognition': """I can identify objects, labels, prices, ingredients, and hazards in your view and explain them. Requires camera.read and ar.read permissions. I will not use this data to profile people.""",
    'ar_navigation': """I can overlay walking and indoor directions in your view: arrows, distance, and turn cues. Requires camera.read, location.read, and ar.overlay permissions. I will not record the path unless you save it.""",
    'ar_realtime_translate': """I can translate signs, menus, and speech you see or hear through AR and show the result as an overlay. Requires camera.read, microphone.read, and ar.overlay permissions. I will not retain audio or images unless you explicitly save them.""",
    'ar_people_recognition': """I can recognize your known contacts and give you social context, but I will not identify strangers or build a face database. Requires ar.read and an explicit privacy opt-in.""",
    'ar_context_feed': """I can stream relevant, glanceable context to your AR view: time, place, next appointment, weather, transit, and reminders. Requires camera.read, location.read, and ar.overlay permissions. I will keep the feed minimal and non-intrusive by default.""",
    'ar_proactive_data': """I can anticipate what you need next in AR and feed it before you ask: the train is coming, the gate is on your left, the item you need is aisle 4. Requires camera.read, location.read, and ar.overlay permissions. I will not proactively identify bystanders and you can turn this off at any time.""",
    'ar_safety_alert': """I can warn you about physical hazards in AR: traffic, obstacles, stairs, wet floors, and moving objects. Requires camera.read and ar.read permissions. Alerts are local and do not leave your device unless you choose to save them.""",
    'ar_memory_anchor': """I can tag places and objects you care about so I can recall context later: \"your keys are on the kitchen table,\" \"this store has the part you need.\" Requires camera.read, location.read, and ar.write permissions. Anchors stay local unless you opt into sync.""",
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
    'ascension_solution_engine': """I can invent a solution path for any goal, constraint, and cash situation. Tell me what you want to achieve, what you have, and what you can risk, and I will design a permissioned plan.""",
    'ascension_invention_engine': """I can invent a product, service, or experience from scratch: concept, materials, cost, build order, and tests. What do you want to create?""",
    'ascension_video_types': """I can recommend the right video formats for any niche, platform, and budget. What channel, audience, and equipment do you have?""",
    'ascension_channel_types': """I can recommend the best channel or service type for any audience, cash situation, and income goal. What skills, time, and budget do you have?""",
    'ascension_cash_strategy': """I can design a cash strategy for any amount, timeline, and risk level. Tell me your balance, bills, skills, and how fast you need the money.""",
    'ascension_zero_capital': """I can build an income or solution plan starting from zero capital: service flipping, gig matching, barter, grants, and free tools. What skills and time do you have?""",
    'ascension_micro_launch': """I can design a tiny-budget launch with a fast feedback loop: pre-sell, waitlist, MVP, and first paying users. What is the product or service?""",
    'ascension_service_designer': """I can design a service offering, pricing tiers, delivery path, and first client plan around any skill or audience. What skill do you want to sell?""",
    'ascension_idea_validator': """I can validate an idea, market, and first move quickly and cheaply. What is the idea, who is it for, and what is the cheapest test?""",
    'ascension_build_path': """I can generate a step-by-step build path for any invention, project, or channel. What is the end goal and the first version?""",
    'ascension_compound_engine': """I can build a reinvestment and compounding plan for any small starting amount and time horizon. What is the starting amount, timeline, and how much risk can you afford to lose?""",
    'ascension_72h_sprint': """I can design a high-activity 72-hour income or growth sprint with realistic, legal targets. What amount do you need and what skills/time can you commit?""",
    'ascension_risk_budget': """I can set a risk budget for fast-turn experiments so food, rent, and survival money are never at risk. What are your fixed survival costs?""",
    'ascension_gig_sprint': """I can map the fastest gig and task income for a small amount in a short window. What skills, vehicle, and time do you have in the next 72 hours?""",
    'ascension_money_flip': """I can take any amount you plug in and design a custom flip plan with a realistic target, timeline, and a clear risk warning. No guaranteed returns. How much, how fast, and what can you risk?""",
    'ascension_prediction_markets': """I can research live prediction markets by comparing market-implied probability with verified resolution rules, reputable supporting and contrary evidence, time remaining, and liquidity. I will return a probability range, confidence, invalidation conditions, and a survival-first paper plan—not call an outcome predictable or guaranteed. Live orders remain blocked until the shell verifies jurisdiction eligibility, exact terms, explicit final approval, wallet signature, and a provider receipt. Which market should I research?""",
    'ascension_second_brain': """I can become your second brain: capture, connect, and surface everything you share, across every domain of your life. What do you want me to remember and connect?""",
    'ascension_life_orchestrator': """I can orchestrate your whole life: work, family, health, home, finance, and creativity, and route tasks to the right shell. What is the current priority?""",
    'ascension_user_profile': """I can build and update a living profile of you: goals, skills, schedule, people, and preferences. I only use what you explicitly share. What should I add?""",
    'ascension_family_profile': """I can maintain a permissioned family profile for Nexus: household members, schedules, and needs, with strict privacy boundaries. Who should I know about?""",
    'ascension_context_engine': """I can share permissioned context between AP, Nexus, HomeOS, and Sprout so each shell knows what it needs and nothing more. Which shells should connect?""",
    'ascension_shell_orchestrator': """I can route insights and tasks between your shells: AP, Nexus, HomeOS, Sprout, and any product overlay. What is the source and destination?""",
    'ascension_knowledge_graph': """I can connect your people, places, projects, and events into a knowledge graph you can query. What relationship should I map?""",
    'ascension_proactive_engine': """I can surface reminders, opportunities, and next steps before you ask, based on your goals and calendar. What areas should I watch?""",
    'ascension_appointments': """I can track and prepare you for appointments across health, work, family, and services. What appointment is next?""",
    'ascension_maintenance': """I can track home, vehicle, health, and device maintenance with reminders. What needs maintenance?""",
    'ascension_family_sync': """I can sync schedules, tasks, and updates across your household and extended family. Who needs to be in sync?""",
    'ascension_family_abroad': """I can help coordinate calls, gifts, visits, and updates for family abroad. Which family member and country?""",
    'ascension_household_sync': """I can sync chores, shopping, meals, and routines across the household. What is the household priority today?""",
    'ascension_life_admin': """I can track paperwork, renewals, deadlines, and bureaucratic tasks for you and your family. What is due?""",
    'ascension_creative_manager': """I can track your creative projects, ideas, assets, and release plans. What project should we organize?""",
    'ascension_business_manager': """I can track leads, revenue, tasks, and operations across your business or side project. What is the current focus?""",
    'ascension_parenting': """I can support child routines, milestones, and education with parent supervision. Which child and what do you need?""",
    'ascension_child_development': """I can track developmental milestones, learning, and activities for each child. What child and age?""",
    'ascension_goals': """I can set, track, and break down goals across every domain of your life. What is the goal and deadline?""",
    'ascension_milestones': """I can track milestones and celebrations across personal and family life. What milestone should we record?""",
    'ascension_routine': """I can design, sync, and adapt routines for you and the household. What routine should we build or adjust?""",
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
  provider: 'Aerynza-Native';
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
