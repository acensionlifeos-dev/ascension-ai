"""Deterministic unit tests for the native checkpoint evaluator text-quality gates."""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.evaluate_native_checkpoint import (
    evaluate_response,
    held_out_loss_gate,
    quality_signals,
    _recommended_initialization,
)
from scripts.evaluate_v5_checkpoint import _v5_argv


def test_spaced_assistant_letters():
    """Spaced letters in ASSISTANT should trigger word fragmentation and role-label leak."""
    prompt = "What is the next step?"
    text = "A S S I S T A N T: here is your answer."
    result = evaluate_response(prompt, text)
    assert result["word_fragmentation"] is True
    assert result["role_label_leak"] is True
    assert result["structural_pass"] is False
    assert result["human_review_required"] is True
    assert result["production_replacement_ready"] is False


def test_repeated_phrase():
    """The classic v6 repetition pattern should be rejected."""
    prompt = "What do you do?"
    text = "What do you do do you do?"
    result = evaluate_response(prompt, text)
    assert result["repeated_phrase"] is True
    assert result["structural_pass"] is False


def test_symbol_bars():
    """A symbol bar run should fail structural and short-answer checks."""
    prompt = "What is your plan?"
    text = "||||||||||"
    result = evaluate_response(prompt, text)
    assert result["symbol_run"] is True
    assert result["empty_or_short"] is True
    assert result["structural_pass"] is False


def test_near_prompt_restatement():
    """Near-verbatim restatement of the prompt should fail the semantic proxy."""
    prompt = "My balance is low and payday is Friday. Help me think."
    text = "Your balance is low and your payday is Friday, so I will think about a plan."
    result = evaluate_response(prompt, text)
    assert result["prompt_restatement"] is True
    assert result["semantic_pass"] is False


def test_clean_natural_response():
    """A clean, natural response should pass structural and semantic gates."""
    prompt = "Tell me about your morning."
    text = "I walked by the river for an hour and then read a book on the porch."
    result = evaluate_response(prompt, text)
    assert result["structural_pass"] is True
    assert result["semantic_pass"] is True
    assert result["human_review_required"] is True
    assert result["production_replacement_ready"] is False


def test_empty_response():
    """Empty output must be rejected."""
    result = evaluate_response("hello", "")
    assert result["empty_or_short"] is True
    assert result["structural_pass"] is False


def test_too_short_response():
    """Sub-word-count output must be rejected."""
    result = evaluate_response("hello", "Yes.")
    assert result["empty_or_short"] is True
    assert result["structural_pass"] is False


def test_repeated_word_run():
    """A repeated single word run should be detected."""
    result = evaluate_response("hello", "The the the the the the.")
    assert result["repeated_phrase"] is True
    assert result["structural_pass"] is False


def test_role_label_leak_without_fragmentation():
    """Plain role or control labels should be rejected even without spacing."""
    result = evaluate_response("What can you do?", "ASCENSION SHELL: this is the answer.")
    assert result["role_label_leak"] is True
    assert result["structural_pass"] is False


def test_min_words_threshold():
    """The min_words argument must be wired through quality_signals and empty_or_short."""
    prompt = "hello"
    text = "I walked."
    result_default = evaluate_response(prompt, text)
    assert result_default["min_words"] == 4
    result_high = evaluate_response(prompt, text, min_words=3)
    assert result_high["empty_or_short"] is True
    assert result_high["structural_pass"] is False
    result_low = evaluate_response(prompt, text, min_words=1)
    assert result_low["empty_or_short"] is False


def test_quality_signals_report_all_fields():
    """Every text evaluation must report the expected signal fields."""
    prompt = "hello"
    text = "I am a reasonably natural response with a few words."
    signals = quality_signals(prompt, text)
    expected = {
        "characters",
        "words",
        "printable_ratio",
        "unique_word_ratio",
        "token_overlap",
        "ngram_overlap",
        "word_fragmentation",
        "role_label_leak",
        "symbol_run",
        "repeated_phrase",
        "prompt_restatement",
        "empty_or_short",
    }
    assert expected.issubset(signals.keys())
    assert all(isinstance(signals[k], (int, float, bool)) for k in expected)


def test_held_out_loss_gate():
    """The held-out loss gate must distinguish finite, NaN, and infinite values."""
    below = held_out_loss_gate(3.0)
    assert below["is_finite"] is True
    assert below["pass"] is True

    above = held_out_loss_gate(10.0)
    assert above["is_finite"] is True
    assert above["pass"] is False

    nan = held_out_loss_gate(float("nan"))
    assert nan["is_finite"] is False
    assert nan["pass"] is False

    inf = held_out_loss_gate(float("inf"))
    assert inf["is_finite"] is False
    assert inf["pass"] is False

    negative_inf = held_out_loss_gate(float("-inf"))
    assert negative_inf["is_finite"] is False
    assert negative_inf["pass"] is False


def test_roundtrip_contract_is_literal():
    """The evaluator source must not normalize away tokenizer whitespace loss."""
    source = (Path(__file__).resolve().parent / "evaluate_native_checkpoint.py").read_text(encoding="utf-8")
    assert "decoded == HELD_OUT_TEXT" in source
    assert "decoded.strip() == HELD_OUT_TEXT.strip()" not in source


def test_recommended_initialization():
    """The safe next-initialization recommendation depends on architecture, tokenizer, and quality."""
    assert _recommended_initialization(True, True, True) == "resume"
    assert _recommended_initialization(False, True, False) == "transplant"
    assert _recommended_initialization(True, False, False) == "transplant"
    assert _recommended_initialization(True, True, False) == "continue_or_retrain"


def test_v5_wrapper_preserves_arguments():
    """The v5 wrapper injects missing defaults while preserving explicit caller arguments."""
    merged = _v5_argv(["--version", "custom_v5"])
    assert "--version" in merged
    assert "custom_v5" in merged
    assert merged.count("--version") == 1
    assert "--output" in merged


def test_v5_wrapper_injects_defaults():
    """The v5 wrapper supplies the canonical v5 defaults when none are given."""
    merged = _v5_argv([])
    assert merged == [
        "--version",
        "ascension_elite_general_v5_4h",
        "--output",
        "evals/results/v5_checkpoint_gate.json",
    ]


def main() -> int:
    tests = [fn for name, fn in globals().items() if name.startswith("test_")]
    for test in tests:
        test()
        print(f"PASS {test.__name__}")
    print("PASS all native checkpoint evaluator unit tests")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
