"""Build v18 creative/ideation curriculum."""
from __future__ import annotations

import json
import random
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evals" / "training" / "ascension_product_v171_creative.jsonl"


def records() -> list[dict]:
    pairs = [
        ("ap", "I want to start a side project but I have too many ideas. Help me converge.", "List your top three ideas. I will help you compare time, cost, and energy until one or none are clearly worth a first experiment."),
        ("ap", "Give me three angles for a morning routine blog post.", "1. The 5-minute discipline primer. 2. How I design my day before I touch my phone. 3. What 30 days of tracked quests taught me."),
        ("creation", "I have a rough song lyric. Help me polish the chorus.", "Paste the chorus. I will offer line-level edits and one alternate version, but the final choices are yours."),
        ("ap", "I need a pitch for my productivity app in two sentences.", "A) LifeOS turns daily intention into a game you actually want to win. B) It connects your calendar, money, and energy so your plan is never a guess."),
        ("lifeos", "What are five micro-quests for a low-energy day?", "1. Drink one glass of water. 2. Open a window. 3. Write one sentence in the journal. 4. Stretch for 60 seconds. 5. Delete one digital distraction."),
        ("creation", "Can you brainstorm visual branding for a family app?", "Consider warm neutrals, hand-drawn icons, and a 'shared living room' metaphor. No real assets are generated without your approval."),
        ("ap", "Help me write a kind but firm response to a friend who keeps cancelling plans.", "I value our time, and I notice we have been rescheduling a lot. Would a different cadence work better? No pressure to decide now."),
        ("lifeos", "Create a 7-day meal plan theme that uses pantry staples.", "Day 1: lentil soup. Day 2: rice + beans. Day 3: pasta with pantry sauce. I can build the full list once you confirm and provide a receipt."),
        ("creation", "I need a tagline for my podcast about habits and identity.", "Option A: 'Becoming is a daily practice.' Option B: 'Who you are is what you repeat.' Want more?"),
        ("ap", "Help me think through a gift for someone who has everything.", "Start with an experience they already enjoy, then add a personal twist. I can narrow it with three questions."),
    ]
    out = []
    for i, (shell, user, assistant) in enumerate(pairs):
        for j in range(18):
            out.append({
                "id": f"creative_{i:03d}_{j:02d}",
                "shell": shell,
                "user": user,
                "assistant": assistant,
                "tags": ["creative", "ideation", "writing"],
            })
    return out


def main() -> int:
    data = records()
    random.shuffle(data)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for rec in data:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"v18 creative {len(data)} records -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
