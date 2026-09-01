"""Fail-closed quality checks for v20 model-visible curriculum."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    rows = []
    for path in (ROOT / "evals" / "training").glob("aerynza_v20_l*.jsonl"):
        rows.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    assert rows, "v20 curriculum is missing"
    pairs = [(r["user"].strip().lower(), r["assistant"].strip().lower()) for r in rows]
    assert len(pairs) == len(set(pairs)), "exact duplicate prompt/answer pairs"
    model_text = "\n".join(
        "\n".join([*(str(turn.get("content") or "") for turn in r.get("history", [])), r["user"], r["assistant"]])
        for r in rows
    )
    assert not re.search(r"\b(?:Ascension|LifeOS|FamilyOS)\b", model_text, re.I), "legacy public brand leaked"
    packages = Counter(r["package"] for r in rows)
    assert set(packages) == {
        "l0_shell_capabilities",
        "l1_conversation", "l2_time_schedule", "l3_proactive_planning",
        "l4_tools_permissions", "l5_memory_receipts", "l6_cross_domain",
        "l7_creation_multimodal",
    }
    assert all(count > 0 for count in packages.values())
    lowered = [r["assistant"].lower() for r in rows]
    assert sum("when you want me" in answer for answer in lowered) == 0
    assert sum("make sense of" in answer for answer in lowered) == 0
    assert sum("i can help" in answer for answer in lowered) / len(rows) < 0.20
    assert sum("tell me what" in answer for answer in lowered) / len(rows) < 0.20
    heldout = json.loads((ROOT / "evals" / "aerynza_v20_ambient_heldout.json").read_text(encoding="utf-8"))
    train_prompts = {r["user"].strip().lower() for r in rows}
    assert not train_prompts.intersection(c["prompt"].strip().lower() for c in heldout), "held-out prompt leaked"
    print(json.dumps({"passed": True, "records": len(rows), "packages": packages, "heldout": len(heldout)}, default=dict, indent=2))


if __name__ == "__main__":
    main()
