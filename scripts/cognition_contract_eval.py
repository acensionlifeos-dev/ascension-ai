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

    prediction = build_cognitive_packet("Research this Polymarket question and prepare a prediction market paper plan", {}, [], [])
    require("trading" in prediction["domains"], "Polymarket language must route to prediction-market intelligence")
    require({"trading.refresh_prediction_markets", "trading.prepare_prediction_position"} <= action_names(prediction), "prediction markets must refresh live evidence and prepare a paper position")
    paper = next(item for item in prediction["action_proposals"] if item["action"] == "trading.prepare_prediction_position")
    require({"verified resolution rules", "jurisdiction eligibility", "disposable risk budget", "maximum acceptable loss"} <= set(paper["missing_variables"]), "prediction planning must name the material unknowns")

    live_prediction = build_cognitive_packet("Buy this Polymarket position", {}, [], [])
    submit = next(item for item in live_prediction["action_proposals"] if item["action"] == "trading.submit_prediction_order")
    require(submit["approval"] == "explicit_confirmation" and submit["risk"] == "critical", "real prediction orders must be critical and explicitly confirmed")
    require({"verified jurisdiction eligibility", "wallet signature", "provider receipt"} <= set(submit["missing_variables"]), "real prediction orders must remain gated on eligibility, signature, and receipt")

    schedule_only = build_cognitive_packet("I'm short on cash and pay $50 to my landlord", {}, ["schedule"])
    require(schedule_only["domains"] == [], "restricted requests must not fall back to an unauthorized identity domain")
    require(not schedule_only["memory_candidates"], "restricted requests must not emit memory candidates from unauthorized domains")
    require(not schedule_only["action_proposals"], "restricted requests must not emit action proposals from unauthorized domains")

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
