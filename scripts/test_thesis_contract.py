"""Contract tests for AP, NexusHome, and FamilyOS thesis boundaries."""

from __future__ import annotations

import sys
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.thesis import build_family_thesis, build_home_thesis, build_human_thesis, build_member_thesis_contribution, build_product_thesis, build_sprout_thesis


def test_human_thesis_is_private_and_correctable() -> None:
    thesis = build_human_thesis("user-1", {
        "profile": {"preferred_name": "A"},
        "goals": [{"name": "Build consistency", "confidence": 0.9}],
        "finance": {"available_balance": 125},
    })
    assert thesis["scope"] == "human"
    assert thesis["owner"] == "user-1"
    assert all(claim["visibility"] == "private_ap" for claim in thesis["claims"])
    assert thesis["correction_right"]
    assert thesis["execution_authority"] == "none"


def test_sprout_thesis_is_child_centered_and_grows_into_teen_mode() -> None:
    thesis = build_sprout_thesis("child-1", {
        "guardian_ids": ["parent-1"],
        "guardian_consent_receipt_id": "guardian-receipt-1",
        "age": 12,
        "child_voice": {"preferred_name": "Sky", "current_interest": "robotics"},
        "chores": {"room": "Saturday"},
        "allowance": {"weekly": 10},
        "finance": {"adult_account_balance": 5000},
        "dating": {"private": "excluded"},
    })
    encoded = json.dumps(thesis["claims"], sort_keys=True)
    assert thesis["scope"] == "sprout" and thesis["experience_mode"] == "teen"
    assert "robotics" in encoded and "Saturday" in encoded
    assert "5000" not in encoded and "dating" not in encoded
    assert thesis["child_voice_right"] and thesis["not_diagnosis_or_destiny"] is True


def test_sprout_thesis_requires_guardian_authorization() -> None:
    try:
        build_sprout_thesis("child-1", {"child_voice": {"interest": "art"}})
        raise AssertionError("unauthorized Sprout thesis was accepted")
    except ValueError as exc:
        assert "guardian" in str(exc)


def test_home_thesis_accepts_only_home_scoped_contributions() -> None:
    thesis = build_home_thesis("home-1", {
        "private_memories": [{"text": "must never surface"}],
        "home_shared_facts": [{"section": "calendar", "key": "pickup", "value": "Friday", "confidence": 1}],
        "member_thesis_contributions": [
            {"member_id": "u1", "consent_scopes": ["nexus_home"], "claims": [
                {"section": "rhythms", "key": "quiet_hours", "value": "9pm", "share_scope": "nexus_home"},
                {"section": "resources", "key": "private_cash", "value": 500, "share_scope": "nexus_family"},
            ]},
            {"member_id": "u2", "consent_scopes": [], "claims": [
                {"section": "needs", "key": "medical", "value": "private", "share_scope": "nexus_home"},
            ]},
        ],
    })
    encoded = json.dumps(thesis["claims"], sort_keys=True)
    assert "must never surface" not in encoded and "private_cash" not in encoded and "medical" not in encoded
    assert thesis["contributors"] == ["u1"]
    assert thesis["rejected_contributions"]


def test_ap_exports_only_exact_claims_with_explicit_consent() -> None:
    human = build_human_thesis("u1", {
        "goals": {"shared_goal": "buy a family home", "private_goal": "private detail"},
        "finance": {"balance": 500},
    })
    shared_claim = next(claim for claim in human["claims"] if claim["key"] == "shared_goal")
    contribution = build_member_thesis_contribution(
        "u1",
        "nexus_family",
        human,
        [{"claim_id": shared_claim["claim_id"], "destination_section": "goals"}],
        "consent-receipt-1",
    )
    encoded = json.dumps(contribution["claims"], sort_keys=True)
    assert "buy a family home" in encoded
    assert "private detail" not in encoded and "500" not in encoded
    assert contribution["consent_receipt_id"] == "consent-receipt-1"
    assert contribution["revocable"] is True


