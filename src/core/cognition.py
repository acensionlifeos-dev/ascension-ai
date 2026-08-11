"""Ascension-first cognition, retrieval, memory-candidate, and action planning.

This layer is deliberately stateless. The authenticated Ascension shell owns
user memory, permissions, integrations, execution, receipts, and corrections.
The native core interprets the permission-scoped packet and returns structured
intelligence that the shell may validate and apply.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any

from .capabilities import CAPABILITIES, detect_domains


TALENTS: dict[str, dict[str, Any]] = {
    "conversation": {"domains": ["emotional", "identity"], "surfaces": ["chat"], "state": "active", "abilities": ["natural dialogue", "presence before advice", "multi-turn continuity"]},
    "personal_memory": {"domains": ["identity", "relationships", "schedule"], "surfaces": ["memory", "profile"], "state": "active", "abilities": ["memory candidates", "correction candidates", "importance scoring"]},
    "hybrid_retrieval": {"domains": ["research", "documents", "learning"], "surfaces": ["chat", "learn", "creation"], "state": "active", "abilities": ["permission-scoped retrieval", "source ranking", "evidence excerpts"]},
    "agent_planning": {"domains": ["schedule", "finance", "creation", "business", "research"], "surfaces": ["chat", "ap", "creation"], "state": "active", "abilities": ["tool selection", "action proposals", "approval classification"]},
    "schedule_intelligence": {"domains": ["schedule"], "surfaces": ["calendar", "weekly_map", "quests"], "state": "active", "abilities": ["shorthand schedule parsing", "recurrence understanding", "conflict questions"]},
    "financial_intelligence": {"domains": ["finance"], "surfaces": ["financial_profile", "wealth", "aspirations"], "state": "active", "abilities": ["cash-flow reasoning", "budget preparation", "missing-context questions"]},
    "creation_intelligence": {"domains": ["creation", "business"], "surfaces": ["creation", "creator_tools"], "state": "active", "abilities": ["seed capture", "project development", "artifact planning"]},
    "learning_intelligence": {"domains": ["learning"], "surfaces": ["learn", "academy", "books"], "state": "active", "abilities": ["course planning", "adaptive practice", "resource routing"]},
    "health_wellness": {"domains": ["health"], "surfaces": ["health", "workout", "nutrition", "self_care"], "state": "active", "abilities": ["contextual coaching", "plan preparation", "risk-aware escalation"]},
    "family_coordination": {"domains": ["family", "home"], "surfaces": ["family_dashboard", "family_chat", "coparenting"], "state": "active", "abilities": ["role-aware coordination", "privacy boundaries", "shared planning"]},
    "career_intelligence": {"domains": ["career"], "surfaces": ["career_hub", "jobs", "learn"], "state": "active", "abilities": ["job enrichment planning", "skill gaps", "application preparation"]},
    "document_intelligence": {"domains": ["documents", "business"], "surfaces": ["documents", "founder_enterprise"], "state": "active", "abilities": ["analysis", "structured drafting", "evidence-aware extraction"]},
    "multilingual": {"domains": ["identity"], "surfaces": ["all"], "state": "active", "abilities": ["multilingual conversation", "translation reasoning", "cultural tone adaptation"]},
    "vision": {"domains": ["environment"], "surfaces": ["camera", "ascension_hub"], "state": "shell_required", "abilities": ["image-context reasoning when the shell supplies observations"]},
    "voice": {"domains": ["emotional"], "surfaces": ["voice", "chat"], "state": "shell_required", "abilities": ["voice conversation when the shell supplies transcription and playback"]},
    "web_research": {"domains": ["research"], "surfaces": ["browser", "chat", "learn"], "state": "shell_required", "abilities": ["research planning and synthesis from shell-provided results"]},
    "external_execution": {"domains": ["safety"], "surfaces": ["all"], "state": "shell_required", "abilities": ["permission-aware execution proposals; authenticated shell executes"]},
}


ACTION_CATALOG: dict[str, dict[str, str]] = {
    "schedule.upsert_recurring_work": {"domain": "schedule", "risk": "low", "approval": "safe_internal_auto", "surface": "calendar"},
    "schedule.prepare_week": {"domain": "schedule", "risk": "low", "approval": "safe_internal_auto", "surface": "weekly_map"},
    "finance.refresh_cashflow": {"domain": "finance", "risk": "low", "approval": "safe_read", "surface": "financial_profile"},
    "finance.prepare_budget": {"domain": "finance", "risk": "low", "approval": "safe_internal_auto", "surface": "wealth"},
    "housing.search_options": {"domain": "finance", "risk": "low", "approval": "safe_research", "surface": "aspirations"},
    "creation.save_seed": {"domain": "creation", "risk": "low", "approval": "safe_internal_auto", "surface": "creation"},
    "creation.prepare_project": {"domain": "creation", "risk": "low", "approval": "safe_internal_auto", "surface": "creation"},
    "nutrition.research_recipes": {"domain": "health", "risk": "low", "approval": "safe_research", "surface": "nutrition"},
    "nutrition.prepare_meal_plan": {"domain": "health", "risk": "low", "approval": "safe_internal_auto", "surface": "nutrition"},
    "learning.prepare_course": {"domain": "learning", "risk": "low", "approval": "safe_internal_auto", "surface": "academy"},
    "career.research_jobs": {"domain": "career", "risk": "low", "approval": "safe_research", "surface": "career_hub"},
    "documents.prepare_draft": {"domain": "documents", "risk": "low", "approval": "safe_internal_auto", "surface": "documents"},
    "messages.send": {"domain": "relationships", "risk": "high", "approval": "explicit_confirmation", "surface": "messages"},
    "calendar.external_write": {"domain": "schedule", "risk": "high", "approval": "explicit_confirmation", "surface": "calendar"},
    "finance.payment": {"domain": "finance", "risk": "critical", "approval": "explicit_confirmation", "surface": "financial_profile"},
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
    for key in ("knowledge", "documents", "memories", "evidence"):
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


def propose_actions(text: str, memory_candidates: list[dict], available_actions: list[str] | None = None) -> list[dict]:
    lowered = str(text or "").lower()
    proposals: list[dict] = []
    schedule = next((item for item in memory_candidates if item.get("type") == "recurring_schedule"), None)
    if schedule:
        proposals.append(_proposal("schedule.upsert_recurring_work", "The user explicitly supplied a complete recurring work pattern.", schedule["value"]))
    if re.search(r"\b(short on cash|broke|low on money|can't afford|cannot afford|overdrawn|overdraft)\b", lowered):
        proposals.extend([
            _proposal("finance.refresh_cashflow", "Current balances, bills, income timing, and overdraft terms change the safe plan."),
            _proposal("finance.prepare_budget", "Prepare a protected-expense budget after current cash flow is refreshed.", missing=["verified balances", "dated bills", "income timing"]),
        ])
    if re.search(r"\b(place to stay|apartment hunting|house hunting|find (?:an? )?(?:apartment|house|home))\b", lowered):
        proposals.append(_proposal("housing.search_options", "The user has expressed an active housing need.", missing=["location", "move-in date", "household needs", "verified monthly housing limit", "total move-in cash available"]))
    if re.search(r"\b(recipe|what can i cook|meal ideas?)\b", lowered):
        proposals.append(_proposal("nutrition.research_recipes", "Return specific recipes with evidence and save controls.", missing=["dietary restrictions"] if "allerg" not in lowered else []))
    if re.search(r"\b(meal plan|grocery budget|shopping list)\b", lowered):
        proposals.append(_proposal("nutrition.prepare_meal_plan", "Coordinate nutrition, favorites, schedule, household size, and cash flow.", missing=["planning mode", "servings", "available budget"] ))
    if re.search(r"\b(?:learn|teach me|course|training program)\b", lowered):
        proposals.append(_proposal("learning.prepare_course", "The user requested learning; prepare an optional adaptive Academy course.", missing=["current skill level", "time available", "desired outcome"]))
    if re.search(r"\b(?:job|career|resume|apply)\b", lowered):
        proposals.append(_proposal("career.research_jobs", "Research and enrich relevant opportunities without inventing missing facts."))
    if re.search(r"\b(?:add|schedule|book|put|create|remove|delete|cancel)\b.{0,50}\b(?:appointment|event|calendar|meeting)\b", lowered):
        proposals.append(_proposal("calendar.external_write", "A calendar change must be resolved to a specific event and confirmed by the connected calendar provider.", {"request": str(text or "")[:1000]}, missing=["resolved date and timezone", "target calendar", "explicit final confirmation"]))
    if re.search(r"\b(?:i have an idea|idea for|create|build|make)\b", lowered):
        proposals.append(_proposal("creation.save_seed", "Preserve the idea without interrupting the conversation."))
    if re.search(r"\b(?:send|email|message|post)\b", lowered):
        proposals.append(_proposal("messages.send", "External communication requires the user to approve the exact recipient and content.", missing=["recipient", "final content", "connected provider"]))
    if re.search(r"\b(?:pay|purchase|buy|transfer money)\b", lowered):
        proposals.append(_proposal("finance.payment", "A financial transaction is high consequence and cannot execute silently.", missing=["amount", "destination", "funding source", "explicit final confirmation"]))

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
    if allowed_capabilities:
        permitted = set(allowed_capabilities) | {"safety"}
        domains = [domain for domain in domains if domain in permitted]
    domains = domains or ["identity"]
    memories = extract_memory_candidates(text)
    actions_from_context = available_actions or (context.get("available_actions", []) if isinstance(context, dict) else [])
    actions = propose_actions(text, memories, actions_from_context)
    retrieval = hybrid_retrieve(text, context)
    surfaces = []
    for domain in domains:
        surfaces.extend(CAPABILITIES.get(domain, {}).get("surfaces", []))
    surfaces.extend(proposal["surface"] for proposal in actions)
    return {
        "domains": domains,
        "talents": active_talents(domains),
        "retrieval": retrieval,
        "memory_candidates": memories,
        "action_proposals": actions,
        "surface_recommendations": list(dict.fromkeys(surfaces))[:16],
        "authority": {
            "intelligence_core": "propose_and_explain",
            "authenticated_shell": "validate_permissions_execute_persist_and_return_receipts",
            "external_high_risk_actions": "explicit_confirmation_required",
        },
    }
