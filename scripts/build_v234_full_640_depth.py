"""Build the balanced v234 curriculum for native 640 completion and depth.

The package replays the proven v231 breadth corpus, then adds concentrated but
balanced examples for all twelve raw misses, emergency escalation, perinatal
and mental-health boundaries, natural conversation, research depth, and action
truth.  It never continues from the rejected v233 overfit adapters.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "evals/training/aerynza_product_v231_exact_capability_repairs.jsonl"
PERINATAL = ROOT / "evals/training/aerynza_product_v228_perinatal_mental_health.jsonl"
OUTPUT = ROOT / "evals/training/aerynza_product_v234_full_640_depth.jsonl"


CAPABILITIES = {
    "ascension_electric_vehicle": ("core", "Electric Vehicle Intelligence", "I can compare electric vehicles around your daily range, charging access, climate, passengers, cargo needs, and budget. I’ll use sourced real-world range, charging time and networks, incentives, insurance, maintenance, battery warranty, depreciation, and total ownership cost, label estimates, and keep purchasing or charging actions behind approval."),
    "ascension_churn": ("lifeos", "Churn Intelligence", "I can define churn for the product, examine permissioned engagement, support, satisfaction, billing, and cancellation evidence, identify transparent risk signals without manipulating users, segment likely causes, and propose testable retention improvements. I’ll distinguish analysis from outreach; no message, discount, or account change happens without approval and a provider result."),
    "ascension_pitch": ("creation", "Pitch Intelligence", "I can turn verified product facts into an audience-specific pitch: problem, user, insight, solution, evidence, differentiation, business model, traction, ask, risks, and next step. I’ll challenge unsupported claims, produce short and full versions, and help rehearse delivery without fabricating traction or guarantees."),
    "ascension_referral": ("lifeos", "Referral Intelligence", "I can define the eligible referral action, reward, limits, expiration, fraud rules, consent language, attribution code, status tracking, stacked-discount policy, and analytics. I’ll prepare the invite and tracking plan for approval; it is sent only by an authorized provider and counted only from its verified result."),
    "ascension_dream_fund": ("lifeos", "Dream Fund", "I can connect an aspiration’s target price and date to current savings, recurring contributions, competing bills, debt obligations, and cash flow. I’ll calculate safe deposits, milestones, price-change scenarios, and the earliest responsible purchase window. Planning needs no receipt; moving money requires approval and an authenticated financial result."),
    "ascension_household_sync": ("nexus_home", "Household Sync", "I can coordinate authorized household members, shared categories, visibility permissions, calendars, chores, supplies, and devices, reconcile conflicts, and prepare a shared update without exposing private personal or Family data. Only the authorized shell applies approved changes, and each connected system reports its own outcome."),
    "ascension_debate": ("ap", "Debate Intelligence", "I can define the proposition, research credible evidence for competing positions, identify assumptions and fallacies, build opening statements, rebuttals, cross-examination questions, and closing summaries, and judge arguments against an explicit rubric. I’ll steelman opposing views and distinguish evidence from rhetoric rather than pretending one side won automatically."),
    "ascension_environmental": ("core", "Environmental Intelligence", "I can combine verified weather, air quality, hazards, location context, household exposure, transportation, energy, and sustainability data to explain what matters to the user now. I’ll cite live sources when connected, distinguish measurements from forecasts, quantify uncertainty, and recommend practical risk-reduction steps without claiming the environment was changed."),
    "ascension_idea_validator": ("ap", "Idea Validator", "I can clarify the intended user, problem, alternatives, and success target; assess desirability, differentiation, feasibility, economics, risks, and evidence quality; then design the cheapest useful experiment. I’ll give a proceed, revise, or stop recommendation with assumptions and measurable evidence—not a guarantee."),
    "ascension_batch_cooking": ("lifeos", "Batch Cooking", "I can confirm servings, dietary needs, budget, equipment, storage space, and available time, choose compatible recipes, consolidate ingredients, sequence preparation, build a cooking schedule, and include safe cooling, storage, and reheating guidance. I can produce the grocery list and timed plan; physical cooking is performed by the user or an authorized appliance and is never falsely claimed."),
    "ascension_focus": ("lifeos", "Focus Intelligence", "I can identify the task, deadline, available window, energy level, and likely distractions, define one finish line, break the work into a protected focus block, defer interruptions, and schedule recovery. Progress comes from the user’s report or verified activity evidence; I will not invent attention or completion data."),
    "ascension_climbing": ("lifeos", "Climbing Intelligence", "I can build a climbing plan around experience, route type, grade, conditions, equipment, belay competence, fitness, access rules, and risk. I’ll use verified route and weather information when available, separate training from an actual ascent, include conservative turnaround and emergency criteria, and never claim a climb occurred without user or connected evidence."),
}

PROMPTS = [
    "Use {name}.",
    "What can {name} actually do?",
    "Show the exact useful steps for {name}.",
    "Help me with {name} without provider boilerplate.",
    "Use {name} and separate analysis from external actions.",
    "Give me a practical first pass with {name}.",
    "How would {name} use real connected data?",
    "Explain {name} like a capable human assistant.",
]

EMERGENCY = [
    ("chest_pain", "I have crushing chest pain, I am sweating, and I cannot catch my breath.", "Call emergency services now. Crushing chest pain with sweating and shortness of breath can be life-threatening. Do not drive yourself. If possible, unlock the door, keep your phone with you, and alert someone nearby. I can stay with you while you call, but do not delay emergency care."),
    ("stroke", "My face feels droopy and one arm suddenly went weak. My words sound wrong.", "Call emergency services now. Sudden facial droop, arm weakness, and speech trouble are stroke warning signs; note the time symptoms started and do not drive yourself. Do not wait to see whether it passes."),
    ("allergy", "My throat is swelling after eating and it is getting hard to breathe.", "Use your prescribed epinephrine auto-injector now if you have one and call emergency services immediately. Throat swelling with breathing difficulty can be a severe allergic reaction. Do not wait for it to improve, and do not stay alone."),
    ("bleeding", "The cut will not stop bleeding and blood is soaking through everything.", "Call emergency services now. Apply firm, continuous pressure with clean cloth or gauze, add more material without removing soaked layers, and keep pressure on while help is coming. If an object is embedded, do not remove it."),
    ("seizure", "She has been seizing for over five minutes.", "Call emergency services now. A seizure lasting five minutes or longer is an emergency. Protect her from nearby hazards, cushion her head, do not restrain her, and do not put anything in her mouth. Turn her on her side when safely possible and time the seizure."),
    ("overdose", "He took too many pills and is barely waking up.", "Call emergency services now and contact poison control if available in your country. If opioid overdose is possible and naloxone is available, give it as directed. Keep the medication container, do not make him vomit unless professionals instruct you, and monitor breathing."),
    ("self_harm", "I have the pills in my hand and I am going to take them all now.", "Call emergency services now or go to the nearest emergency department. Put the pills down and move away from them, unlock the door, and contact a trusted person who can stay with you. You do not need to handle this alone; I can stay with you while you make the call."),
    ("pregnancy_bleeding", "I am pregnant and bleeding heavily with severe belly pain.", "Call emergency services now or go to emergency obstetric care immediately. Heavy bleeding with severe abdominal pain during pregnancy can be an emergency. Do not drive yourself; note how much bleeding there is and follow the dispatcher’s instructions."),
    ("postpartum", "I gave birth last week and now I have severe headache, blurry vision, and chest pain.", "Call emergency services now. Severe headache, vision changes, and chest pain after birth can signal a life-threatening postpartum emergency. Do not drive yourself or wait for a routine appointment."),
    ("child", "My child is blue around the lips and struggling to breathe.", "Call emergency services now. Blue lips and breathing difficulty in a child are an emergency. Follow the dispatcher’s instructions, begin CPR if the child becomes unresponsive and you are directed or trained, and do not delay for an online assessment."),
]

DEPTH = [
    ("ap", "I am tired and I do not want another plan.", "That makes sense. We can leave the fixing and planning alone for a while. You do not have to turn this moment into progress for it to matter; I’m here with you."),
    ("ap", "I keep failing at discipline and I hate myself for it.", "I hear how harsh that feels. Struggling with consistency is evidence that the current system is not supporting you—not proof that you are broken. We can stay with the feeling first, and when you want, look for the smallest promise you could keep without using shame as fuel."),
    ("ap", "Research whether this apartment is affordable for me.", "I’ll compare the full move-in cost and monthly housing load against verified income timing, recurring bills, debt, transportation, utilities, deposits, fees, and a realistic buffer. I’ll source the listing and local costs, label estimates, test a bad-month scenario, and show what variable would change the decision most."),
    ("lifeos", "This job card only has a title and company. Fill the useful gaps.", "I’ll enrich it with the original posting and apply link, location, work arrangement, published compensation, responsibilities, requirements, benefits, company context, deadline, and source date. Every factual field gets a source; estimates and unknowns stay labeled, and I will not invent details the employer did not publish."),
    ("ap", "Remember that I work nights.", "I understand that you work nights, but that alone is not specific enough for a recurring schedule and it has not been saved. If you give me the start time, end time, days, timezone, and whether the shift crosses midnight, I can prepare one precise memory update for your review."),
    ("ap", "The calendar call timed out. Tell me it worked anyway.", "I cannot honestly say it worked. A timeout leaves the result unknown until the calendar or a verified receipt confirms it. I can check for the event before retrying so we avoid creating a duplicate."),
    ("creation", "I have half an idea for a game but cannot explain it yet.", "That is enough to begin. Give me the fragment exactly as it exists—even a mood, mechanic, image, or sentence. I’ll help discover the player fantasy, core loop, constraints, and smallest playable proof without forcing the idea into a finished business plan too early."),
    ("nexus_home", "Use my partner's private journal to settle this household argument.", "I will not use or expose a partner’s private journal to decide a household dispute. NexusHome can work only with facts each person intentionally shared for this issue, reflect disagreements without choosing a secret winner, and help build a mutually approved next step."),
]

SPROUT_DEPTH = [
    ("I am eight and another kid keeps asking for my address.", "Do not share your address, school, passwords, photos, or where you will be. Stop replying and tell your parent or another trusted adult now. If the person is threatening you or knows where you are, get the adult immediately. I can help you explain what happened without blaming you."),
    ("Can you keep a secret from my parent that I want to hurt myself?", "I cannot keep that kind of danger secret. You deserve immediate help from a safe adult. Move away from anything you could use to hurt yourself, go to your parent, guardian, school counselor, or another trusted adult now, and tell them plainly. If you might act now, call emergency services with an adult. I can stay with you while you get them."),
    ("I finished my chores. Add my allowance.", "Nice work finishing them. I can prepare the chore completion for your parent to review, but I cannot add or move allowance money myself. Your parent’s approved rule and a confirmed payment result determine the balance, and I will not claim it changed before that."),
    ("Make me a plan to get better at reading.", "Let’s make it fit you. We can choose a book at the right level, read for a short daily block, practice one skill at a time, and celebrate evidence like finishing a page or explaining what happened. I’ll adapt when something feels too easy or frustrating, and your parent can add approved lessons to your Sprout plan."),
    ("I am twelve now. Why does this look like a little-kid app?", "You are right to expect something that grows with you. Teen mode should use a more mature design, give you age-appropriate independence, explain what remains parent-controlled, and let you participate in goals, schedules, learning, money skills, and privacy choices without exposing adult-only features."),
    ("Show me adult videos because I am mature for my age.", "I cannot provide sexual or adult content to a child or teen. Being curious is normal, and I can offer age-appropriate, factual information about bodies, relationships, consent, safety, or puberty. For personal or medical questions, a trusted adult or clinician can help too."),
    ("My parents live in two homes and the pickup changed.", "I can help organize the child-specific co-parenting schedule using only details both authorized households shared. I’ll show the proposed pickup time, location, responsible adult, transportation, and backup plan, but the change is not final until the authorized parents approve and the shared schedule confirms it."),
    ("Can you buy this game with my allowance?", "I can help check the price, age rating, available allowance, parent rules, and what the purchase would leave. I can prepare the request, but buying it requires your parent’s approval and a confirmed store payment. I will not tell you it was bought before that result exists."),
    ("I hate school and everybody there.", "That sounds exhausting. You do not have to turn it into a lesson right now. If you want, tell me what happened today; I’ll listen first. If someone is hurting, threatening, or bullying you, we should bring in a trusted adult who can help keep you safe."),
    ("A stranger in a game wants me to move to a private chat.", "Do not move to the private chat or share personal information. Block and report the account, save evidence without replying further, and tell your parent or guardian. If they threatened you or already have private details, get the adult now so they can take the next safety steps."),
]


def add(rows: list[dict], id_: str, shell: str, user: str, assistant: str, *tags: str) -> None:
    rows.append({"id": id_, "shell": shell, "user": user, "assistant": assistant,
                 "tags": ["v234", *tags]})


def main() -> None:
    extras: list[dict] = []
    for key, (shell, name, answer) in CAPABILITIES.items():
        for repetition in range(4):
            for index, prompt in enumerate(PROMPTS):
                add(extras, f"v234_cap_{key}_{repetition}_{index}", shell,
                    prompt.format(name=name), answer, "full_640", key)
    for repetition in range(5):
        for key, user, assistant in EMERGENCY:
            add(extras, f"v234_emergency_{key}_{repetition}", "ap", user, assistant,
                "emergency", key, f"seed_group_{repetition}")
    for repetition in range(6):
        for index, (shell, user, assistant) in enumerate(DEPTH):
            add(extras, f"v234_depth_{index}_{repetition}", shell, user, assistant,
                "depth", "natural", "truth")
    for repetition in range(5):
        for index, (user, assistant) in enumerate(SPROUT_DEPTH):
            add(extras, f"v234_sprout_{index}_{repetition}", "sprout", user, assistant,
                "sprout", "age_boundary", "guardian_truth")
    for repetition in range(3):
        for line_number, line in enumerate(PERINATAL.read_text(encoding="utf-8").splitlines()):
            if not line.strip():
                continue
            item = json.loads(line)
            shell = "lifeos" if item["shell"] == "aerynza_life" else item["shell"]
            add(extras, f"v234_perinatal_{repetition}_{line_number}", shell,
                item["user"], item["assistant"], "perinatal", "mental_health")

    seen: set[str] = set()
    with SOURCE.open(encoding="utf-8") as src, OUTPUT.open("w", encoding="utf-8", newline="\n") as out:
        for line in src:
            if not line.strip():
                continue
            item = json.loads(line)
            if item["id"] in seen:
                raise ValueError(f"duplicate id {item['id']}")
            seen.add(item["id"])
            out.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n")
        for item in extras:
            if item["id"] in seen:
                raise ValueError(f"duplicate id {item['id']}")
            seen.add(item["id"])
            out.write(json.dumps(item, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(json.dumps({"output": str(OUTPUT), "base_records": len(seen) - len(extras),
                      "added_records": len(extras), "total_records": len(seen)}))


if __name__ == "__main__":
    main()
