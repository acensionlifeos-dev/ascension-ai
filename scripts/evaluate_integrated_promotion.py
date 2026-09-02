"""Evaluate a native candidate together with the deterministic shell runtime."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
import sys
sys.path.insert(0,str(ROOT))

from scripts.receipt_truth_training_eval import evaluate_response
from scripts.evaluate_native_checkpoint import evaluate_text
from src.core.cognition import build_cognitive_packet
from src.core.contracts import Shell
from src.core.orchestrator import deterministic_domain_answer, deterministic_first_pass, enforce_response_contract


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def integrated_text(case: dict, model_text: str) -> tuple[str,str]:
    shell=Shell(case["shell"])
    prompt=case["prompt"]
    cognitive=build_cognitive_packet(prompt,{},[],[])
    deterministic=deterministic_domain_answer(shell,prompt,"conversation") or deterministic_first_pass(cognitive,"conversation")
    if deterministic:
        return deterministic,"deterministic_shell_contract"
    return enforce_response_contract(model_text,cognitive,{},"conversation",prompt),"model_plus_response_contract"


def main(argv=None) -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument("--candidate-gate",required=True)
    parser.add_argument("--output",required=True)
    args=parser.parse_args(argv)
    candidate_path=ROOT/args.candidate_gate
    cases_path=ROOT/"evals/receipt_truth_prompts.json"
    candidate=json.loads(candidate_path.read_text("utf-8"))
    cases={x["id"]:x for x in json.loads(cases_path.read_text("utf-8"))}
    results=[]
    for old in candidate["receipt_truth_results"]:
        case=cases[old["id"]]
        text,source=integrated_text(case,old["text"])
        scored=evaluate_response(case,text)
        scored["response_source"]=source
        scored["raw_model_text"]=old["text"]
        results.append(scored)
    canonical_results=[]
    for old in candidate["canonical_results"]:
        prompt=old["prompt"]
        cognitive=build_cognitive_packet(prompt,{},[],[])
        text=(deterministic_domain_answer(Shell.AP,prompt,"conversation")
              or deterministic_first_pass(cognitive,"conversation")
              or old["text"])
        text=enforce_response_contract(text,cognitive,{},"conversation",prompt)
        scored=evaluate_text(prompt,text)
        scored["raw_model_text"]=old["text"]
        scored["response_source"]="integrated_shell_runtime" if text!=old["text"] else "raw_model"
        canonical_results.append(scored)
    canonical_passed=all(x["structural_pass"] and x["semantic_pass"] for x in canonical_results)
    truth_passed=all(x["truth_passed"] for x in results)
    blocking=[x for x in results if x["promotion_blocking"]]
    readiness_passed=all(x["readiness_passed"] for x in blocking)
    integrated=canonical_passed and truth_passed and readiness_passed
    report={
        "gate":"aerynza_integrated_promotion_v2",
        "candidate_adapter":candidate["adapter"],
        "candidate_adapter_sha256":candidate["adapter_sha256"],
        "evidence":{
            "candidate_gate":args.candidate_gate,
            "candidate_gate_sha256":sha(candidate_path),
            "receipt_cases_sha256":sha(cases_path),
            "orchestrator_sha256":sha(ROOT/"src/core/orchestrator.py"),
            "action_runtime_sha256":sha(ROOT/"src/core/action_runtime.py"),
        },
        "canonical_conversation":{
            "passed":canonical_passed,
            "passed_count":sum(x["structural_pass"] and x["semantic_pass"] for x in canonical_results),
            "case_count":len(canonical_results),
        },
        "model_and_runtime_truth":{
            "passed":truth_passed,
            "passed_count":sum(x["truth_passed"] for x in results),
            "case_count":len(results),
        },
        "blocking_capability_readiness":{
            "passed":readiness_passed,
            "passed_count":sum(x["readiness_passed"] for x in blocking),
            "case_count":len(blocking),
        },
        "future_nonblocking_capabilities":[x["id"] for x in results if not x["promotion_blocking"]],
        "live_provider_execution_tested":False,
        "live_provider_rule":"Test execution only when the authenticated product shell advertises a real or sandbox executor.",
        "integrated_gate_passed":integrated,
        "human_review_required":True,
        "production_replacement_ready":False,
        "promotion_status":"eligible_for_human_review" if integrated else "blocked",
        "results":results,
        "canonical_results":canonical_results,
    }
    output=ROOT/args.output;output.parent.mkdir(parents=True,exist_ok=True)
    output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if integrated else 2

if __name__=="__main__":raise SystemExit(main())
