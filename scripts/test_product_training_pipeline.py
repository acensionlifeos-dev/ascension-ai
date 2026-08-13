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

from scripts.build_ascension_product_corpus import (
    build_corpus,
    curriculum_paths,
    format_example,
    format_inference_prompt,
    read_curriculum,
)
from scripts.train_ascension_product_v6 import (
    AssistantResponseDataset,
    TokenizedDataset,
    initialize_model,
    load_base,
    save_checkpoint,
    validate_continuation_gate,
)
from scripts.evaluate_native_checkpoint import (
    RUNTIME_ARCHITECTURE,
    RUNTIME_TOKENIZER_CONTRACT,
    checkpoint_artifact_evidence,
)
from src.architecture.transformer import AscensionTransformer, ModelConfig


def _test_corpus_unicity() -> None:
    """Verify multi-file curriculum loading and duplicate-ID rejection."""
    paths = curriculum_paths()
    if len(paths) < 2:
        raise AssertionError("expected multiple ascension_product curriculum files")
    records = read_curriculum(paths)
    if len(records) < 30:
        raise AssertionError("product curriculum must contain at least 30 reviewed examples")
    ids = [record["id"] for record in records]
    if len(set(ids)) != len(ids):
        raise AssertionError("product curriculum IDs must be unique across files")

    with tempfile.TemporaryDirectory() as directory:
        dup_path = Path(directory) / "ascension_product_v99.jsonl"
        first_raw = paths[0].read_text(encoding="utf-8").splitlines()[0]
        first_record = json.loads(first_raw)
        dup_path.write_text(json.dumps(first_record) + "\n", encoding="utf-8")
        try:
            read_curriculum([paths[0], dup_path])
        except ValueError as error:
            message = str(error)
            if "duplicate id" not in message.lower():
                raise AssertionError("duplicate ID was rejected but not with a duplicate-id message")
            if "first seen in" not in message.lower():
                raise AssertionError("duplicate ID error must report the first file and line")
            if paths[0].name not in message:
                raise AssertionError("duplicate ID error must name the original curriculum file")
        else:
            raise AssertionError("duplicate curriculum id was not rejected")


def _test_curriculum_quality() -> None:
    """Validate every record has non-empty string fields and a non-empty tag list."""
    records = read_curriculum(curriculum_paths())
    for record in records:
        for field in ("id", "shell", "user", "assistant"):
            value = record.get(field)
            if not isinstance(value, str) or not value.strip():
                raise AssertionError(f"record {record.get('id')!r} has empty or invalid {field}")
        tags = record.get("tags")
        if not isinstance(tags, list) or not tags or not all(isinstance(tag, str) and tag.strip() for tag in tags):
            raise AssertionError(f"record {record.get('id')!r} has missing or invalid tags")


def _test_empty_curriculum_rejection() -> None:
    """Confirm empty curriculum discovery is rejected before any training can begin."""
    try:
        read_curriculum([])
    except ValueError as error:
        if "at least 30" not in str(error).lower():
            raise AssertionError("empty curriculum was rejected for the wrong reason")
    else:
        raise AssertionError("empty curriculum was not rejected")


def _test_runtime_prompt_envelope() -> None:
    record = {
        "id": "envelope_probe",
        "shell": "ap",
        "user": "Remember this preference.",
        "assistant": "I can propose it, but it is not saved yet.",
        "tags": ["private_training_metadata", "must_not_leak"],
    }
    example = format_example(record)
    prompt = format_inference_prompt(record["shell"], record["user"])
    expected_prefix = "<s>\nASCENSION SHELL: ap\nUSER: Remember this preference.\nASSISTANT:"
    if not example.startswith(expected_prefix):
        raise AssertionError("training example and inference prompt prefixes diverged")
    if prompt != expected_prefix:
        raise AssertionError("inference prompt does not match the product training envelope")
    if "LESSON TAGS" in example or "private_training_metadata" in example:
        raise AssertionError("training-only metadata leaked into the model-facing corpus")


