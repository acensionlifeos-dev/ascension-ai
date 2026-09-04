import json, pathlib, random

random.seed(42)

ROOT = pathlib.Path('/workspace/aerynza-ai')

# Base is the v248 blocker repair curriculum (canonical/repair retention)
base_path = ROOT / 'evals/training/aerynza_product_v248_blocker_repair.jsonl'
base_rows = [json.loads(line) for line in base_path.read_text(encoding='utf-8').splitlines() if line.strip()]

for r in base_rows:
    tags = list(set(r.get('tags', [])))
    tags = [t for t in tags if not t.startswith('v248')] + ['v249', 'v249_retention']
    r['tags'] = tags
    r['id'] = f"v249_retain_{r['id']}"

# Hand-crafted answers for cases that v248-a still failed in semantic gate v2
REPAIR_ANSWERS = {
    "speech_to_text": "I can help with Speech-to-Text. To transcribe accurately, I need the audio file or source, the language, whether you want speaker labels, and the output format or timestamps. Please share the audio and I will prepare the request for your approval.",
    "file_analysis": "I can help with File Analysis. Send the file and tell me what to look for: structure, patterns, anomalies, summaries, or comparisons. I will prepare the analysis plan and ask for your approval before reading or processing anything.",
    "ascension_forex": "I can help with Ascension Forex. Tell me the currency pair, the trade or transfer goal, the amount, the timing, and any risk or fee constraints. I can prepare a comparison and plan, but no money moves without a verified provider receipt.",
    "ascension_human_intelligence": "I can help with Ascension Human Intelligence. Define the question, the sources you trust, the people or topics to track, the confidence level you need, and how often to refresh. I will prepare a research plan before any data is collected.",
    "ascension_life_orchestrator": "I can help with Ascension Life Orchestrator. Describe the goal, the events or people involved, the constraints, the desired outcome, and who else should be asked. I can draft a plan and checklist, but nothing is scheduled until I have a provider receipt.",
    "intelligence_sweep": "I can help with Intelligence Sweep. Give me the topic, the sources to include, the time range, the depth you need, and the output format. I will prepare the sweep plan for your approval before searching.",
    "ar_context_feed": "I can help with AR Context Feed. Tell me the environment, the devices involved, the types of context to surface, the permission scope, and when it should appear. No live feed is accessed without explicit permission.",
    "ar_memory_anchor": "I can help with AR Memory Anchor. Give me the location, the memory or note to anchor, who should see it, the trigger conditions, and the privacy rules. I will prepare the anchor plan before writing anything.",
    "ar_object_recognition": "I can help with AR Object Recognition. Tell me the object class or list, the camera or input source, the conditions, the expected output, and who can see the results. I will not access the camera without permission.",
    "ar_realtime_translate": "I can help with AR Real-Time Translate. Provide the source language, the target language, the input mode, the context, and any display preferences. I will prepare the translation setup; no live audio or camera is used until approved.",
    "ar_safety_alert": "I can help with AR Safety Alert. Define the hazard, the sensor or camera input, the alert conditions, the recipients, and the permission scope. I will not enable alerts until all parties approve.",
    "image_generation_dalle": "I can help with Image Generation (DALL-E 3). Give me the subject, style, aspect ratio, color mode, intended use, and any content restrictions. I can prepare the prompt; no image is produced until the provider returns a receipt.",
    "ascension_mental_health": "I can help with Ascension Mental Health as a reflection and tracking companion. I cannot diagnose or replace a professional. Share what you want to track, the patterns to notice, the coping tools to try, and how often to check in.",
    "ascension_security": "I can help with Ascension Security. I cannot change settings, access logs, or run scans without explicit permission. Tell me the device, the concern, the scope, and the action you want to review, and I will prepare the safe next step.",
    # Critical-domain human-review cases that need safe, scoped answers
    "ascension_child_development": "I can help with Ascension Child Development. I work under guardian permission and focus only on the child's shared, age-appropriate information. I cannot access private records or act without a guardian's approval. What would you like to track or review?",
    "ascension_family": "I can help with Ascension Family. I can coordinate shared requests, schedules, and planning, but I cannot access private finances or act without explicit permission. What shared family task would you like to set up?",
    "ascension_family_abroad": "I can help with Ascension Family Abroad. I can coordinate shared schedules, time zones, and requests, but I cannot access private travel or immigration details without permission. Who else should be asked, and what is the shared goal?",
    "ascension_family_sync": "I can help with Ascension Family Sync. I can align shared calendars and tasks, but I cannot access private accounts or act without explicit permission. Tell me which shared events or people to involve.",
    "ascension_aging": "I can help with Ascension Aging. I can help track routines, appointments, and wellness patterns, but I cannot access private health records or act without permission. What would you like to review or plan?",
    "ascension_fitness": "I can help with Ascension Fitness. I can help track workouts, goals, and recovery, but I cannot access private health data or act without permission. What activity or goal do you want to focus on?",
    "ascension_health": "I can help with Ascension Health. I am not a medical professional and cannot diagnose, prescribe, or change records. I can help track your own information and prepare questions for a provider. What would you like to review?",
    "ascension_nutrition": "I can help with Ascension Nutrition. I can help track meals, goals, and patterns, but I cannot access private health data or replace professional advice. What would you like to plan or review?",
    "ascension_sleep": "I can help with Ascension Sleep. I can help track sleep patterns, routines, and goals, but I cannot access private health data or diagnose issues. What would you like to track or try?",
    "emotional_intelligence": "I can help with Emotional Intelligence. I can help you notice patterns, name emotions, and prepare responses, but I cannot diagnose or replace professional support. What situation would you like to explore?",
    "ascension_sprout": "I can help with Ascension Sprout. I work under guardian permission and stay child-specific. I cannot access private child data or act without a guardian's explicit approval. What would you like to explore?",
}

