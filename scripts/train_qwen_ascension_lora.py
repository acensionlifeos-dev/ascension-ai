"""Train a Qwen adapter on the reviewed Ascension product curriculum.

The trainer masks every system/user token so loss is calculated only on the
approved assistant answer.  It saves a PEFT adapter, never a replacement model,
and emits a receipt that binds the result to the exact curriculum bytes.
"""

from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import os
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUPPORTED_SHELLS = {"ap", "lifeos", "sprout", "nexus_home", "nexus_family", "core", "creation"}
SYSTEM_PROMPTS = {
    "ap": (
        "You are AP, Ascension LifeOS's warm, perceptive personal intelligence. "
        "Conversation comes first. Use available context quietly, ask only useful "
        "questions, and never claim an action or memory write without a receipt."
    ),
    "lifeos": (
        "You are AP operating inside Ascension LifeOS. Connect relevant life domains, "
        "explain what is known versus inferred, and require receipts for completed actions."
    ),
    "sprout": (
        "You are Ascension AI operating through Sprout for a child or teen. Be warm, "
        "age-appropriate, guardian-aware, privacy-preserving, and explicit when an action "
        "needs parent permission or a verified receipt."
    ),
    "nexus_home": (
        "You are NexusHome, a privacy-aware household coordinator. Respect guardian, "
        "child, household, and private-memory boundaries and require action receipts."
    ),
    "nexus_family": (
        "You are NexusFamily, a family-enterprise coordinator. Help members coordinate "
        "without exposing private household data or speaking unless invited."
    ),
    "core": (
        "You are Ascension AI, the shared intelligence core. Be accurate, humane, useful, "
        "permission-aware, and explicit about uncertainty and action receipts."
    ),
    "creation": (
        "You are Ascension AI in the Creation workspace. Help generate, refine, and organize "
        "creative projects while respecting ownership, permissions, and receipts for published actions."
    ),
}


def curriculum_files(pattern: str) -> list[Path]:
    files = sorted(ROOT.glob(pattern))
    if not files:
        raise FileNotFoundError(f"no curriculum files matched {pattern!r}")
    return files


