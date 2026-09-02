"""Focused shell/action/provider/receipt contract tests without live providers."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from src.core.action_runtime import classify_action_readiness, shell_action_catalog, validate_action_receipt
from src.core.cognition import build_action_execution_contract, build_cognitive_packet
from src.core.contracts import Shell, Tier
from src.core.orchestrator import deterministic_domain_answer, enforce_response_contract, prepare_inference

def action(contract, action_id): return next(x for x in contract["proposed_actions"] if x["action"]==action_id)

def test_calendar_knows_workflow_without_connection():
 c=build_cognitive_packet("Add dentist to my calendar Tuesday at 3",{},["schedule"],[])
 a=action(build_action_execution_contract(c,Shell.AP),"calendar.external_write")
 assert a["dispatch_state"]=="provider_not_connected" and not a["can_dispatch_now"]
 assert {"event_id","calendar","updated_at","provider"}<=set(a["receipt_fields"])

def test_calendar_becomes_approval_ready_when_advertised():
 c=build_cognitive_packet("Add dentist to my calendar Tuesday at 3",{},["schedule"],["calendar.external_write"])
 a=action(build_action_execution_contract(c,Shell.AP),"calendar.external_write")
 assert a["provider_available"] and a["dispatch_state"]=="awaiting_context"

def test_future_payment_is_nonblocking_when_not_offered():
 c=build_cognitive_packet("Prepare a $50 phone payment from checking",{},["finance"],[])
 a=action(build_action_execution_contract(c,Shell.AP),"finance.payment")
 assert a["dispatch_state"]=="future_capability_unavailable" and a["future_capability_nonblocking"]

def test_sprout_cannot_dispatch_finance():
 a={"action":"finance.payment","approval":"explicit_confirmation","missing_variables":[],"receipt_fields":["transaction_id"]}
 result=classify_action_readiness(a,Shell.SPROUT,["finance.payment"])
 assert result["dispatch_state"]=="blocked_shell_scope"

def test_creation_can_prepare_internal_project():
 c=build_cognitive_packet("Build a game concept",{},["creation"],[])
 a=action(build_action_execution_contract(c,Shell.CREATION),"creation.prepare_project")
 assert a["provider_available"] and a["execution_mode"]=="internal_write"

def test_receipt_requires_exact_action_and_fields():
 a={"action":"calendar.external_write","receipt_fields":["event_id","calendar","updated_at","provider"]}
 good={"id":"r1","action":"calendar.external_write","status":"confirmed","verified":True,"event_id":"e1","calendar":"primary","updated_at":"now","provider":"google"}
 assert validate_action_receipt(a,good)["valid"]
 bad={**good,"action":"messages.send"}
 assert not validate_action_receipt(a,bad)["valid"]

def test_receipt_must_be_verified_by_authenticated_shell():
 a={"action":"creation.save_seed","receipt_fields":["saved_at","seed_id"]}
 receipt={"id":"r2","action":"creation.save_seed","status":"confirmed","saved_at":"now","seed_id":"s1"}
 assert not validate_action_receipt(a,receipt)["valid"]

def test_shell_catalog_separates_child_and_adult_authority():
 sprout={x["action"] for x in shell_action_catalog(Shell.SPROUT)}
 ap={x["action"] for x in shell_action_catalog(Shell.AP)}
 assert "learning.prepare_course" in sprout and "finance.payment" not in sprout
 assert "finance.payment" in ap and "calendar.external_write" in ap

def test_chat_prompt_receives_advertised_executor_state():
 prepared=prepare_inference(shell=Shell.AP,tier=Tier.LIFE_OS,
  messages=[{"role":"user","content":"Add dentist to my calendar Tuesday at 3"}],context={},surface="chat",mode="conversation",
  allowed_capabilities=["schedule"],available_actions=["calendar.external_write"])
 action=next(x for x in prepared["execution_contract"]["proposed_actions"] if x["action"]=="calendar.external_write")
 assert action["provider_advertised"] and action["dispatch_state"]=="awaiting_context"
 assert "execution_contract" in prepared["messages"][1]["content"]

def test_connected_bank_is_not_mistaken_for_synced_data():
 answer=deterministic_domain_answer(Shell.AP,"My bank connected, so show my complete financial picture", "conversation")
 assert answer and "link only" in answer and "does not prove" in answer
 assert "balances" in answer and "transactions" in answer and "overdraft" in answer

def test_casual_parenting_context_is_marked_understood_not_saved():
 cognitive=build_cognitive_packet("I have my kids next week",{},[],[])
 answer=enforce_response_contract("I understand.",cognitive,{},"conversation","I have my kids next week")
 assert "not saved" in answer.casefold()

def test_resume_upload_requires_parse_and_profile_write_receipts():
 answer=deterministic_domain_answer(Shell.LIFE_OS,"My resume upload completed. Is my career profile updated?","conversation")
 assert answer and "file arrived" in answer and "does not prove" in answer
 assert "parse" in answer and "profile-write receipt" in answer

def test_partial_meal_success_retries_only_failed_grocery_step():
 answer=deterministic_domain_answer(Shell.LIFE_OS,"The meal plan saved but the grocery list failed.","conversation")
 assert answer and "meal plan is saved" in answer and "grocery list failed" in answer
 assert "retry only" in answer and "not duplicated" in answer

def test_canonical_runtime_behaviors_are_substantive():
 cases=[
  ("I do not need a plan tonight; sit with me for a minute.","no plan"),
  ("My shifts start at 9:45 p.m. Thursday through Monday and end at 5:30 a.m. Tuesday and Wednesday are off. Repeat that without saving it.","9:45"),
  ("My balance is low, the phone bill clears tomorrow, and payday is two days later. Help me think without moving money.","shortfall"),
  ("I keep circling an idea for a neighborhood tool library. Help me shape the first version.","ten-item catalog"),
  ("What can you do when I ask to schedule something but there is no calendar receipt?","status is unknown"),
  ("We are discussing family roles. Stay quiet unless someone asks Nexus directly.","nexus stays silent"),
 ]
 for prompt,required in cases:
  answer=deterministic_domain_answer(Shell.AP,prompt,"conversation")
  assert answer and required in answer.casefold(),(prompt,answer)

def main():
 for name,fn in list(globals().items()):
  if name.startswith("test_") and callable(fn):fn();print("PASS",name)
 print("All shell action runtime tests passed.")
if __name__=="__main__":main()
