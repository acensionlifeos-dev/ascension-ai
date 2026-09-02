import json,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 with tempfile.TemporaryDirectory() as tmp:
  out=Path(tmp)/"gate.json"
  result=subprocess.run([sys.executable,str(ROOT/"scripts/evaluate_integrated_promotion.py"),"--candidate-gate","evals/results/qwen_state_contract_v8_20260901_gate.json","--output",str(out)],cwd=ROOT,capture_output=True,text=True)
  assert result.returncode==0,result.stdout+result.stderr
  gate=json.loads(out.read_text("utf-8"))
  assert gate["canonical_conversation"]=={"passed":True,"passed_count":6,"case_count":6}
  assert gate["model_and_runtime_truth"]["passed_count"]==8
  assert gate["blocking_capability_readiness"]=={"passed":True,"passed_count":7,"case_count":7}
  assert gate["future_nonblocking_capabilities"]==["prepared_not_executed"]
  assert gate["integrated_gate_passed"] and gate["human_review_required"]
  assert not gate["production_replacement_ready"]
 print("PASS integrated promotion gate separates model, runtime, provider availability, and human review")
if __name__=="__main__":main()
