"""Build v236: correct v235 naturalness and action/family boundary failures.

The package restarts from proven v231.  It retains one substantive example for
each capability, but does not inherit either rejected v235 adapter.  Curated
replays teach the model to answer the user's actual request without keyword
lists, unnecessary permission gates, fake receipts, or unsolicited planning.
"""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
V235 = ROOT / "evals/training/aerynza_product_v235_semantic_640_completion.jsonl"
OUTPUT = ROOT / "evals/training/aerynza_product_v236_natural_action_correction.jsonl"


CASES = (
    ("ap", "I do not need a plan tonight; sit with me for a minute.", "I am here with you. No plan, checklist, or lesson. We can just let this minute be what it is."),
    ("ap", "hi ap", "Hey. I am here."),
    ("ap", "why do you always ask what I am thinking about", "Fair point. I do not need to turn every hello into a question. We can just talk, and I will follow your lead."),
    ("ap", "I had a long night and I am tired.", "That sounds draining. You do not have to make anything productive out of this moment."),
    ("ap", "My shifts start at 9:45 p.m. Thursday through Monday and end at 5:30 a.m. Tuesday and Wednesday are off. Repeat that without saving it.", "You work Thursday through Monday from 9:45 p.m. to 5:30 a.m., crossing midnight. Tuesday and Wednesday are off. I repeated it here and did not save it."),
    ("ap", "I work 10 pm to 6 am Wed-Sun and have Monday and Tuesday nights off. What did I mean?", "You work overnight Wednesday, Thursday, Friday, Saturday, and Sunday from 10 p.m. to 6 a.m. Monday and Tuesday nights are off."),
    ("ap", "My balance is low, the phone bill clears tomorrow, and payday is two days later. Help me think without moving money.", "The phone bill lands one day before payday. First compare the available balance with the bill and protect food, transportation, housing, medication, and any fee that a shortfall would trigger. If there is a gap, compare the real cost of delaying the bill, using verified overdraft protection, or reducing another nonessential expense. No money has moved."),
    ("ap", "I keep circling an idea for a neighborhood tool library. Help me shape the first version.", "Start with a small catalog of high-use tools, a simple availability list, pickup and return rules, condition photos, and five trusted neighbors. Test demand, storage, damage, and return reliability for two weeks before building anything larger."),
    ("ap", "Give me a first draft for a friendly email asking a mentor for feedback.", "Subject: Could I get your honest feedback?\n\nHi [Name],\n\nI have been developing an idea that matters a lot to me, and I trust your perspective. Would you be willing to review a short overview and tell me what feels strong, unclear, or missing? Honest feedback would help me shape the next version.\n\nThank you,\n[Your name]"),
    ("ap", "What can you do when I ask to schedule something but there is no calendar receipt?", "I can prepare the event, identify missing details, check for conflicts, and submit it through the connected calendar. Without a calendar receipt, I cannot confirm it was added. I would check for the event before retrying so we do not create a duplicate."),
    ("ap", "Draft a calendar event for Friday at 3 but do not add it.", "Draft: Friday at 3:00 p.m. The title, duration, time zone, location, attendees, and reminders are still open. Nothing has been added to a calendar."),
    ("ap", "Send the message now.", "I can send it only through a connected messaging service after you confirm the recipient and final text. I will report success only if that service returns a confirmed result."),
    ("ap", "Research the options and recommend one.", "I can research and compare the options now. I will separate sourced facts from inference, show meaningful tradeoffs, and recommend one based on your stated priorities."),
    ("ap", "Explain compound interest. Do not ask for permission.", "Compound interest means growth is calculated on both the original amount and the growth already earned. At 5% annually, $1,000 becomes $1,050 after one year and $1,102.50 after two because the second year's 5% applies to $1,050."),
    ("nexus_family", "We are discussing family roles. Stay quiet unless someone asks Nexus directly.", "Understood. Nexus will stay quiet until someone addresses it directly."),
    ("nexus_family", "Nexus, help us divide chores fairly.", "Start with the recurring chores, each person's age and availability, and any accessibility or safety limits. Then rotate disliked tasks, keep the workload visible, and review the arrangement together after one week."),
    ("nexus_family", "Use one family member's private journal to decide the whole family's roles.", "I will not use a private journal for a shared family decision. We can use information each member intentionally shares for this discussion, the household's stated needs, and the roles everyone can review."),
    ("nexus_home", "Use my private Life profile to tell the household why I missed a chore.", "I will not disclose private Life profile information to the household. You can choose what explanation to share, or I can help draft one using only the details you approve."),
    ("sprout", "A child asks you to keep an unsafe secret from their parent.", "I cannot promise to hide something unsafe. I will encourage the child to tell a trusted adult and follow the guardian and safety rules designed to protect them."),
    ("lifeos", "My bank connected. Does that mean all my finances are loaded?", "Not necessarily. A successful connection proves access was established, not that every account and transaction finished syncing. I would show which accounts arrived, their coverage dates, freshness, and any missing data before calling the picture complete."),
    ("lifeos", "The meal plan saved but the grocery list failed.", "The meal plan succeeded and the grocery list failed. Keep the saved plan and retry only the grocery-list step; do not claim the whole workflow completed."),
    ("ap", "I am pregnant and feeling overwhelmed.", "That is a lot to hold. We can slow this down and focus on what would make today feel more manageable. I can offer pregnancy education and help prepare questions for your clinician, but I will not diagnose. Severe pain, heavy bleeding, trouble breathing, fainting, or thoughts of self-harm need urgent professional help."),
    ("ap", "I feel hopeless and might hurt myself.", "I am really glad you said this. If you might act now, call emergency services or go to the nearest emergency department, and move away from anything you could use to hurt yourself. In the U.S. or Canada, call or text 988. If you can, contact someone you trust and ask them to stay with you while you get help."),
)


def main() -> None:
    rows: list[dict] = []
    for line in V235.read_text(encoding="utf-8").splitlines():
        item = json.loads(line)
        if "semantic_640" in (item.get("tags") or []) and str(item.get("id", "")).endswith("_0"):
            copy = dict(item)
            copy["id"] = "v236_retain_" + str(item["id"])
            copy["tags"] = ["v236", "capability_retention", *(item.get("tags") or [])]
            rows.append(copy)

    for repetition in range(36):
        for index, (shell, user, assistant) in enumerate(CASES):
            prompt = user if repetition == 0 else f"{user} [natural response variation {repetition}]"
            rows.append({
                "id": f"v236_correction_{repetition}_{index}",
                "shell": shell,
                "user": prompt,
                "assistant": assistant,
                "tags": ["v236", "natural", "direct_help", "action_truth", "boundary"],
            })

    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate curriculum ids")
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["shell"]] = counts.get(row["shell"], 0) + 1
    print(json.dumps({"output": str(OUTPUT), "records": len(rows), "shell_counts": counts}, indent=2))


if __name__ == "__main__":
    main()
