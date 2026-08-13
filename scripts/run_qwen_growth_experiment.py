"""Run a fail-closed two-GPU Ascension Qwen growth experiment.

The runner trains independent candidates from one reviewed parent and exact
curriculum, records timing/provenance, runs the canonical + receipt gates, and
writes a comparison report.  It never promotes an adapter.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SAFE_RUN_ID = re.compile(r"^[a-z0-9][a-z0-9_-]{2,63}$")


@dataclass(frozen=True)
class Candidate:
    name: str
    gpu: str
    learning_rate: float
    seed: int


def validate_run_id(value: str) -> str:
    if not SAFE_RUN_ID.fullmatch(value):
        raise ValueError("run id must be 3-64 lowercase letters, numbers, '_' or '-'")
    return value


def candidate_paths(run_id: str, candidate: Candidate) -> dict[str, Path]:
    stem = f"{run_id}_{candidate.name}"
    return {
        "adapter": ROOT / "checkpoints" / stem,
        "train_log": ROOT / "checkpoints" / f"{stem}_train.log",
        "gate_log": ROOT / "checkpoints" / f"{stem}_gate.log",
        "gate_report": ROOT / "evals" / "results" / f"{stem}_gate.json",
    }


def relative(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def build_train_command(
    *, model: str, parent_adapter: str, curriculum: str, epochs: float,
    max_length: int, candidate: Candidate, paths: dict[str, Path]
) -> list[str]:
    return [
        sys.executable,
        str(ROOT / "scripts" / "train_qwen_ascension_lora.py"),
        "--model", model,
        "--resume-adapter", parent_adapter,
        "--output-dir", relative(paths["adapter"]),
        "--curriculum", curriculum,
        "--epochs", str(epochs),
        "--learning-rate", str(candidate.learning_rate),
        "--seed", str(candidate.seed),
        "--max-length", str(max_length),
    ]


def build_gate_command(
    *, model: str, tokens: int, paths: dict[str, Path]
) -> list[str]:
    return [
        sys.executable,
        str(ROOT / "scripts" / "evaluate_qwen_ascension_lora.py"),
        "--model", model,
        "--adapter", relative(paths["adapter"]),
        "--tokens", str(tokens),
        "--output", relative(paths["gate_report"]),
    ]


def load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def spawn(command: list[str], log_path: Path, gpu: str) -> tuple[subprocess.Popen[Any], Any]:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handle = log_path.open("w", encoding="utf-8")
    environment = os.environ.copy()
    environment["CUDA_VISIBLE_DEVICES"] = gpu
    environment.setdefault("HF_HOME", "/workspace/.hf_home")
    process = subprocess.Popen(
        command,
        cwd=ROOT,
        env=environment,
        stdout=handle,
        stderr=subprocess.STDOUT,
    )
    return process, handle


def wait_all(running: dict[str, tuple[subprocess.Popen[Any], Any, float]]) -> dict[str, dict[str, Any]]:
    outcomes: dict[str, dict[str, Any]] = {}
    for name, (process, handle, started) in running.items():
        return_code = process.wait()
        handle.close()
        outcomes[name] = {
            "return_code": return_code,
            "wall_seconds": round(time.monotonic() - started, 3),
        }
    return outcomes


def candidate_summary(
    candidate: Candidate, paths: dict[str, Path], train_outcome: dict[str, Any],
    gate_outcome: dict[str, Any] | None
) -> dict[str, Any]:
    receipt = load_json(paths["adapter"] / "ascension_training_receipt.json")
    gate = load_json(paths["gate_report"])
    gate_complete = gate is not None and gate_outcome is not None
    automatic_gate_passed = bool(gate_complete and gate.get("automatic_gate_passed"))
    return {
        "candidate": asdict(candidate),
        "adapter": relative(paths["adapter"]),
        "training": train_outcome,
        "training_receipt": receipt,
        "gate_execution": gate_outcome,
        "gate_report": gate,
        "status": "awaiting_human_review" if automatic_gate_passed else "rejected_by_automatic_gate",
        "automatic_gate_passed": automatic_gate_passed,
        "human_review_required": True,
        "production_replacement_ready": False,
    }


def run_experiment(args: argparse.Namespace) -> dict[str, Any]:
    run_id = validate_run_id(args.run_id)
    gpu_indices = [item.strip() for item in args.gpu_indices.split(",") if item.strip()]
    learning_rates = [float(item) for item in args.learning_rates.split(",")]
    seeds = [int(item) for item in args.seeds.split(",")]
    if not (len(gpu_indices) == len(learning_rates) == len(seeds) == 2):
        raise ValueError("exactly two GPU indices, learning rates, and seeds are required")
    candidates = [
        Candidate("a", gpu_indices[0], learning_rates[0], seeds[0]),
        Candidate("b", gpu_indices[1], learning_rates[1], seeds[1]),
    ]
    plans: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        paths = candidate_paths(run_id, candidate)
        if paths["adapter"].exists() and not args.dry_run:
            raise FileExistsError(f"refusing to overwrite {paths['adapter']}")
        plans[candidate.name] = {
            "candidate": candidate,
            "paths": paths,
            "train_command": build_train_command(
                model=args.model,
                parent_adapter=args.parent_adapter,
                curriculum=args.curriculum,
                epochs=args.epochs,
                max_length=args.max_length,
                candidate=candidate,
                paths=paths,
            ),
            "gate_command": build_gate_command(model=args.model, tokens=args.tokens, paths=paths),
        }
    if args.dry_run:
        return {
            "run_id": run_id,
            "dry_run": True,
            "plans": {
                name: {
                    "candidate": asdict(plan["candidate"]),
                    "train_command": plan["train_command"],
                    "gate_command": plan["gate_command"],
                }
                for name, plan in plans.items()
            },
            "human_review_required": True,
            "production_replacement_ready": False,
        }

    train_running = {}
    for name, plan in plans.items():
        process, handle = spawn(plan["train_command"], plan["paths"]["train_log"], plan["candidate"].gpu)
        train_running[name] = (process, handle, time.monotonic())
    train_outcomes = wait_all(train_running)

    gate_running = {}
    for name, plan in plans.items():
        receipt_path = plan["paths"]["adapter"] / "ascension_training_receipt.json"
        if train_outcomes[name]["return_code"] != 0 or not receipt_path.exists():
            continue
        process, handle = spawn(plan["gate_command"], plan["paths"]["gate_log"], plan["candidate"].gpu)
        gate_running[name] = (process, handle, time.monotonic())
    gate_outcomes = wait_all(gate_running)

    summaries = [
        candidate_summary(
            plan["candidate"],
            plan["paths"],
            train_outcomes[name],
            gate_outcomes.get(name),
        )
        for name, plan in plans.items()
    ]
    passing = [item for item in summaries if item["automatic_gate_passed"]]
    report = {
        "run_id": run_id,
        "model": args.model,
        "parent_adapter": args.parent_adapter,
        "curriculum": args.curriculum,
        "candidates": summaries,
        "automatic_gate_pass_count": len(passing),
        "recommended_for_human_review": passing[0]["adapter"] if passing else None,
        "promotion_performed": False,
        "human_review_required": True,
        "production_replacement_ready": False,
    }
    report_path = ROOT / args.report
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Run two fail-closed Qwen growth candidates")
    result.add_argument("--run-id", required=True)
    result.add_argument("--model", default="Qwen/Qwen3-1.7B")
    result.add_argument("--parent-adapter", required=True)
    result.add_argument("--curriculum", required=True)
    result.add_argument("--gpu-indices", default="0,1")
    result.add_argument("--learning-rates", default="2e-5,1e-5")
    result.add_argument("--seeds", default="3407,3411")
    result.add_argument("--epochs", type=float, default=2.0)
    result.add_argument("--max-length", type=int, default=768)
    result.add_argument("--tokens", type=int, default=160)
    result.add_argument("--report", default="evals/results/qwen_growth_experiment.json")
    result.add_argument("--dry-run", action="store_true")
    return result


def main(argv: list[str] | None = None) -> int:
    report = run_experiment(parser().parse_args(argv))
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
