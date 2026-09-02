"""Bounded wait for a completed smoke adapter, then evaluate without promotion."""
import json
import time
from pathlib import Path
import torch
import evaluate_qwen_ascension_lora as evaluator


def main():
    adapter = "checkpoints/qwen_recovery_smoke_20260831"
    output = "evals/results/qwen_recovery_smoke_20260831_gate.json"
    if (evaluator.ROOT / output).exists():
        raise FileExistsError("Preserve existing evaluation")
    receipt_path = evaluator.ROOT / adapter / "ascension_training_receipt.json"
    deadline = time.monotonic() + 1800
    print("Waiting up to 30 minutes for completed training receipt", flush=True)
    while not receipt_path.exists():
        if time.monotonic() >= deadline:
            raise TimeoutError("No completed training receipt; evaluation not started")
        time.sleep(5)
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if receipt.get("status") != "trained_not_promoted" or receipt.get("production_replacement_ready") is not False:
        raise ValueError("Unexpected training receipt")
    base = Path(receipt["base_model"])
    if base.name != "c1899de289a04d12100db370d81485cdf75e47ca" or not base.is_dir():
        raise ValueError("Training did not use the expected pinned base")
    torch.set_num_threads(4)
    print("Training complete; evaluating canonical and receipt-truth cases", flush=True)
    return evaluator.main(["--model", str(base), "--adapter", adapter, "--tokens", "128", "--output", output])


if __name__ == "__main__":
    raise SystemExit(main())
