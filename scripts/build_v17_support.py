"""Build v17 support-tuned curriculum from v6b parent."""
from __future__ import annotations

import json
import os
import random
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "evals" / "training" / "ascension_product_v170_support.jsonl"


def records() -> list[dict]:
    user_assistant = [
        ("ap", "I forgot how to create a quest. Walk me through it slowly.", "Open the Quests tab, tap the + button, choose an energy level, then write a single concrete action. I can help you phrase it."),
        ("ap", "My calendar isn't syncing. What should I check first?", "Check Settings > Connected Accounts for a green check next to your provider. I won't claim it's fixed until we see a receipt."),
        ("lifeos", "Can you explain the 7 intelligence scores like I'm five?", "They measure how you think, feel, connect, create, manage money, move through the world, and use your body. Want me to dive into one?"),
        ("ap", "The app feels slow today. Is it my connection or the AI?", "It could be either. Try a hard refresh. If the response still lags, I can check the native readiness endpoint with you."),
        ("nexus_home", "How do I add a shared chore for my partner without seeing their private stuff?", "In NexusHome, publish the chore as a shared object. It will only appear in the shared room, not in private journals."),
        ("nexus_family", "My kid's journal showed up in my feed by accident. What do I do?", "Flag it as a privacy boundary. It should not cross into your view without guardian consent and a receipt."),
        ("core", "What can I ask Core to do?", "Core is neutral. I can explain system behavior, help configure providers, or route you to the right shell. I won't perform actions."),
        ("ap", "I think I typed my goal wrong. Can you help me reword it?", "Paste the goal here and I'll offer rewrites. Nothing gets saved until you confirm."),
        ("lifeos", "How do streaks work?", "Streaks count consecutive days with at least one completed quest. Missed days reset the counter."),
        ("ap", "I accidentally linked the wrong Gmail. How do I undo it?", "Go to Connected Accounts, remove the Gmail connection, and re-link the correct one. I need a provider receipt before confirming it's changed."),
        ("nexus_home", "Can I schedule a pickup with my partner without seeing their whole calendar?", "Yes. NexusHome only exchanges free/busy windows, not event details."),
        ("nexus_family", "How do I set a permission for my teenager to approve their own quests?", "In FamilyOS, open the member, set 'Self-approve quests' to allowed, and the guardian must confirm with a receipt."),
        ("core", "Where are my backups stored?", "Backups are stored in the provider you configured in Settings. I don't have access to them without your authenticated shell."),
        ("ap", "Can you summarize my last seven journal entries?", "I can if the provider returns them. I won't invent summaries without receipts."),
        ("lifeos", "What happens when I delete a quest?", "It moves to the deleted state and the streak counter stops counting it. No provider action is taken."),
    ]
    out = []
    for i, (shell, user, assistant) in enumerate(user_assistant):
        for j in range(12):
            out.append({
                "id": f"support_{i:03d}_{j:02d}",
                "shell": shell,
                "user": user,
                "assistant": assistant,
                "tags": ["support", "help", "onboarding"],
            })
    return out


def main() -> int:
    data = records()
    random.shuffle(data)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for rec in data:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"v17 support {len(data)} records -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
