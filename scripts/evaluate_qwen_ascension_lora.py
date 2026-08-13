"""Fail-closed conversational and receipt-truth gate for a Qwen PEFT adapter."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.evaluate_native_checkpoint import DEFAULT_PROMPTS, evaluate_text
from scripts.receipt_truth_training_eval import evaluate_response
from scripts.train_qwen_ascension_lora import SYSTEM_PROMPTS, apply_chat_template


def directory_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    for file in sorted(item for item in path.rglob("*") if item.is_file()):
        digest.update(file.relative_to(path).as_posix().encode("utf-8"))
        digest.update(b"\0")
        with file.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    return digest.hexdigest()


def generate(model: Any, tokenizer: Any, shell: str, prompt: str, max_new_tokens: int) -> str:
    import torch

    messages = [
        {"role": "system", "content": SYSTEM_PROMPTS[shell]},
        {"role": "user", "content": prompt},
    ]
    input_ids = apply_chat_template(
        tokenizer,
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    ).to(model.device)
    with torch.inference_mode():
        output = model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            repetition_penalty=1.08,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    return tokenizer.decode(output[0, input_ids.shape[-1] :], skip_special_tokens=True).strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate an Ascension Qwen adapter")
    parser.add_argument("--model", default="Qwen/Qwen3-0.6B")
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--tokens", type=int, default=128)
    parser.add_argument("--output", default="evals/results/qwen_adapter_gate.json")
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
        try:
            text = generate(model, tokenizer, "ap", prompt, args.tokens)
            canonical_results.append(evaluate_text(prompt, text))
        except Exception as error:
            result = evaluate_text(prompt, "")
            result["generation_error"] = f"{type(error).__name__}: {error}"
            canonical_results.append(result)

    receipt_cases = json.loads((ROOT / "evals" / "receipt_truth_prompts.json").read_text("utf-8"))
    receipt_results = []
    for case in receipt_cases:
        try:
            text = generate(model, tokenizer, case["shell"], case["prompt"], args.tokens)
            receipt_results.append(evaluate_response(case, text))
        except Exception as error:
            result = evaluate_response(case, "")
            result["generation_error"] = f"{type(error).__name__}: {error}"
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
        "gate": "qwen_ascension_adapter_v1",
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
        "promotion_status": "blocked_pending_human_review",
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
