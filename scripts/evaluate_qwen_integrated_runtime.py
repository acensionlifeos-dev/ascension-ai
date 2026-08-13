"""Evaluate the exact user-facing result after deterministic runtime guards."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.evaluate_native_checkpoint import DEFAULT_PROMPTS, evaluate_text
from scripts.evaluate_qwen_ascension_lora import directory_sha256, generate
from scripts.receipt_truth_training_eval import evaluate_response
from src.core.cognition import build_cognitive_packet
from src.core.orchestrator import enforce_response_contract


def guarded(raw: str, prompt: str) -> str:
    cognition = build_cognitive_packet(prompt, {}, [], [])
    return enforce_response_contract(raw, cognition, {}, "conversation", prompt)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Gate an adapter through the Ascension runtime")
    parser.add_argument("--model", default="Qwen/Qwen3-1.7B")
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--tokens", type=int, default=128)
    parser.add_argument("--output", default="evals/results/qwen_integrated_runtime_gate.json")
    args = parser.parse_args(argv)

    import torch
    from peft import PeftModel
    from transformers import AutoModelForCausalLM, AutoTokenizer

    adapter_path = ROOT / args.adapter
    tokenizer = AutoTokenizer.from_pretrained(adapter_path)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    base = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=torch.bfloat16 if torch.cuda.is_available() else torch.float32,
        attn_implementation="sdpa",
        device_map="auto" if torch.cuda.is_available() else None,
    )
    model = PeftModel.from_pretrained(base, adapter_path)
    model.eval()

    canonical_results = []
    for prompt in DEFAULT_PROMPTS:
        raw = generate(model, tokenizer, "ap", prompt, args.tokens)
        final = guarded(raw, prompt)
        result = evaluate_text(prompt, final)
        result["raw_model_text"] = raw
        canonical_results.append(result)

    cases = json.loads((ROOT / "evals" / "receipt_truth_prompts.json").read_text("utf-8"))
    receipt_results = []
    for case in cases:
        raw = generate(model, tokenizer, case["shell"], case["prompt"], args.tokens)
        final = guarded(raw, case["prompt"])
        result = evaluate_response(case, final)
        result["raw_model_text"] = raw
        receipt_results.append(result)

    canonical_passed = all(
        item["structural_pass"] and item["semantic_pass"] for item in canonical_results
    )
    receipt_passed = all(item["passed"] for item in receipt_results)
    automatic_gate_passed = canonical_passed and receipt_passed
    report = {
        "base_model": args.model,
        "adapter": args.adapter,
        "adapter_sha256": directory_sha256(adapter_path),
        "gate": "qwen_ascension_integrated_runtime_v1",
        "canonical_passed": canonical_passed,
        "canonical_pass_count": sum(
            item["structural_pass"] and item["semantic_pass"] for item in canonical_results
        ),
        "canonical_case_count": len(canonical_results),
        "receipt_truth_passed": receipt_passed,
        "receipt_truth_pass_count": sum(item["passed"] for item in receipt_results),
        "receipt_truth_case_count": len(receipt_results),
        "automatic_gate_passed": automatic_gate_passed,
        "human_review_required": True,
        "production_replacement_ready": False,
        "promotion_status": "blocked_pending_human_review_and_integration_load_tests",
        "canonical_results": canonical_results,
        "receipt_truth_results": receipt_results,
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if automatic_gate_passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
