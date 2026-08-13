"""Continue the native model on reviewed Ascension-first product material.

This trainer never reads production conversations or private user data. It
resumes a reviewed base checkpoint, writes rotating recovery state, and keeps
promotion separate from training.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import shutil
import sys
import time
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset
from tokenizers import Tokenizer

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.build_ascension_product_corpus import ROOT, build_corpus
from scripts.evaluate_native_checkpoint import RUNTIME_ARCHITECTURE, RUNTIME_TOKENIZER_CONTRACT
from src.architecture.transformer import AscensionTransformer, ModelConfig


class TokenizedDataset(Dataset):
    def __init__(self, token_ids: list[int], length: int):
        if len(token_ids) < length + 2:
            raise ValueError("product corpus is too small for the configured sequence length")
        self.token_ids = token_ids
        self.length = length

    def __len__(self) -> int:
        return len(self.token_ids) - self.length - 1

    def __getitem__(self, index: int) -> torch.Tensor:
        return torch.tensor(self.token_ids[index:index + self.length + 1], dtype=torch.long)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train Ascension Product v6")
    parser.add_argument("--base-version", default="ascension_elite_general_v5_4h")
    parser.add_argument("--version", default="ascension_product_v6")
    parser.add_argument("--initialization", choices=("resume", "transplant", "fresh"))
    parser.add_argument("--gate-result", help="JSON receipt produced by evaluate_native_checkpoint.py")
    parser.add_argument(
        "--human-review-approved",
        action="store_true",
        help="confirm that the held-out generations in the gate receipt were reviewed",
    )
    parser.add_argument("--steps", type=int, default=20000)
    parser.add_argument("--batch-size", type=int, default=16)
    parser.add_argument("--learning-rate", type=float, default=2e-5)
    parser.add_argument("--print-every", type=int, default=250)
    parser.add_argument("--save-every", type=int, default=2500)
    parser.add_argument("--product-repeats", type=int, default=12)
    parser.add_argument("--general-replay-ratio", type=float, default=0.2)
    parser.add_argument("--resume-latest", action="store_true")
    parser.add_argument("--smoke", action="store_true", help="run a two-step CPU pipeline test")
    return parser.parse_args()


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)


def save_checkpoint(path: Path, payload: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    torch.save(payload, temporary)
    temporary.replace(path)


def load_base(checkpoint_dir: Path, version: str) -> tuple[dict, dict, Path]:
    model_path = checkpoint_dir / f"{version}.pt"
    meta_path = checkpoint_dir / f"{version}_meta.json"
    tokenizer_path = checkpoint_dir / f"{version}_tokenizer.json"
    for path in (model_path, meta_path, tokenizer_path):
        if not path.is_file():
            raise FileNotFoundError(f"required base artifact is missing: {path}")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    if meta.get("architecture") != RUNTIME_ARCHITECTURE:
        raise ValueError("base checkpoint does not declare the causal attention v2 architecture")
    if meta.get("tokenizer_contract") != RUNTIME_TOKENIZER_CONTRACT:
        raise ValueError("base checkpoint does not declare the reversible byte-level BPE tokenizer contract")
    with torch.serialization.safe_globals([ModelConfig]):
        checkpoint = torch.load(model_path, map_location="cpu", weights_only=True)
    return checkpoint, meta, tokenizer_path


def validate_continuation_gate(
    gate_path: Path,
    base_version: str,
    human_review_approved: bool,
    requested_initialization: str | None,
) -> tuple[str, dict]:
    """Bind product continuation to the reviewed evaluator evidence for its exact base."""
    if not gate_path.is_file():
        raise FileNotFoundError(f"continuation gate receipt is missing: {gate_path}")
    raw = gate_path.read_bytes()
    gate = json.loads(raw.decode("utf-8"))
    if gate.get("version") != base_version:
        raise ValueError("continuation gate version does not match the requested base checkpoint")
    if not gate.get("automatic_gate_passed"):
        raise ValueError("base checkpoint has not passed the automatic continuation gate")
    if not human_review_approved:
        raise ValueError("held-out generations require human review before product continuation")
    recommended = gate.get("recommended_next_initialization")
    if recommended not in {"resume", "transplant", "fresh"}:
        raise ValueError(f"continuation gate returned an unsupported initialization: {recommended!r}")
    if requested_initialization and requested_initialization != recommended:
        raise ValueError(
            f"requested initialization {requested_initialization!r} conflicts with gate recommendation {recommended!r}"
        )
    receipt = {
        "path": str(gate_path),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "base_version": base_version,
        "automatic_gate_passed": True,
        "human_review_approved": True,
        "recommended_initialization": recommended,
    }
    return recommended, receipt


def initialize_model(config: ModelConfig, checkpoint: dict, strategy: str) -> tuple[AscensionTransformer, dict]:
    model = AscensionTransformer(config)
    source = checkpoint["model_state_dict"]
    if strategy == "resume":
        model.load_state_dict(source, strict=True)
        return model, {"strategy": strategy, "reused_tensors": len(source), "reinitialized_attention": False}
    if strategy == "transplant":
        reusable = {key: value for key, value in source.items() if ".attention." not in key}
        result = model.load_state_dict(reusable, strict=False)
        if result.unexpected_keys:
            raise ValueError(f"unexpected transplanted keys: {result.unexpected_keys}")
        return model, {
            "strategy": strategy,
            "reused_tensors": len(reusable),
            "reinitialized_attention": True,
            "missing_tensors": len(result.missing_keys),
        }
    return model, {"strategy": strategy, "reused_tensors": 0, "reinitialized_attention": True}


def main() -> int:
    args = parse_args()
    random.seed(42)
    torch.manual_seed(42)
    checkpoint_dir = ROOT / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    if args.smoke:
        args.steps = 2
        args.batch_size = 2
        args.print_every = 1
        args.save_every = 1
        args.product_repeats = 1
        args.general_replay_ratio = 0.0

    if args.smoke:
        args.initialization = args.initialization or "transplant"
        continuation_gate = {
            "mode": "smoke_test_only",
            "automatic_gate_passed": False,
            "human_review_approved": False,
        }
    else:
        if not args.gate_result:
            raise ValueError("--gate-result is required for a non-smoke product continuation")
        args.initialization, continuation_gate = validate_continuation_gate(
            ROOT / args.gate_result,
            args.base_version,
            args.human_review_approved,
            args.initialization,
        )

    base_checkpoint, base_meta, base_tokenizer_path = load_base(checkpoint_dir, args.base_version)
    config = ModelConfig(**base_meta["config"])
    if config.max_length < 64:
        raise ValueError("base checkpoint context window is too small for product continuation")

    corpus_path = ROOT / "data" / f"{args.version}_corpus.txt"
    manifest = build_corpus(
        corpus_path,
        product_repeats=args.product_repeats,
        general_replay_ratio=args.general_replay_ratio,
        general_path=ROOT / "data" / "general_corpus_v5.txt",
    )
    tokenizer = Tokenizer.from_file(str(base_tokenizer_path))
    roundtrip_probe = "AP understands night-shift context, punctuation, and natural spacing."
    if tokenizer.decode(tokenizer.encode(roundtrip_probe).ids) != roundtrip_probe:
        raise ValueError("base tokenizer failed the exact reversible-text contract")
    token_ids = tokenizer.encode(corpus_path.read_text(encoding="utf-8")).ids
    if tokenizer.get_vocab_size() != config.vocab_size:
        raise ValueError("base tokenizer vocabulary does not match the model checkpoint")

    model, initialization = initialize_model(config, base_checkpoint, args.initialization)
    device = "cuda" if torch.cuda.is_available() and not args.smoke else "cpu"
    model = model.to(device)
    dataset = TokenizedDataset(token_ids, min(config.max_length, 256))
    dataloader = DataLoader(dataset, batch_size=args.batch_size, shuffle=True, num_workers=0)
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.learning_rate, weight_decay=0.01, betas=(0.9, 0.95))
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=max(args.steps, 1))
    criterion = nn.CrossEntropyLoss()

    latest_path = checkpoint_dir / f"{args.version}_latest.pt"
    model_path = checkpoint_dir / f"{args.version}.pt"
    tokenizer_path = checkpoint_dir / f"{args.version}_tokenizer.json"
    meta_path = checkpoint_dir / f"{args.version}_meta.json"
    status_path = checkpoint_dir / f"{args.version}_status.json"
    log_path = checkpoint_dir / f"{args.version}_train.log"
    shutil.copy2(base_tokenizer_path, tokenizer_path)

    start_step = 0
    total_loss = 0.0
    best_window_loss = float("inf")
    windows: list[float] = []
    window_loss = 0.0
    if args.resume_latest:
        if not latest_path.is_file():
            raise FileNotFoundError(f"resume requested but recovery checkpoint is missing: {latest_path}")
        with torch.serialization.safe_globals([ModelConfig]):
            recovery = torch.load(latest_path, map_location=device, weights_only=True)
        if recovery.get("version") != args.version:
            raise ValueError("recovery checkpoint output version does not match this run")
        if recovery.get("base_version") != args.base_version:
            raise ValueError("recovery checkpoint base version does not match this run")
        if int(recovery.get("total_steps", 0)) != args.steps:
            raise ValueError("recovery checkpoint step budget does not match this run")
        if recovery.get("initialization") != initialization:
            raise ValueError("recovery checkpoint initialization does not match the reviewed gate")
        if recovery.get("continuation_gate", {}).get("sha256") != continuation_gate.get("sha256"):
            raise ValueError("recovery checkpoint continuation gate does not match this run")
        if recovery.get("corpus_manifest") != manifest:
            raise ValueError("recovery checkpoint corpus manifest does not match this run")
        model.load_state_dict(recovery["model_state_dict"], strict=True)
        optimizer.load_state_dict(recovery["optimizer_state_dict"])
        scheduler.load_state_dict(recovery["scheduler_state_dict"])
        start_step = int(recovery["step"])
        total_loss = float(recovery.get("total_loss", 0.0))
        best_window_loss = float(recovery.get("best_window_loss", float("inf")))
        windows = list(recovery.get("window_losses", []))
        window_loss = float(recovery.get("window_loss", 0.0))

    log_file = log_path.open("a", encoding="utf-8", buffering=1)

    def log(message: str) -> None:
        print(message, flush=True)
        print(message, file=log_file)

    started = time.perf_counter()
    log(f"Ascension product continuation: {args.base_version} -> {args.version}")
    log(f"Initialization: {initialization}")
    log(f"Corpus: {manifest['example_count']} reviewed examples, {len(token_ids):,} tokens")
    log(f"Device: {device}; steps: {start_step}/{args.steps}")
    write_json(status_path, {
        "version": args.version,
        "base_version": args.base_version,
        "status": "training",
        "step": start_step,
        "total_steps": args.steps,
        "initialization": initialization,
        "corpus_manifest": manifest,
        "continuation_gate": continuation_gate,
        "promotion_status": "not_evaluated",
    })

    model.train()
    step = start_step
    iterator = iter(dataloader)
    while step < args.steps:
        try:
            batch = next(iterator)
        except StopIteration:
            iterator = iter(dataloader)
            batch = next(iterator)
        batch = batch.to(device)
        input_ids = batch[:, :-1]
        targets = batch[:, 1:]
        logits = model(input_ids)
        loss = criterion(logits.reshape(-1, logits.size(-1)), targets.reshape(-1))
        optimizer.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        optimizer.step()
        scheduler.step()
        value = float(loss.item())
        total_loss += value
        window_loss += value
        step += 1

        if step % args.print_every == 0 or step == args.steps:
            window_steps = step % args.print_every or args.print_every
            average = window_loss / window_steps
            windows.append(average)
            best_window_loss = min(best_window_loss, average)
            log(f"Step {step}/{args.steps} window loss: {average:.4f}")
            window_loss = 0.0
            write_json(status_path, {
                "version": args.version,
                "base_version": args.base_version,
                "status": "training" if step < args.steps else "saving",
                "step": step,
                "total_steps": args.steps,
                "window_loss": round(average, 4),
                "best_window_loss": round(best_window_loss, 4),
                "elapsed_seconds": round(time.perf_counter() - started, 2),
                "initialization": initialization,
                "corpus_manifest": manifest,
                "continuation_gate": continuation_gate,
                "promotion_status": "not_evaluated",
            })

        if step % args.save_every == 0 and step < args.steps:
            save_checkpoint(latest_path, {
                "version": args.version,
                "model_state_dict": model.state_dict(),
                "optimizer_state_dict": optimizer.state_dict(),
                "scheduler_state_dict": scheduler.state_dict(),
                "config": config,
                "step": step,
                "total_steps": args.steps,
                "total_loss": total_loss,
                "window_loss": window_loss,
                "best_window_loss": best_window_loss,
                "window_losses": windows,
                "base_version": args.base_version,
                "initialization": initialization,
                "continuation_gate": continuation_gate,
                "corpus_manifest": manifest,
            })
            log(f"Recovery checkpoint saved at step {step}")

    elapsed = time.perf_counter() - started
    final_loss = windows[-1] if windows else total_loss / max(step - start_step, 1)
    save_checkpoint(model_path, {
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict(),
        "config": config,
        "losses": windows,
        "step": step,
        "base_version": args.base_version,
        "initialization": initialization,
        "continuation_gate": continuation_gate,
        "corpus_manifest": manifest,
    })
    write_json(meta_path, {
        "model_path": str(model_path),
        "tokenizer_path": str(tokenizer_path),
        "config": config.__dict__,
        "base_version": args.base_version,
        "initialization": initialization,
        "architecture": RUNTIME_ARCHITECTURE,
        "tokenizer_contract": RUNTIME_TOKENIZER_CONTRACT,
        "final_loss": final_loss,
        "best_loss": best_window_loss,
        "train_seconds": elapsed,
        "device": device,
        "num_steps": args.steps,
        "corpus_manifest": manifest,
        "continuation_gate": continuation_gate,
        "promotion_status": "not_evaluated",
    })
    write_json(status_path, {
        "version": args.version,
        "base_version": args.base_version,
        "status": "complete",
        "step": args.steps,
        "total_steps": args.steps,
        "loss": round(final_loss, 4),
        "best_loss": round(best_window_loss, 4),
        "elapsed_seconds": round(elapsed, 2),
        "initialization": initialization,
        "continuation_gate": continuation_gate,
        "promotion_status": "not_evaluated",
    })
    latest_path.unlink(missing_ok=True)
    log(f"Training complete in {elapsed:.2f}s; checkpoint: {model_path}")
    log("Promotion remains blocked pending held-out evaluation.")
    log_file.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
