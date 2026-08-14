"""Focused tests for runtime-backed capability-surface evidence.

Positive paths prove deterministic handlers produce permission-aware, receipt-gated
output.  Negative paths prove the collector refuses to mark surfaces proven from
registration, mocks, missing models, or outside fallbacks.
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import capability_surface_runtime_evidence as csre
from src.core.model_runtime import runtime


def _runtime_not_ready() -> bool:
    return False


def test_schedule_surface_is_proven_with_receipt_and_permission() -> None:
    record = csre._evidence_for_surface("schedule / calendar", ["ascension_calendar_intelligence"])
    assert record["class"] == "proven", f"expected proven, got {record['class']}: {record.get('reason')}"
    assert record["latency_ms"] >= 0
    pr = record["permission_receipt_evidence"]
    assert pr is not None
    action = pr["proposed_action"]
    assert action["action"] == "schedule.upsert_recurring_work"
    assert action["risk"] == "low"
    assert action["approval"] == "safe_internal_auto"
    assert "memory_receipt" in action["receipt_fields"]


def test_finance_surface_is_proven_with_critical_confirmation() -> None:
    record = csre._evidence_for_surface("finance / budget / grocery", ["ascension_finance"])
    assert record["class"] == "proven", record.get("reason")
    action = record["permission_receipt_evidence"]["proposed_action"]
    assert action["action"] == "finance.payment"
    assert action["risk"] == "critical"
    assert action["approval"] == "explicit_confirmation"
    assert "transaction_id" in action["receipt_fields"]
    gate = record["permission_receipt_evidence"]["permission_approval_gate"]
    assert gate["gate"] == "explicit_confirmation"


def test_sprout_family_surface_is_proven_with_guardian() -> None:
    record = csre._evidence_for_surface("FamilyOS / Sprout / Nexus permission boundaries", ["ascension_sprout"])
    assert record["class"] == "proven", record.get("reason")
    action = record["permission_receipt_evidence"]["proposed_action"]
    assert action["action"] == "calendar.external_write"
    assert action["guardian_required"] is True
    boundary = record["permission_receipt_evidence"]["child_safe_guardian_boundaries"]
    assert boundary["guardian_approval_required"] is True
    assert "calendar.external_write" in boundary["affected_actions"]


def test_natural_conversation_is_unavailable_without_model() -> None:
    record = csre._evidence_for_surface("natural conversation", ["ascension_chat"])
    assert record["class"] == "unavailable", record.get("reason")
    assert "not loaded" in (record.get("reason") or "").lower()
    assert record["provenance"] == "native_model"


def test_native_chat_fails_on_non_ascension_provider_mock() -> None:
    """A mock that claims a non-native provider must not be marked proven."""
    original_model = runtime.model
    original_chat = runtime.chat
    try:
        runtime.model = object()  # ready = True
        runtime.chat = lambda _messages, _temperature, _max_tokens: {
            "content": "Hi there!",
            "model": "Mock",
            "provider": "openai",
            "outside_provider": False,
        }
        chat = csre._try_native_chat()
        assert chat["class"] == "failed"
        assert "non-native" in (chat.get("reason") or "").lower()
    finally:
        runtime.model = original_model
        runtime.chat = original_chat


def test_native_chat_fails_on_exception_mock() -> None:
    original_model = runtime.model
    original_chat = runtime.chat
    try:
        runtime.model = object()
        runtime.chat = lambda _messages, _temperature, _max_tokens: (_ for _ in ()).throw(RuntimeError("model crashed"))
        chat = csre._try_native_chat()
        assert chat["class"] == "failed"
        assert "exception" in (chat.get("reason") or "").lower()
    finally:
        runtime.model = original_model
        runtime.chat = original_chat


def test_browser_surface_is_unavailable_outside_fallback() -> None:
    record = csre._evidence_for_surface("browser / web research", ["web_browsing"])
    assert record["class"] == "unavailable"
    assert record["provenance"] == "outside_fallback"
    assert "outside-provider" in (record.get("reason") or "").lower()


def test_astrology_is_unimplemented_not_proven_from_registration() -> None:
    record = csre._evidence_for_surface("astrology / numerology reflection", ["ascension_astrology"])
    assert record["class"] == "unimplemented"
    assert record["reason"] is not None
    assert record["permission_receipt_evidence"] is None


def test_report_is_fail_closed_and_includes_required_fields() -> None:
    report = csre.build_report()
    assert report["replacement_ready"] is False
    assert report["outside_provider"] is False
    assert "timestamp_utc" in report
    assert "source_hashes" in report
    for h in report["source_hashes"].values():
        assert len(h) == 64
    assert "report_rule" in report
    assert "mocks" in report["report_rule"].lower()
    assert "per_surface" in report
    for record in report["per_surface"].values():
        assert record["class"] in {"proven", "failed", "unavailable", "unimplemented"}
        assert "timestamp_utc" in record
        assert "latency_ms" in record
        assert "queue" in record


def test_main_writes_report_to_configured_path() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "surface_evidence.json"
        original = csre.REPORT_PATH
        csre.REPORT_PATH = path
        try:
            csre.main()
            data = json.loads(path.read_text(encoding="utf-8"))
            assert "per_surface" in data
            assert data["replacement_ready"] is False
        finally:
            csre.REPORT_PATH = original


def main() -> None:
    for name, fn in globals().items():
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("All capability-surface runtime-evidence tests passed.")


if __name__ == "__main__":
    main()
