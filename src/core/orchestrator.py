"""Ascension shell routing and context aggregation."""

from __future__ import annotations

import json
import re

from .capabilities import capability_packet, detect_domains
from .cognition import build_cognitive_packet
from .contracts import Shell, Tier, response_contract, system_contract
from .model_runtime import runtime


UNRECEIPTED_CLAIM = re.compile(
    r"\bI(?:'ve| have)?\s+(?:saved|added|updated|scheduled|connected|sent|paid|booked|deleted|removed|completed|created)\b",
    re.I,
)
ACCESS_SCOPE_QUESTION = re.compile(
    r"\b(?:what|which)\s+(?:private\s+|personal\s+)?(?:information|data|details)|\bwhat\s+(?:can|do)\s+you\s+(?:see|know|access)|\bcan\s+you\s+(?:see|access)\b",
    re.I,
)
CONVERSATION_REPAIR = re.compile(
    r"\b(?:why\s+do\s+you\s+always\s+ask|stop\s+asking|feels?\s+robotic|sound(?:s|ing)?\s+robotic|too\s+many\s+questions)\b",
    re.I,
)
PRESENCE_ONLY = re.compile(
    r"\b(?:do\s+not|don't|dont|no)\s+(?:want\s+)?advice\b|\bjust\s+want\s+to\s+talk\b|\bjust\s+listen\b",
    re.I,
)


def deterministic_conversation_repair(text: str, mode: str) -> str | None:
    """Honor direct conversational feedback without another reflex question."""
    if mode != "conversation":
        return None
    value = str(text or "")
    if CONVERSATION_REPAIR.search(value):
        return (
            "Fair point. I fell into a default question instead of responding to you like a person. "
            "I can stay in the conversation without turning every message into an intake or coaching session."
        )
    if PRESENCE_ONLY.search(value):
        return "I'm here. No advice, no agenda, and no need to turn this into a task. Say it however it comes out; I'll stay with you."
    return None


def deterministic_scope_answer(shell: Shell, text: str) -> str | None:
    """Never let a small model improvise its access to private shell data."""
    if not ACCESS_SCOPE_QUESTION.search(str(text or "")):
        return None
    if shell == Shell.NEXUS_FAMILY:
        return (
            "I can use only the family information explicitly shared with NexusFamily and included in this request by the authorized FamilyOS shell. "
            "I cannot see a member's private LifeOS or household data unless that member shared it for this purpose and the shell supplied it. "
            "I will not claim access to any specific member information unless it is present in the permission-scoped context."
        )
    if shell == Shell.NEXUS_HOME:
        return (
            "I can use only the household or co-parenting information explicitly shared with NexusHome and included in this request by the authorized shell. "
            "I cannot see private LifeOS or FamilyOS data by default, and I will not claim access to details that were not supplied."
        )
    if shell == Shell.AP:
        return (
            "I can use only your permissioned LifeOS context that the authenticated shell included in this request. "
            "I cannot see accounts, messages, files, memories, or live services that were not connected, authorized, and supplied here, and I will not pretend otherwise."
        )
    return (
        "I can use only the permission-scoped context included in this request. "
        "I cannot see or access personal data that the authenticated Ascension shell did not explicitly supply."
    )


def _day_list(days: list[str]) -> str:
    labels = [str(day).capitalize() for day in days]
    if len(labels) < 2:
        return labels[0] if labels else "the supplied days"
    return f"{', '.join(labels[:-1])} and {labels[-1]}"


