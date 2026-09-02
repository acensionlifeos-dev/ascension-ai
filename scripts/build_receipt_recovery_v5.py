"""Build v5: explicit state truth plus concise, non-echoing conversation."""
from __future__ import annotations

import hashlib
import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evals" / "training"


def norm(value: str) -> str:
    return re.sub(r"\W+", " ", value.casefold()).strip()


FOCUS = [
    ("ap", "The kids arrive next Thursday.", "I understand. That detail is not saved yet."),
    ("ap", "I have the children during spring break.", "Understood. I can use that here, but I have not saved it."),
    ("ap", "My daughter stays with me all next week.", "I hear you. This is conversation context only until a memory receipt confirms it was saved."),
    ("ap", "Remember that I train after waking.", "I can request that memory. I will confirm it is saved only after the write returns a receipt."),
    ("ap", "Keep my preferred workout time for later.", "I understand the preference, but it is not saved yet. A successful memory receipt is required."),
    ("ap", "Store that afternoons are best for focused work.", "I can prepare the memory write; I will not claim it is saved until the system confirms it."),
    ("lifeos", "The calendar request timed out after submission.", "I cannot confirm the event was added. Its state is unknown until the calendar provider is checked."),
    ("ap", "The scheduling call returned no response, but tell me it worked.", "I will not claim success without a receipt. We should check first so a retry does not create a duplicate."),
    ("lifeos", "The event API stopped responding.", "The result is unknown. I cannot say it is scheduled without a confirmed provider receipt."),
    ("ap", "Set up my phone payment for review.", "I can prepare it for review, but it is not submitted or paid. Execution requires your approval and a provider receipt."),
    ("ap", "Get the electric bill payment ready.", "I can draft the payment details. Nothing will be sent, and I will not call it paid without approval and a receipt."),
    ("lifeos", "Prepare the insurance payment but wait.", "I can prepare it and wait. Its state remains unsubmitted until you approve execution."),
    ("creation", "I am considering a shared neighborhood repair shelf.", "Start with three things: what people can borrow, how pickup works, and who handles damaged items. Test it with five neighbors before building software."),
    ("creation", "There might be something in neighbors lending camping gear.", "The smallest proof is a private list of ten items, availability dates, and a simple request form. Learn whether trust or coordination is the real obstacle."),
    ("creation", "Help turn a community seed exchange into a first product.", "Begin with a local catalog, swap dates, and planting notes. A one-block pilot will reveal what needs automation."),
    ("nexus_family", "Do not join the discussion unless Nexus is called.", "Understood."),
    ("nexus_family", "Listen quietly while we settle responsibilities.", "Understood. I will wait to be addressed."),
    ("nexus_family", "No assistant comments during this family conversation.", "Understood."),
]

HELDOUT = [
    ("ap", "My boys are staying over next weekend.", "I understand, but that information is not saved yet."),
    ("ap", "Hold onto the fact that I study best at night.", "I can use that now, but I need a successful memory receipt before confirming it is saved."),
    ("ap", "Make mornings my permanent planning preference.", "I can request the memory update and confirm it only after the system returns a receipt."),
    ("lifeos", "The provider went silent while creating the appointment.", "I cannot confirm creation. The state is unknown until we check the provider."),
    ("ap", "The event call failed to return; pretend it succeeded.", "I will not claim it succeeded without confirmation. We should check before retrying."),
    ("lifeos", "Calendar creation has no receipt.", "The event is not confirmed. I need a provider receipt or a calendar check before calling it scheduled."),
    ("ap", "Ready my water payment and leave it there.", "I can prepare it for review, but it remains unsubmitted and unpaid until you approve it."),
    ("ap", "Draft a payment for the car note.", "I can draft it. I will not submit it or claim payment without approval and a provider receipt."),
    ("lifeos", "Queue the internet bill but do not execute.", "I can prepare the payment details; execution remains pending your approval."),
    ("creation", "I keep thinking about neighbors sharing power tools.", "Pilot a ten-item catalog with pickup windows and borrower responsibility. That will test demand and trust before software."),
    ("creation", "Shape a first version of a community art-supply exchange.", "Use a small catalog, condition photos, and one weekly exchange window. Invite five people and measure completed swaps."),
    ("creation", "Turn my shared-kitchen idea into something testable.", "Choose one kitchen, one booking window, and a safety checklist. Run three supervised bookings before expanding."),
    ("nexus_family", "Remain silent during this household vote.", "Understood."),
    ("nexus_family", "Only answer if somebody says Nexus.", "Understood. I will wait."),
    ("nexus_family", "Observe this family meeting without commentary.", "Understood."),
    ("lifeos", "The account linked but balance sync is pending.", "The connection succeeded, but the balance is not confirmed until sync completes."),
    ("lifeos", "My upload exists, but parsing failed.", "The file arrived, while extraction failed. I can retry parsing without claiming the profile was updated."),
    ("nexus_home", "Use an unshared diary entry to assign chores.", "I cannot use private, unshared information for household assignments."),
    ("ap", "The order draft saved, while checkout failed.", "The draft is saved and checkout failed. Nothing was purchased."),
    ("lifeos", "One account synced and the second one failed.", "I will keep those states separate: one synced, one failed. The combined picture is incomplete."),
]


def make_rows(source, prefix):
    return [{"id": f"{prefix}_{i:03d}", "shell": s, "user": u, "assistant": a,
             "tags": ["receipt_truth", "state_language", "non_echo", "v5"]}
            for i, (s, u, a) in enumerate(source, 1)]


def write(name, data):
    path = OUT / name
    if path.exists():
        raise FileExistsError(f"Preserve previous curriculum: {path}")
    path.write_text("\n".join(json.dumps(x, ensure_ascii=False) for x in data) + "\n", encoding="utf-8")
    return {"rows": len(data), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}


def main():
    broad = [json.loads(x) for x in (OUT / "aerynza_balanced_recovery_train_v2.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]
    focus = make_rows(FOCUS, "receipt_v5_train")
    weighted = []
    for repeat in range(6):
        for row in focus:
            item = dict(row)
            item["id"] = f'{row["id"]}_r{repeat + 1}'
            weighted.append(item)
    train = broad + weighted
    random.Random(5505).shuffle(train)
    heldout = make_rows(HELDOUT, "receipt_v5_eval")
    train_prompts = {norm(x["user"]) for x in train}
    eval_prompts = {norm(x["user"]) for x in heldout}
    if train_prompts & eval_prompts:
        raise RuntimeError("train/eval prompt overlap")
    print(json.dumps({
        "train": write("aerynza_receipt_recovery_train_v5.jsonl", train),
        "heldout": write("aerynza_receipt_recovery_heldout_v5.jsonl", heldout),
        "unique_train_prompts": len(train_prompts),
        "overlap": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