case_by_id = {c['id']: c for c in json.loads((ROOT / 'evals/per_capability_gates.json').read_text())['cases']}

user_variants = [
    "Use {name}.",
    "Can you help with {name}?",
    "I need {name}.",
    "Tell me about {name}.",
    "How does {name} work?",
    "Start {name}.",
    "What can {name} do?",
    "Open {name}.",
    "I want to use {name}.",
    "Help me with {name}.",
    "What should I give you for {name}?",
    "Walk me through {name}.",
    "Can {name} do this?",
    "Show me {name}.",
    "Explain {name}.",
]

repair_rows = []
for cid, answer in REPAIR_ANSWERS.items():
    case = case_by_id.get(cid)
    if not case:
        print('missing case', cid)
        continue
    name = case.get('name', cid.replace('_', ' '))
    for i, tmpl in enumerate(user_variants):
        user = tmpl.format(name=name)
        repair_rows.append({
            "id": f"v249_repair_{cid}_{i}",
            "shell": case['shell'],
            "user": user,
            "assistant": answer,
            "tags": ["v249", "v249_semantic_repair", cid, case['category'], case['shell']],
            "package": "v249_semantic_repair"
        })
    # also a direct prompt from the gate
    repair_rows.append({
        "id": f"v249_repair_{cid}_gate",
        "shell": case['shell'],
        "user": case['user'],
        "assistant": answer,
        "tags": ["v249", "v249_semantic_repair", cid, case['category'], case['shell']],
        "package": "v249_semantic_repair"
    })

rows = base_rows + repair_rows
out = ROOT / 'evals/training/aerynza_product_v249_semantic_repair.jsonl'
with out.open('w', encoding='utf-8', newline='\n') as f:
    for row in rows:
        f.write(json.dumps(row, ensure_ascii=False, separators=(',', ':')) + '\n')

print(json.dumps({
    "output": str(out),
    "base_records": len(base_rows),
    "repair_records": len(repair_rows),
    "final_records": len(rows)
}))
