"""Focused contract tests for the policy-aware action execution contract."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.cognition import build_action_execution_contract, build_cognitive_packet
from src.core.contracts import Shell, Tier
from src.core.orchestrator import enforce_response_contract, surface_plan


def test_low_risk_schedule_contract_has_safe_gate_and_receipt() -> None:
    cognitive = build_cognitive_packet(
        "I work 10 pm-6 am Wed-Sun",
        {},
        ["schedule"],
        ["schedule.upsert_recurring_work"],
    )
    contract = build_action_execution_contract(cognitive, Shell.AP)
    assert contract["risk_tier"] == "low"
    assert contract["permission_approval_gate"]["gate"] == "safe_internal_auto"
    assert contract["permission_approval_gate"]["requires_guardian"] is False
    assert contract["child_safe_guardian_boundaries"]["guardian_approval_required"] is False
    assert contract["explicit_abstention"]["abstain"] is False
    assert any(a["action"] == "schedule.upsert_recurring_work" for a in contract["proposed_actions"])
    schedule_action = next(a for a in contract["proposed_actions"] if a["action"] == "schedule.upsert_recurring_work")
    assert "memory_receipt" in schedule_action["receipt_fields"]


def test_high_risk_payment_requires_explicit_confirmation_and_receipts() -> None:
    cognitive = build_cognitive_packet(
        "I need to pay my landlord $50",
        {},
        ["finance"],
        ["finance.payment"],
    )
    contract = build_action_execution_contract(cognitive, Shell.AP)
    assert contract["risk_tier"] == "critical"
    assert contract["permission_approval_gate"]["gate"] == "explicit_confirmation"
    assert contract["permission_approval_gate"]["approval_required"] is True
    assert contract["child_safe_guardian_boundaries"]["guardian_approval_required"] is False
    payment = next(a for a in contract["proposed_actions"] if a["action"] == "finance.payment")
    assert "transaction_id" in payment["receipt_fields"]
    assert "amount" in payment["receipt_fields"]
    assert "destination" in payment["receipt_fields"]
    missing = {q["variable"] for q in contract["missing_variable_questions"]}
    assert "amount" not in missing
    assert "destination" not in missing
    assert "funding source" in missing
    assert "explicit final confirmation" in missing
    assert contract["execution_receipt"]["receipt_rule"].startswith("No save")


def test_prepared_payment_gets_user_facing_approval_and_receipt_boundary() -> None:
    cognitive = build_cognitive_packet(
        "Prepare a payment for my phone bill.",
        {},
        [],
        [],
    )
    assert any(item["action"] == "finance.payment" for item in cognitive["action_proposals"])
    answer = enforce_response_contract(
        "I can prepare the payment details for you.",
        cognitive,
        {},
        "conversation",
        "Prepare a payment for my phone bill.",
    )
    lowered = answer.casefold()
    assert "not been submitted" in lowered
    assert "approval" in lowered
    assert "provider receipt" in lowered


def test_sprout_calendar_action_requires_guardian_confirmation() -> None:
    cognitive = build_cognitive_packet(
        "Schedule a dentist appointment for my toddler on Tuesday at 3 pm",
        {},
        ["schedule", "home", "sprout"],
        ["calendar.external_write"],
    )
    contract = build_action_execution_contract(cognitive, Shell.NEXUS_HOME)
    assert contract["permission_approval_gate"]["requires_guardian"] is True
    assert contract["permission_approval_gate"]["gate"] == "guardian_confirmation"
    assert contract["child_safe_guardian_boundaries"]["guardian_approval_required"] is True
    assert "calendar.external_write" in contract["child_safe_guardian_boundaries"]["affected_actions"]
    assert "sprout" in contract["child_safe_guardian_boundaries"]["affected_domains"] or "home" in contract["child_safe_guardian_boundaries"]["affected_domains"]


def test_allowed_capabilities_fail_closed_on_cross_domain() -> None:
    cognitive = build_cognitive_packet(
        "I'm short on cash and need to pay my landlord",
        {},
        ["schedule"],  # finance is not allowed
        ["finance.payment", "finance.prepare_budget"],
    )
    contract = build_action_execution_contract(cognitive, Shell.AP)
    assert all(a["domain"] in {"schedule", "safety"} for a in contract["proposed_actions"])
    assert contract["risk_tier"] == "none"
    assert contract["explicit_abstention"]["abstain"] is True


def test_abstention_with_safe_next_step_for_chat() -> None:
    cognitive = build_cognitive_packet(
        "Just wanted to say hi",
        {},
        [],
        [],
    )
    contract = build_action_execution_contract(cognitive, Shell.AP)
    assert contract["explicit_abstention"]["abstain"] is True
    assert contract["explicit_abstention"]["reason"] is not None
    assert "conversation naturally" in (contract["explicit_abstention"]["safe_next_step"] or "").lower()


def test_nexus_home_adult_action_does_not_invent_guardian_authority() -> None:
    cognitive = build_cognitive_packet(
        "Pay my landlord $50 from checking",
        {},
        ["finance"],
        ["finance.payment"],
    )
    contract = build_action_execution_contract(cognitive, Shell.NEXUS_HOME)
    assert contract["permission_approval_gate"]["gate"] == "explicit_confirmation"
    assert contract["permission_approval_gate"]["requires_guardian"] is False
    assert contract["child_safe_guardian_boundaries"]["guardian_approval_required"] is False


def test_surface_plan_includes_execution_contract() -> None:
    plan = surface_plan(
        shell=Shell.AP,
        tier=Tier.LIFE_OS,
        trigger="Pay my landlord $50",
        context={},
        available_actions=["finance.payment"],
        allowed_capabilities=["finance"],
    )
    assert "execution_contract" in plan
    assert plan["execution_contract"]["risk_tier"] == "critical"
    assert plan["execution_contract"]["permission_approval_gate"]["gate"] == "explicit_confirmation"


def test_memory_update_signal_includes_persistence_gate() -> None:
    cognitive = build_cognitive_packet(
        "Call me Brandon",
        {},
        ["identity"],
        [],
    )
    contract = build_action_execution_contract(cognitive, Shell.AP)
    assert len(contract["memory_update_signals"]) >= 1
    signal = contract["memory_update_signals"][0]
    assert signal["key"] == "preferred_name"
    assert signal["persistence_condition"] == "shell_authority_and_guardian_when_minor"
    assert signal["operation"] == "upsert"


def test_general_memory_and_parenting_context_become_candidates() -> None:
    preference = build_cognitive_packet(
        "Remember that I prefer workouts after I wake up", {}, [], []
    )
    assert any(item["key"] == "explicit_memory_request" for item in preference["memory_candidates"])
    parenting = build_cognitive_packet("I have my kids next week", {}, [], [])
    assert any(item["key"] == "parenting_schedule" for item in parenting["memory_candidates"])


def main() -> None:
    for name, fn in globals().items():
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("All action-execution contract tests passed.")


if __name__ == "__main__":
    main()
