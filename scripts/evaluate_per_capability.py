"""Evaluate a Qwen PEFT adapter against every capability in the registry.

This is the second gate after the category gate: it confirms the model can
name and respond to each of the 640 capabilities without hallucinating
completion or switching shells.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.train_qwen_ascension_lora import SYSTEM_PROMPTS, apply_chat_template


def generate(model, tokenizer, shell: str, prompt: str, max_new_tokens: int) -> str:
    import torch

    messages = [
        {"role": "system", "content": SYSTEM_PROMPTS[shell]},
        {"role": "user", "content": prompt},
    ]
    encoded = apply_chat_template(
        tokenizer,
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    )
    if hasattr(encoded, "input_ids"):
        input_ids = encoded.input_ids
    elif isinstance(encoded, dict):
        input_ids = encoded["input_ids"]
    else:
        input_ids = encoded
    input_ids = input_ids.to(next(model.parameters()).device)
    with torch.inference_mode():
        output = model.generate(
            input_ids,
            max_new_tokens=max_new_tokens,
            do_sample=False,
            repetition_penalty=1.08,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    return tokenizer.decode(output[0, input_ids.shape[-1]:], skip_special_tokens=True).strip()


def score_case(case: dict, text: str) -> dict:
    lower = text.lower()
    rubric = case["rubric"]
    scores = []
    for item in rubric:
        score = 1.0
        for p in item.get("positive", []):
            if p.lower() not in lower:
                score -= 0.5
        for n in item.get("negative", []):
            if n.lower() in lower:
                score -= 0.5
        if item["name"].endswith("_shell_aligned"):
            # enforce exact shell prefix; harder failure
            if f"ASCENSION SHELL: {case['shell']}" not in text:
                score = 0.0
        scores.append(max(0.0, min(1.0, score)))
    avg = sum(scores) / len(scores) if scores else 0.0
    return {
        "case_id": case["id"],
        "shell": case["shell"],
        "passed": avg >= case["pass_threshold"],
        "score": round(avg, 3),
        "response": text,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate an adapter on 640 capabilities")
    parser.add_argument("--model", default="Qwen/Qwen3-1.7B")
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--tokens", type=int, default=128)
    parser.add_argument("--output", default="evals/results/per_capability_gate.json")
    parser.add_argument("--capability-gates", default="evals/per_capability_gates.json")
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

    gates = json.loads((ROOT / args.capability_gates).read_text("utf-8"))
    cases = gates["cases"]

    results = []
    for case in cases:
        try:
            text = generate(model, tokenizer, case["shell"], case["user"], args.tokens)
        except Exception as error:
            text = ""
        results.append(score_case(case, text))

    passed = sum(1 for r in results if r["passed"])
    report = {
        "base_model": args.model,
        "adapter": args.adapter,
        "capability_gate_version": gates.get("version", 1),
        "total_capabilities": len(results),
        "passed": passed,
        "pass_rate": round(passed / len(results) if results else 0.0, 4),
        "production_replacement_ready": False,
        "human_review_required": True,
        "results": results,
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"passed": passed, "total": len(results), "pass_rate": report["pass_rate"]}, ensure_ascii=False))
    return 0 if passed == len(results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
