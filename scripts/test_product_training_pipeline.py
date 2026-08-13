"""Fast CPU smoke test for the gated Ascension product training pipeline."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import torch
import torch.nn.functional as F
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.trainers import BpeTrainer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_ascension_product_corpus import build_corpus
from scripts.train_ascension_product_v6 import (
    TokenizedDataset,
    initialize_model,
    load_base,
    save_checkpoint,
)
from src.architecture.transformer import AscensionTransformer, ModelConfig


def main() -> int:
    torch.manual_seed(11)
    with tempfile.TemporaryDirectory(prefix="ascension-product-smoke-") as directory:
        root = Path(directory)
        prefix = "tiny_base"
        corpus_path = root / "product.txt"
        manifest = build_corpus(corpus_path, product_repeats=1, general_replay_ratio=0)
        if manifest["example_count"] < 30 or manifest["contains_private_user_data"]:
            raise AssertionError("product corpus provenance contract failed")

        tokenizer = Tokenizer(BPE(unk_token="<unk>"))
        tokenizer.pre_tokenizer = Whitespace()
        tokenizer.train_from_iterator(
            [corpus_path.read_text(encoding="utf-8")],
            BpeTrainer(vocab_size=256, special_tokens=["<pad>", "<unk>", "<s>", "</s>"]),
        )
        tokenizer_path = root / f"{prefix}_tokenizer.json"
        tokenizer.save(str(tokenizer_path))
        config = ModelConfig(
            vocab_size=tokenizer.get_vocab_size(),
            max_length=64,
            num_layers=1,
            num_heads=2,
            hidden_size=16,
            ff_size=32,
            dropout=0.0,
        )
        base_model = AscensionTransformer(config)
        save_checkpoint(root / f"{prefix}.pt", {
            "model_state_dict": base_model.state_dict(),
            "optimizer_state_dict": {},
            "config": config,
            "losses": [],
        })
        (root / f"{prefix}_meta.json").write_text(json.dumps({
            "tokenizer_path": str(tokenizer_path),
            "config": config.__dict__,
            "final_loss": None,
        }), encoding="utf-8")

        checkpoint, meta, loaded_tokenizer = load_base(root, prefix)
        if loaded_tokenizer != tokenizer_path or meta["config"]["max_length"] != 64:
            raise AssertionError("base artifact contract failed")
        model, details = initialize_model(config, checkpoint, "transplant")
        if not details["reinitialized_attention"] or details["reused_tensors"] <= 0:
            raise AssertionError("attention-safe transplant contract failed")

        ids = tokenizer.encode(corpus_path.read_text(encoding="utf-8")).ids
        dataset = TokenizedDataset(ids, length=32)
        batch = dataset[0].unsqueeze(0)
        logits = model(batch[:, :-1])
        loss = F.cross_entropy(logits.reshape(-1, logits.size(-1)), batch[:, 1:].reshape(-1))
        loss.backward()
        if not torch.isfinite(loss):
            raise AssertionError("product training smoke loss is not finite")

    print("PASS reviewed product corpus provenance")
    print("PASS base checkpoint and tokenizer loading")
    print("PASS attention-safe weight transplant")
    print("PASS causal product training step")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
