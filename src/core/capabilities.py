"""Capability and UI-surface registry derived from the Ascension AI canon."""

from __future__ import annotations

import re


CAPABILITIES = {
    "identity": {"surfaces": ["profile", "aspirations", "dream_board", "progress", "quests"], "abilities": ["identity evidence", "alignment grading", "blind-spot detection", "growth paths"]},
    "schedule": {"surfaces": ["calendar", "weekly_map", "quests", "check_in"], "abilities": ["circadian-aware planning", "conflict detection", "recurring schedule understanding", "reminders"]},
    "finance": {"surfaces": ["financial_profile", "wealth", "aspirations", "nutrition", "creation"], "abilities": ["cash-flow analysis", "income and bill recognition", "spending classification", "budgeting", "purchase timing", "overdraft awareness"]},
    "health": {"surfaces": ["health", "workout", "nutrition", "self_care", "progress"], "abilities": ["baseline comparison", "fitness adjustment", "nutrition impact", "recovery planning", "risk-aware escalation"]},
    "learning": {"surfaces": ["learn", "academy", "books", "lessons"], "abilities": ["adaptive courses", "skill assessment", "practice generation", "resource recommendation", "learning analytics"]},
    "creation": {"surfaces": ["creation", "creator_tools", "business", "aspirations"], "abilities": ["idea development", "writing", "content planning", "audience intelligence", "business building"]},
    "relationships": {"surfaces": ["relationships", "social", "calendar", "messages"], "abilities": ["relationship context", "follow-up preparation", "communication support", "pattern reflection"]},
    "family": {"surfaces": ["family_dashboard", "family_chat", "family_tree", "family_economy"], "abilities": ["role coordination", "family trust", "enterprise continuity", "shared planning", "records"]},
    "home": {"surfaces": ["household", "coparenting", "shared_calendar", "sprout"], "abilities": ["household coordination", "co-parenting logistics", "shared resources", "child continuity"]},
    "career": {"surfaces": ["career_hub", "jobs", "learn", "creation"], "abilities": ["job matching", "resume analysis", "skill gaps", "career planning", "opportunity ranking"]},
    "emotional": {"surfaces": ["chat", "journal", "self_care", "check_in"], "abilities": ["emotion recognition", "empathetic response", "pattern reflection", "support routing"]},
    "documents": {"surfaces": ["documents", "founder_enterprise", "career", "vault"], "abilities": ["analysis", "summarization", "comparison", "drafting", "structured extraction"]},
    "research": {"surfaces": ["browser", "learn", "career", "creation", "aspirations"], "abilities": ["retrieval", "source comparison", "citation preparation", "opportunity discovery"]},
    "environment": {"surfaces": ["home", "self_care", "workout", "ascension_hub"], "abilities": ["environmental context", "spatial awareness", "energy and recovery support", "AR-ready overlays"]},
    "business": {"surfaces": ["founder_enterprise", "creation", "funding", "crm"], "abilities": ["planning", "CRM intelligence", "grant and investor preparation", "operations", "decision support"]},
    "safety": {"surfaces": ["all"], "abilities": ["permission checks", "confidence labeling", "abstention", "auditability", "human approval"]},
}

KEYWORDS = {
    "identity": r"\b(identity|become|aspiration|dream|goal|alignment|quest|future self)\b",
    "schedule": r"\b(schedule|calendar|shift|work hours?|appointment|event|weekly|remind|circadian|sleep)\b",
    "finance": r"\b(money|cash|bank|payroll|income|salary|budget|bill|debt|credit|overdraft|wealth|afford|price)\b",
    "health": r"\b(health|workout|exercise|nutrition|meal|food|weight|sleep|recovery|medication|gym)\b",
    "learning": r"\b(learn|lesson|course|academy|book|study|skill|teach|practice)\b",
    "creation": r"\b(create|creation|content|video|music|write|idea|audience|youtube|twitch|kick)\b",
    "relationships": r"\b(friend|relationship|dating|partner|social|message|reply|person|people)\b",
    "family": r"\b(family|familyos|nexusfamily|family tree|family economy|relative)\b",
    "home": r"\b(household|homeos|nexushome|coparent|co-parent|child|children|custody|sprout)\b",
    "career": r"\b(job|career|resume|employer|interview|work opportunity|profession)\b",
    "emotional": r"\b(feel|emotion|sad|angry|anxious|stressed|overwhelmed|happy|lonely|journal)\b",
    "documents": r"\b(document|pdf|resume|contract|patent|grant|application|agreement|form)\b",
    "research": r"\b(research|search|find|source|evidence|browser|news|compare)\b",
    "environment": r"\b(camera|room|environment|spatial|ar|vr|location|weather|object)\b",
    "business": r"\b(business|company|founder|crm|revenue|investor|funding|grant|market)\b",
}


def detect_domains(text: str, context: dict | None = None) -> list[str]:
    haystack = f"{text} {' '.join((context or {}).keys())}".lower()
    domains = [name for name, pattern in KEYWORDS.items() if re.search(pattern, haystack, re.I)]
    return domains[:6] or ["identity"]


def capability_packet(domains: list[str]) -> dict:
    selected = {domain: CAPABILITIES[domain] for domain in domains if domain in CAPABILITIES}
    selected["safety"] = CAPABILITIES["safety"]
    return selected
