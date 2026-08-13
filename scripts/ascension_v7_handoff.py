"""Post-training v7 handoff CLI.

Safe to run only after a training run has completed and the training status file
confirms the final step was reached. It invokes the canonical native
checkpoint evaluator and turns the evaluator receipt into a compact human-review
packet. It never promotes a model, sets replacement readiness, starts training,
or modifies checkpoint files.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.evaluate_native_checkpoint import ROOT, checkpoint_artifact_evidence


def load_status(checkpoints_dir: Path, version: str) -> dict:
    """Read the training status file and confirm completion."""
    status_path = checkpoints_dir / f"{version}_status.json"
    if not status_path.is_file():
        raise FileNotFoundError(f"training status is missing: {status_path}")
    status = json.loads(status_path.read_text(encoding="utf-8"))
    if not isinstance(status, dict):
        raise ValueError("training status must be a JSON object")
    if status.get("version") != version:
        raise ValueError(
            f"training status version {status.get('version')!r} does not match {version!r}"
        )
    if status.get("status") != "complete":
        raise ValueError(f"training status is {status.get('status')!r}; must be 'complete'")
    step = status.get("step")
    total_steps = status.get("total_steps")
    if (
        isinstance(step, bool)
        or not isinstance(step, int)
        or isinstance(total_steps, bool)
        or not isinstance(total_steps, int)
        or total_steps <= 0
    ):
        raise ValueError("training step and total_steps must be positive integer evidence")
    if step != total_steps:
        raise ValueError(
            f"training step {step} != total_steps {total_steps}"
        )
    return status


def artifact_files_exist(checkpoints_dir: Path, version: str) -> list[Path]:
    """Fail closed if any expected artifact is missing."""
    artifacts = [
        checkpoints_dir / f"{version}.pt",
        checkpoints_dir / f"{version}_meta.json",
        checkpoints_dir / f"{version}_tokenizer.json",
    ]
    missing = [str(p) for p in artifacts if not p.is_file()]
    if missing:
        raise FileNotFoundError(f"required v7 artifacts are missing: {missing}")
    return artifacts


def run_canonical_evaluation(version: str, gate_output: Path) -> int:
    """Invoke the canonical evaluator without duplicating its gates."""
    completed = subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "evaluate_native_checkpoint.py"),
            "--version",
            version,
            "--output",
            str(gate_output),
        ],
        check=False,
        text=True,
        capture_output=True,
    )
    if completed.returncode not in (0, 2):
        raise RuntimeError(f"evaluator failed with code {completed.returncode}: {completed.stderr}")
    return completed.returncode


def validate_gate_receipt(
    version: str,
    gate: dict,
    checkpoints_dir: Path,
    artifacts: list[Path],
) -> None:
    """Validate receipt completeness and its binding to the current checkpoint bytes."""
    if not isinstance(gate, dict):
        raise ValueError("evaluator gate receipt must be a JSON object")
    if gate.get("version") != version:
        raise ValueError(
            f"gate receipt version {gate.get('version')!r} does not match {version!r}"
        )

    expected_artifacts = checkpoint_artifact_evidence(
        checkpoints_dir, version, artifacts[2]
    )
    if gate.get("checkpoint_artifacts") != expected_artifacts:
        raise ValueError("gate receipt artifact hashes do not match current checkpoint bytes")

    expected_sample_count = gate.get("expected_sample_count")
    samples = gate.get("samples")
    generation_errors = gate.get("generation_errors")
    if (
        isinstance(expected_sample_count, bool)
        or not isinstance(expected_sample_count, int)
        or expected_sample_count <= 0
    ):
        raise ValueError("gate receipt expected_sample_count is missing or invalid")
    if not isinstance(samples, list) or len(samples) != expected_sample_count:
        raise ValueError("gate receipt does not contain every expected evaluation sample")
    if gate.get("sample_count") != len(samples):
        raise ValueError("gate receipt sample_count does not match its sample evidence")
    if not isinstance(generation_errors, list):
        raise ValueError("gate receipt generation_errors must be a list")
    if not isinstance(gate.get("automatic_gate_passed"), bool):
        raise ValueError("gate receipt automatic_gate_passed must be boolean")


def build_handoff_packet(
    version: str,
    status: dict,
    gate_path: Path,
    handoff_output: Path,
    checkpoints_dir: Path,
) -> dict:
    """Compose a compact human-review packet from the evaluator receipt."""
    if not gate_path.is_file():
        raise FileNotFoundError(f"evaluator gate receipt is missing: {gate_path}")
    gate = json.loads(gate_path.read_text(encoding="utf-8"))

    artifacts = artifact_files_exist(checkpoints_dir, version)
    validate_gate_receipt(version, gate, checkpoints_dir, artifacts)

    automatic_gate_passed = gate["automatic_gate_passed"]
    pass_for_human_review = automatic_gate_passed

    packet = {
        "version": version,
        "handoff_type": "v7_post_training",
        "status_precondition": status,
        "precondition_pass": True,
        "automatic_gate_passed": automatic_gate_passed,
        "pass_for_human_review": pass_for_human_review,
        "human_review_required": True,
        "production_replacement_ready": False,
        "promotion_status": (
            "blocked_pending_human_review"
            if automatic_gate_passed
            else "blocked_automatic_gate_failed"
        ),
        "artifact_hashes": gate["checkpoint_artifacts"],
        "metrics": {
            "held_out_loss": gate.get("held_out_loss"),
            "held_out_loss_pass": gate.get("held_out_loss_pass"),
            "architecture_pass": gate.get("architecture_pass"),
            "tokenizer_metadata_pass": gate.get("tokenizer_metadata_pass"),
            "tokenizer_roundtrip_pass": gate.get("tokenizer_roundtrip_pass"),
            "structural_passes": gate.get("structural_passes"),
            "semantic_passes": gate.get("semantic_passes"),
            "sample_count": gate.get("sample_count"),
            "expected_sample_count": gate.get("expected_sample_count"),
            "sample_count_pass": gate.get("sample_count_pass"),
            "generation_errors_count": len(gate.get("generation_errors", [])),
            "generation_errors": gate.get("generation_errors"),
            "recommended_next_initialization": gate.get("recommended_next_initialization"),
        },
        "samples": gate["samples"],
        "gate_path": str(gate_path),
    }

    handoff_output.parent.mkdir(parents=True, exist_ok=True)
    handoff_output.write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding="utf-8")
    return packet


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a safe post-training v7 handoff packet")
    parser.add_argument("--version", default="ascension_causal_general_v7")
    parser.add_argument(
        "--gate-output",
        default=str(ROOT / "evals" / "results" / "native_checkpoint_gate.json"),
        help="path where the canonical evaluator will write its gate receipt",
    )
    parser.add_argument(
        "--handoff-output",
        default=str(ROOT / "evals" / "results" / "v7_handoff.json"),
        help="path where the human-review handoff packet will be written",
    )
    args = parser.parse_args(argv)

    checkpoints_dir = ROOT / "checkpoints"
    gate_output = Path(args.gate_output)
    handoff_output = Path(args.handoff_output)

    status = load_status(checkpoints_dir, args.version)
    artifact_files_exist(checkpoints_dir, args.version)
    run_canonical_evaluation(args.version, gate_output)
    packet = build_handoff_packet(
        args.version, status, gate_output, handoff_output, checkpoints_dir
    )

    print(json.dumps(packet, ensure_ascii=False, indent=2))
    return 0 if packet["pass_for_human_review"] else 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
