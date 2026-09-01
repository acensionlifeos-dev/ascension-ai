"""Build deterministic, leakage-resistant v20 language growth packages.

This builder intentionally removes exact repetition from the historical corpus.
Weighting belongs in the sampler/training plan, not in thousands of copied rows.
Prompts with conflicting answers are quarantined for review instead of selecting
an answer silently.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TRAINING = ROOT / "evals" / "training"
RESULTS = ROOT / "evals" / "results"

PACKAGES = (
    "l0_shell_capabilities",
    "l1_conversation",
    "l2_time_schedule",
    "l3_proactive_planning",
    "l4_tools_permissions",
    "l5_memory_receipts",
    "l6_cross_domain",
    "l7_creation_multimodal",
)
# Keep every unique lesson. Package balancing is performed by the trainer's
# sampler; it must never be simulated by deleting knowledge or copying rows.
MAX_RECORDS_PER_PACKAGE = 10000


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def current_branding(value: str) -> str:
    """Remove legacy public product names from model-visible training text."""
    replacements = (
        (r"\bAscension LifeOS\b", "AerynzaLife"),
        (r"\bAscension AI\b", "Aerynza AI"),
        (r"\bFamilyOS\b", "Aerynza Family"),
        (r"\bLifeOS\b", "AerynzaLife"),
        (r"\bAscension\b", "Aerynza"),
        (r"\bAP\b", "Aerynza"),
    )
    for pattern, replacement in replacements:
        value = re.sub(pattern, replacement, value, flags=re.IGNORECASE)
    return value


GENERIC_CAPABILITY_PATTERN = re.compile(
    r"^I can help with (?P<name>.+?)\. (?P<description>.+?) "
    r"I won['’]t take any action without your permission and a provider receipt\. "
    r"Tell me what you['’]d like to do first\.$",
    re.IGNORECASE,
)


def deepen_capability_answer(user: str, assistant: str) -> str:
    """Retain capability knowledge without teaching one robotic response shape."""
    match = GENERIC_CAPABILITY_PATTERN.match(assistant.strip())
    if not match:
        return assistant
    name = current_branding(match.group("name").strip())
    description = current_branding(match.group("description").strip().rstrip("."))
    variants = (
        f"{name} covers {description.lower()}. I’ll turn the result you want into a concrete first output, ask only for details that materially change it, and keep preparation distinct from execution.",
        f"Use {name} for {description.lower()}. I’ll connect relevant authorized context, produce something you can review, and leave any external step pending until the shell confirms it.",
        f"The working scope of {name} is {description.lower()}. Bring the outcome or raw material you have; I’ll develop the next useful artifact and label assumptions rather than inventing facts.",
        f"For {name}, Aerynza can handle {description.lower()}. We’ll begin with the smallest useful result, improve it from your feedback, and verify any saved or external outcome separately.",
    )
    selector = int(hashlib.sha256(normalize(user).encode("utf-8")).hexdigest()[:8], 16)
    return variants[selector % len(variants)]


def row_text(row: dict) -> tuple[str, str]:
    user = str(row.get("user") or row.get("prompt") or "").strip()
    assistant = str(row.get("assistant") or row.get("response") or "").strip()
    return user, assistant


def heldout_prompts() -> set[str]:
    prompts: set[str] = set()
    receipt = ROOT / "evals" / "receipt_truth_prompts.json"
    if receipt.is_file():
        for row in json.loads(receipt.read_text(encoding="utf-8")):
            prompts.add(normalize(str(row.get("prompt") or "")))
    for path in TRAINING.glob("*heldout*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                user, _ = row_text(json.loads(line))
                prompts.add(normalize(user))
    return {prompt for prompt in prompts if prompt}


def package_for(row: dict, source: str) -> str:
    user, assistant = row_text(row)
    text = normalize(" ".join([source, user, assistant, " ".join(map(str, row.get("tags") or []))]))
    if GENERIC_CAPABILITY_PATTERN.match(assistant.strip()):
        return "l0_shell_capabilities"
    if any(word in text for word in ("receipt", "saved", "memory write", "sync state", "timeout", "confirmed")):
        return "l5_memory_receipts"
    if any(word in text for word in ("permission", "provider", "tool", "execute", "publish", "submit", "approval")):
        return "l4_tools_permissions"
    if any(word in text for word in ("schedule", "calendar", "shift", "circadian", "tomorrow", "weekly", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday")):
        return "l2_time_schedule"
    if any(word in text for word in ("create", "creation", "creative", "image", "video", "music", "writer", "game", "recipe", "workspace", "design")):
        return "l7_creation_multimodal"
    if any(word in text for word in ("plan", "missing", "clarify", "next step", "proactive", "check-in", "goal", "quest")):
        return "l3_proactive_planning"
    if any(word in text for word in ("feel", "friend", "listen", "talk", "conversation", "thinking", "with me", "hear you")):
        return "l1_conversation"
    return "l6_cross_domain"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-prefix", default="aerynza_v20")
    args = parser.parse_args()

    heldout = heldout_prompts()
    by_pair: dict[tuple[str, str], dict] = {}
    answers_by_prompt: dict[str, set[str]] = defaultdict(set)
    raw_count = invalid = heldout_excluded = 0

    for path in sorted(TRAINING.glob("*.jsonl")):
        if "heldout" in path.name or path.name.startswith(args.output_prefix):
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            raw_count += 1
            try:
                original = json.loads(line)
                user, assistant = row_text(original)
            except (json.JSONDecodeError, TypeError):
                invalid += 1
                continue
            prompt_key, answer_key = normalize(user), normalize(assistant)
            if not prompt_key or not answer_key:
                invalid += 1
                continue
            if prompt_key in heldout:
                heldout_excluded += 1
                continue
            answers_by_prompt[prompt_key].add(answer_key)
            pair = (prompt_key, answer_key)
            if pair not in by_pair:
                by_pair[pair] = {
                    "shell": str(original.get("shell") or "ap"),
                    "user": user,
                    "assistant": assistant,
                    "source": f"{path.name}:{line_number}",
                    "tags": sorted(set(map(str, original.get("tags") or []))),
                }

    conflicts = {prompt for prompt, answers in answers_by_prompt.items() if len(answers) > 1}
    packages: dict[str, list[dict]] = {name: [] for name in PACKAGES}
    quarantined: list[dict] = []
    for (prompt_key, _), row in by_pair.items():
        if prompt_key in conflicts:
            quarantined.append(row)
            continue
        package = package_for(row, row["source"])
        clean = {key: value for key, value in row.items() if key != "source"}
        clean["user"] = current_branding(clean["user"])
        clean["assistant"] = current_branding(deepen_capability_answer(clean["user"], clean["assistant"]))
        if clean.get("history"):
            clean["history"] = [
                {"role": str(turn["role"]), "content": current_branding(str(turn["content"]))}
                for turn in clean["history"]
            ]
        clean["id"] = f"v20_{package}_{len(packages[package]) + 1:05d}"
        clean["package"] = package
        clean["provenance"] = row["source"]
        packages[package].append(clean)

    # Stable hash ordering makes capped sampling reproducible and prevents file
    # order from deciding which examples survive. Repetition/weighting is left
    # to the training sampler and cannot leak back into the stored curriculum.
    uncapped_counts = {name: len(rows) for name, rows in packages.items()}
    for name, rows in packages.items():
        rows.sort(key=lambda row: hashlib.sha256(
            (normalize(row["user"]) + "\0" + normalize(row["assistant"])).encode("utf-8")
        ).hexdigest())
        packages[name] = rows[:MAX_RECORDS_PER_PACKAGE]

    outputs = {}
    for name, rows in packages.items():
        path = TRAINING / f"{args.output_prefix}_{name}.jsonl"
        path.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8")
        outputs[name] = {"path": str(path.relative_to(ROOT)), "records": len(rows), "sha256": digest(path)}

    master_path = TRAINING / f"{args.output_prefix}_balanced_master.jsonl"
    master_rows = [row for name in PACKAGES for row in packages[name]]
    master_path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in master_rows),
        encoding="utf-8",
    )

    quarantine_path = RESULTS / f"{args.output_prefix}_conflicts.json"
    quarantine_path.write_text(json.dumps(quarantined, ensure_ascii=False, indent=2), encoding="utf-8")
    manifest = {
        "version": "v20",
        "raw_records_scanned": raw_count,
        "invalid_records": invalid,
        "heldout_prompt_count": len(heldout),
        "heldout_rows_excluded": heldout_excluded,
        "unique_pairs_after_heldout_exclusion": len(by_pair),
        "conflicting_prompt_count": len(conflicts),
        "quarantined_rows": len(quarantined),
        "train_records": sum(item["records"] for item in outputs.values()),
        "max_records_per_package": MAX_RECORDS_PER_PACKAGE,
        "uncapped_package_counts": uncapped_counts,
        "packages": outputs,
        "balanced_master": {
            "path": str(master_path.relative_to(ROOT)),
            "records": len(master_rows),
            "sha256": digest(master_path),
        },
        "conflicts_path": str(quarantine_path.relative_to(ROOT)),
        "policy": "Every unique non-conflicting lesson retained; exact copies removed; held-out prompts excluded; conflicts quarantined; equal-package weighting performed by the trainer.",
    }
    manifest_path = RESULTS / f"{args.output_prefix}_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0 if invalid == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
