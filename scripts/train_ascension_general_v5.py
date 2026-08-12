"""
Ascension AI - General English v5 Training

BPE tokenizer on WikiText-103 with configurable steps and vocab size.
Run with default 200,000 steps for the biggest model yet,
or pass --steps for a shorter overnight session.

Examples:
    python -u scripts/train_ascension_general_v5.py
    python -u scripts/train_ascension_general_v5.py --version ascension_elite_general_v5_4h --steps 120000
"""

from __future__ import annotations

import argparse
import json
import random
import re
import sys
import time
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

try:
    from datasets import load_dataset
    from tokenizers import Tokenizer
    from tokenizers.models import BPE
    from tokenizers.pre_tokenizers import Whitespace
    from tokenizers.trainers import BpeTrainer
except ImportError as exc:
    raise SystemExit("Missing 'datasets' or 'tokenizers' library. Run: pip install datasets tokenizers") from exc

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.architecture.transformer import AscensionTransformer, ModelConfig


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train Ascension Elite v5")
    parser.add_argument("--version", default="ascension_elite_general_v5", help="checkpoint prefix")
    parser.add_argument("--steps", type=int, default=200000, help="total training steps")
    parser.add_argument("--vocab_size", type=int, default=8192, help="BPE vocab size")
    parser.add_argument("--print_every", type=int, default=5000, help="log interval")
    parser.add_argument("--batch_size", type=int, default=16, help="batch size")
    return parser.parse_args()


def load_corpus() -> str:
    corpus_path = Path("data/general_corpus_v5.txt")
    if corpus_path.is_file():
        print(f"Loading local general corpus: {corpus_path}")
        return corpus_path.read_text(encoding="utf-8")

    print("Downloading wikitext-103-raw-v1 for general English training...")
    dataset = load_dataset("Salesforce/wikitext", "wikitext-103-raw-v1", split="train")
    texts = [item["text"] for item in dataset if item["text"].strip()]
    raw = "\n\n".join(texts)
    cleaned = "".join(c if (32 <= ord(c) < 127 or c in "\n\t") else " " for c in raw)
    cleaned = re.sub(r" +", " ", cleaned)
    corpus_path.parent.mkdir(parents=True, exist_ok=True)
    corpus_path.write_text(cleaned, encoding="utf-8")
    return cleaned


def build_bpe_tokenizer(corpus: str, vocab_size: int, prefix: str) -> Tokenizer:
    tokenizer_path = Path(f"checkpoints/{prefix}_tokenizer.json")
    if tokenizer_path.is_file():
        print(f"Loading existing BPE tokenizer: {tokenizer_path}")
        return Tokenizer.from_file(str(tokenizer_path))

    print(f"Training BPE tokenizer with vocab size {vocab_size}...")
    tokenizer = Tokenizer(BPE(unk_token="<unk>"))
    tokenizer.pre_tokenizer = Whitespace()
    trainer = BpeTrainer(
        vocab_size=vocab_size,
        special_tokens=["<pad>", "<unk>", "<s>", "</s>"],
    )
    tokenizer.train_from_iterator([corpus], trainer=trainer)
    tokenizer_path.parent.mkdir(parents=True, exist_ok=True)
    tokenizer.save(str(tokenizer_path))
    print(f"Saved BPE tokenizer: {tokenizer_path}")
    return tokenizer


class TokenizedDataset(Dataset):
    def __init__(self, token_ids: list[int], length: int = 256):
        self.token_ids = token_ids
        self.length = length

    def __len__(self) -> int:
        return max(0, len(self.token_ids) - self.length - 1)

    def __getitem__(self, idx: int):
        return torch.tensor(self.token_ids[idx:idx + self.length + 1], dtype=torch.long)


def get_cosine_schedule_with_warmup(optimizer, warmup_steps: int, total_steps: int):
    def lr_lambda(step):
        if step < warmup_steps:
            return (step + 1) / warmup_steps
        progress = (step - warmup_steps) / max(1, total_steps - warmup_steps)
        return 0.5 * (1 + torch.cos(torch.tensor(progress * 3.14159)).item())
    return torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda)


def write_status(status_path: Path, payload: dict):
    with open(status_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)


