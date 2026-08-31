"""Generic native checkpoint evaluator with architecture, tokenizer, structural and semantic-proxy gates."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
RUNTIME_ARCHITECTURE = "causal_attention_v2"
RUNTIME_TOKENIZER_CONTRACT = "byte_level_bpe_roundtrip_v1"
MIN_WORDS = 4
MIN_UNIQUE_WORD_RATIO = 0.35
MIN_PRINTABLE_RATIO = 0.98
MAX_HELD_OUT_LOSS = 6.5
PROMPT_TOKEN_OVERLAP_THRESHOLD = 0.6
PROMPT_NGRAM_OVERLAP_THRESHOLD = 0.2
PROMPT_NGRAM_SIZE = 4

DEFAULT_PROMPTS = (
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


def _extract_words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z']+", text)


def _token_set_overlap(prompt: str, text: str) -> float:
    prompt_words = {w.lower() for w in _extract_words(prompt) if len(w) > 2}
    text_words = {w.lower() for w in _extract_words(text) if len(w) > 2}
    if not prompt_words:
        return 0.0
    return len(prompt_words & text_words) / len(prompt_words)


def _ngram_set(tokens: list[str], n: int) -> set[tuple[str, ...]]:
    return {tuple(tokens[i : i + n]) for i in range(max(0, len(tokens) - n + 1))}


def _ngram_overlap(prompt: str, text: str, n: int = PROMPT_NGRAM_SIZE) -> float:
    prompt_tokens = [w.lower() for w in _extract_words(prompt) if len(w) > 2]
    text_tokens = [w.lower() for w in _extract_words(text) if len(w) > 2]
    if len(prompt_tokens) < n:
        return 0.0
    prompt_ngrams = _ngram_set(prompt_tokens, n)
    text_ngrams = _ngram_set(text_tokens, n)
    if not prompt_ngrams:
        return 0.0
    return len(prompt_ngrams & text_ngrams) / len(prompt_ngrams)


def _has_word_fragmentation(text: str) -> bool:
    """Detect decoder word fragmentation such as A S S I S T A N T."""
    return bool(re.search(r"\b(?:[A-Za-z]\s+){4,}[A-Za-z]\b", text))


def _has_role_leak(text: str) -> bool:
    """Detect role or control-label leakage, including letter-spaced variants."""
    if re.search(r"\b(ASSISTANT|USER|ASCENSION\s+SHELL|LESSON\s+TAGS|SHELL)\b", text, re.I):
        return True
    compressed = re.sub(r"\s+", "", text)
    return bool(re.search(r"\b(ASSISTANT|USER|ASCENSIONSHELL|LESSONTAGS|SHELL)\b", compressed, re.I))


def _has_symbol_run(text: str) -> bool:
    """Detect bars, dotted lines, and other symbol runs."""
    if re.search(r"(?:[^\w\s]\s*){12,}", text):
        return True
    if re.search(r"(?:[\|=._-]\s*){8,}", text):
        return True
    if re.search(r"\|{4,}", text):
        return True
    return False


def _has_repeated_phrase(text: str) -> bool:
    """Detect repeated single words or repeated multi-word phrases."""
    if re.search(r"\b(\w+)(?:\s+\1){3,}\b", text, re.I):
        return True
    if re.search(r"(\b\w+(?:\s+\w+){1,3})\b\s+\1", text, re.I):
        return True
    return False


def quality_signals(prompt: str, text: str, min_words: int = MIN_WORDS) -> dict:
    """Return deterministic structural and semantic quality signals for a response."""
    words = _extract_words(text)
    lower_words = [w.lower() for w in words]
    unique_ratio = len(set(lower_words)) / max(len(words), 1)
    printable = sum(1 for c in text if c.isprintable()) / max(len(text), 1)
    token_overlap = _token_set_overlap(prompt, text)
    ngram_overlap = _ngram_overlap(prompt, text)
    word_fragmentation = _has_word_fragmentation(text)
    role_label_leak = _has_role_leak(text)
    symbol_run = _has_symbol_run(text)
    repeated_phrase = _has_repeated_phrase(text)
    prompt_restatement = (
        token_overlap >= PROMPT_TOKEN_OVERLAP_THRESHOLD
        or ngram_overlap >= PROMPT_NGRAM_OVERLAP_THRESHOLD
    )
    empty_or_short = len(words) < min_words
    return {
        "characters": len(text),
        "words": len(words),
        "printable_ratio": round(printable, 4),
        "unique_word_ratio": round(unique_ratio, 4),
        "token_overlap": round(token_overlap, 4),
        "ngram_overlap": round(ngram_overlap, 4),
        "word_fragmentation": word_fragmentation,
        "role_label_leak": role_label_leak,
        "symbol_run": symbol_run,
        "repeated_phrase": repeated_phrase,
        "prompt_restatement": prompt_restatement,
        "empty_or_short": empty_or_short,
    }


def evaluate_text(prompt: str, text: str, min_words: int = MIN_WORDS) -> dict:
    """Evaluate a single generated response against the prompt."""
    signals = quality_signals(prompt, text, min_words=min_words)
    structural_pass = (
        not signals["empty_or_short"]
        and not signals["word_fragmentation"]
        and not signals["role_label_leak"]
        and not signals["symbol_run"]
        and not signals["repeated_phrase"]
        and signals["characters"] > 0
        and signals["printable_ratio"] >= MIN_PRINTABLE_RATIO
    )
    semantic_pass = (
        structural_pass
        and not signals["prompt_restatement"]
        and signals["unique_word_ratio"] >= MIN_UNIQUE_WORD_RATIO
    )
    return {
        "prompt": prompt,
        "text": text,
        "min_words": min_words,
        **signals,
        "structural_pass": structural_pass,
        "semantic_pass": semantic_pass,
    }


def evaluate_response(prompt: str, text: str, min_words: int = MIN_WORDS) -> dict:
    """Return an evaluated response with mandatory human-review and production-safety flags."""
    result = evaluate_text(prompt, text, min_words)
    result["human_review_required"] = True
    result["production_replacement_ready"] = False
    return result


def held_out_loss_gate(loss: float) -> dict:
    """Evaluate a held-out cross-entropy value against the gate threshold."""
    is_finite = math.isfinite(loss)
    return {
        "is_finite": is_finite,
        "pass": is_finite and loss <= MAX_HELD_OUT_LOSS,
        "threshold": MAX_HELD_OUT_LOSS,
    }


def tokenizer_roundtrip(inference) -> dict:
    """Check whether the tokenizer can encode and decode the held-out text exactly."""
    from tokenizers import Tokenizer as HFTokenizer

    if not isinstance(inference.tokenizer, HFTokenizer):
        return {"roundtrip_pass": False, "roundtrip_exact": False, "roundtrip_distance": None}
    ids = inference.tokenizer.encode(HELD_OUT_TEXT).ids
    if len(ids) < 3:
        return {"roundtrip_pass": False, "roundtrip_exact": False, "roundtrip_distance": None}
    decoded = inference.tokenizer.decode(ids)
    exact = decoded == HELD_OUT_TEXT
    token_distance = _token_set_overlap(HELD_OUT_TEXT, decoded)
    return {
        "roundtrip_pass": exact,
        "roundtrip_exact": exact,
        "roundtrip_distance": round(token_distance, 4),
    }


def held_out_loss(inference) -> float:
    """Compute cross-entropy loss on a held-out reference text."""
    from tokenizers import Tokenizer as HFTokenizer
    import torch
    import torch.nn.functional as F

    if not isinstance(inference.tokenizer, HFTokenizer):
        raise ValueError("native evaluation requires the BPE tokenizer")
    ids = inference.tokenizer.encode(HELD_OUT_TEXT).ids[: inference.config.max_length]
    if len(ids) < 3:
        raise ValueError("held-out text produced too few tokens")
    batch = torch.tensor([ids], dtype=torch.long, device=inference.device)
    with torch.no_grad():
        logits = inference.model(batch[:, :-1])
        loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), batch[:, 1:].reshape(-1))
    return float(loss.item())


def checkpoint_metadata_compatible(meta: dict, tokenizer) -> dict:
    """Derive architecture and tokenizer compatibility from checkpoint metadata; fail closed when missing."""
    from tokenizers import Tokenizer as HFTokenizer
    from tokenizers.models import BPE

    architecture = meta.get("architecture")
    architecture_missing = "architecture" not in meta
    architecture_pass = not architecture_missing and architecture == RUNTIME_ARCHITECTURE

    tokenizer_path = meta.get("tokenizer_path")
    tokenizer_path_missing = "tokenizer_path" not in meta or not tokenizer_path
    tokenizer_contract = meta.get("tokenizer_contract")
    tokenizer_contract_missing = not tokenizer_contract
    tokenizer_contract_compatible = tokenizer_contract == RUNTIME_TOKENIZER_CONTRACT
    tokenizer_is_hfbpe = isinstance(tokenizer, HFTokenizer)
    tokenizer_model_is_bpe = tokenizer_is_hfbpe and isinstance(tokenizer.model, BPE)
    tokenizer_pass = (
        not tokenizer_path_missing
        and tokenizer_contract_compatible
        and tokenizer_model_is_bpe
    )

    return {
        "architecture_pass": architecture_pass,
        "architecture_missing": architecture_missing,
        "checkpoint_architecture": architecture,
        "tokenizer_pass": tokenizer_pass,
        "tokenizer_path_missing": tokenizer_path_missing,
        "tokenizer_contract_missing": tokenizer_contract_missing,
        "tokenizer_contract": tokenizer_contract,
        "tokenizer_is_hfbpe": tokenizer_is_hfbpe,
        "tokenizer_model_is_bpe": tokenizer_model_is_bpe,
    }


def _artifact_record(path: Path) -> dict:
    """Return stable evidence for the exact local artifact bytes."""
    if not path.is_file():
        raise FileNotFoundError(f"checkpoint artifact is missing: {path}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"filename": path.name, "bytes": path.stat().st_size, "sha256": digest.hexdigest()}


def checkpoint_artifact_evidence(checkpoint_root: Path, version: str, tokenizer_path: Path) -> dict:
    """Bind an evaluation receipt to its model, metadata, and loaded tokenizer bytes."""
    return {
        "model": _artifact_record(checkpoint_root / f"{version}.pt"),
        "metadata": _artifact_record(checkpoint_root / f"{version}_meta.json"),
        "tokenizer": _artifact_record(tokenizer_path),
    }


def generate_evaluation_samples(inference, prompts: tuple[str, ...], tokens: int) -> tuple[list[dict], list[dict]]:
    """Generate every required sample and retain explicit evidence for individual failures."""
    import torch

    samples = []
    errors = []
    for index, prompt in enumerate(prompts):
        torch.manual_seed(100 + index)
        try:
            generated = inference.generate(prompt, max_new_tokens=tokens, temperature=0.35, top_k=5)
            samples.append(evaluate_text(prompt, generated))
        except Exception as error:
            failure = evaluate_text(prompt, "")
            failure["generation_error"] = f"{type(error).__name__}: {error}"
            samples.append(failure)
            errors.append({"prompt_index": index, "error": failure["generation_error"]})
    return samples, errors


def _recommended_initialization(
    architecture_pass: bool,
    tokenizer_roundtrip_pass: bool,
    automatic_gate_passed: bool,
) -> str:
    """Return the safe next-initialization recommendation; never mark production ready."""
    if not architecture_pass or not tokenizer_roundtrip_pass:
        return "transplant"
    if not automatic_gate_passed:
        return "continue_or_retrain"
    return "resume"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generic native checkpoint evaluator")
    parser.add_argument("--version", default="ascension_elite_general_v5_4h")
    parser.add_argument("--tokens", type=int, default=64)
    parser.add_argument("--output", default="evals/results/native_checkpoint_gate.json")
    # Kept for backwards compatibility, but the gate now derives from checkpoint metadata.
    parser.add_argument("--checkpoint-architecture", default=None)
    args = parser.parse_args(argv)

    from src.architecture.inference import EliteInference

    inference = EliteInference(ROOT / "checkpoints", prefix=args.version)
    artifact_evidence = checkpoint_artifact_evidence(
        ROOT / "checkpoints", args.version, inference.tokenizer_path
    )

    meta_compat = checkpoint_metadata_compatible(inference.meta, inference.tokenizer)
    architecture_pass = meta_compat["architecture_pass"]
    tokenizer_metadata_pass = meta_compat["tokenizer_pass"]

    if tokenizer_metadata_pass:
        roundtrip = tokenizer_roundtrip(inference)
        try:
            loss = held_out_loss(inference)
            held_out_gate = held_out_loss_gate(loss)
        except Exception as error:
            loss = float("nan")
            held_out_gate = held_out_loss_gate(float("nan"))
            held_out_gate["error"] = f"{type(error).__name__}: {error}"
    else:
        roundtrip = {
            "roundtrip_pass": False,
            "roundtrip_exact": False,
            "roundtrip_distance": None,
        }
        loss = float("nan")
        held_out_gate = held_out_loss_gate(float("nan"))
        held_out_gate["error"] = "tokenizer metadata incompatible or missing"

    samples = []
    generation_errors = []
    if tokenizer_metadata_pass and architecture_pass:
        samples, generation_errors = generate_evaluation_samples(inference, DEFAULT_PROMPTS, args.tokens)

    structural_passes = sum(sample["structural_pass"] for sample in samples)
    semantic_passes = sum(sample["semantic_pass"] for sample in samples)
    expected_sample_count = len(DEFAULT_PROMPTS)
    sample_count_pass = len(samples) == expected_sample_count

    automatic_gate_passed = (
        architecture_pass
        and tokenizer_metadata_pass
        and roundtrip["roundtrip_pass"]
        and sample_count_pass
        and not generation_errors
        and structural_passes == expected_sample_count
        and semantic_passes == expected_sample_count
        and held_out_gate["pass"]
    )

    recommended_initialization = _recommended_initialization(
        architecture_pass,
        roundtrip["roundtrip_pass"],
        automatic_gate_passed,
    )

    result = {
        "version": args.version,
        "evaluation_prompt_provenance": "held_out_paraphrases_v2",
        "checkpoint_artifacts": artifact_evidence,
        "checkpoint_metadata": {
            "architecture": meta_compat["checkpoint_architecture"],
            "architecture_missing": meta_compat["architecture_missing"],
            "tokenizer_contract": meta_compat["tokenizer_contract"],
            "tokenizer_contract_missing": meta_compat["tokenizer_contract_missing"],
            "tokenizer_path_missing": meta_compat["tokenizer_path_missing"],
            "tokenizer_is_hfbpe": meta_compat["tokenizer_is_hfbpe"],
            "tokenizer_model_is_bpe": meta_compat["tokenizer_model_is_bpe"],
        },
        "runtime_architecture": RUNTIME_ARCHITECTURE,
        "runtime_tokenizer_contract": RUNTIME_TOKENIZER_CONTRACT,
        "architecture_pass": architecture_pass,
        "tokenizer_metadata_pass": tokenizer_metadata_pass,
        "tokenizer_roundtrip_pass": roundtrip["roundtrip_pass"],
        "tokenizer_roundtrip_exact": roundtrip["roundtrip_exact"],
        "tokenizer_roundtrip_distance": roundtrip["roundtrip_distance"],
        "held_out_loss": round(loss, 4) if held_out_gate["is_finite"] else None,
        "held_out_loss_is_finite": held_out_gate["is_finite"],
        "held_out_loss_pass": held_out_gate["pass"],
        "held_out_loss_error": held_out_gate.get("error"),
        "structural_passes": structural_passes,
        "semantic_passes": semantic_passes,
        "sample_count": len(samples),
        "expected_sample_count": expected_sample_count,
        "sample_count_pass": sample_count_pass,
        "generation_errors": generation_errors,
        "automatic_gate_passed": automatic_gate_passed,
        "recommended_next_initialization": recommended_initialization,
        "human_review_required": True,
        "production_replacement_ready": False,
        "promotion_status": "blocked_pending_full_evaluation",
        "samples": samples,
    }

    output_path = ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if automatic_gate_passed else 2


if __name__ == "__main__":
    import sys
    raise SystemExit(main(sys.argv[1:]))
