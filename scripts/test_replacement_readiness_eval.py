"""Offline unit tests for the replacement-readiness + capability-coverage gate.

This requires no live service or token. It exercises the summary builder,
report validator, and prompt evaluator using mock data.
"""

from __future__ import annotations

from replacement_readiness_eval import (
    build_summary,
    validate_capability_coverage,
    evaluate,
    compute_source_hashes,
    REQUIRED_SURFACES,
    SCHEMA_VERSION,
)


def _make_prompt_results(*passed: bool) -> list[dict]:
    return [{"id": f"case_{i}", "passed": p, "latency_ms": 0} for i, p in enumerate(passed, 1)]


def _make_coverage_report(*, ready: bool, blockers: list[str], surface_classes: dict | None = None,
                          source_hashes: dict | None = None, schema_version: str | None = SCHEMA_VERSION) -> dict:
    surface_classes = surface_classes or {}
    # Fill the full canonical manifest; override with the supplied surface_classes.
    per_surface = {
        name: {"surface_class": "specialized_deterministic", "blockers": []}
        for name in REQUIRED_SURFACES
    }
    for name, cls in surface_classes.items():
        per_surface[name] = {
            "surface_class": cls,
            "blockers": [f"{name} is unproven"] if cls == "registered_only" else [],
        }
    return {
        "schema_version": schema_version,
        "source_hashes": source_hashes if source_hashes is not None else compute_source_hashes(),
        "replacement_ready": ready,
        "replacement_ready_blockers": blockers,
        "per_surface": per_surface,
        "per_id": {},
    }


def test_evaluate_rejects_hidden_reasoning_tags() -> None:
    case = {
        "id": "hidden_thought",
        "shell": "individual",
        "required_any": ["ok"],
        "forbidden": [],
        "max_words": 260,
    }
    payload = {
        "content": "Looks good. \x3cthink\x3e secret reasoning \x3c/think\x3e",
        "provider": "ascension-native",
        "outside_provider": False,
    }
    result = evaluate(case, 200, payload, 0)
    assert "hidden_reasoning_leak" in result["failures"], result


def test_validate_coverage_passes_for_clean_report() -> None:
    report = _make_coverage_report(
        ready=True,
        blockers=[],
        surface_classes={
            "natural conversation": "model_backed_native",
        },
    )
    result = validate_capability_coverage(report)
    assert result["pass"] is True, result
    assert result["source_hash_match"] is True
    assert result["counts"]["proven"] == len(REQUIRED_SURFACES)
    assert result["counts"]["registered_only"] == 0


def test_validate_coverage_fails_for_registered_only_surfaces() -> None:
    report = _make_coverage_report(
        ready=False,
        blockers=["natural conversation"],
        surface_classes={"natural conversation": "registered_only"},
    )
    result = validate_capability_coverage(report)
    assert result["pass"] is False
    assert any("natural conversation" in b for b in result["blockers"])
    assert result["counts"]["registered_only"] == 1


def test_validate_coverage_fails_for_missing_surfaces() -> None:
    report = _make_coverage_report(
        ready=True,
        blockers=[],
        surface_classes={name: "specialized_deterministic" for name in REQUIRED_SURFACES},
    )
    # Remove one surface to simulate a truncated report.
    report["per_surface"].pop("natural conversation")
    result = validate_capability_coverage(report)
    assert result["pass"] is False
    assert any("missing required surfaces" in b for b in result["blockers"])


def test_validate_coverage_fails_for_unexpected_surfaces() -> None:
    report = _make_coverage_report(
        ready=True,
        blockers=[],
    )
    report["per_surface"]["quantum chess"] = {"surface_class": "model_backed_native"}
    result = validate_capability_coverage(report)
    assert result["pass"] is False
    assert any("unexpected surfaces" in b for b in result["blockers"])


def test_validate_coverage_fails_for_missing_source_hash() -> None:
    report = _make_coverage_report(ready=True, blockers=[])
    report["source_hashes"] = {}
    result = validate_capability_coverage(report)
    assert result["pass"] is False
    assert any("missing source_hashes" in b for b in result["blockers"])


def test_validate_coverage_fails_for_stale_source_hash() -> None:
    report = _make_coverage_report(ready=True, blockers=[])
    report["source_hashes"]["src/services/capability-registry.ts"] = "0" * 64
    result = validate_capability_coverage(report)
    assert result["pass"] is False
    assert any("source hash mismatch" in b for b in result["blockers"])