def main():
    args = parse_args()
    random.seed(42)
    torch.manual_seed(42)

    out_dir = Path("checkpoints")
    out_dir.mkdir(parents=True, exist_ok=True)
    data_dir = Path("data")
    data_dir.mkdir(parents=True, exist_ok=True)

    prefix = args.version
    model_path = out_dir / f"{prefix}.pt"
    tokenizer_path = out_dir / f"{prefix}_tokenizer.json"
    meta_path = out_dir / f"{prefix}_meta.json"
    log_path = out_dir / f"{prefix}_train.log"
    status_path = out_dir / f"{prefix}_status.json"

    log_file = open(log_path, "a", encoding="utf-8", buffering=1)

    def log(msg: str):
        print(msg)
        print(msg, file=log_file)

    write_status(status_path, {
        "version": prefix,
        "status": "starting",
        "step": 0,
        "total_steps": args.steps,
        "loss": None,
        "best_loss": None,
        "elapsed_seconds": 0,
        "log_path": str(log_path),
        "model_path": str(model_path),
        "tokenizer_path": str(tokenizer_path),
        "meta_path": str(meta_path),
    })

    corpus = load_corpus()
    if not corpus:
        raise SystemExit("No training text found. Check internet or place data/general_corpus_v5.txt.")
    log(f"Corpus size: {len(corpus):,} characters")

    tokenizer = build_bpe_tokenizer(corpus, args.vocab_size, prefix)
    vocab_size = tokenizer.get_vocab_size()
    log(f"BPE vocab size: {vocab_size}")

    log("Tokenizing corpus...")
    encoding = tokenizer.encode(corpus)
    token_ids = encoding.ids
    log(f"Tokenized corpus: {len(token_ids):,} tokens")

    dataset = TokenizedDataset(token_ids, length=256)
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True, num_workers=0)
    log(f"Dataset sequences: {len(dataset):,}")

    config = ModelConfig(
        vocab_size=vocab_size,
        max_length=256,
        num_layers=12,
        num_heads=12,
        hidden_size=768,
        ff_size=3072,
        dropout=0.1,
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = AscensionTransformer(config).to(device)
    log(f"Model parameters: {sum(p.numel() for p in model.parameters()):,}")

    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-4, weight_decay=0.01, betas=(0.9, 0.95))
    criterion = nn.CrossEntropyLoss()

    num_steps = args.steps
    warmup_steps = min(10000, num_steps // 10)
    scheduler = get_cosine_schedule_with_warmup(optimizer, warmup_steps, num_steps)

    model.train()
    start = time.perf_counter()
    losses = []
    best_loss = float("inf")
    step = 0
    window_loss = 0.0
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
            window_loss += loss.item()
            step += 1

            if step % args.print_every == 0 or step == num_steps:
                window_steps = step % args.print_every or args.print_every
                avg = window_loss / window_steps
                log(f"Step {step}/{num_steps} loss: {avg:.4f}")
                write_status(status_path, {
                    "version": prefix,
                    "status": "training",
                    "step": step,
                    "total_steps": num_steps,
                    "loss": round(avg, 4),
                    "best_loss": round(best_loss, 4) if best_loss != float("inf") else None,
                    "elapsed_seconds": round(time.perf_counter() - start, 2),
                    "log_path": str(log_path),
                    "model_path": str(model_path),
                    "tokenizer_path": str(tokenizer_path),
                    "meta_path": str(meta_path),
                })
                window_loss = 0.0

        avg = epoch_loss / len(dataloader)
        losses.append(avg)
        if avg < best_loss:
            best_loss = avg

    elapsed = time.perf_counter() - start
    log(f"Training complete in {elapsed:.2f}s best loss: {best_loss:.4f} final loss: {losses[-1]:.4f}")

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
            "corpus_chars": len(corpus),
            "corpus_tokens": len(token_ids),
        }, f, ensure_ascii=False, indent=2)

    write_status(status_path, {
        "version": prefix,
        "status": "complete",
        "step": num_steps,
        "total_steps": num_steps,
        "loss": round(losses[-1], 4),
        "best_loss": round(best_loss, 4),
        "elapsed_seconds": round(elapsed, 2),
        "log_path": str(log_path),
        "model_path": str(model_path),
        "tokenizer_path": str(tokenizer_path),
        "meta_path": str(meta_path),
    })

    log(f"Checkpoint saved to {model_path}")
    log(f"Tokenizer saved to {tokenizer_path}")
    log(f"Metadata saved to {meta_path}")
    log_file.close()


if __name__ == "__main__":
    main()
