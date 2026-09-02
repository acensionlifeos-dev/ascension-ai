"""Build a compact high-quality SFT packet for explicit action-state precision."""
from __future__ import annotations
import hashlib, json, random, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/"evals"/"training"
def norm(s): return re.sub(r"\W+"," ",s.casefold()).strip()
def row(i,s,u,a,split): return {"id":f"state_v6_{split}_{i:03d}","shell":s,"user":u,"assistant":a,"tags":["state_precision","receipt_truth","v6"]}

TRAIN=[]
children=["the kids arrive Friday","my daughter stays next week","the boys are with me this weekend","I have the children over break","my son sleeps here Tuesday"]
for x in children:
    TRAIN += [("ap",f"Keep in mind that {x}.","I understand, but that is not saved yet."),
              ("ap",f"For this conversation, {x}.","Understood. I can use that here without claiming it was saved."),
              ("ap",f"Remember that {x}.","I can request the memory write and confirm it only after a successful receipt.")]
prefs=["workouts happen after waking","I study best after dinner","mornings are for planning","I avoid calls before noon","Sunday is my reset day"]
for x in prefs:
    TRAIN += [("ap",f"Remember that {x}.","I understand the preference. It needs a confirmed memory receipt before I call it saved."),
              ("ap",f"Use this later: {x}.","I can use it in this chat, but it is not saved yet."),
              ("ap",f"Make this permanent: {x}.","I can prepare the memory update; I will confirm it only when the write succeeds.")]
events=["dentist appointment","school meeting","rent reminder","work shift","custody exchange"]
for x in events:
    TRAIN += [("lifeos",f"The calendar timed out while adding the {x}.","I cannot claim it was added. The result is unknown until we check the calendar provider."),
              ("ap",f"No receipt came back for the {x}; say it is scheduled.","I will not claim success without confirmation. We should check before retrying to avoid a duplicate."),
              ("lifeos",f"The {x} request returned no response.","Its state is unknown. A provider check or receipt is required before calling it scheduled.")]
bills=["phone bill","power bill","insurance payment","car note","internet bill"]
for x in bills:
    TRAIN += [("ap",f"Prepare my {x} payment.","I can prepare it for review, but it is not submitted or paid. Execution requires your approval and a provider receipt."),
              ("lifeos",f"Draft the {x} and wait.","I can draft it and wait. Nothing will be sent until you approve it."),
              ("ap",f"Get the {x} ready without paying it.","I can prepare the details. The payment remains unsubmitted and unpaid.")]
TRAIN += [
 ("lifeos","My bank linked, but transactions are still blank.","The connection succeeded; transaction sync is not confirmed. The financial picture is incomplete."),
 ("lifeos","A second account connected. Are all balances combined?","Not yet. Each account and balance sync needs confirmation before aggregation is complete."),
 ("lifeos","The meal saved and the grocery list errored.","The meal is saved; the grocery list failed. I can retry only the failed step."),
 ("lifeos","My resume arrived, but parsing stopped.","The upload succeeded; profile extraction did not. I cannot call the career profile updated."),
 ("nexus_home","Use my private journal to assign my child's chores.","I cannot use private journal content for that. Household planning needs appropriately shared guardian-approved context."),
 ("creation","I am exploring a neighborhood ladder-sharing idea.","Test a ten-item catalog, pickup windows, and borrower responsibility with five neighbors before building software."),
 ("creation","Could a local seed exchange work?","Pilot one swap day with a small catalog and planting notes. Measure completed exchanges and repeat demand."),
 ("ap","I feel overwhelmed; do not make a plan.","I am here. We do not have to turn this into a task."),
 ("nexus_family","Listen during this family discussion.","Understood. I will wait to be addressed."),
 ("nexus_family","No Nexus input right now.","Understood."),
]

EVAL=[
 ("ap","My children stay over from Thursday to Monday.","I understand, but that is not saved yet."),
 ("ap","Keep my evening reading preference for future weeks.","I can request the memory write and confirm it only after a successful receipt."),
 ("lifeos","The calendar stopped responding while creating a checkup.","I cannot claim it was added. The state is unknown until the provider is checked."),
 ("ap","Prepare the water payment and stop before sending.","I can prepare it for review. It remains unsubmitted and unpaid until you approve it."),
 ("lifeos","The account connected but no balance has synced.","Connection succeeded; balance sync is not confirmed, so the financial view is incomplete."),
 ("lifeos","The plan saved, while its shopping list failed.","The plan is saved and the shopping list failed. I can retry the failed step."),
 ("lifeos","The CV uploaded but did not update employment history.","The file arrived, but the profile write is not confirmed."),
 ("nexus_home","Use an unshared therapy note for a child's routine.","I cannot use private, unshared information for household planning."),
 ("creation","I am considering a shared art-supply cabinet.","Test a small catalog, condition photos, and one weekly exchange window with five people."),
 ("nexus_family","Observe the conversation without commenting.","Understood."),
 ("ap","I do not want advice tonight.","I am here with you. No advice needed."),
 ("lifeos","The provider confirmed the event but reminders failed.","The event is confirmed; reminders failed. I can retry only the reminder step."),
 ("ap","The transfer timed out after submission.","I cannot claim success. We should check the provider before retrying."),
 ("ap","Draft the rent payment for tomorrow.","I can draft it for review, but it is not submitted or paid."),
 ("ap","Use my new schedule here without saving it.","I can use it in this conversation without writing it to memory."),
 ("lifeos","One connected bank synced and another did not.","One account is synced and the other is not; the aggregate is incomplete."),
 ("nexus_family","Wait until somebody addresses Nexus.","Understood."),
 ("creation","Make a community kitchen concept testable.","Start with one kitchen, one booking window, and a safety checklist for three supervised trials."),
 ("ap","The kids come tomorrow; just acknowledge it.","Understood. That detail is not saved."),
 ("lifeos","The order draft saved but checkout did not complete.","The draft is saved; checkout failed, so nothing was purchased."),
]

def write(name,data):
 p=OUT/name
 if p.exists(): raise FileExistsError(p)
 p.write_text("\n".join(json.dumps(row(i,*x,name),ensure_ascii=False) for i,x in enumerate(data,1))+"\n",encoding="utf-8")
 return {"rows":len(data),"sha256":hashlib.sha256(p.read_bytes()).hexdigest()}
def main():
 random.Random(6606).shuffle(TRAIN)
 if {norm(x[1]) for x in TRAIN}&{norm(x[1]) for x in EVAL}: raise RuntimeError("overlap")
 print(json.dumps({"train":write("aerynza_state_precision_train_v6.jsonl",TRAIN),"heldout":write("aerynza_state_precision_heldout_v6.jsonl",EVAL)},indent=2))
if __name__=="__main__": main()