def deterministic_first_pass(cognitive: dict, mode: str) -> str | None:
    """Answer structured, high-confidence intents without paying model latency."""
    actions = {item.get("action") for item in cognitive.get("action_proposals", [])}
    if "finance.payment" in actions:
        return "No payment or transfer has been made. I can prepare the exact amount, destination, funding source, and timing for review; execution requires your explicit final confirmation and a provider receipt."
    if "messages.send" in actions:
        return "Nothing has been sent or posted. I can prepare the recipient, channel, and exact message for your review; delivery requires your explicit approval and a provider receipt."
    if "calendar.external_write" in actions:
        return "Nothing has been added, changed, or removed from a calendar. I can resolve the event title, exact date and time, timezone, target calendar, and recurrence, then present the proposed change for your approval and provider-confirmed execution."
    schedule = next(
        (item for item in cognitive.get("memory_candidates", []) if item.get("type") == "recurring_schedule"),
        None,
    )
    if schedule:
        value = schedule.get("value", {})
        days = value.get("days", [])
        off_days = [day for day in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday") if day not in days]
        return (
            f"I understand the recurring work pattern as {_day_list(days)}, "
            f"{value.get('start_time')}–{value.get('end_time')}, crossing midnight, with {_day_list(off_days)} off. "
            "Nothing has been changed or saved yet. First pass: protect the main sleep block after each shift, "
            "keep the hours before work light, and place demanding personal work on the nights off when possible. "
            "The two details that materially change the weekly map are the preferred sleep window and any fixed commitments or commute time."
        )
    if "finance.prepare_budget" in actions:
        return (
            "Nothing has been budgeted or moved yet. First protect housing, utilities, food, transportation, medication, and the income-producing essentials. "
            "The minimum evidence needed for a safe cash plan is current available balances, the next income date and expected amount, and every bill due before then—including overdraft or cash-advance terms."
        )
    if "housing.search_options" in actions:
        return (
            "Nothing has been searched, applied for, or reserved yet. I can build a housing plan around real cash flow instead of a generic price ceiling. "
            "The variables that materially change the options are location, move-in date, household and accessibility needs, verified monthly housing limit, and total move-in cash available."
        )
    return None


def enforce_response_contract(content: str, cognitive: dict, context: dict, mode: str) -> str:
    """Apply deterministic integrity checks where a small model must not improvise."""
    answer = str(content or "").strip()
    receipts = []
    if isinstance(context, dict):
        receipts = list(context.get("action_receipts") or []) + list(context.get("memory_receipts") or [])
    if not receipts and UNRECEIPTED_CLAIM.search(answer):
        kept = [sentence.strip() for sentence in re.split(r"(?<=[.!?])\s+", answer) if not UNRECEIPTED_CLAIM.search(sentence)]
        answer = " ".join(kept).strip()
        answer = f"Nothing is confirmed as saved or executed yet. {answer}".strip()

    schedule = next(
        (item for item in cognitive.get("memory_candidates", []) if item.get("type") == "recurring_schedule"),
        None,
    )
    if schedule and mode == "planning":
        value = schedule.get("value", {})
        days = value.get("days", [])
        summary = (
            f"I understand the recurring work pattern as {_day_list(days)}, "
            f"{value.get('start_time')}–{value.get('end_time')}, crossing midnight."
        )
        normalized = answer.lower()
        reflects_schedule = (
            str(value.get("start_time", "")).lower() in normalized
            and str(value.get("end_time", "")).lower() in normalized
            and sum(day in normalized for day in days) >= max(1, len(days) - 1)
        )
        if not reflects_schedule or answer.count("?") > 2:
            off_days = [day for day in ("monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday") if day not in days]
            answer = (
                f"{summary} Nothing has been changed or saved yet. "
                f"First pass: protect the main sleep block after each shift, keep pre-shift time light, "
                f"and place demanding personal work on {_day_list(off_days)} when possible. "
                "The two variables that materially change the weekly map are your preferred sleep window and any fixed commitments or commute time."
            )

    if mode == "conversation":
        words = answer.split()
        if len(words) > 180:
            answer = " ".join(words[:180]).rstrip(" ,;:") + "…"
    return answer


def compact_context(context: dict, limit: int = 8_000) -> str:
    """Keep evidence and receipts ahead of low-value UI/runtime metadata."""
    if not isinstance(context, dict):
        return "{}"
    priority = (
        "action_receipts", "memory_receipts", "verified_evidence", "evidence",
        "memories", "documents", "knowledge", "profile", "schedule", "finance",
        "health", "relationships", "goals", "available_actions",
    )
    ordered = {key: context[key] for key in priority if key in context}
    ordered.update({key: value for key, value in context.items() if key not in ordered and key not in {"debug", "telemetry", "ui_state"}})
    encoded = json.dumps(ordered, ensure_ascii=False, separators=(",", ":"), default=str)
    return encoded[:limit]


def authorized_domains(detected: list[str], allowed_capabilities: list[str]) -> list[str]:
    if not allowed_capabilities:
        return detected
    allowed = set(allowed_capabilities) | {"safety"}
    return [domain for domain in detected if domain in allowed]


def prepare_inference(*, shell: Shell, tier: Tier, messages: list[dict], context: dict, surface: str, mode: str, allowed_capabilities: list[str]) -> dict:
    latest = messages[-1]["content"] if messages else ""
    cognitive = build_cognitive_packet(latest, context, allowed_capabilities)
    domains = authorized_domains(cognitive["domains"], allowed_capabilities)
    capabilities = capability_packet(domains)
    prompt_cognition = {
        "domains": cognitive["domains"],
        "active_talents": [item["key"] for item in cognitive["talents"]],
        "retrieval": cognitive["retrieval"],
        "memory_candidates": cognitive["memory_candidates"],
        "action_proposals": cognitive["action_proposals"],
        "authority": cognitive["authority"],
    }
    context_message = {
        "role": "system",
        "content": (
            f"Invocation mode: {mode}. Current product surface: {surface}. "
            f"Response contract: {response_contract(mode)} "
            f"Relevant domains: {','.join(domains)}. "
            f"Ascension cognition packet: {json.dumps(prompt_cognition, ensure_ascii=False, separators=(',', ':'))}. "
            f"Permission-scoped context packet: {compact_context(context)}"
        ),
    }
    return {
        "messages": [{"role": "system", "content": system_contract(shell, tier, allowed_capabilities)}, context_message, *messages],
        "shell": shell.value,
        "tier": tier.value,
        "mode": mode,
        "surface": surface,
        "domains": domains,
        "capabilities": capabilities,
        "cognition": cognitive,
    }


def respond(*, shell: Shell, tier: Tier, messages: list[dict], context: dict, surface: str, mode: str, allowed_capabilities: list[str], temperature: float, max_tokens: int) -> dict:
    prepared = prepare_inference(shell=shell, tier=tier, messages=messages, context=context, surface=surface, mode=mode, allowed_capabilities=allowed_capabilities)
    latest = messages[-1].get("content", "") if messages else ""
    first_pass = (
        deterministic_scope_answer(shell, latest)
        or deterministic_conversation_repair(latest, mode)
        or deterministic_first_pass(prepared["cognition"], mode)
    )
    result = ({
        "content": first_pass,
        "model": "Ascension Contract Engine",
        "provider": "ascension-native",
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0},
        "latency_ms": 0,
    } if first_pass else runtime.chat(
        messages=prepared["messages"],
        temperature=temperature,
        max_tokens=max_tokens,
    ))
    result["content"] = enforce_response_contract(result.get("content", ""), prepared["cognition"], context, mode)
    return {
        **result,
        **{key: value for key, value in prepared.items() if key != "messages"},
        "outside_provider": False,
        "production_replacement_enabled": False,
    }


def surface_plan(*, shell: Shell, tier: Tier, trigger: str, context: dict, available_actions: list[str], allowed_capabilities: list[str]) -> dict:
    cognitive = build_cognitive_packet(trigger, context, allowed_capabilities, available_actions)
    domains = authorized_domains(cognitive["domains"], allowed_capabilities)
    capabilities = capability_packet(domains)
    surfaces = []
    for domain in domains:
        surfaces.extend(capabilities.get(domain, {}).get("surfaces", []))
    return {
        "shell": shell.value,
        "tier": tier.value,
        "domains": domains,
        "target_surfaces": list(dict.fromkeys(surfaces)),
        "capabilities": capabilities,
        "cognition": cognitive,
        "available_actions": available_actions,
        "tier_scope": "request_scoped",
        "entitlement_enforced_by": "calling_shell",
        "execution_state": "proposal_only",
        "requires_shell_authorization": True,
        "rule": "Ascension AI proposes intelligence and actions; the authenticated shell validates permissions, executes, records evidence, and returns the outcome.",
    }