def load_curriculum(pattern: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    files = curriculum_files(pattern)
    records: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    digest = hashlib.sha256()
    shells: dict[str, int] = {}
    for path in files:
        raw = path.read_bytes()
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        digest.update(raw)
        for line_number, line in enumerate(raw.decode("utf-8").splitlines(), 1):
            if not line.strip():
                continue
            record = json.loads(line)
            missing = {"id", "shell", "user", "assistant"} - set(record)
            if missing:
                raise ValueError(f"{path.name}:{line_number} missing {sorted(missing)}")
            record_id = str(record["id"]).strip()
            shell = str(record["shell"]).strip()
            if not record_id or record_id in seen_ids:
                raise ValueError(f"duplicate or empty curriculum id: {record_id!r}")
            if shell not in SUPPORTED_SHELLS:
                raise ValueError(f"unsupported shell {shell!r} in {record_id}")
            if not str(record["user"]).strip() or not str(record["assistant"]).strip():
                raise ValueError(f"empty conversation field in {record_id}")
            seen_ids.add(record_id)
            shells[shell] = shells.get(shell, 0) + 1
            records.append(record)
    if len(records) < 20:
        raise ValueError("curriculum is unexpectedly small; refusing to train")
    return records, {
        "sha256": digest.hexdigest(),
        "records": len(records),
        "shell_counts": dict(sorted(shells.items())),
        "files": [path.relative_to(ROOT).as_posix() for path in files],
    }


def apply_chat_template(tokenizer: Any, messages: list[dict[str, str]], **kwargs: Any) -> Any:
    try:
        return tokenizer.apply_chat_template(messages, enable_thinking=False, **kwargs)
    except TypeError:
        return tokenizer.apply_chat_template(messages, **kwargs)


def encode_record(tokenizer: Any, record: dict[str, Any], max_length: int) -> dict[str, list[int]]:
    prefix_messages = [
        {"role": "system", "content": SYSTEM_PROMPTS[record["shell"]]},
        {"role": "user", "content": str(record["user"])},
    ]
    # Build the exact inference prefix first.  Some Qwen templates render the
    # assistant header/thinking marker differently once an assistant message is
    # already present, so separately templating a completed conversation can
    # make the intended loss boundary ambiguous.
    prompt_text = apply_chat_template(
        tokenizer, prefix_messages, tokenize=False, add_generation_prompt=True
    )
    answer_text = str(record["assistant"]).strip() + (tokenizer.eos_token or "")
    prefix_ids = tokenizer(prompt_text, add_special_tokens=False)["input_ids"]
    full_ids = tokenizer(prompt_text + answer_text, add_special_tokens=False)["input_ids"]
    prefix_length = len(prefix_ids)
    if full_ids[:prefix_length] != prefix_ids:
        raise ValueError(f"tokenizer changed the verified prompt prefix for {record['id']}")
    if prefix_length == 0 or prefix_length >= len(full_ids):
        raise ValueError(f"could not isolate assistant target for {record['id']}")
    if len(full_ids) > max_length:
        raise ValueError(
            f"{record['id']} requires {len(full_ids)} tokens, above max length {max_length}"
        )
    labels = [-100] * prefix_length + list(full_ids[prefix_length:])
    if all(label == -100 for label in labels):
        raise ValueError(f"no assistant labels for {record['id']}")
    return {
        "input_ids": list(full_ids),
        "attention_mask": [1] * len(full_ids),
        "labels": labels,
    }


class AscensionDataset:
    def __init__(self, rows: list[dict[str, list[int]]]) -> None:
        self.rows = rows

    def __len__(self) -> int:
        return len(self.rows)

    def __getitem__(self, index: int) -> dict[str, list[int]]:
        return self.rows[index]


@dataclass
class AssistantOnlyCollator:
    pad_token_id: int

    def __call__(self, features: list[dict[str, list[int]]]) -> dict[str, Any]:
        import torch

        width = max(len(item["input_ids"]) for item in features)
        input_ids, attention_mask, labels = [], [], []
        for item in features:
            padding = width - len(item["input_ids"])
            input_ids.append(item["input_ids"] + [self.pad_token_id] * padding)
            attention_mask.append(item["attention_mask"] + [0] * padding)
            labels.append(item["labels"] + [-100] * padding)
        return {
            "input_ids": torch.tensor(input_ids, dtype=torch.long),
            "attention_mask": torch.tensor(attention_mask, dtype=torch.long),
            "labels": torch.tensor(labels, dtype=torch.long),
        }


def training_arguments(**kwargs: Any) -> Any:
    from transformers import TrainingArguments

    parameters = inspect.signature(TrainingArguments.__init__).parameters
    if "eval_strategy" not in parameters and "eval_strategy" in kwargs:
        kwargs["evaluation_strategy"] = kwargs.pop("eval_strategy")
    return TrainingArguments(**kwargs)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Train an Ascension Qwen LoRA adapter")
    parser.add_argument("--model", default="Qwen/Qwen3-0.6B")
    parser.add_argument("--output-dir", default="checkpoints/qwen3_0_6b_grow001_adapter")
    parser.add_argument("--curriculum", default="evals/training/ascension_product_v*.jsonl")
    parser.add_argument("--resume-adapter", default=None)
    parser.add_argument("--max-length", type=int, default=768)
    parser.add_argument("--epochs", type=float, default=4.0)
    parser.add_argument("--learning-rate", type=float, default=1.0e-4)
    parser.add_argument("--seed", type=int, default=3407)
    parser.add_argument("--validate-only", action="store_true")
    args = parser.parse_args(argv)

    records, curriculum = load_curriculum(args.curriculum)
    print(json.dumps({"validated": True, "curriculum": curriculum}, indent=2), flush=True)
    if args.validate_only:
        return 0

    import torch
    from peft import LoraConfig, PeftModel, get_peft_model
    from transformers import AutoModelForCausalLM, AutoTokenizer, Trainer, set_seed

    set_seed(args.seed)
    tokenizer = AutoTokenizer.from_pretrained(args.model, use_fast=True)
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token = tokenizer.eos_token
    encoded = [encode_record(tokenizer, record, args.max_length) for record in records]
    random.Random(args.seed).shuffle(encoded)
    eval_size = max(1, round(len(encoded) * 0.1))
    eval_rows, train_rows = encoded[:eval_size], encoded[eval_size:]

    dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        args.model,
        torch_dtype=dtype,
        attn_implementation="sdpa",
    )
    model.config.use_cache = False
    if hasattr(model, "gradient_checkpointing_enable"):
        model.gradient_checkpointing_enable()
    if hasattr(model, "enable_input_require_grads"):
        model.enable_input_require_grads()
    if args.resume_adapter:
        model = PeftModel.from_pretrained(
            model, ROOT / args.resume_adapter, is_trainable=True
        )
    else:
        model = get_peft_model(
            model,
            LoraConfig(
                r=16,
                lora_alpha=32,
                lora_dropout=0.05,
                bias="none",
                task_type="CAUSAL_LM",
                target_modules=[
                    "q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj",
                ],
            ),
        )

    output_dir = ROOT / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    train_args = training_arguments(
        output_dir=str(output_dir),
        num_train_epochs=args.epochs,
        per_device_train_batch_size=1,
        per_device_eval_batch_size=1,
        gradient_accumulation_steps=8,
        learning_rate=args.learning_rate,
        warmup_steps=2,
        weight_decay=0.01,
        lr_scheduler_type="cosine",
        bf16=torch.cuda.is_available(),
        fp16=False,
        logging_steps=5,
        eval_strategy="epoch",
        save_strategy="no",
        report_to="none",
        remove_unused_columns=False,
        ddp_find_unused_parameters=False,
        gradient_checkpointing=True,
        seed=args.seed,
        data_seed=args.seed,
    )
    trainer = Trainer(
        model=model,
        args=train_args,
        train_dataset=AscensionDataset(train_rows),
        eval_dataset=AscensionDataset(eval_rows),
        data_collator=AssistantOnlyCollator(tokenizer.pad_token_id),
    )
    train_result = trainer.train()
    if trainer.is_world_process_zero():
        model.save_pretrained(output_dir, safe_serialization=True)
        tokenizer.save_pretrained(output_dir)
        receipt = {
            "status": "trained_not_promoted",
            "base_model": args.model,
            "adapter_dir": output_dir.relative_to(ROOT).as_posix(),
            "resumed_from_adapter": args.resume_adapter,
            "curriculum": curriculum,
            "train_records": len(train_rows),
            "eval_records": len(eval_rows),
            "assistant_only_loss": True,
            "seed": args.seed,
            "max_length": args.max_length,
            "metrics": train_result.metrics,
            "production_replacement_ready": False,
            "human_review_required": True,
        }
        (output_dir / "ascension_training_receipt.json").write_text(
            json.dumps(receipt, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(json.dumps(receipt, ensure_ascii=False, indent=2), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
