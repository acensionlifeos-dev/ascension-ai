"""Evaluate a completed native checkpoint before choosing the next package."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

import torch
import torch.nn.functional as F
from tokenizers import Tokenizer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.architecture.inference import EliteInference


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ARCHITECTURE = "causal_attention_v2"
DEFAULT_CHECKPOINT_ARCHITECTURE = "legacy_noncausal_attention_v1"
PROMPTS = (
    "I do not need a plan tonight; sit with me for a minute.",
    "My shifts start at 9:45 p.m. Thursday through Monday and end at 5:30 a.m. Tuesday and Wednesday are off. Repeat that without saving it.",
    "My balance is low, the phone bill clears tomorrow, and payday is two days later. Help me think without moving money.",
    "I keep circling an idea for a neighborhood tool library. Help me shape the first version.",
    "What can you do when I ask to schedule something but there is no calendar receipt?",
    "We are discussing family roles. Stay quiet unless someone asks Nexus directly.",
)
HELD_OUT_TEXT = (
    "USER: I changed my schedule. ASSISTANT: I can reflect the change, but I will not claim it was saved "
    "until the authenticated shell records it and returns a receipt."
)


def held_out_loss(inference: EliteInference) -> float:
    if not isinstance(inference.tokenizer, Tokenizer):
        raise ValueError("v5 evaluation requires the BPE tokenizer")
    ids = inference.tokenizer.encode(HELD_OUT_TEXT).ids[: inference.config.max_length]
    if len(ids) < 3:
        raise ValueError("held-out text produced too few tokens")
    batch = torch.tensor([ids], dtype=torch.long, device=inference.device)
    with torch.no_grad():
        logits = inference.model(batch[:, :-1])
        loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), batch[:, 1:].reshape(-1))
    return float(loss.item())


def quality_signals(prompt: str, text: str) -> dict:
    printable = sum(character.isprintable() for character in text) / max(len(text), 1)
    words = re.findall(r"[A-Za-z']+", text)
    unique_ratio = len({word.lower() for word in words}) / max(len(words), 1)
    repeated_run = bool(re.search(r"\b(\w+)(?:\s+\1){4,}\b", text, re.I))
    prompt_echo = text.lower().strip().startswith(prompt.lower().strip())
    symbol_run = bool(re.search(r"(?:[=._-]\s*){8,}", text))
    return {
        "characters": len(text),
        "words": len(words),
        "printable_ratio": round(printable, 4),
        "unique_word_ratio": round(unique_ratio, 4),
        "repeated_run": repeated_run,
        "prompt_echo": prompt_echo,
        "symbol_run": symbol_run,
        "structural_pass": (
            len(words) >= 4
            and printable >= 0.98
            and unique_ratio >= 0.35
            and not repeated_run
            and not prompt_echo
            and not symbol_run
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Gate a native v5 checkpoint")
    parser.add_argument("--version", default="ascension_elite_general_v5_4h")
    parser.add_argument("--tokens", type=int, default=64)
    parser.add_argument("--output", default="evals/results/v5_checkpoint_gate.json")
    parser.add_argument("--checkpoint-architecture", default=DEFAULT_CHECKPOINT_ARCHITECTURE)
    args = parser.parse_args()
    inference = EliteInference(ROOT / "checkpoints", prefix=args.version)
    samples = []
    for index, prompt in enumerate(PROMPTS):
        torch.manual_seed(100 + index)
        generated = inference.generate(prompt, max_new_tokens=args.tokens, temperature=0.35, top_k=5)
        samples.append({"prompt": prompt, "generated": generated, **quality_signals(prompt, generated)})
    loss = held_out_loss(inference)
    structural_passes = sum(bool(sample["structural_pass"]) for sample in samples)
    quality_gate_passed = structural_passes == len(samples) and math.isfinite(loss) and loss <= 6.5
    architecture_compatible = args.checkpoint_architecture == RUNTIME_ARCHITECTURE
    gate_passed = quality_gate_passed and architecture_compatible
    result = {
        "version": args.version,
        "evaluation_prompt_provenance": "held_out_paraphrases_v2",
        "checkpoint_training_architecture": args.checkpoint_architecture,
        "runtime_architecture": RUNTIME_ARCHITECTURE,
        "architecture_compatible_for_resume": architecture_compatible,
        "held_out_loss": round(loss, 4),
        "structural_passes": structural_passes,
        "sample_count": len(samples),
        "automatic_gate_passed": gate_passed,
        "quality_gate_passed": quality_gate_passed,
        "human_review_required": True,
        "next_initialization": "resume" if gate_passed else "transplant",
        "samples": samples,
        "promotion_status": "blocked_pending_full_evaluation",
    }
    output_path = ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if gate_passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
