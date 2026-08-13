"""Regression checks for the native training transformer's causal attention."""

from __future__ import annotations

import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.architecture.transformer import AscensionTransformer, ModelConfig


def main() -> int:
    torch.manual_seed(7)
    config = ModelConfig(
        vocab_size=64,
        max_length=16,
        num_layers=2,
        num_heads=4,
        hidden_size=32,
        ff_size=64,
        dropout=0.0,
    )
    model = AscensionTransformer(config).eval()

    original = torch.tensor([[1, 2, 3, 4, 5, 6]], dtype=torch.long)
    future_changed = torch.tensor([[1, 2, 3, 4, 19, 27]], dtype=torch.long)
    with torch.no_grad():
        original_logits = model(original)
        changed_logits = model(future_changed)

    # Changing tokens at positions 4-5 must not alter positions 0-3.
    if not torch.allclose(original_logits[:, :4], changed_logits[:, :4], atol=1e-6, rtol=1e-6):
        raise AssertionError("future tokens leaked into earlier causal positions")

    # The changed tokens should still affect their own/later predictions.
    if torch.allclose(original_logits[:, 4:], changed_logits[:, 4:], atol=1e-6, rtol=1e-6):
        raise AssertionError("attention path is not responding to changed input tokens")

    print("PASS causal attention blocks future-token leakage")
    print("PASS attention remains responsive to available context")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
