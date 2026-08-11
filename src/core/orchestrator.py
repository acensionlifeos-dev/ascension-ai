"""Ascension shell routing and context aggregation."""

from __future__ import annotations

import json

from .capabilities import capability_packet, detect_domains
from .cognition import build_cognitive_packet
from .contracts import Shell, Tier, system_contract
from .model_runtime import runtime


def compact_context(context: dict, limit: int = 12_000) -> str:
    encoded = json.dumps(context or {}, ensure_ascii=False, separators=(",", ":"), default=str)
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
            f"Relevant capability map: {json.dumps(capabilities, separators=(',', ':'))}. "
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
    result = runtime.chat(
        messages=prepared["messages"],
        temperature=temperature,
        max_tokens=max_tokens,
    )
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
