"""Aerynza-first cognition, retrieval, memory-candidate, and action planning.

This layer is deliberately stateless. The authenticated Aerynza shell owns
user memory, permissions, integrations, execution, receipts, and corrections.
The native core interprets the permission-scoped packet and returns structured
intelligence that the shell may validate and apply.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any

from .capabilities import CAPABILITIES, detect_domains, resolve_ascension_capabilities
from .contracts import Shell


TALENTS: dict[str, dict[str, Any]] = {
    "conversation": {"domains": ["emotional", "identity"], "surfaces": ["chat"], "state": "active", "abilities": ["natural dialogue", "presence before advice", "multi-turn continuity"]},
    "personal_memory": {"domains": ["identity", "relationships", "schedule"], "surfaces": ["memory", "profile"], "state": "active", "abilities": ["memory candidates", "correction candidates", "importance scoring"]},
    "thesis_intelligence": {"domains": ["identity", "home", "family", "business"], "surfaces": ["profile", "sprout_profile", "parent_dashboard", "home_dashboard", "family_dashboard", "founder_enterprise"], "state": "active", "abilities": ["private Human Thesis", "guardian-authorized Sprout Growth Thesis", "shared Home Thesis", "consent-aggregated Family Thesis", "privacy-thresholded Global Product Thesis", "source and confidence tracking", "contradiction visibility", "member coverage accounting", "correction and revocation boundaries"]},
    "hybrid_retrieval": {"domains": ["research", "documents", "learning"], "surfaces": ["chat", "learn", "creation"], "state": "active", "abilities": ["permission-scoped retrieval", "source ranking", "evidence excerpts"]},
    "agent_planning": {"domains": ["schedule", "finance", "creation", "business", "research"], "surfaces": ["chat", "ap", "creation"], "state": "active", "abilities": ["tool selection", "action proposals", "approval classification"]},
    "schedule_intelligence": {"domains": ["schedule"], "surfaces": ["calendar", "weekly_map", "quests"], "state": "active", "abilities": ["shorthand schedule parsing", "recurrence understanding", "conflict questions"]},
    "financial_intelligence": {"domains": ["finance"], "surfaces": ["financial_profile", "wealth", "aspirations"], "state": "active", "abilities": ["cash-flow reasoning", "budget preparation", "missing-context questions"]},
    "prediction_market_intelligence": {"domains": ["trading", "research", "finance"], "surfaces": ["wealth", "chat"], "state": "shell_required", "abilities": ["live-odds interpretation", "resolution-rule research", "contrary-evidence review", "probability ranges", "paper-position planning"]},
    "creation_intelligence": {"domains": ["creation", "business"], "surfaces": ["creation", "creator_tools"], "state": "active", "abilities": ["seed capture", "project development", "artifact planning"]},
    "learning_intelligence": {"domains": ["learning"], "surfaces": ["learn", "academy", "books"], "state": "active", "abilities": ["course planning", "adaptive practice", "resource routing"]},
    "health_wellness": {"domains": ["health"], "surfaces": ["health", "workout", "nutrition", "self_care"], "state": "active", "abilities": ["contextual coaching", "plan preparation", "risk-aware escalation"]},
    "family_coordination": {"domains": ["family", "home"], "surfaces": ["family_dashboard", "family_chat", "coparenting"], "state": "active", "abilities": ["role-aware coordination", "privacy boundaries", "shared planning"]},
    "career_intelligence": {"domains": ["career"], "surfaces": ["career_hub", "jobs", "learn"], "state": "active", "abilities": ["job enrichment planning", "skill gaps", "application preparation"]},
    "document_intelligence": {"domains": ["documents", "business"], "surfaces": ["documents", "founder_enterprise"], "state": "active", "abilities": ["analysis", "structured drafting", "evidence-aware extraction"]},
    "multilingual": {"domains": ["identity"], "surfaces": ["all"], "state": "active", "abilities": ["multilingual conversation", "translation reasoning", "cultural tone adaptation"]},
    "vision": {"domains": ["environment"], "surfaces": ["camera", "ascension_hub"], "state": "shell_required", "abilities": ["image-context reasoning when the shell supplies observations"]},
    "immersive_world_intelligence": {"domains": ["environment", "creation"], "surfaces": ["ascension_hub", "creation", "ar", "vr"], "state": "engine_required", "abilities": ["engine-neutral 3D scene compilation", "AR/VR spatial manifests", "asset provenance", "performance and comfort budgets", "WebXR/OpenXR/ARKit/ARCore routing", "render-receipt verification"]},
    "voice": {"domains": ["emotional"], "surfaces": ["voice", "chat"], "state": "shell_required", "abilities": ["voice conversation when the shell supplies transcription and playback"]},
    "web_research": {"domains": ["research"], "surfaces": ["browser", "chat", "learn"], "state": "shell_required", "abilities": ["research planning and synthesis from shell-provided results"]},
    "external_execution": {"domains": ["safety"], "surfaces": ["all"], "state": "shell_required", "abilities": ["permission-aware execution proposals; authenticated shell executes"]},
}


ACTION_CATALOG: dict[str, dict[str, str]] = {
    "schedule.upsert_recurring_work": {"domain": "schedule", "risk": "low", "approval": "safe_internal_auto", "surface": "calendar"},
    "schedule.prepare_week": {"domain": "schedule", "risk": "low", "approval": "safe_internal_auto", "surface": "weekly_map"},
    "finance.refresh_cashflow": {"domain": "finance", "risk": "low", "approval": "safe_read", "surface": "financial_profile"},
    "finance.prepare_budget": {"domain": "finance", "risk": "low", "approval": "safe_internal_auto", "surface": "wealth"},
    "trading.refresh_prediction_markets": {"domain": "trading", "risk": "low", "approval": "safe_read", "surface": "wealth"},
    "trading.prepare_prediction_position": {"domain": "trading", "risk": "low", "approval": "safe_internal_auto", "surface": "wealth"},
    "trading.submit_prediction_order": {"domain": "trading", "risk": "critical", "approval": "explicit_confirmation", "surface": "wealth"},
    "housing.search_options": {"domain": "finance", "risk": "low", "approval": "safe_research", "surface": "aspirations"},
    "creation.save_seed": {"domain": "creation", "risk": "low", "approval": "safe_internal_auto", "surface": "creation"},
    "creation.prepare_project": {"domain": "creation", "risk": "low", "approval": "safe_internal_auto", "surface": "creation"},
    "immersive.prepare_world": {"domain": "creation", "risk": "low", "approval": "safe_internal_auto", "surface": "ascension_hub"},
    "nutrition.research_recipes": {"domain": "health", "risk": "low", "approval": "safe_research", "surface": "nutrition"},
    "nutrition.prepare_meal_plan": {"domain": "health", "risk": "low", "approval": "safe_internal_auto", "surface": "nutrition"},
    "learning.prepare_course": {"domain": "learning", "risk": "low", "approval": "safe_internal_auto", "surface": "academy"},
    "career.research_jobs": {"domain": "career", "risk": "low", "approval": "safe_research", "surface": "career_hub"},
    "documents.prepare_draft": {"domain": "documents", "risk": "low", "approval": "safe_internal_auto", "surface": "documents"},
    "messages.send": {"domain": "relationships", "risk": "high", "approval": "explicit_confirmation", "surface": "messages"},
    "calendar.external_write": {"domain": "schedule", "risk": "high", "approval": "explicit_confirmation", "surface": "calendar"},
    "finance.payment": {"domain": "finance", "risk": "critical", "approval": "explicit_confirmation", "surface": "financial_profile"},
    "task.create_quest": {"domain": "identity", "risk": "low", "approval": "safe_internal_auto", "surface": "quests"},
}

MEMORY_CANDIDATE_DOMAINS = {
    "work_schedule": "schedule",
    "preferred_name": "identity",
    "cash_pressure": "finance",
    "housing_search": "finance",
    "creation_idea": "creation",
    "explicit_memory_request": "identity",
    "parenting_schedule": "relationships",
}


DAY_NAMES = {
    "mon": "monday", "monday": "monday", "tue": "tuesday", "tues": "tuesday", "tuesday": "tuesday",
    "wed": "wednesday", "weds": "wednesday", "wednesday": "wednesday", "thu": "thursday", "thur": "thursday",
    "thurs": "thursday", "thursday": "thursday", "fri": "friday", "friday": "friday", "sat": "saturday",
    "saturday": "saturday", "sun": "sunday", "sunday": "sunday",
}
DAY_ORDER = list(dict.fromkeys(DAY_NAMES.values()))


def _words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9']+", str(text or "").lower())


def _document_rows(context: dict) -> list[dict]:
    rows: list[dict] = []
    for key in ("knowledge", "documents", "memories", "evidence", "verified_evidence", "human_thesis", "home_thesis", "family_thesis", "sprout_profile", "child_profile", "profile", "schedule", "finance", "health", "goals", "relationships"):
        value = context.get(key, []) if isinstance(context, dict) else []
        if isinstance(value, dict):
            value = [value]
        if not isinstance(value, list):
            continue
        for index, item in enumerate(value[:80]):
            if isinstance(item, str):
                text, metadata = item, {"source": key, "index": index}
            elif isinstance(item, dict):
                text = str(item.get("text") or item.get("content") or item.get("summary") or item.get("fact") or "")
                metadata = {k: v for k, v in item.items() if k not in {"text", "content"}}
                metadata.setdefault("source", key)
            else:
                continue
            text = text.strip()
            if text:
                rows.append({"text": text[:6000], "metadata": metadata})
    return rows


def hybrid_retrieve(query: str, context: dict, top_k: int = 6) -> list[dict]:
    """Small deterministic BM25-like retriever over shell-supplied evidence."""
    documents = _document_rows(context)
    if not documents:
        return []
    query_terms = _words(query)
    if not query_terms:
        return []
    doc_terms = [_words(row["text"]) for row in documents]
    document_frequency = Counter(term for terms in doc_terms for term in set(terms))
    average_length = sum(len(terms) for terms in doc_terms) / max(1, len(doc_terms))
    ranked = []
    for row, terms in zip(documents, doc_terms):
        counts = Counter(terms)
        score = 0.0
        for term in set(query_terms):
            frequency = counts.get(term, 0)
            if not frequency:
                continue
            inverse = math.log(1 + (len(documents) - document_frequency[term] + 0.5) / (document_frequency[term] + 0.5))
            denominator = frequency + 1.2 * (0.25 + 0.75 * len(terms) / max(1, average_length))
            score += inverse * frequency * 2.2 / denominator
        if score > 0:
            ranked.append({
                "score": round(score, 4),
                "excerpt": row["text"][:900],
                "metadata": row["metadata"],
            })
    ranked.sort(key=lambda item: item["score"], reverse=True)
    return ranked[: max(1, min(top_k, 10))]


def _expand_day_range(start: str, end: str) -> list[str]:
    start_day, end_day = DAY_NAMES.get(start.lower()), DAY_NAMES.get(end.lower())
    if not start_day or not end_day:
        return []
    start_index, end_index = DAY_ORDER.index(start_day), DAY_ORDER.index(end_day)
    if start_index <= end_index:
        return DAY_ORDER[start_index : end_index + 1]
    return DAY_ORDER[start_index:] + DAY_ORDER[: end_index + 1]


def _schedule_candidate(text: str) -> dict | None:
    match = re.search(
        r"\b(?:i\s+)?work\s+(\d{1,2}(?::\d{2})?\s*(?:a\.?m\.?|p\.?m\.?)?)\s*(?:-|to|until)\s*"
        r"(\d{1,2}(?::\d{2})?\s*(?:a\.?m\.?|p\.?m\.?)?)\s+"
        r"(mon(?:day)?|tue(?:s|sday)?|wed(?:s|nesday)?|thu(?:r|rs|rsday)?|fri(?:day)?|sat(?:urday)?|sun(?:day)?)"
        r"\s*(?:-|to|through)\s*"
        r"(mon(?:day)?|tue(?:s|sday)?|wed(?:s|nesday)?|thu(?:r|rs|rsday)?|fri(?:day)?|sat(?:urday)?|sun(?:day)?)",
        text,
        re.I,
    )
    if not match:
        return None
    days = _expand_day_range(match.group(3), match.group(4))
    return {
        "type": "recurring_schedule",
        "key": "work_schedule",
        "value": {"start_time": match.group(1), "end_time": match.group(2), "days": days, "crosses_midnight": True},
        "confidence": 0.98,
        "source": "explicit_user_statement",
        "operation": "upsert",
    }


def extract_memory_candidates(text: str) -> list[dict]:
    """Extract only explicit, useful candidates; the shell decides persistence."""
    source = str(text or "").strip()
    lowered = source.lower()
    candidates: list[dict] = []
    schedule = _schedule_candidate(source)
    if schedule:
        candidates.append(schedule)

    name = re.search(r"\b(?:call me|i go by|my preferred name is)\s+([A-Za-z][A-Za-z' -]{0,40})", source, re.I)
    if name:
        candidates.append({"type": "preference", "key": "preferred_name", "value": name.group(1).strip(), "confidence": 0.99, "source": "explicit_user_statement", "operation": "upsert"})

    if re.search(r"\b(?:i'm|i am)\s+(?:short on cash|broke|low on money)\b", lowered):
        candidates.append({"type": "time_bound_constraint", "key": "cash_pressure", "value": source, "confidence": 0.96, "source": "explicit_user_statement", "operation": "append", "expires": "contextual"})
    if re.search(r"\b(?:i need|we need|looking for|find me)\s+(?:a\s+)?(?:place to stay|apartment|house|home)\b", lowered):
        candidates.append({"type": "active_intent", "key": "housing_search", "value": source, "confidence": 0.94, "source": "explicit_user_statement", "operation": "upsert"})
    if re.search(r"\b(?:i want to create|i have an idea|idea for|build an?\s+)\b", lowered):
        candidates.append({"type": "creation_seed", "key": "creation_idea", "value": source, "confidence": 0.90, "source": "explicit_user_statement", "operation": "append"})
    parenting = re.search(
        r"\b(?:i\s+have|the)\s+(?:my\s+)?(?:kids?|children|son|daughter)\s+(?:are\s+with\s+me\s+)?(?:for\s+)?(?:all\s+)?next\s+week\b",
        lowered,
    )
    if parenting:
        candidates.append({"type": "time_bound_context", "key": "parenting_schedule", "value": source, "confidence": 0.95, "source": "explicit_user_statement", "operation": "upsert", "requires_dates": True})
    remembered = re.search(r"\b(?:remember|save|store|record)\s+(?:that\s+)?(.{3,240})", source, re.I)
    if remembered and not any(candidate.get("key") == "explicit_memory_request" for candidate in candidates):
        candidates.append({"type": "explicit_memory", "key": "explicit_memory_request", "value": remembered.group(1).strip(), "confidence": 0.97, "source": "explicit_user_request", "operation": "upsert"})
    return candidates[:8]


def _proposal(action: str, reason: str, arguments: dict | None = None, missing: list[str] | None = None) -> dict:
    contract = ACTION_CATALOG[action]
    return {
        "action": action,
        "domain": contract["domain"],
        "surface": contract["surface"],
        "risk": contract["risk"],
        "approval": contract["approval"],
        "reason": reason,
        "arguments": arguments or {},
        "missing_variables": missing or [],
        "execution_state": "proposal_only",
    }


CAPABILITY_ACTION_MAP: dict[str, dict] = {
    "audio": {"action": "creation.prepare_project", "missing": ["content description", "target platform"]},
    "video": {"action": "creation.prepare_project", "missing": ["content description", "target platform"]},
    "voice": {"action": "creation.prepare_project", "missing": ["content description", "target platform"]},
    "vision": {"action": "creation.prepare_project", "missing": ["content description", "target device"]},
    "documents": {"action": "documents.prepare_draft", "missing": ["what you want to do"]},
    "text": {"action": "documents.prepare_draft", "missing": ["what you want to do"]},
    "code": {"action": "documents.prepare_draft", "missing": ["what you want to do"]},
    "legal": {"action": "documents.prepare_draft", "missing": ["what you want to do"]},
    "finance": {"action": "finance.prepare_budget", "missing": ["verified balances", "dated bills", "income timing"]},
    "cooking": {"action": "nutrition.research_recipes", "missing": ["dietary restrictions"]},
    "nutrition": {"action": "nutrition.prepare_meal_plan", "missing": ["servings", "available budget"]},
    "health": {"action": "nutrition.prepare_meal_plan", "missing": ["dietary restrictions"]},
    "wellness": {"action": "task.create_quest", "missing": ["title", "target outcome", "target completion"]},
    "fitness": {"action": "task.create_quest", "missing": ["title", "target outcome", "target completion"]},
    "sports": {"action": "task.create_quest", "missing": ["title", "target outcome", "target completion"]},
    "career": {"action": "career.research_jobs", "missing": ["what you want to do"]},
    "learning": {"action": "learning.prepare_course", "missing": ["current skill level", "time available", "desired outcome"]},
    "education": {"action": "learning.prepare_course", "missing": ["current skill level", "time available", "desired outcome"]},
}


def propose_actions(text: str, memory_candidates: list[dict], available_actions: list[str] | None = None) -> list[dict]:
    source = str(text or "")
    lowered = source.lower()
    proposals: list[dict] = []
    schedule = next((item for item in memory_candidates if item.get("type") == "recurring_schedule"), None)
    if schedule:
        proposals.append(_proposal("schedule.upsert_recurring_work", "The user explicitly supplied a complete recurring work pattern.", schedule["value"]))
    if re.search(r"\b(?:build|make|plan|map|set)\b.{0,30}\b(?:my|the|our)?\s*(?:week|weekly plan|weekly map)\b", lowered):
        proposals.append(_proposal(
            "schedule.prepare_week",
            "Prepare a weekly map from confirmed commitments, rhythms, responsibilities, resources, and priorities.",
            missing=["unconnected fixed commitments", "primary weekly outcome"],
        ))
    if re.search(r"\b(short on cash|broke|low on money|can't afford|cannot afford|overdrawn|overdraft)\b", lowered):
        proposals.extend([
            _proposal("finance.refresh_cashflow", "Current balances, bills, income timing, and overdraft terms change the safe plan."),
            _proposal("finance.prepare_budget", "Prepare a protected-expense budget after current cash flow is refreshed.", missing=["verified balances", "dated bills", "income timing"]),
        ])
    if re.search(r"\b(?:make|earn|need|want|get).{0,40}(?:money|cash|funds|\$|\d+k).{0,40}(?:fast|quick|easy|now|weeks?|months?|days?|soon|by|within)\b", lowered):
        proposals.extend([
            _proposal("task.create_quest", "Create a tracked income-generation quest from the user's goal.", {"goal": str(text or "")[:1000]}, missing=["title", "target outcome", "target completion"]),
            _proposal("finance.prepare_budget", "Prepare a cash-flow plan that closes the stated money gap safely.", {"goal": str(text or "")[:1000]}, missing=["verified balances", "dated bills", "income timing"]),
        ])
    if re.search(r"\b(place to stay|apartment hunting|house hunting|find (?:an? )?(?:apartment|house|home))\b", lowered):
        proposals.append(_proposal("housing.search_options", "The user has expressed an active housing need.", missing=["location", "move-in date", "household needs", "verified monthly housing limit", "total move-in cash available"]))
    if re.search(r"\b(polymarket|prediction market|market odds|implied probability)\b", lowered):
        proposals.extend([
            _proposal("trading.refresh_prediction_markets", "Live odds, deadlines, liquidity, and resolution rules are required before analyzing a prediction market."),
            _proposal("trading.prepare_prediction_position", "Prepare a paper-only thesis that compares market-implied probability with sourced supporting and contrary evidence.", missing=["verified resolution rules", "jurisdiction eligibility", "disposable risk budget", "time horizon", "maximum acceptable loss"]),
        ])
    if re.search(r"\b(place|submit|execute|buy|sell|enter)\b.{0,40}\b(polymarket|prediction market|prediction position|market order)\b", lowered):
        proposals.append(_proposal("trading.submit_prediction_order", "A real prediction-market order is high consequence and must remain blocked until the shell verifies eligibility, exact terms, explicit final approval, wallet signature, and a provider receipt.", missing=["verified jurisdiction eligibility", "connected eligible provider account", "exact market and outcome", "limit price", "maximum loss", "explicit final confirmation", "wallet signature", "provider receipt"] ))
    if re.search(r"\b(recipe|what can i cook|meal ideas?)\b", lowered):
        proposals.append(_proposal("nutrition.research_recipes", "Return specific recipes with evidence and save controls.", missing=["dietary restrictions"] if "allerg" not in lowered else []))
    if re.search(r"\b(meal plan|grocery budget|shopping list)\b", lowered):
        proposals.append(_proposal("nutrition.prepare_meal_plan", "Coordinate nutrition, favorites, schedule, household size, and cash flow.", missing=["planning mode", "servings", "available budget"] ))
    if re.search(r"\b(?:learn|teach me|course|training program)\b", lowered):
        proposals.append(_proposal("learning.prepare_course", "The user requested learning; prepare an optional adaptive Academy course.", missing=["current skill level", "time available", "desired outcome"]))
    if re.search(r"\b(?:job|career|resume|apply)\b", lowered):
        proposals.append(_proposal("career.research_jobs", "Research and enrich relevant opportunities without inventing missing facts."))
    if re.search(r"\b(?:quest|task)\b", lowered):
        proposals.append(_proposal("task.create_quest", "Create a tracked quest from the user's explicit goal.", missing=["title", "target outcome", "target completion"]))
    if re.search(r"\b(?:add|schedule|book|put|create|remove|delete|cancel)\b.{0,50}\b(?:appointment|event|calendar|meeting)\b", lowered):
        proposals.append(_proposal("calendar.external_write", "A calendar change must be resolved to a specific event and confirmed by the connected calendar provider.", {"request": str(text or "")[:1000]}, missing=["resolved date and timezone", "target calendar", "explicit final confirmation"]))
    if re.search(r"\b(?:i have an idea|idea for|create|build|make)\b", lowered):
        proposals.append(_proposal("creation.save_seed", "Preserve the idea without interrupting the conversation."))
        resolved = resolve_ascension_capabilities(source)
        resolved_ids = [cap.get("id") for cap in resolved]
        if re.search(r"\b(?:build|make|create|write|draft)\b", lowered):
            if re.search(r"\b(?:ebook|book|document|guide|manual|pdf|article|blog|post)\b", lowered):
                proposals.append(_proposal(
                    "documents.prepare_draft",
                    "User requested a written artifact; prepare a draft for review.",
                    {"topic": source, "resolved_capabilities": resolved_ids},
                    missing=["content details"],
                ))
            proposals.append(_proposal(
                "creation.prepare_project",
                "User wants to turn an idea into a product for execution.",
                {"topic": source, "resolved_capabilities": resolved_ids},
                missing=["target outcome", "target completion"],
            ))
    if re.search(r"\buse\b.{0,40}\bascension\s+streaming\b", lowered):
        proposals.append(_proposal(
            "creation.prepare_project",
            "User wants to start an Aerynza Streaming channel.",
            {"capability": "ascension_streaming"},
            missing=["streaming platform", "content focus"],
        ))
    if re.search(r"\b(?:3d world|virtual world|vr experience|ar experience|augmented reality|virtual reality|spatial scene)\b", lowered):
        proposals.append(_proposal("immersive.prepare_world", "Compile an Aerynza-native spatial world manifest; a real engine receipt is required before claiming it rendered.", missing=["target device", "experience mode", "authorized assets"]))
    if re.search(r"\b(?:send|email|message|post)\b", lowered):
        proposals.append(_proposal("messages.send", "External communication requires the user to approve the exact recipient and content.", missing=["recipient", "final content", "connected provider"]))
    if re.search(r"\b(?:pay|payment|purchase|buy|transfer money)\b", lowered):
        payment_missing = []
        if not re.search(r"(?:\$|usd\s*)\s*\d+(?:[,.]\d{1,2})?\b", source, re.I):
            payment_missing.append("amount")
        if not re.search(r"\b(?:pay|send|transfer(?:\s+money)?)\s+(?:my\s+)?[A-Za-z][A-Za-z0-9&'. -]{1,60}?(?=\s+(?:\$|usd\s*\d)|\s+from\b|\s+using\b|$)", source, re.I):
            payment_missing.append("destination")
        if not re.search(r"\b(?:checking|savings|card|account|wallet|cash balance)\b", lowered):
            payment_missing.append("funding source")
        payment_missing.append("explicit final confirmation")
        proposals.append(_proposal("finance.payment", "A financial transaction is high consequence and cannot execute silently.", missing=payment_missing))

    # Generic 640-capability invocation: if the user names a known Aerynza capability, propose a project for it.
    if re.search(r"\buse\b", lowered):
        resolved = resolve_ascension_capabilities(source, top_n=1)
        if resolved:
            cap = resolved[0]
            mapping = CAPABILITY_ACTION_MAP.get(cap.get("category"), {})
            action = mapping.get("action", "creation.prepare_project")
            missing = mapping.get("missing", ["target outcome", "target completion"])
            proposals.append(_proposal(
                action,
                f"User wants to use {cap['name']}.",
                {"capability": cap["id"], "category": cap.get("category")},
                missing=missing,
            ))

    allowed = set(available_actions or [])
    if allowed:
        proposals = [proposal for proposal in proposals if proposal["action"] in allowed]
    seen = set()
    unique = []
    for proposal in proposals:
        if proposal["action"] not in seen:
            seen.add(proposal["action"])
            unique.append(proposal)
    return unique[:8]


def active_talents(domains: list[str]) -> list[dict]:
    selected = []
    for key, talent in TALENTS.items():
        if set(talent["domains"]) & set(domains) or key in {"conversation", "personal_memory", "agent_planning"}:
            selected.append({"key": key, **talent})
    return selected


def build_cognitive_packet(text: str, context: dict, allowed_capabilities: list[str], available_actions: list[str] | None = None) -> dict:
    domains = detect_domains(text, context)
    permitted: set[str] | None = None
    if allowed_capabilities:
        permitted = set(allowed_capabilities) | {"safety"}
        domains = [domain for domain in domains if domain in permitted]
    memories = extract_memory_candidates(text)
    if permitted is not None:
        memories = [
            candidate for candidate in memories
            if MEMORY_CANDIDATE_DOMAINS.get(str(candidate.get("key") or "")) in permitted
        ]
    actions_from_context = available_actions or (context.get("available_actions", []) if isinstance(context, dict) else [])
    actions = propose_actions(text, memories, actions_from_context)
    if permitted is not None:
        actions = [proposal for proposal in actions if proposal.get("domain") in permitted]
    retrieval = hybrid_retrieve(text, context)
    surfaces = []
    for domain in domains:
        surfaces.extend(CAPABILITIES.get(domain, {}).get("surfaces", []))
    surfaces.extend(proposal["surface"] for proposal in actions)
    return {
        "domains": domains,
        "subject_scope": (
            "child"
            if re.search(r"\b(?:child|children|kid|kids|toddler|minor|son|daughter|sprout)\b", str(text or ""), re.I)
            else "adult_or_unspecified"
        ),
        "talents": active_talents(domains),
        "retrieval": retrieval,
        "memory_candidates": memories,
        "action_proposals": actions,
        "available_actions": list(dict.fromkeys(str(item).strip() for item in actions_from_context if str(item).strip())),
        "surface_recommendations": list(dict.fromkeys(surfaces))[:16],
        "data_panels": extract_data_panels(context),
        "authority": {
            "intelligence_core": "propose_and_explain",
            "authenticated_shell": "validate_permissions_execute_persist_and_return_receipts",
            "external_high_risk_actions": "explicit_confirmation_required",
        },
    }


DATA_PANEL_TITLES: dict[str, str] = {
    "human_thesis": "Human Thesis",
    "home_thesis": "Home Thesis",
    "family_thesis": "Family Thesis",
    "sprout_profile": "Sprout",
    "child_profile": "Child Profile",
    "verified_evidence": "Evidence",
    "evidence": "Evidence",
    "documents": "Documents",
    "memories": "Memories",
    "knowledge": "Knowledge",
    "profile": "Profile",
    "schedule": "Schedule",
    "finance": "Finance",
    "health": "Health",
    "relationships": "Relationships",
    "goals": "Goals",
    "action_receipts": "Action Receipts",
    "memory_receipts": "Memory Receipts",
    "available_actions": "Available Actions",
}


def _format_panel_item(value: Any, key: str = "") -> str:
    if isinstance(value, dict):
        text = (
            value.get("summary")
            or value.get("text")
            or value.get("content")
            or value.get("fact")
            or value.get("name")
            or value.get("title")
        )
        if text:
            return str(text)[:220]
        pairs = [f"{k}: {v}" for k, v in value.items() if v is not None and k not in {"text", "content", "summary"}]
        return "; ".join(pairs)[:220]
    if isinstance(value, (list, tuple)):
        return "; ".join(str(item) for item in value[:3])[:220]
    return str(value)[:220]


def extract_data_panels(context: dict) -> list[dict]:
    """Turn the permission-scoped context into front-end data panels.

    The AI reads each context key and produces a structured panel so the
    shell front ends can render live cards for the current user/household/family.
    """
    if not isinstance(context, dict):
        return []
    panels: list[dict] = []
    for key, value in context.items():
        if key in {"debug", "telemetry", "ui_state", "provider_keys"}:
            continue
        title = DATA_PANEL_TITLES.get(key, key.replace("_", " ").title())
        items: list[str] = []
        if isinstance(value, dict):
            items.append(_format_panel_item(value, key))
        elif isinstance(value, list):
            for item in value[:5]:
                formatted = _format_panel_item(item, key)
                if formatted:
                    items.append(formatted)
        else:
            items.append(str(value)[:220])
        items = [item for item in items if item]
        if items:
            panels.append({"id": key, "title": title, "items": items, "count": len(value) if isinstance(value, list) else None})
    return panels[:12]


RECEIPT_FIELDS: dict[str, list[str]] = {
    "schedule.upsert_recurring_work": ["memory_receipt", "saved_schedule_id"],
    "schedule.prepare_week": ["memory_receipt", "weekly_map_reference"],
    "finance.refresh_cashflow": ["provider", "fetched_at", "balances", "bills", "income"],
    "finance.prepare_budget": ["prepared_at", "budget_id"],
    "trading.refresh_prediction_markets": ["provider", "fetched_at", "markets", "source"],
    "trading.prepare_prediction_position": ["prepared_at", "thesis_id", "sources"],
    "trading.submit_prediction_order": ["order_id", "market", "outcome", "maximum_loss", "status", "provider"],
    "housing.search_options": ["prepared_at", "search_id"],
    "creation.save_seed": ["saved_at", "seed_id"],
    "creation.prepare_project": ["prepared_at", "project_id"],
    "immersive.prepare_world": ["world_id", "manifest_sha256", "prepared_at", "engine_target"],
    "nutrition.research_recipes": ["prepared_at", "recipe_ids", "source"],
    "nutrition.prepare_meal_plan": ["prepared_at", "plan_id"],
    "learning.prepare_course": ["prepared_at", "course_id"],
    "task.create_quest": ["quest_id", "created_at", "status", "semantic_key"],
    "career.research_jobs": ["prepared_at", "search_id", "source"],
    "documents.prepare_draft": ["prepared_at", "draft_id"],
    "messages.send": ["message_id", "recipient", "channel", "sent_at", "provider"],
    "calendar.external_write": ["event_id", "calendar", "updated_at", "provider"],
    "finance.payment": ["transaction_id", "amount", "destination", "funding_source", "confirmed_at", "provider"],
}


MISSING_QUESTIONS: dict[str, str] = {
    "unconnected fixed commitments": "What fixed commitments are not already connected?",
    "primary weekly outcome": "What is the one outcome that matters most this week?",
    "verified balances": "What are your current available balances?",
    "dated bills": "What bills are due before your next income, and when?",
    "income timing": "When is your next income expected, and how much?",
    "amount": "What is the exact amount?",
    "destination": "Who or what is the destination?",
    "funding source": "Which account or funding source should be used?",
    "resolved date and timezone": "What is the exact date, time, and timezone?",
    "target calendar": "Which calendar should it go on?",
    "recipient": "Who is the recipient?",
    "final content": "What is the exact message to send?",
    "connected provider": "Which connected provider will be used?",
    "location": "What location are you considering?",
    "move-in date": "When do you need to move in?",
    "household needs": "What household or accessibility needs matter?",
    "verified monthly housing limit": "What is your verified monthly housing limit?",
    "total move-in cash available": "How much cash do you have available for move-in?",
    "dietary restrictions": "What dietary restrictions or allergies should I consider?",
    "planning mode": "Is this a one-time meal plan or a repeating grocery list?",
    "servings": "How many servings?",
    "available budget": "What is the available food budget?",
    "current skill level": "What is your current skill level?",
    "time available": "How much time can you commit?",
    "desired outcome": "What outcome do you want from this learning?",
    "title": "What should this quest be called?",
    "target outcome": "What result will show this quest is complete?",
    "target completion": "When do you want to complete it?",
    "target device": "Which device or headset should run this world?",
    "experience mode": "Should this be 3D, augmented reality, virtual reality, or mixed reality?",
    "authorized assets": "Which owned or licensed images and 3D assets may this world use?",
    "explicit final confirmation": "Please confirm this action before it runs.",
}


_RISK_ORDER = {"low": 0, "high": 1, "critical": 2}


def _risk_tier(actions: list[dict]) -> str:
    if not actions:
        return "none"
    ranked = sorted(actions, key=lambda a: _RISK_ORDER.get(a.get("risk"), 0), reverse=True)
    return str(ranked[0].get("risk") or "low")


def _missing_question(variable: str) -> str:
    return MISSING_QUESTIONS.get(variable, f"Please provide the {variable}.")


def _guardian_required(action: dict, shell: Shell | None, domains: list[str], subject_scope: str) -> bool:
    if shell is None:
        return False
    return subject_scope == "child" or action.get("domain") == "sprout" or "sprout" in domains


def _action_contract(action: dict, shell: Shell | None, domains: list[str], subject_scope: str) -> dict:
    action_id = str(action.get("action", ""))
    missing = list(action.get("missing_variables") or [])
    return {
        **action,
        "receipt_fields": RECEIPT_FIELDS.get(action_id, ["memory_receipt"]),
        "guardian_required": _guardian_required(action, shell, domains, subject_scope),
        "missing_questions": [
            {"variable": variable, "question": _missing_question(variable), "present_in_context": False}
            for variable in missing
        ],
    }


def _memory_signal(candidate: dict, shell: Shell | None, domains: list[str]) -> dict:
    domain = MEMORY_CANDIDATE_DOMAINS.get(str(candidate.get("key") or ""), "identity")
    child_scope = domain in {"sprout"} or shell in {Shell.NEXUS_HOME, Shell.NEXUS_FAMILY}
    return {
        "type": candidate.get("type"),
        "key": candidate.get("key"),
        "operation": candidate.get("operation"),
        "domain": domain,
        "persistence_condition": "shell_authority_and_guardian_when_minor",
        "guardian_required": child_scope,
        "value_preview": str(candidate.get("value"))[:120],
    }


def build_action_execution_contract(cognitive: dict, shell: Shell | None = None) -> dict:
    """Assemble a fail-closed, policy-aware action execution contract.

    The contract is deterministic and does not execute.  It tells the
    authenticated shell exactly what is being proposed, what is missing, what
    permission and guardian gates apply, and what execution receipts must be
    returned for any claim to be valid.
    """
    actions = list(cognitive.get("action_proposals") or [])
    memories = list(cognitive.get("memory_candidates") or [])
    domains = list(cognitive.get("domains") or [])
    subject_scope = str(cognitive.get("subject_scope") or "adult_or_unspecified")

    from .action_runtime import classify_action_readiness

    available_actions = list(cognitive.get("available_actions") or [])
    contracted_actions = []
    for action in actions:
        contracted = _action_contract(action, shell, domains, subject_scope)
        contracted.update(classify_action_readiness(contracted, shell, available_actions))
        contracted_actions.append(contracted)
    memory_signals = [_memory_signal(candidate, shell, domains) for candidate in memories]

    risk_tier = _risk_tier(actions)
    any_explicit = any(action.get("approval") == "explicit_confirmation" for action in actions)
    any_guardian = any(action.get("guardian_required") for action in contracted_actions)
    child_domain = "sprout" in domains or "home" in domains or "family" in domains

    if any_guardian:
        permission_gate = "guardian_confirmation"
    elif any_explicit:
        permission_gate = "explicit_confirmation"
    elif any(action.get("approval") == "safe_read" for action in actions):
        permission_gate = "safe_read"
    elif any(action.get("approval") == "safe_research" for action in actions):
        permission_gate = "safe_research"
    elif actions:
        permission_gate = "safe_internal_auto"
    else:
        permission_gate = "none"

    missing_questions: list[dict] = []
    receipt_fields: set[str] = set()
    context_requirements: dict[str, dict] = {}
    for action in contracted_actions:
        for question in action["missing_questions"]:
            if question["variable"] not in context_requirements:
                context_requirements[question["variable"]] = {
                    "variable": question["variable"],
                    "question": question["question"],
                    "present_in_context": False,
                    "required_for_actions": [],
                }
            context_requirements[question["variable"]]["required_for_actions"].append(action["action"])
            if question not in missing_questions:
                missing_questions.append(question)
        for field in action.get("receipt_fields", []):
            receipt_fields.add(field)

    abstain = not actions and not memories
    abstention_reason = (
        "No permissioned, executable action or memory proposal could be prepared from the supplied packet."
        if abstain
        else None
    )
    if abstain and not domains:
        abstention_reason = "No recognized product domain or capability was identified in the supplied packet."

    return {
        "structured_intent": {
            "domains": domains,
            "talents": [talent.get("key") for talent in cognitive.get("talents", [])],
            "surface_recommendations": cognitive.get("surface_recommendations", []),
            "action_categories": [action["action"] for action in contracted_actions],
        },
        "context_requirements": list(context_requirements.values()),
        "missing_variable_questions": missing_questions,
        "proposed_actions": contracted_actions,
        "risk_tier": risk_tier,
        "permission_approval_gate": {
            "gate": permission_gate,
            "approval_required": any_explicit or any_guardian,
            "requires_guardian": any_guardian,
            "child_or_household_scope": child_domain,
        },
        "execution_receipt": {
            "required_fields": sorted(receipt_fields),
            "per_action_receipts": [
                {
                    "action": action["action"],
                    "receipt_fields": action["receipt_fields"],
                    "guardian_required": action["guardian_required"],
                }
                for action in contracted_actions
            ],
            "receipt_rule": "No save, send, payment, calendar change, connection, or external action may be claimed without the matching verified receipt returned by the authenticated shell.",
            "validation_contract": "receipt action, successful status, verification state, identifier, and action-specific fields must all match",
        },
        "provider_availability": {
            "advertised_actions": available_actions,
            "rule": "Provider availability affects dispatch, not model competence. Unavailable providers remain plannable and must never be reported as executed.",
            "ready_actions": [action["action"] for action in contracted_actions if action["can_dispatch_now"]],
            "unavailable_actions": [action["action"] for action in contracted_actions if action["dispatch_state"] in {"provider_not_connected", "future_capability_unavailable"}],
        },
        "memory_update_signals": memory_signals,
        "child_safe_guardian_boundaries": {
            "guardian_approval_required": any_guardian,
            "affected_actions": [action["action"] for action in contracted_actions if action["guardian_required"]],
            "affected_domains": [domain for domain in domains if domain in {"sprout", "home", "family"}],
            "rule": "Sprout, household, and high-consequence family actions require guardian or shell authority before execution, and the authenticated shell owns the final go/no-go.",
        },
        "explicit_abstention": {
            "abstain": abstain,
            "reason": abstention_reason,
            "safe_next_step": (
                "Continue the conversation naturally without inventing an action."
                if abstain and set(domains) & {"emotional", "identity"}
                else "Ask only for a material missing variable, and never pretend an action was executed."
            ) if abstain else None,
        },
        "authority": cognitive.get("authority", {}),
    }