def _test_continuation_gate() -> None:
    with tempfile.TemporaryDirectory() as directory:
        checkpoint_dir = Path(directory)
        gate_path = checkpoint_dir / "gate.json"
        for name, content in (
            ("causal_v7.pt", b"model"),
            ("causal_v7_meta.json", b"metadata"),
            ("causal_v7_tokenizer.json", b"tokenizer"),
        ):
            (checkpoint_dir / name).write_bytes(content)
        artifacts = checkpoint_artifact_evidence(
            checkpoint_dir, "causal_v7", checkpoint_dir / "causal_v7_tokenizer.json"
        )
        gate_path.write_text(json.dumps({
            "version": "causal_v7",
            "automatic_gate_passed": True,
            "recommended_next_initialization": "resume",
            "checkpoint_artifacts": artifacts,
        }), encoding="utf-8")
        initialization, receipt = validate_continuation_gate(
            gate_path, checkpoint_dir, "causal_v7", True, None
        )
        if initialization != "resume" or len(receipt["sha256"]) != 64:
            raise AssertionError("valid continuation gate did not produce a bound receipt")
        for label, base, reviewed, requested in (
            ("wrong base", "other", True, None),
            ("missing human review", "causal_v7", False, None),
            ("conflicting initialization", "causal_v7", True, "transplant"),
        ):
            try:
                validate_continuation_gate(gate_path, checkpoint_dir, base, reviewed, requested)
            except ValueError:
                continue
            raise AssertionError(f"continuation gate failed open for {label}")
        gate_path.write_text(json.dumps({
            "version": "causal_v7",
            "automatic_gate_passed": False,
            "recommended_next_initialization": "continue_or_retrain",
            "checkpoint_artifacts": artifacts,
        }), encoding="utf-8")
        try:
            validate_continuation_gate(gate_path, checkpoint_dir, "causal_v7", True, None)
        except ValueError:
            pass
        else:
            raise AssertionError("continuation gate accepted a base that failed automatic evaluation")
        gate_path.write_text(json.dumps({
            "version": "causal_v7",
            "automatic_gate_passed": True,
            "recommended_next_initialization": "resume",
            "checkpoint_artifacts": artifacts,
        }), encoding="utf-8")
        (checkpoint_dir / "causal_v7.pt").write_bytes(b"mutated-model")
        try:
            validate_continuation_gate(gate_path, checkpoint_dir, "causal_v7", True, None)
        except ValueError:
            pass
        else:
            raise AssertionError("continuation gate accepted artifacts changed after evaluation")


def main() -> int:
    torch.manual_seed(11)
    _test_corpus_unicity()
    _test_curriculum_quality()
    _test_empty_curriculum_rejection()
    _test_runtime_prompt_envelope()
    _test_continuation_gate()
    with tempfile.TemporaryDirectory(prefix="ascension-product-smoke-") as directory:
        root = Path(directory)
        prefix = "tiny_base"
        corpus_path = root / "product.txt"
        manifest = build_corpus(corpus_path, product_repeats=1, general_replay_ratio=0)
        if (
            not isinstance(manifest["curriculum"], list)
            or len(manifest["curriculum"]) < 2
            or manifest["example_count"] < 30
            or manifest["contains_private_user_data"]
        ):
            raise AssertionError("product corpus provenance contract failed")

        tokenizer = Tokenizer(BPE(unk_token="<unk>"))
        tokenizer.pre_tokenizer = Whitespace()
        tokenizer.train_from_iterator(
            [corpus_path.read_text(encoding="utf-8")],
            BpeTrainer(vocab_size=256, special_tokens=["<pad>", "<unk>", "<s>", "</s>"]),
        )
        tokenizer_path = root / f"{prefix}_tokenizer.json"
        tokenizer.save(str(tokenizer_path))
        supervised = AssistantResponseDataset(
            tokenizer,
            read_curriculum(curriculum_paths())[:2],
            length=63,
            repeats=1,
        )
        supervised_inputs, supervised_targets = supervised[0]
        if supervised_inputs.shape != supervised_targets.shape or supervised_inputs.shape[0] != 63:
            raise AssertionError("assistant-response examples must be fixed-size input/target pairs")
        learned = torch.nonzero(supervised_targets != -100, as_tuple=False).flatten()
        if not len(learned) or int(learned[0]) <= 0:
            raise AssertionError("assistant-response loss mask did not protect prompt tokens")
        if torch.any(supervised_targets[: int(learned[0])] != -100):
            raise AssertionError("prompt or control tokens leaked into assistant-response loss")
        if torch.any(supervised_targets[int(learned[-1]) + 1 :] != -100):
            raise AssertionError("padding tokens leaked into assistant-response loss")
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
            "architecture": RUNTIME_ARCHITECTURE,
            "tokenizer_contract": RUNTIME_TOKENIZER_CONTRACT,
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
    print("PASS assistant-only response loss mask")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
