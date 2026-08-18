"""Build a provenance-checked, de-identified Ascension-first training corpus."""

from __future__ import annotations

import argparse
import json
import random
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CURRICULUM_DIR = ROOT / "evals" / "training"
CURRICULUM_GLOB = "ascension_product_v*.jsonl"
SAFE_DOCS = (
    ROOT / "AGENTS.md",
    ROOT / "README.md",
    ROOT / "docs" / "SAFETY.md",
    ROOT / "docs" / "AI_GROWTH_LOOP.md",
    ROOT / "docs" / "HUMAN_LIFE_AND_PSYCHOLOGY.md",
)
SECRET_PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "openai_key": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "github_token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b"),
    "bearer_token": re.compile(r"\bBearer\s+[A-Za-z0-9._~+/-]{20,}", re.I),
    "aws_key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
}


def curriculum_paths() -> list[Path]:
    return sorted(CURRICULUM_DIR.glob(CURRICULUM_GLOB))


def read_curriculum(paths: list[Path] | None = None) -> list[dict]:
    records = []
    seen_ids: dict[str, tuple[str, int]] = {}
    for path in paths if paths is not None else curriculum_paths():
        for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if not raw.strip():
                continue
            record = json.loads(raw)
            required = {"id", "shell", "user", "assistant", "tags"}
            missing = required - record.keys()
            if missing:
                raise ValueError(f"{path}:{line_number} missing {sorted(missing)}")
            if record["shell"] not in {"ap", "lifeos", "nexus_home", "nexus_family", "core", "sprout"}:
                raise ValueError(f"{path}:{line_number} has unsupported shell")
            if record["id"] in seen_ids:
                first_path, first_line = seen_ids[record["id"]]
                raise ValueError(
                    f"{path}:{line_number} duplicate id {record['id']!r} "
                    f"(first seen in {first_path}:{first_line})"
                )
            seen_ids[record["id"]] = (str(path), line_number)
            records.append(record)
    if len(records) < 30:
        raise ValueError("Ascension product curriculum must contain at least 30 reviewed examples")
    return records


def assert_no_secrets(text: str, source: str) -> None:
    for label, pattern in SECRET_PATTERNS.items():
        if pattern.search(text):
            raise ValueError(f"blocked {label} pattern in {source}")


def format_example(record: dict) -> str:
    """Render only fields that the native inference envelope supplies.

    Lesson tags remain provenance metadata in JSONL. Putting them into the
    model-facing text taught earlier checkpoints to depend on and sometimes
    emit a control field that does not exist at runtime.
    """
    return (
        "<s>\n"
        f"ASCENSION SHELL: {record['shell']}\n"
        f"USER: {record['user'].strip()}\n"
        f"ASSISTANT: {record['assistant'].strip()}\n"
        "</s>"
    )


def format_inference_prompt(shell: str, user: str) -> str:
    """Build the exact prefix used to evaluate a product checkpoint."""
    return (
        "<s>\n"
        f"ASCENSION SHELL: {shell}\n"
        f"USER: {user.strip()}\n"
        "ASSISTANT:"
    )


def sample_general_replay(path: Path, target_chars: int, seed: int = 42) -> str:
    if target_chars <= 0 or not path.is_file():
        return ""
    size = path.stat().st_size
    if size <= target_chars:
        return path.read_text(encoding="utf-8", errors="ignore")
    rng = random.Random(seed)
    chunk_size = min(8192, target_chars)
    chunks = []
    remaining = target_chars
    with path.open("rb") as handle:
        while remaining > 0:
            take = min(chunk_size, remaining)
            offset = rng.randrange(0, max(1, size - take))
            handle.seek(offset)
            if offset:
                handle.readline()
            chunk = handle.read(take).decode("utf-8", errors="ignore")
            chunks.append(chunk)
            remaining -= len(chunk)
    return "\n\n".join(chunks)


def build_corpus(
    output_path: Path,
    product_repeats: int = 12,
    general_replay_ratio: float = 0.2,
    general_path: Path | None = None,
) -> dict:
    if not 0 <= general_replay_ratio < 0.5:
        raise ValueError("general replay ratio must be between 0 and 0.5")
    records = read_curriculum(curriculum_paths())
    product_sections = [format_example(record) for record in records]
    for path in SAFE_DOCS:
        text = path.read_text(encoding="utf-8")
        assert_no_secrets(text, str(path.relative_to(ROOT)))
        product_sections.append(f"<s>\nASCENSION REFERENCE: {path.name}\n{text.strip()}\n</s>")

    product_once = "\n\n".join(product_sections)
    assert_no_secrets(product_once, "compiled product curriculum")
    product_text = "\n\n".join(product_once for _ in range(max(1, product_repeats)))
    replay_chars = int(len(product_text) * general_replay_ratio / max(1e-9, 1 - general_replay_ratio))
    replay_path = general_path or ROOT / "data" / "general_corpus_v5.txt"
    general_text = sample_general_replay(replay_path, replay_chars)
    assert_no_secrets(general_text, "general replay sample")

    final_text = product_text
    if general_text:
        final_text += "\n\n<s>\nGENERAL LANGUAGE REPLAY\n" + general_text + "\n</s>"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final_text, encoding="utf-8")
    manifest = {
        "curriculum": [str(path.relative_to(ROOT)) for path in curriculum_paths()],
        "example_count": len(records),
        "shells": sorted({record["shell"] for record in records}),
        "safe_docs": [str(path.relative_to(ROOT)) for path in SAFE_DOCS],
        "product_repeats": max(1, product_repeats),
        "general_replay_ratio_requested": general_replay_ratio,
        "product_chars": len(product_text),
        "general_replay_chars": len(general_text),
        "total_chars": len(final_text),
        "contains_private_user_data": False,
    }
    output_path.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the Ascension product continuation corpus")
    parser.add_argument("--output", default="data/ascension_product_v1.txt")
    parser.add_argument("--product-repeats", type=int, default=12)
    parser.add_argument("--general-replay-ratio", type=float, default=0.2)
    parser.add_argument("--general-path", default="data/general_corpus_v5.txt")
    args = parser.parse_args()
    manifest = build_corpus(
        ROOT / args.output,
        product_repeats=args.product_repeats,
        general_replay_ratio=args.general_replay_ratio,
        general_path=ROOT / args.general_path,
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