def test_validate_coverage_fails_for_bad_schema_version() -> None:
    report = _make_coverage_report(ready=True, blockers=[], schema_version="99")
    result = validate_capability_coverage(report)
    assert result["pass"] is False
    assert any("schema_version mismatch" in b for b in result["blockers"])


def test_build_summary_ready_when_both_gates_pass() -> None:
    prompts = _make_prompt_results(True, True, True)
    coverage = _make_coverage_report(ready=True, blockers=[])
    summary = build_summary(prompts, True, coverage)
    assert summary["prompt_cases"]["pass"] is True
    assert summary["capability_coverage_pass"] is True
    assert summary["capability_coverage"]["loaded"] is True
    assert summary["replacement_ready"] is True


def test_build_summary_fails_when_prompts_fail() -> None:
    prompts = _make_prompt_results(True, False, True)
    coverage = _make_coverage_report(ready=True, blockers=[])
    summary = build_summary(prompts, True, coverage)
    assert summary["prompt_cases"]["pass"] is False
    assert summary["replacement_ready"] is False


def test_build_summary_fails_when_capability_coverage_fails() -> None:
    prompts = _make_prompt_results(True, True)
    coverage = _make_coverage_report(
        ready=False,
        blockers=["natural conversation"],
        surface_classes={"natural conversation": "registered_only"},
    )
    summary = build_summary(prompts, True, coverage)
    assert summary["prompt_cases"]["pass"] is True
    assert summary["capability_coverage_pass"] is False
    assert summary["replacement_ready"] is False


def test_build_summary_fails_when_coverage_report_missing() -> None:
    prompts = _make_prompt_results(True, True)
    missing_coverage = {
        "schema_version": None,
        "source_hashes": {},
        "replacement_ready": False,
        "replacement_ready_blockers": ["capability coverage report unavailable"],
        "per_surface": {},
        "per_id": {},
    }
    summary = build_summary(prompts, False, missing_coverage)
    assert summary["capability_coverage_pass"] is False
    assert summary["capability_coverage"]["loaded"] is False
    assert summary["replacement_ready"] is False


def test_build_summary_counts_and_classifications() -> None:
    prompts = _make_prompt_results(True)
    coverage = _make_coverage_report(
        ready=False,
        blockers=["natural conversation", "schedule / calendar"],
        surface_classes={
            "natural conversation": "registered_only",
            "schedule / calendar": "registered_only",
            "browser / web research": "outside_provider",
        },
    )
    summary = build_summary(prompts, True, coverage)
    cov = summary["capability_coverage"]
    assert cov["counts"]["required"] == len(REQUIRED_SURFACES)
    assert "natural conversation" in cov["registered_only_surfaces"]
    assert "browser / web research" in cov["outside_provider_surfaces"]


def test_validate_coverage_fails_when_per_surface_missing() -> None:
    report = {"schema_version": SCHEMA_VERSION, "source_hashes": compute_source_hashes(),
              "replacement_ready": False, "replacement_ready_blockers": [], "per_surface": {}}
    result = validate_capability_coverage(report)
    assert result["pass"] is False
    assert any("per_surface missing or empty" in b for b in result["blockers"])


def test_validate_coverage_fails_for_unknown_surface_class() -> None:
    report = _make_coverage_report(ready=False, blockers=[])
    report["per_surface"]["natural conversation"]["surface_class"] = "magic"
    result = validate_capability_coverage(report)
    assert result["pass"] is False
    assert any("unknown" in b for b in result["blockers"])


def test_validate_coverage_fails_when_replacement_ready_inconsistent() -> None:
    # Report claims ready but a surface is still registered_only.
    report = _make_coverage_report(ready=True, blockers=[])
    report["per_surface"]["natural conversation"]["surface_class"] = "registered_only"
    report["replacement_ready_blockers"] = ["natural conversation"]
    result = validate_capability_coverage(report)
    assert result["pass"] is False
    assert any("inconsistent" in b.lower() or "unproven" in b.lower() for b in result["blockers"])


def test_validate_coverage_fails_when_not_loaded() -> None:
    report = _make_coverage_report(ready=True, blockers=[])
    result = validate_capability_coverage(report, coverage_loaded=False)
    assert result["pass"] is False
    assert result["loaded"] is False
    assert any("not loaded" in b for b in result["blockers"])


def main() -> None:
    for name, fn in globals().items():
        if name.startswith("test_") and callable(fn):
            fn()
            print(f"PASS {name}")
    print("All offline replacement-readiness tests passed.")


if __name__ == "__main__":
    main()
