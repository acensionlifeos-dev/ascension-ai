"""
Ascension AI - Seed Training

Trains a tiny Ascension-native transformer on a synthetic seed corpus to prove
the custom training and checkpoint pipeline. This is intentionally small so it
finishes in seconds on CPU. Real production runs use train.py / train_distributed.py.
"""

from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

# Ensure src/ is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.architecture.transformer import AscensionTransformer, ModelConfig
from src.data.tokenizer import CharTokenizer


SEED_CORPUS = [
    "Ascension AI is a personal intelligence for human improvement.",
    "AP helps one person at a time with privacy and permission.",
    "NexusHome coordinates household and co-parenting plans.",
    "NexusFamily supports family enterprise and shared records.",
    "Understanding is not saving. A proposal is not execution.",
    "AP asks for permissions it needs to improve its usefulness.",
    "The native model runs locally and keeps user data private.",
    "Ascension replaces outside AI only when every replacement gate is proven.",
    "Health guidance must not become diagnosis.",
    "Financial intelligence must not make unsupported guarantees.",
]


def load_docs() -> list[str]:
    docs_dir = Path(__file__).resolve().parents[1] / "docs"
    if not docs_dir.exists():
        return []
    texts = []
    for path in docs_dir.glob("*.md"):
        texts.append(path.read_text(encoding="utf-8"))
    return texts


def augment(text: str) -> str:
    # Keep it simple: repeat to make a longer training example
    return text + " " + text


class TextDataset(Dataset):
    def __init__(self, sequences, length: int = 32):
        self.sequences = []
        for seq in sequences:
            if len(seq) >= length + 1:
                for i in range(0, len(seq) - length - 1, 8):
                    self.sequences.append(seq[i:i + length + 1])

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        return torch.tensor(self.sequences[idx], dtype=torch.long)


def main():
    random.seed(42)
    torch.manual_seed(42)

    out_dir = Path("checkpoints")
    out_dir.mkdir(parents=True, exist_ok=True)
    model_path = out_dir / "ascension_seed.pt"
    tokenizer_path = out_dir / "ascension_seed_tokenizer.json"
    meta_path = out_dir / "ascension_seed_meta.json"

    texts = [augment(t) for t in SEED_CORPUS]
    docs = load_docs()
    texts.extend(docs)
    tokenizer = CharTokenizer(texts)

    # Save tokenizer
    with open(tokenizer_path, "w", encoding="utf-8") as f:
        json.dump({
            "char_to_idx": tokenizer.char_to_idx,
            "idx_to_char": tokenizer.idx_to_char,
            "vocab_size": tokenizer.vocab_size
        }, f, ensure_ascii=False, indent=2)

    sequences = [tokenizer.encode(t) for t in texts]
    dataset = TextDataset(sequences, length=32)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

    # Tiny config for seconds-long CPU training
    config = ModelConfig(
        vocab_size=tokenizer.vocab_size,
        max_length=64,
        num_layers=2,
        num_heads=2,
        hidden_size=64,
        ff_size=128,
        dropout=0.1,
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AscensionTransformer(config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=5e-4)
    criterion = nn.CrossEntropyLoss()

    model.train()
    start = time.perf_counter()
    num_steps = 50
    losses = []
    for step in range(num_steps):
        for batch in dataloader:
            batch = batch.to(device)
            input_ids = batch[:, :-1]
            targets = batch[:, 1:]
            logits = model(input_ids)
            loss = criterion(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        losses.append(loss.item())
        if step % 10 == 0:
            print(f"Step {step}/{num_steps} loss: {loss.item():.4f}")

    elapsed = time.perf_counter() - start
    print(f"Training complete in {elapsed:.2f}s final loss: {losses[-1]:.4f}")

    torch.save({
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "config": config,
        "losses": losses,
    }, model_path)

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump({
            "model_path": str(model_path),
            "tokenizer_path": str(tokenizer_path),
            "config": config.__dict__,
            "final_loss": losses[-1],
            "train_seconds": elapsed,
            "device": device,
            "num_steps": num_steps,
        }, f, ensure_ascii=False, indent=2)

    print(f"Checkpoint saved to {model_path}")
    print(f"Tokenizer saved to {tokenizer_path}")
    print(f"Metadata saved to {meta_path}")


if __name__ == "__main__":
    main()
