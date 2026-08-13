"""Offline contract tests for the two-GPU growth runner."""

from __future__ import annotations

import tempfile
from pathlib import Path

from run_qwen_growth_experiment import (
    Candidate,
    build_gate_command,
    build_train_command,
    candidate_paths,
    candidate_summary,
    validate_run_id,
)


def test_run_id_fails_closed() -> None:
    assert validate_run_id("grow004_context") == "grow004_context"
    for invalid in ("UPPER", "../escape", "x", "space here"):
        try:
            validate_run_id(invalid)
        except ValueError:
            continue
        raise AssertionError(f"unsafe run id accepted: {invalid}")


def test_commands_bind_candidate_provenance() -> None:
    candidate = Candidate("a", "0", 2e-5, 3407)
    paths = candidate_paths("grow004_context", candidate)
    train = build_train_command(
        model="Qwen/Qwen3-1.7B",
        parent_adapter="checkpoints/parent",
        curriculum="evals/training/reviewed.jsonl",
        epochs=2,
        max_length=768,
        candidate=candidate,
        paths=paths,
    )
    gate = build_gate_command(model="Qwen/Qwen3-1.7B", tokens=160, paths=paths)
    assert "checkpoints/parent" in train
    assert "evals/training/reviewed.jsonl" in train
    assert "2e-05" in train
    assert "3407" in train
    assert "checkpoints/grow004_context_a" in gate


def test_missing_gate_is_rejected() -> None:
    candidate = Candidate("a", "0", 2e-5, 3407)
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        paths = {
            "adapter": root / "adapter",
            "train_log": root / "train.log",
            "gate_log": root / "gate.log",
            "gate_report": root / "gate.json",
        }
        summary = candidate_summary(candidate, paths, {"return_code": 0}, None)
    assert summary["status"] == "rejected_by_automatic_gate"
    assert summary["automatic_gate_passed"] is False
    assert summary["production_replacement_ready"] is False


def main() -> None:
    tests = [
        test_run_id_fails_closed,
        test_commands_bind_candidate_provenance,
        test_missing_gate_is_rejected,
    ]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print("All growth-runner tests passed.")


if __name__ == "__main__":
    main()
