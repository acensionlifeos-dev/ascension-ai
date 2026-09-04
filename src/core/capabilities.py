"""Capability and UI-surface registry derived from the Aerynza AI canon."""

from __future__ import annotations

import json
import re
from pathlib import Path


CAPABILITIES = {
    "identity": {"surfaces": ["profile", "aspirations", "dream_board", "progress", "quests"], "abilities": ["identity evidence", "alignment grading", "blind-spot detection", "growth paths"]},
    "schedule": {"surfaces": ["calendar", "weekly_map", "quests", "check_in"], "abilities": ["circadian-aware planning", "conflict detection", "recurring schedule understanding", "reminders"]},
    "finance": {"surfaces": ["financial_profile", "wealth", "aspirations", "nutrition", "creation"], "abilities": ["cash-flow analysis", "income and bill recognition", "spending classification", "budgeting", "purchase timing", "overdraft awareness"]},
    "health": {"surfaces": ["health", "workout", "nutrition", "self_care", "progress"], "abilities": ["baseline comparison", "fitness adjustment", "nutrition impact", "recovery planning", "risk-aware escalation", "wellness planning", "symptom guidance"]},
    "learning": {"surfaces": ["learn", "academy", "books", "lessons"], "abilities": ["adaptive courses", "skill assessment", "practice generation", "resource recommendation", "learning analytics"]},
    "creation": {"surfaces": ["creation", "creator_tools", "business", "aspirations"], "abilities": ["idea development", "writing", "content planning", "audience intelligence", "business building"]},
    "relationships": {"surfaces": ["relationships", "social", "calendar", "messages"], "abilities": ["relationship context", "follow-up preparation", "communication support", "pattern reflection"]},
    "family": {"surfaces": ["family_dashboard", "family_chat", "family_tree", "family_economy"], "abilities": ["role coordination", "family trust", "enterprise continuity", "shared planning", "records", "legacy planning", "governance"]},
    "home": {"surfaces": ["household", "coparenting", "shared_calendar", "sprout"], "abilities": ["household coordination", "co-parenting logistics", "shared resources", "child continuity", "smart home", "chore rotation"]},
    "sprout": {"surfaces": ["sprout", "learn", "progress", "health"], "abilities": ["child development", "learning paths", "milestone tracking", "parent guidance", "age-appropriate content"]},
    "career": {"surfaces": ["career_hub", "jobs", "learn", "creation"], "abilities": ["job matching", "resume analysis", "skill gaps", "career planning", "opportunity ranking"]},
    "emotional": {"surfaces": ["chat", "journal", "self_care", "check_in"], "abilities": ["emotion recognition", "empathetic response", "pattern reflection", "support routing"]},
    "documents": {"surfaces": ["documents", "founder_enterprise", "career", "vault"], "abilities": ["analysis", "summarization", "comparison", "drafting", "structured extraction"]},
    "research": {"surfaces": ["browser", "learn", "career", "creation", "aspirations"], "abilities": ["retrieval", "source comparison", "citation preparation", "opportunity discovery"]},
    "environment": {"surfaces": ["home", "self_care", "workout", "ascension_hub"], "abilities": ["environmental context", "spatial awareness", "energy and recovery support", "AR-ready overlays"]},
    "business": {"surfaces": ["founder_enterprise", "creation", "funding", "crm"], "abilities": ["planning", "CRM intelligence", "grant and investor preparation", "operations", "decision support"]},
    "trading": {"surfaces": ["wealth", "financial_profile", "creation"], "abilities": ["market analysis", "prediction-market research", "probability comparison", "backtesting", "paper trading", "strategy evaluation", "risk limits"]},
    "safety": {"surfaces": ["all"], "abilities": ["permission checks", "confidence labeling", "abstention", "auditability", "human approval"]},
}

