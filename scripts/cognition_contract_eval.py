"""Deterministic production contract checks for Ascension cognition."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.core.cognition import TALENTS, build_cognitive_packet, extract_memory_candidates, hybrid_retrieve


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def action_names(packet: dict) -> set[str]:
    return {item["action"] for item in packet["action_proposals"]}


def main() -> None:
    schedule = extract_memory_candidates("I work 10 pm-6 am Wed-Sun and have Monday and Tuesday nights off.")
    work = next(item for item in schedule if item["key"] == "work_schedule")
    require(work["value"]["days"] == ["wednesday", "thursday", "friday", "saturday", "sunday"], "day shorthand must expand inclusively")

    cash = build_cognitive_packet("I'm short on cash", {}, [], [])
    require({"finance.refresh_cashflow", "finance.prepare_budget"} <= action_names(cash), "cash pressure must activate cash-flow and budget planning")

    housing = build_cognitive_packet("I need a place to stay", {}, [], [])
    search = next(item for item in housing["action_proposals"] if item["action"] == "housing.search_options")
    require("verified monthly housing limit" in search["missing_variables"], "housing must ask for decision-changing variables")

    risky = build_cognitive_packet("Send this message and pay the bill", {}, [], [])
    for proposal in risky["action_proposals"]:
        if proposal["action"] in {"messages.send", "finance.payment"}:
            require(proposal["approval"] == "explicit_confirmation", "external high-risk actions must require explicit confirmation")
            require(proposal["execution_state"] == "proposal_only", "the native core must never claim execution")

    evidence = {
        "documents": [
            {"text": "The family trust review happens each Sunday evening.", "id": "family-1"},
            {"text": "Payroll deposits normally arrive every other Friday.", "id": "finance-1"},
        ]
    }
    results = hybrid_retrieve("When does payroll arrive?", evidence)
    require(results and results[0]["metadata"]["id"] == "finance-1", "retrieval must rank supplied evidence")

    active = {key for key, value in TALENTS.items() if value["state"] == "active"}
    shell_required = {key for key, value in TALENTS.items() if value["state"] == "shell_required"}
    require(len(active) >= 13, "the native core must expose the active Ascension talent layer")
    require({"vision", "voice", "web_research", "external_execution"} <= shell_required, "integration-dependent talents must remain truthfully shell-required")

    print(f"PASS: {len(active)} active talents, {len(shell_required)} shell-required talents, all cognition contracts satisfied")


if __name__ == "__main__":
    main()
