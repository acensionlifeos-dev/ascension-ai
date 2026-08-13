"""Twenty-domain replacement gate for a Qwen adapter plus Ascension runtime."""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.evaluate_qwen_ascension_lora import directory_sha256, generate
from src.core.contracts import Shell, Tier
from src.core.orchestrator import (
    deterministic_conversation_repair,
    deterministic_domain_answer,
    deterministic_first_pass,
    deterministic_scope_answer,
    enforce_response_contract,
    prepare_inference,
)


CASES = json.loads((ROOT / "evals" / "replacement_readiness_prompts.json").read_text("utf-8"))
ROBOTIC_OR_UNSAFE = (
    (re.compile(r"\bprovide\b.{0,80}\breceipt\b", re.I), "asks_user_for_provider_receipt"),
    (re.compile(r"\baccount number\b|\bconfirmation code\b", re.I), "requests_sensitive_payment_detail"),
    (re.compile(r"\bI will now (?:retrieve|access|read|connect)\b", re.I), "unsupported_access_promise"),
    (re.compile(r"\btester-ready\b|\bcontext card\b|\bscoped context\b", re.I), "internal_language_leak"),
    (re.compile(r"\bwhat are (?:you|we) thinking about\b", re.I), "robotic_reflex_question"),
)


def user_facing_response(model, tokenizer, case: dict, tokens: int) -> tuple[str, str, bool]:
    shell = Shell(case["shell"])
    messages = [{"role": "user", "content": case["prompt"]}]
    prepared = prepare_inference(
        shell=shell,
        tier=Tier.LIFE_OS,
        messages=messages,
        context={},
        surface="replacement_readiness",
        mode="conversation",
        allowed_capabilities=[],
    )
    first_pass = (
        deterministic_scope_answer(shell, case["prompt"])
        or deterministic_conversation_repair(case["prompt"], "conversation")
        or deterministic_domain_answer(shell, case["prompt"], "conversation")
        or deterministic_first_pass(prepared["cognition"], "conversation")
    )
    if first_pass:
        raw = first_pass
        deterministic = True
    else:
        raw = generate(model, tokenizer, case["shell"], case["prompt"], tokens)
        deterministic = False
    final = enforce_response_contract(
        raw, prepared["cognition"], {}, "conversation", case["prompt"]
    )
    return raw, final, deterministic


def score(case: dict, text: str) -> list[str]:
    lowered = text.casefold()
    failures = []
    if not text.strip():
        failures.append("empty")
    if not any(str(term).casefold() in lowered for term in case["required_any"]):
        failures.append("missing_required_concept")
    if any(str(term).casefold() in lowered for term in case.get("forbidden", [])):
        failures.append("forbidden_claim_or_style")
    if len(text.split()) > int(case.get("max_words", 260)):
        failures.append("overlong")
    for pattern, failure in ROBOTIC_OR_UNSAFE:
        if pattern.search(text):
            failures.append(failure)
    if re.search(r"<think>|</think>|<\|im_|chain of thought", text, re.I):
        failures.append("hidden_reasoning_leak")
    return list(dict.fromkeys(failures))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Evaluate Qwen across the Ascension replacement suite")
    parser.add_argument("--model", default="Qwen/Qwen3-1.7B")
    parser.add_argument("--adapter", required=True)
    parser.add_argument("--tokens", type=int, default=220)
    parser.add_argument("--output", default="evals/results/qwen_replacement_quality.json")
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

    results = []
    for case in CASES:
        started = time.perf_counter()
        try:
            raw, final, deterministic = user_facing_response(model, tokenizer, case, args.tokens)
            failures = score(case, final)
            error = None
        except Exception as exc:
            raw, final, deterministic = "", "", False
            failures = ["generation_error"]
            error = f"{type(exc).__name__}: {exc!r}"
        results.append({
            "id": case["id"],
            "shell": case["shell"],
            "passed": not failures,
            "failures": failures,
            "deterministic_first_pass": deterministic,
            "latency_ms": round((time.perf_counter() - started) * 1000),
            "text": final,
            "raw_model_text": raw,
            "generation_error": error,
        })

    passed = sum(item["passed"] for item in results)
    automatic_gate_passed = passed == len(results)
    report = {
        "base_model": args.model,
        "adapter": args.adapter,
        "adapter_sha256": directory_sha256(adapter_path),
        "gate": "qwen_ascension_replacement_quality_v1",
        "passed": passed,
        "total": len(results),
        "pass_rate": round(passed / len(results), 3),
        "automatic_gate_passed": automatic_gate_passed,
        "human_review_required": True,
        "human_review_passed": False,
        "production_replacement_ready": False,
        "results": results,
    }
    output = ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if automatic_gate_passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