KEYWORDS = {
    "identity": r"\b(identity|become|aspiration|dream|goal|alignment|quest|future self)\b",
    "schedule": r"\b(schedule|calendar|shift|work hours?|appointment|event|weekly|remind|circadian|sleep)\b|\bwork\s+\d{1,2}(?::\d{2})?\s*(?:a\.?m\.?|p\.?m\.?)?",
    "finance": r"\b(money|cash|bank|payroll|income|salary|budget|bill|debt|credit|overdraft|wealth|afford|price)\b",
    "health": r"\b(health|workout|exercise|nutrition|meal|food|weight|sleep|recovery|medication|gym|symptom|wellness|vitals)\b",
    "learning": r"\b(learn|lesson|course|academy|book|study|skill|teach|practice)\b",
    "creation": r"\b(create|creation|content|video|music|write|idea|audience|youtube|twitch|kick)\b",
    "relationships": r"\b(friend|relationship|dating|partner|social|message|reply|person|people)\b",
    "family": r"\b(family|familyos|nexusfamily|family tree|family economy|relative|legacy|governance)\b",
    "home": r"\b(household|homeos|nexushome|coparent|co-parent|child|children|custody|sprout|chore|smart home|device)\b",
    "sprout": r"\b(sprout|child development|milestone|parenting|learning path|age appropriate|kid|toddler|teen)\b",
    "career": r"\b(job|career|resume|employer|interview|work opportunity|profession)\b",
    "emotional": r"\b(feel|emotion|sad|angry|anxious|stressed|overwhelmed|happy|lonely|journal)\b",
    "documents": r"\b(document|pdf|resume|contract|patent|grant|application|agreement|form)\b",
    "research": r"\b(research|search|find|source|evidence|browser|news|compare)\b",
    "environment": r"\b(camera|room|environment|spatial|ar|vr|location|weather|object)\b",
    "business": r"\b(business|company|founder|crm|revenue|investor|funding|grant|market)\b",
    "trading": r"\b(stock|forex|crypto|coin|commodity|trade|trading|backtest|strategy|margin|polymarket|prediction market|market odds|implied probability)\b",
}


def detect_domains(text: str, context: dict | None = None) -> list[str]:
    haystack = f"{text} {' '.join((context or {}).keys())}".lower()
    domains = [name for name, pattern in KEYWORDS.items() if re.search(pattern, haystack, re.I)]
    return domains[:6] or ["identity"]


def capability_packet(domains: list[str]) -> dict:
    selected = {domain: CAPABILITIES[domain] for domain in domains if domain in CAPABILITIES}
    selected["safety"] = CAPABILITIES["safety"]
    return selected


_CAPABILITY_CACHE: dict | None = None


def _capability_report_path() -> Path:
    return Path(__file__).resolve().parents[2] / "public" / "capability_report.json"


def load_capability_report() -> dict:
    global _CAPABILITY_CACHE
    if _CAPABILITY_CACHE is None:
        try:
            with open(_capability_report_path(), "r", encoding="utf-8-sig") as report_file:
                _CAPABILITY_CACHE = json.load(report_file)
        except (OSError, json.JSONDecodeError):
            _CAPABILITY_CACHE = {"capabilities": []}
    return _CAPABILITY_CACHE


def _capability_terms(capability: dict) -> set[str]:
    terms: set[str] = set()
    for field in ("id", "name", "category"):
        value = str(capability.get(field) or "").lower().replace("_", " ").replace("-", " ")
        terms.update(re.findall(r"[a-z0-9]+", value))
    return terms


def resolve_ascension_capabilities(text: str, top_n: int = 5) -> list[dict]:
    """Resolve the most relevant Aerynza AI capabilities from the 640-capability report."""
    report = load_capability_report()
    capabilities = report.get("capabilities", [])
    if not capabilities:
        return []
    words = set(re.findall(r"[a-z0-9]+", str(text or "").lower()))
    if not words:
        return []
    scored: list[tuple[float, dict]] = []
    for capability in capabilities:
        cap_words = _capability_terms(capability)
        if not cap_words:
            continue
        overlap = len(words & cap_words) / max(1, min(len(words), len(cap_words)))
        if overlap > 0:
            scored.append((overlap, capability))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [capability for _, capability in scored[:top_n]]
