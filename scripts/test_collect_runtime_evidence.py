"""Offline gates for the native runtime evidence collector."""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import collect_runtime_evidence as collector


def valid_payload() -> dict:
    return {
        "content": "Hi there. I am here with you.",
        "model": "Ascension Test Model",
        "provider": "ascension-native",
        "outside_provider": False,
        "production_replacement_enabled": False,
        "latency_ms": 120,
        "queue_wait_ms": 4,
        "inference_ms": 116,
    }


def valid_health() -> dict:
    return {
        "provider": "ascension-native",
        "outside_provider": False,
        "replacement_ready": False,
        "runtime": {
            "model": "Ascension Test Model",
            "profile": "test",
            "repo_id": "ascension/test",
            "filename": "test.gguf",
            "inference": "local_gguf_llama_cpp",
            "queue": {"queue_depth": 0, "active_requests": 0},
        },
    }


def report(*, provenance: str = "mock", payload=None, health=None, i_status=200, h_status=200, hashes=None):
    return collector.build_report(
        intelligence_status=i_status,
        payload=payload or valid_payload(),
        client_latency_ms=125,
        health_status=h_status,
        health=health or valid_health(),
        provenance=provenance,
        source_hashes=hashes or collector.compute_source_hashes(),
    )


def test_source_hashes_cover_runtime_path() -> None:
    hashes = collector.compute_source_hashes()
    assert all(len(hashes[path]) == 64 for path in collector.SOURCE_FILES)


def test_valid_mock_is_never_proven() -> None:
    result = report()
    assert result["gated_reasons"] == []
    assert result["proven"] is False
    assert result["replacement_ready"] is False


def test_valid_live_shape_can_be_proven_without_enabling_replacement() -> None:
    result = report(provenance="live")
    assert result["proven"] is True
    assert result["replacement_ready"] is False
    assert "content_hash" in result["response_evidence"]
    assert "content" not in result["response_evidence"]


def test_http_statuses_fail_closed() -> None:
    assert "intelligence_http_status_not_200" in report(i_status=504)["gated_reasons"]
    assert "health_http_status_not_200" in report(h_status=503)["gated_reasons"]


def test_outside_provider_fails_closed() -> None:
    payload = valid_payload()
    payload["outside_provider"] = True
    assert "outside_provider_not_false" in report(payload=payload)["gated_reasons"]


def test_missing_health_provider_fails_closed() -> None:
    health = valid_health()
    health.pop("provider")
    assert "health_provider_not_ascension_native" in report(health=health)["gated_reasons"]


def test_missing_queue_and_metrics_fail_closed() -> None:
    payload = valid_payload()
    for key in ("latency_ms", "queue_wait_ms", "inference_ms"):
        payload.pop(key)
    health = valid_health()
    health["runtime"].pop("queue")
    reasons = report(payload=payload, health=health)["gated_reasons"]
    assert "server_latency_missing" in reasons
    assert "queue_wait_missing" in reasons
    assert "inference_time_missing" in reasons
    assert "runtime_queue_missing" in reasons


def test_missing_source_hash_fails_closed() -> None:
    hashes = collector.compute_source_hashes()
    hashes[collector.SOURCE_FILES[0]] = ""
    assert "source_hash_evidence_missing" in report(hashes=hashes)["gated_reasons"]


def test_write_refuses_mock_or_failed_evidence() -> None:
    directory = Path(tempfile.mkdtemp(prefix="ascension_runtime_evidence_"))
    try:
        destination = directory / "report.json"
        for candidate in (report(), report(provenance="live", i_status=500)):
            try:
                collector.write_report(candidate, destination)
                raise AssertionError("unproven evidence was written")
            except collector.EvidenceCollectionError:
                pass
        assert not destination.exists()
    finally:
        shutil.rmtree(directory, ignore_errors=True)


def main() -> None:
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print(f"Runtime evidence tests passed: {len(tests)}/{len(tests)}")


if __name__ == "__main__":
    main()
