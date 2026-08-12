"""
Ascension AI - Elite v3 Training

Native transformer scaled up for GPU. 12 layers, 768 hidden, 256 max length.
Trains on all .md documents in docs/ and the repo root for a larger corpus.
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

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.architecture.transformer import AscensionTransformer, ModelConfig
from src.data.tokenizer import CharTokenizer


def load_docs() -> list[str]:
    root = Path(__file__).resolve().parents[1]
    docs_dir = root / "docs"
    texts = []
    if docs_dir.exists():
        for path in sorted(docs_dir.glob("*.md")):
            try:
                texts.append(path.read_text(encoding="utf-8"))
            except Exception:
                pass
    for path in sorted(root.glob("*.md")):
        try:
            texts.append(path.read_text(encoding="utf-8"))
        except Exception:
            pass
    return texts


def chunk(text: str, size: int, overlap: int = 128) -> list[str]:
    pieces = []
    start = 0
    while start < len(text):
        pieces.append(text[start:start + size])
        start += size - overlap
    return pieces


class TextDataset(Dataset):
    def __init__(self, sequences, length: int = 128):
        self.sequences = []
        for seq in sequences:
            if len(seq) >= length + 1:
                for i in range(0, len(seq) - length - 1, length):
                    self.sequences.append(seq[i:i + length + 1])

    def __len__(self):
        return len(self.sequences)

    def __getitem__(self, idx):
        return torch.tensor(self.sequences[idx], dtype=torch.long)


def get_cosine_schedule_with_warmup(optimizer, warmup_steps: int, total_steps: int):
    def lr_lambda(step):
        if step < warmup_steps:
            return (step + 1) / warmup_steps
        progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
        return 0.5 * (1 + torch.cos(torch.tensor(progress * 3.14159)).item())
    return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)


def main():
    random.seed(42)
    torch.manual_seed(42)

    out_dir = Path("checkpoints")
    out_dir.mkdir(parents=True, exist_ok=True)
    prefix = "ascension_elite_v3"
    model_path = out_dir / f"{prefix}.pt"
    tokenizer_path = out_dir / f"{prefix}_tokenizer.json"
    meta_path = out_dir / f"{prefix}_meta.json"

    docs = load_docs()
    if not docs:
        raise SystemExit("No .md docs found. Add docs before training.")

    corpus = "\n\n".join(docs)
    print(f"Loaded {len(docs)} documents, {len(corpus):,} characters")

    chunks = chunk(corpus, size=1024)
    tokenizer = CharTokenizer(chunks)

    with open(tokenizer_path, "w", encoding="utf-8") as f:
        json.dump({
            "char_to_idx": tokenizer.char_to_idx,
            "idx_to_char": tokenizer.idx_to_char,
            "vocab_size": tokenizer.vocab_size,
        }, f, ensure_ascii=False, indent=2)

    sequences = [tokenizer.encode(c) for c in chunks]
    dataset = TextDataset(sequences, length=128)
    dataloader = DataLoader(dataset, batch_size=16, shuffle=True, drop_last=True)

    config = ModelConfig(
        vocab_size=tokenizer.vocab_size,
        max_length=256,
        num_layers=12,
        num_heads=12,
        hidden_size=768,
        ff_size=2048,
        dropout=0.1,
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AscensionTransformer(config).to(device)
    print(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")

    optimizer = torch.optim.AdamW(model.parameters(), lr=3e-4, weight_decay=0.01, betas=(0.9, 0.95))
    criterion = nn.CrossEntropyLoss()

    num_steps = 5000
    warmup_steps = 250
    scheduler = get_cosine_schedule_with_warmup(optimizer, warmup_steps, num_steps)

    model.train()
    start = time.perf_counter()
    losses = []
    best_loss = float("inf")
    step = 0
    while step < num_steps:
        epoch_loss = 0
        for batch in dataloader:
            if step >= num_steps:
                break
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
            step += 1

        avg = epoch_loss / len(dataloader)
        losses.append(avg)
        if avg < best_loss:
            best_loss = avg
        if (step - 1) % 100 == 0 or step == num_steps:
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
