"""Train and fail-closed gate the Aerynza 1.7B v20 candidate."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODEL = "Qwen/Qwen3-1.7B"
REVISION = "70d244cc86ccca08cf5af4e1e306ecf908b1ad5e"
ADAPTER = "checkpoints/aerynza_qwen3_1_7b_v20_candidate"
RESULTS = ROOT / "evals" / "results"


def run(name: str, args: list[str]) -> dict:
    log = RESULTS / f"aerynza_v20_{name}.log"
    started = datetime.now(timezone.utc).isoformat()
    with log.open("w", encoding="utf-8") as handle:
        process = subprocess.run(args, cwd=ROOT, stdout=handle, stderr=subprocess.STDOUT)
    return {"name": name, "command": args, "started_at": started, "exit_code": process.returncode,
            "log": str(log.relative_to(ROOT))}


def main() -> int:
    RESULTS.mkdir(parents=True, exist_ok=True)
    adapter_path = ROOT / ADAPTER
    if adapter_path.exists() and any(adapter_path.iterdir()):
        raise SystemExit(f"refusing to overwrite existing candidate evidence: {adapter_path}")
    stages: list[dict] = []
    train = run("train", [
        sys.executable, "scripts/train_qwen_ascension_lora.py",
        "--model", MODEL, "--model-revision", REVISION,
        "--curriculum", "evals/training/aerynza_v20_balanced_master.jsonl",
        "--eval-curriculum", "evals/training/aerynza_v20_ambient_heldout.jsonl",
        "--output-dir", ADAPTER, "--epochs", "2.0", "--learning-rate", "2e-5",
        "--max-length", "768",
    ])
    stages.append(train)
    if train["exit_code"] != 0:
        return finish(stages, "training_failed")

    canonical = run("canonical_gate", [
        sys.executable, "scripts/evaluate_qwen_ascension_lora.py",
        "--model", MODEL, "--model-revision", REVISION, "--adapter", ADAPTER,
        "--tokens", "192", "--output", "evals/results/aerynza_v20_canonical_gate.json",
    ])
    stages.append(canonical)
    if canonical["exit_code"] != 0:
        return finish(stages, "rejected_by_canonical_gate")

    capability = run("capability_gate", [
        sys.executable, "scripts/evaluate_per_capability.py",
        "--model", MODEL, "--model-revision", REVISION, "--adapter", ADAPTER,
        "--tokens", "128", "--output", "evals/results/aerynza_v20_capability_gate.json",
    ])
    stages.append(capability)
    if capability["exit_code"] != 0:
        return finish(stages, "rejected_by_capability_gate")

    execution = run("execution_gate", [
        sys.executable, "scripts/evaluate_capability_execution.py",
        "--model", MODEL, "--model-revision", REVISION, "--adapter", ADAPTER,
        "--tokens", "160", "--output", "evals/results/aerynza_v20_execution_gate.json",
    ])
    stages.append(execution)
    return finish(stages, "awaiting_human_review" if execution["exit_code"] == 0 else "rejected_by_execution_gate")


def finish(stages: list[dict], status: str) -> int:
    receipt = {
        "candidate": "aerynza_qwen3_1_7b_v20_candidate",
        "base_model": MODEL,
        "base_model_revision": REVISION,
        "protected_production_parent": "pro_v19",
        "status": status,
        "stages": stages,
        "automatic_promotion": False,
        "production_replacement_ready": False,
        "human_review_required": status == "awaiting_human_review",
        "completed_at": datetime.now(timezone.utc).isoformat(),
    }
    path = RESULTS / "aerynza_v20_pipeline_receipt.json"
    path.write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    print(json.dumps(receipt, indent=2))
    return 0 if status == "awaiting_human_review" else 2


if __name__ == "__main__":
    raise SystemExit(main())
