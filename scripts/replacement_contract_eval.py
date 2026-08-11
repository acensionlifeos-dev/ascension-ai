"""Fast, model-free checks for replacement safety contracts."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.contracts import MODE_CONTRACTS, Shell, Tier, response_contract, system_contract
from src.core.model_runtime import NativeModelRuntime
from src.core.orchestrator import compact_context, prepare_inference


def check(name: str, passed: bool) -> None:
    print(f"{'PASS' if passed else 'FAIL'} {name}")
    if not passed:
        raise AssertionError(name)


def main() -> None:
    cases = json.loads((ROOT / "evals" / "replacement_readiness_prompts.json").read_text(encoding="utf-8"))
    check("twenty cross-domain replacement cases exist", len(cases) >= 20)
    check("all intelligence shells are covered", {item["shell"] for item in cases} == {"ap","lifeos","nexus_home","nexus_family","core"})
    check("every case has positive and negative rubrics", all(item.get("required_any") and item.get("forbidden") for item in cases))
    check("every invocation mode has a bounded response contract", set(MODE_CONTRACTS) == {"conversation","proactive","planning","analysis","background"})
    contract = system_contract(Shell.AP, Tier.LIFE_OS, ["schedule"])
    check("receipt discipline is foundational", "Understanding is not saving" in contract and "verified receipt" in contract)
    check("casual conversation blocks automatic ceremony", "Do not force advice" in response_contract("conversation"))
    compacted = compact_context({"ui_state":"noise","debug":"noise","action_receipts":[{"id":1}],"profile":{"name":"A"},"telemetry":"noise"})
    check("receipts survive while debug noise is excluded", "action_receipts" in compacted and "ui_state" not in compacted and "telemetry" not in compacted)
    prepared = prepare_inference(shell=Shell.AP,tier=Tier.LIFE_OS,messages=[{"role":"user","content":"I work 10 pm-6 am Wed-Sun"}],context={},surface="chat",mode="conversation",allowed_capabilities=["schedule"])
    check("inference packet includes response mode and schedule cognition", "Response contract" in prepared["messages"][1]["content"] and "schedule" in prepared["domains"])
    check("unterminated hidden reasoning is suppressed", NativeModelRuntime._clean_content("<think>private reasoning") == "")
    check("control tokens are stripped", "<|" not in NativeModelRuntime._clean_content("Hello <|im_end|>"))
    print("Replacement contract evaluation passed: 10/10")


if __name__ == "__main__":
    main()
