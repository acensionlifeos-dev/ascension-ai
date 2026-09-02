"""Fail-closed conversational corpus checks; never a semantic quality certification."""
import hashlib
import json
import re
from pathlib import Path


def validate(train: Path, heldout: Path) -> dict:
    prompts = set()
    counts = []
    for path in (heldout, train):
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if len(rows) < 20:
            raise ValueError("At least 20 independent conversations per split required")
        local = set()
        for row in rows:
            if not isinstance(row, dict) or not all(isinstance(row.get(k), str) and row[k].strip() for k in ("user", "assistant")):
                raise ValueError("Expected nonempty user/assistant conversations, not raw documentation")
            key = re.sub(r"\W+", " ", row["user"].casefold()).strip()
            if key in local or key in prompts:
                raise ValueError("Duplicate prompt or train/heldout overlap")
            local.add(key)
            if re.search(r"What Was Added|Related Capabilities|Cross-references:", row["assistant"], re.I):
                raise ValueError("Development documentation is not an approved conversational target")
        prompts.update(local)
        counts.append(len(rows))
    return {"format_pass": True, "heldout_records": counts[0], "train_records": counts[1],
            "train_sha256": hashlib.sha256(train.read_bytes()).hexdigest(),
            "heldout_sha256": hashlib.sha256(heldout.read_bytes()).hexdigest(),
            "human_review_required": True, "training_authorized": False}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("train", type=Path)
    parser.add_argument("heldout", type=Path)
    args = parser.parse_args()
    print(json.dumps(validate(args.train, args.heldout), indent=2))