def test_ap_contribution_rejects_wrong_owner_and_missing_consent() -> None:
    human = build_human_thesis("u1", {"goals": {"goal": "shared"}})
    claim_id = human["claims"][0]["claim_id"]
    try:
        build_member_thesis_contribution("u2", "nexus_home", human, [{"claim_id": claim_id, "destination_section": "goals"}], "receipt")
        raise AssertionError("wrong-owner contribution was accepted")
    except ValueError as exc:
        assert "belong" in str(exc)
    try:
        build_member_thesis_contribution("u1", "nexus_home", human, [{"claim_id": claim_id, "destination_section": "goals"}], "")
        raise AssertionError("receipt-free contribution was accepted")
    except ValueError as exc:
        assert "consent" in str(exc)


def test_family_thesis_aggregates_consented_ap_contributions() -> None:
    thesis = build_family_thesis("family-1", {
        "expected_member_ids": ["u1", "u2"],
        "family_shared_facts": [
            {"section": "branches", "key": "ancestor-1", "value": {"name": "Named historical branch", "os_user": False}},
        ],
        "human_thesis": {"private": "excluded"},
        "member_thesis_contributions": [
            {"member_id": "u1", "consent_scopes": ["nexus_family"], "claims": [
                {"section": "roles", "key": "role", "value": "treasurer", "confidence": 0.9, "share_scope": "nexus_family"},
            ]},
            {"member_id": "u2", "consent_scopes": ["nexus_home"], "claims": [
                {"section": "economy", "key": "income", "value": 1000, "share_scope": "nexus_family"},
            ]},
        ],
    })
    encoded = json.dumps(thesis["claims"], sort_keys=True)
    assert thesis["scope"] == "family" and thesis["contributors"] == ["u1"]
    assert "Named historical branch" in encoded
    assert "excluded" not in encoded and "1000" not in encoded
    assert "explicit unknowns" in thesis["comprehensiveness_rule"]
    assert thesis["member_coverage"]["missing_member_ids"] == ["u2"]
    assert thesis["member_coverage"]["status"] == "partial"
    assert thesis["comprehensive"] is False


def test_conflicts_remain_visible_instead_of_being_silently_merged() -> None:
    thesis = build_family_thesis("family-1", {
        "member_thesis_contributions": [
            {"member_id": "u1", "consent_scopes": ["nexus_family"], "claims": [
                {"section": "goals", "key": "priority", "value": "buy property", "share_scope": "nexus_family"},
            ]},
            {"member_id": "u2", "consent_scopes": ["nexus_family"], "claims": [
                {"section": "goals", "key": "priority", "value": "build reserves", "share_scope": "nexus_family"},
            ]},
        ],
    })
    assert thesis["contradictions"] and thesis["contradictions"][0]["status"] == "unresolved"


def test_product_thesis_uses_only_large_aggregate_cohorts_and_public_evidence() -> None:
    thesis = build_product_thesis("being-group", {
        "minimum_cohort_size": 20,
        "aggregate_metrics": [
            {"section": "activation", "key": "onboarding_complete_rate", "value": 0.64, "cohort_size": 240, "period": "30d"},
            {"section": "retention", "key": "small_group", "value": 0.9, "cohort_size": 3},
            {"section": "trust", "key": "bad_row", "value": 1, "cohort_size": 100, "email": "private@example.com"},
        ],
        "public_evidence": [
            {"section": "partnerships", "title": "Public program", "finding": "Possible aligned program", "source_url": "https://example.org/program"},
        ],
        "human_thesis": {"private": "never included"},
    })
    encoded = json.dumps(thesis["claims"], sort_keys=True)
    assert "onboarding_complete_rate" in encoded and "Public program" in encoded
    assert "small_group" not in encoded and "private@example.com" not in encoded and "never included" not in encoded
    assert len(thesis["rejected_contributions"]) == 2
    assert thesis["founder_review_required"] is True and thesis["execution_authority"] == "none"


def main() -> None:
    for name, fn in list(globals().items()):
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("All thesis contract tests passed.")


if __name__ == "__main__":
    main()
