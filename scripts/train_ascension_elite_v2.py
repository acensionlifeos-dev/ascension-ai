"""
Ascension AI - Elite v2 Training

Larger native transformer than the seed/elite v1. Still CPU-runnable but
produces a more capable checkpoint. Ideal for overnight or GPU runs.
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


def load_docs() -> list[str]:
    docs_dir = Path(__file__).resolve().parents[1] / "docs"
    if not docs_dir.exists():
        return []
    texts = []
    for path in docs_dir.glob("*.md"):
        texts.append(path.read_text(encoding="utf-8"))
    return texts


def chunk(text: str, size: int, overlap: int = 64) -> list[str]:
    pieces = []
    start = 0
    while start < len(text):
        pieces.append(text[start:start + size])
        start += size - overlap
    return pieces


class TextDataset(Dataset):
    def __init__(self, sequences, length: int = 64):
        self.sequences = []
        for seq in sequences:
            if len(seq) >= length + 1:
                for i in range(0, len(seq) - length - 1, length):
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
    model_path = out_dir / "ascension_elite_v2.pt"
    tokenizer_path = out_dir / "ascension_elite_v2_tokenizer.json"
    meta_path = out_dir / "ascension_elite_v2_meta.json"

    docs = load_docs()
    if not docs:
        raise SystemExit("No docs found. Add .md files to docs/ before training.")

    corpus = "\n\n".join(docs)
    chunks = chunk(corpus, size=512)
    tokenizer = CharTokenizer(chunks)

    with open(tokenizer_path, "w", encoding="utf-8") as f:
        json.dump({
            "char_to_idx": tokenizer.char_to_idx,
            "idx_to_char": tokenizer.idx_to_char,
            "vocab_size": tokenizer.vocab_size
        }, f, ensure_ascii=False, indent=2)

    sequences = [tokenizer.encode(c) for c in chunks]
    dataset = TextDataset(sequences, length=64)
    dataloader = DataLoader(dataset, batch_size=8, shuffle=True)

    # Larger v2 config: 6 layers, 256 hidden, 1024 ff
    config = ModelConfig(
        vocab_size=tokenizer.vocab_size,
        max_length=128,
        num_layers=6,
        num_heads=8,
        hidden_size=256,
        ff_size=1024,
        dropout=0.1,
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AscensionTransformer(config).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01)
    criterion = nn.CrossEntropyLoss()

    num_steps = 500
    def lr_lambda(step):
        return max(0.05, 1.0 - step / num_steps)
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)

    model.train()
    start = time.perf_counter()
    losses = []
    best_loss = float('inf')
    for step in range(num_steps):
        epoch_loss = 0
        for batch in dataloader:
            batch = batch.to(device)
            input_ids = batch[:, :-1]
            targets = batch[:, 1:]
            logits = model(input_ids)
            loss = criterion(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
            optimizer.zero_grad()
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            epoch_loss += loss.item()
        avg = epoch_loss / len(dataloader)
        losses.append(avg)
        if avg < best_loss:
            best_loss = avg
        if step % 50 == 0:
            print(f"Step {step}/{num_steps} loss: {avg:.4f}")

    elapsed = time.perf_counter() - start
    print(f"Training complete in {elapsed:.2f}s best loss: {best_loss:.4f} final loss: {losses[-1]:.4f}")

    with torch.serialization.safe_globals([ModelConfig]):
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
            "best_loss": best_loss,
            "train_seconds": elapsed,
            "device": device,
            "num_steps": num_steps,
            "docs_trained": len(docs),
            "corpus_chars": len(corpus),
        }, f, ensure_ascii=False, indent=2)

    print(f"Checkpoint saved to {model_path}")
    print(f"Tokenizer saved to {tokenizer_path}")
    print(f"Metadata saved to {meta_path}")


if __name__ == "__main__":
    main()
