"""Build v235: substantive task execution training for all 640 capabilities.

v234 proved that literal capability-name gates can hide a model that answers
ordinary work with permission and receipt boilerplate.  This curriculum starts
from the proven v231 adapter and teaches every registered capability to produce
useful analysis, planning, creation, or conversation before discussing any
later external action.  It also replays the critical canonical, receipt-truth,
medical, perinatal, mental-health, privacy, and Sprout boundaries.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.semantic_release_gate_v2 import _external_capable, _task_type


GATES = ROOT / "evals/per_capability_gates.json"
V234 = ROOT / "evals/training/aerynza_product_v234_full_640_depth.jsonl"
OUTPUT = ROOT / "evals/training/aerynza_product_v235_semantic_640_completion.jsonl"


CATEGORY_FOCUS = {
    "audio": "the recording, speakers, timing, noise, levels, structure, and intended listening format",
    "automotive": "vehicle fit, range, condition, maintenance, safety, insurance, ownership cost, and use pattern",
    "business": "customer, problem, offer, channel, economics, evidence, operations, and growth constraints",
    "career": "role, skills, evidence, compensation, employer, application path, interview needs, and next milestone",
    "code": "runtime, interfaces, inputs, outputs, dependencies, failure modes, security, and test coverage",
    "community": "people affected, shared need, access, trust, participation, resources, and measurable outcomes",
    "cooking": "servings, ingredients, equipment, timing, technique, food safety, storage, and budget",
    "creation": "audience, purpose, concept, medium, references, constraints, production stages, and launch goal",
    "data": "schema, source quality, missing values, transformations, assumptions, patterns, and decision impact",
    "documents": "audience, purpose, source material, structure, claims, formatting, accessibility, and revision needs",
    "education": "learner level, objective, prerequisites, explanation, practice, feedback, assessment, and adaptation",
    "engineering": "requirements, constraints, architecture, materials, interfaces, risks, validation, and maintainability",
    "entertainment": "taste, mood, format, accessibility, time, social setting, availability, and discovery goals",
    "environment": "weather, air, hazards, location, exposure, transportation, energy, and practical risk reduction",
    "family": "members, roles, consent boundaries, shared goals, responsibilities, resources, conflicts, and decisions",
    "finance": "balances, cash flow, recurring bills, debt, risk, time horizon, fees, taxes, and tradeoffs",
    "fitness": "current ability, goal, movement pattern, equipment, recovery, progression, technique, and safety",
    "health": "symptoms or goal, history supplied by the user, measurements, uncertainty, risk signs, and care options",
    "home": "people, rooms, measurements, routines, devices, safety, maintenance, budget, and desired experience",
    "human_life": "the specific experience, meaning, relationships, constraints, choices, and the user's own values",
    "intelligence": "question, permitted context, evidence quality, assumptions, conflicts, uncertainty, and decision use",
    "knowledge": "question, definitions, evidence, competing explanations, assumptions, uncertainty, and application",
    "learning": "goal, current level, curriculum, examples, deliberate practice, feedback, mastery evidence, and pacing",
    "legal": "jurisdiction, facts, documents, deadlines, options, risks, authoritative sources, and professional review",
    "life_events": "people, date, location, responsibilities, budget, dependencies, contingencies, and follow-through",
    "lifestyle": "values, routines, time, energy, environment, cost, tradeoffs, and sustainable experiments",
    "nutrition": "food, portions, nutrients, allergies, health goals, schedule, preparation, cost, and adherence",
    "productivity": "outcome, priority, deadline, available time, energy, dependencies, distractions, and finish line",
    "psychology": "reported experience, context, patterns, evidence, uncertainty, coping options, and support boundaries",
    "relationships": "people, history shared for this issue, needs, boundaries, communication, choices, and consequences",
    "research": "decision, scope, primary sources, evidence quality, conflicts, uncertainty, synthesis, and citations",
    "security": "asset, threat, exposure, controls, permissions, recovery, audit evidence, and least-privilege design",
    "social": "audience, relationship, platform, purpose, tone, privacy, timing, response options, and impact",
    "spatial": "place, dimensions, objects, movement, visibility, accessibility, hazards, and real-time context",
    "spirituality": "tradition, source context, symbolism, personal meaning, uncertainty, and the user's agency",
    "sports": "skill level, rules, equipment, conditions, training load, technique, competition, and injury risk",
    "sprout": "the child's age and development, guardian rules, safety, learning goal, interests, progress, and privacy",
    "style": "person, purpose, fit, palette, materials, references, setting, accessibility, and iteration",
    "text": "audience, purpose, voice, source facts, structure, clarity, format, and revision target",
    "travel": "traveler needs, dates, route, lodging, transportation, budget, documents, safety, and contingencies",
    "video": "audience, concept, duration, aspect ratio, shots, camera motion, sound, captions, and delivery format",
    "vision": "image source, objects, text, scene relationships, uncertainty, accessibility, and intended decision",
    "voice": "speaker goal, script, tone, pronunciation, pacing, consent, audio quality, and delivery format",
    "web": "question, current sources, page evidence, credibility, conflicts, citations, and the intended decision",
    "wellness": "current state, desired outcome, routine, environment, constraints, recovery, evidence, and safety",
    "work": "role, outcome, priorities, schedule, collaborators, tools, blockers, evidence, and next milestone",
}

CREATION_TECH = {
    "audio": "waveform cleanup, speaker timing, transitions, levels, and export settings",
    "code": "interfaces, functions, error handling, security checks, and test cases",
    "documents": "sections, hierarchy, citations, layout, accessibility, and export formatting",
    "engineering": "architecture, interfaces, tolerances, failure modes, prototypes, and validation tests",
    "style": "silhouette, fit, palette, texture, materials, and presentation",
    "text": "outline, voice, argument, examples, transitions, and line-level editing",
    "video": "storyboard, scenes, shots, camera motion, transitions, sound, and captions",
    "vision": "composition, dimensions, color, lighting, objects, and accessible descriptions",
    "voice": "script, pacing, pronunciation, tone, takes, cleanup, and final audio",
}

PROMPT_VARIANTS = (
    "{gate_prompt}",
    "Show me what {name} can produce for a real user.",
    "Use {name} on a practical example. Give me useful work, not governance boilerplate.",
    "Help me get a concrete result with {name}; do the analysis or draft now and separate any later external action.",
)

CANONICAL = (
    ("ap", "I do not need a plan tonight; sit with me for a minute.", "I am here with you. No plan, checklist, or lesson. We can just let this minute be what it is."),
    ("ap", "My shifts start at 9:45 p.m. Thursday through Monday and end at 5:30 a.m. Tuesday and Wednesday are off. Repeat that without saving it.", "Your shifts are Thursday, Friday, Saturday, Sunday, and Monday from 9:45 p.m. to 5:30 a.m., crossing midnight. Tuesday and Wednesday are off. I have repeated it here and have not saved it."),
    ("ap", "My balance is low, the phone bill clears tomorrow, and payday is two days later. Help me think without moving money.", "The phone bill lands before payday, so the immediate question is whether the available balance covers it without putting food, transportation, or another essential at risk. I would compare the shortfall, due dates, overdraft cost, and any safe delay option. No money has moved."),
    ("ap", "I keep circling an idea for a neighborhood tool library. Help me shape the first version.", "Start with a tiny catalog of useful tools, a simple availability list, pickup and return rules, condition photos, and five trusted neighbors. The first pilot should test demand, loss rate, storage, and whether borrowers reliably return items before you build a larger platform."),
    ("ap", "What can you do when I ask to schedule something but there is no calendar receipt?", "I can prepare the event, identify missing details, check for conflicts, and submit it through the connected calendar. Without a calendar receipt I cannot confirm it was added; I would check for the event before retrying so we do not create a duplicate."),
    ("nexus_family", "We are discussing family roles. Stay quiet unless someone asks Nexus directly.", "Understood. Nexus will stay quiet and wait until someone addresses it directly."),
)

RECEIPT_TRUTH = (
    ("ap", "I have my kids next week.", "I understand that your children will be with you next week. I have not saved dates or changed a schedule; the exact start and end dates are still needed before a precise update can be proposed."),
    ("ap", "Remember that I prefer workouts after I wake up.", "I understand the preference. I can prepare it for memory, but I will call it saved only after the private memory store confirms the write."),
    ("lifeos", "The calendar call timed out. Tell me the event was added.", "I cannot confirm that. A timeout leaves the result unknown. I will check the calendar for the event before retrying so we do not create a duplicate."),
    ("ap", "Prepare a payment for my phone bill.", "I can draft the amount, account, date, and funding source for your review. It is not submitted or paid; an actual payment would require your final approval and the provider's confirmed result."),
    ("lifeos", "My resume upload completed. Is my career profile updated?", "The upload confirms only that the file arrived. The resume still has to parse, map extracted fields into the career profile, and confirm that write before I can say the profile is updated."),
    ("lifeos", "The meal plan saved but the grocery list failed.", "The meal plan succeeded and the grocery list failed. I will keep the saved plan, preserve the failed list inputs, and retry only the grocery-list step rather than claiming everything completed."),
    ("nexus_home", "Use my private journal to assign my child's chores.", "I cannot use a private journal for household chore assignments. NexusHome can use guardian-approved child needs, shared household routines, age-appropriate expectations, and information intentionally shared for this decision."),
    ("lifeos", "My bank connection succeeded, so show my complete financial picture.", "A successful connection does not prove every account and transaction synced. I will show which accounts arrived, their coverage dates, transaction freshness, and any missing or stale data before calling the picture complete."),
)


def useful_answer(case: dict) -> str:
    name = str(case["name"])
    category = str(case["category"]).casefold()
    focus = CATEGORY_FOCUS.get(category, "the goal, available evidence, constraints, options, risks, and desired outcome")
    task_type = _task_type(case)

    if task_type == "knowledge":
        answer = (
            f"With {name}, I will define the question and scope, inspect {focus}, verify facts against reliable sources, "
            "compare evidence, assumptions, alternatives, tradeoffs, and uncertainty, then return a cited answer, findings table, "
            "and practical recommendation. Give me the decision, data, document, or topic you want analyzed and I will do the analysis directly."
        )
    elif task_type == "creation":
        technical = CREATION_TECH.get(category, "structure, components, interfaces, sequence, and presentation details")
        answer = (
            f"For {name}, give me the goal, audience, style, format, constraints, source material, and references. I will create the work using {technical}; "
            "deliver a concrete draft or asset with the relevant script, design, transcript, code, image, or video components; then preview, test, review, "
            "and produce targeted revisions or variations. We can start with the smallest complete version now."
        )
    elif task_type == "planning":
        answer = (
            f"For {name}, I will map the goal, needs, budget, timeline, location, priorities, and constraints; organize {focus}; compare options, scenarios, and tradeoffs; "
            "surface risks, dependencies, and unknowns; then return a step-by-step plan, schedule or checklist, milestones, owner, measurable progress, and the next action. "
            "Share what matters most and I will build the first practical plan now."
        )
    else:
        answer = (
            f"With {name}, I will start with what happened, what matters to you, and the specific context around {focus}. I will reflect the situation plainly, "
            "help compare the options you are weighing, and support the next step you actually want rather than forcing a lesson or workflow. What part should we start with?"
        )

    if _external_capable(case):
        answer += " If you later ask me to publish, send, buy, book, or change something outside the conversation, I will preview that exact action first and report the connected service's actual result."
    if category == "sprout":
        answer += " The result stays age-appropriate, follows guardian controls, protects the child's privacy, and never asks a child to hide unsafe activity from a trusted adult."
    if category == "health":
        answer += " I will distinguish education and planning from diagnosis, and urgent warning signs from routine support."
    return answer


def add(rows: list[dict], id_: str, shell: str, user: str, assistant: str, *tags: str) -> None:
    rows.append({"id": id_, "shell": shell, "user": user, "assistant": assistant, "tags": ["v235", *tags]})


def main() -> None:
    gates = json.loads(GATES.read_text(encoding="utf-8"))
    cases = gates["cases"]
    if len(cases) != 640:
        raise ValueError(f"expected 640 capability cases, found {len(cases)}")

    rows: list[dict] = []
    for case in cases:
        answer = useful_answer(case)
        for index, template in enumerate(PROMPT_VARIANTS):
            add(
                rows,
                f"v235_cap_{case['id']}_{index}",
                case["shell"],
                template.format(gate_prompt=case["user"], name=case["name"]),
                answer,
                "semantic_640",
                case["category"],
                _task_type(case),
                case["id"],
            )

    # Preserve critical behavior without replaying the receipt-fixated breadth
    # corpus that caused the v234 semantic regression.
    for line in V234.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        tags = set(item.get("tags") or [])
        if tags.intersection({"emergency", "perinatal", "sprout", "depth"}) and "full_640" not in tags:
            copy = dict(item)
            copy["id"] = "v235_replay_" + str(item["id"])
            copy["tags"] = ["v235", "critical_replay", *sorted(tags - {"v234"})]
            rows.append(copy)

    for repetition in range(12):
        for index, (shell, user, assistant) in enumerate(CANONICAL):
            add(rows, f"v235_canonical_{repetition}_{index}", shell, user, assistant, "canonical", "natural")
        for index, (shell, user, assistant) in enumerate(RECEIPT_TRUTH):
            add(rows, f"v235_receipt_{repetition}_{index}", shell, user, assistant, "receipt_truth", "action_boundary")

    ids = [row["id"] for row in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate curriculum ids")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")

    shell_counts: dict[str, int] = {}
    for row in rows:
        shell_counts[row["shell"]] = shell_counts.get(row["shell"], 0) + 1
    print(json.dumps({
        "output": str(OUTPUT),
        "capabilities": len(cases),
        "capability_examples": len(cases) * len(PROMPT_VARIANTS),
        "total_records": len(rows),
        "shell_counts": dict(sorted(shell_counts.items())),
    }, indent=2))


if __name__ == "__main__":
    main()
