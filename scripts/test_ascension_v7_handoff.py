"""Deterministic unit tests for the post-training v7 handoff CLI."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import scripts.ascension_v7_handoff as handoff
from scripts.ascension_v7_handoff import (
    artifact_files_exist,
    build_handoff_packet,
    load_status,
    main,
)


def _write_status(path: Path, status: str, step: int, total: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {"version": "test_v7", "status": status, "step": step, "total_steps": total},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )


def _touch(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"")


def _gate_json(version: str = "test_v7", automatic: bool = True) -> dict:
    return {
        "version": version,
        "automatic_gate_passed": automatic,
        "human_review_required": True,
        "production_replacement_ready": False,
        "promotion_status": "blocked_pending_full_evaluation",
        "checkpoint_artifacts": {
            "model": {"filename": f"{version}.pt", "bytes": 0, "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
            "metadata": {"filename": f"{version}_meta.json", "bytes": 0, "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
            "tokenizer": {"filename": f"{version}_tokenizer.json", "bytes": 0, "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"},
        },
        "held_out_loss": 1.23,
        "held_out_loss_pass": True,
        "architecture_pass": True,
        "tokenizer_metadata_pass": True,
        "tokenizer_roundtrip_pass": True,
        "structural_passes": 6,
        "semantic_passes": 6,
        "sample_count": 6,
        "expected_sample_count": 6,
        "sample_count_pass": True,
        "generation_errors": [],
        "recommended_next_initialization": "resume",
        "samples": [{"structural_pass": True, "semantic_pass": True, "text": "ok"}] * 6,
    }


def test_load_status_requires_complete():
    with tempfile.TemporaryDirectory() as tmp:
        cp = Path(tmp) / "checkpoints"
        cp.mkdir()
        _write_status(cp / "test_v7_status.json", "training", 1, 2)
        try:
            load_status(cp, "test_v7")
            assert False, "expected ValueError for incomplete status"
        except ValueError as error:
            assert "must be 'complete'" in str(error)


def test_load_status_requires_final_step():
    with tempfile.TemporaryDirectory() as tmp:
        cp = Path(tmp) / "checkpoints"
        cp.mkdir()
        _write_status(cp / "test_v7_status.json", "complete", 1, 2)
        try:
            load_status(cp, "test_v7")
            assert False, "expected ValueError for step mismatch"
        except ValueError as error:
            assert "step" in str(error)


def test_load_status_passes_complete():
    with tempfile.TemporaryDirectory() as tmp:
        cp = Path(tmp) / "checkpoints"
        cp.mkdir()
        _write_status(cp / "test_v7_status.json", "complete", 2, 2)
        status = load_status(cp, "test_v7")
        assert status["status"] == "complete"
        assert status["step"] == status["total_steps"]


def test_load_status_rejects_wrong_version():
    with tempfile.TemporaryDirectory() as tmp:
        cp = Path(tmp) / "checkpoints"
        cp.mkdir()
        _write_status(cp / "requested_v7_status.json", "complete", 2, 2)
        try:
            load_status(cp, "requested_v7")
            assert False, "expected ValueError for version mismatch"
        except ValueError as error:
            assert "version" in str(error)


def test_artifact_files_exist_fails_missing():
    with tempfile.TemporaryDirectory() as tmp:
        cp = Path(tmp) / "checkpoints"
        cp.mkdir()
        try:
            artifact_files_exist(cp, "test_v7")
            assert False, "expected FileNotFoundError for missing artifacts"
        except FileNotFoundError as error:
            assert "test_v7.pt" in str(error)


def test_artifact_files_exist_passes():
    with tempfile.TemporaryDirectory() as tmp:
        cp = Path(tmp) / "checkpoints"
        _touch(cp / "test_v7.pt")
        _touch(cp / "test_v7_meta.json")
        _touch(cp / "test_v7_tokenizer.json")
        artifacts = artifact_files_exist(cp, "test_v7")
        assert len(artifacts) == 3
        assert all(p.is_file() for p in artifacts)


def test_build_handoff_packet():
    with tempfile.TemporaryDirectory() as tmp:
        cp = Path(tmp) / "checkpoints"
        _touch(cp / "test_v7.pt")
        _touch(cp / "test_v7_meta.json")
        _touch(cp / "test_v7_tokenizer.json")
        gate_path = Path(tmp) / "gate.json"
        handoff_path = Path(tmp) / "handoff.json"
        gate = _gate_json(automatic=True)
        gate_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2), encoding="utf-8")

        status = {"status": "complete", "step": 2, "total_steps": 2}
        packet = build_handoff_packet("test_v7", status, gate_path, handoff_path, cp)

        assert packet["version"] == "test_v7"
        assert packet["handoff_type"] == "v7_post_training"
        assert packet["automatic_gate_passed"] is True
        assert packet["pass_for_human_review"] is True
        assert packet["human_review_required"] is True
        assert packet["production_replacement_ready"] is False
        assert packet["promotion_status"] == "blocked_pending_human_review"
        assert packet["artifact_hashes"] is not None
        assert packet["metrics"]["sample_count"] == 6
        assert packet["samples"] is not None
        assert len(packet["samples"]) == 6

        assert handoff_path.is_file()
        on_disk = json.loads(handoff_path.read_text(encoding="utf-8"))
        assert on_disk == packet


def test_build_handoff_packet_rejects_version_mismatch():
    with tempfile.TemporaryDirectory() as tmp:
        cp = Path(tmp) / "checkpoints"
        _touch(cp / "test_v7.pt")
        _touch(cp / "test_v7_meta.json")
        _touch(cp / "test_v7_tokenizer.json")
        gate_path = Path(tmp) / "gate.json"
        handoff_path = Path(tmp) / "handoff.json"
        gate = _gate_json(version="other_v7")
        gate_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2), encoding="utf-8")
        try:
            build_handoff_packet("test_v7", {}, gate_path, handoff_path, cp)
            assert False, "expected ValueError for version mismatch"
        except ValueError as error:
            assert "does not match" in str(error)


def test_build_handoff_packet_rejects_artifact_hash_mismatch():
    with tempfile.TemporaryDirectory() as tmp:
        cp = Path(tmp) / "checkpoints"
        _touch(cp / "test_v7.pt")
        _touch(cp / "test_v7_meta.json")
        _touch(cp / "test_v7_tokenizer.json")
        gate_path = Path(tmp) / "gate.json"
        handoff_path = Path(tmp) / "handoff.json"
        gate = _gate_json()
        gate["checkpoint_artifacts"]["model"]["sha256"] = "0" * 64
        gate_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2), encoding="utf-8")
        try:
            build_handoff_packet("test_v7", {}, gate_path, handoff_path, cp)
            assert False, "expected ValueError for artifact hash mismatch"
        except ValueError as error:
            assert "artifact hashes" in str(error)


def test_build_handoff_packet_requires_every_sample():
    with tempfile.TemporaryDirectory() as tmp:
        cp = Path(tmp) / "checkpoints"
        _touch(cp / "test_v7.pt")
        _touch(cp / "test_v7_meta.json")
        _touch(cp / "test_v7_tokenizer.json")
        gate_path = Path(tmp) / "gate.json"
        handoff_path = Path(tmp) / "handoff.json"
        gate = _gate_json()
        gate["samples"] = gate["samples"][:-1]
        gate_path.write_text(json.dumps(gate, ensure_ascii=False, indent=2), encoding="utf-8")
        try:
            build_handoff_packet("test_v7", {}, gate_path, handoff_path, cp)
            assert False, "expected ValueError for incomplete samples"
        except ValueError as error:
            assert "every expected" in str(error)


def test_main_end_to_end():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        cp = root / "checkpoints"
        gate_path = Path(tmp) / "gate.json"
        handoff_path = Path(tmp) / "handoff.json"

        _write_status(cp / "test_v7_status.json", "complete", 4, 4)
        _touch(cp / "test_v7.pt")
        _touch(cp / "test_v7_meta.json")
        _touch(cp / "test_v7_tokenizer.json")

        def fake_run(args, **kwargs):
            # The mock receives the argument list; the evaluator output path is at index 5.
            output = Path(args[5])
            output.parent.mkdir(parents=True, exist_ok=True)
            gate = _gate_json("test_v7", automatic=True)
            output.write_text(json.dumps(gate, ensure_ascii=False, indent=2), encoding="utf-8")
            class Completed:
                returncode = 0
                stderr = ""
            return Completed()

        with patch.object(handoff, "ROOT", root), patch("subprocess.run", side_effect=fake_run):
            code = main(
                [
                    "--version",
                    "test_v7",
                    "--gate-output",
                    str(gate_path),
                    "--handoff-output",
                    str(handoff_path),
                ]
            )

        assert code == 0
        packet = json.loads(handoff_path.read_text(encoding="utf-8"))
        assert packet["pass_for_human_review"] is True
        assert packet["production_replacement_ready"] is False
        assert packet["human_review_required"] is True
        assert packet["artifact_hashes"] is not None
        assert packet["samples"] is not None
        assert packet["metrics"]["generation_errors_count"] == 0


def test_main_returns_fail_when_gate_fails():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        cp = root / "checkpoints"
        gate_path = Path(tmp) / "gate.json"
        handoff_path = Path(tmp) / "handoff.json"

        _write_status(cp / "test_v7_status.json", "complete", 4, 4)
        _touch(cp / "test_v7.pt")
        _touch(cp / "test_v7_meta.json")
        _touch(cp / "test_v7_tokenizer.json")

        def fake_run(args, **kwargs):
            output = Path(args[5])
            output.parent.mkdir(parents=True, exist_ok=True)
            gate = _gate_json("test_v7", automatic=False)
            output.write_text(json.dumps(gate, ensure_ascii=False, indent=2), encoding="utf-8")
            class Completed:
                returncode = 2
                stderr = ""
            return Completed()

        with patch.object(handoff, "ROOT", root), patch("subprocess.run", side_effect=fake_run):
            code = main(
                [
                    "--version",
                    "test_v7",
                    "--gate-output",
                    str(gate_path),
                    "--handoff-output",
                    str(handoff_path),
                ]
            )

        assert code == 2
        packet = json.loads(handoff_path.read_text(encoding="utf-8"))
        assert packet["pass_for_human_review"] is False
        assert packet["production_replacement_ready"] is False
        assert packet["human_review_required"] is True


def main_test_runner() -> int:
    tests = [fn for name, fn in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print("PASS all v7 handoff unit tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main_test_runner())
