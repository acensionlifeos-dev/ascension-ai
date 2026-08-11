# Ascension AI

Ascension AI is the private, shared intelligence core for Ascension LifeOS. It runs a pinned open-weight model locally through `llama.cpp`; the production runtime does not call OpenAI, Gemini, Anthropic, or another hosted model.

Current status: native alpha 2.3. The standalone service is live and suitable for evaluation and staged LifeOS routing. It is not yet approved as the only production intelligence provider; `/v1/readiness` deliberately reports that distinction.

## Product shells

- **AP** — one person’s conversational partner, assistant, task manager, coach, and mentor.
- **LifeOS** — domain intelligence that turns permissioned context into screen-ready insights and proposed next actions.
- **NexusHome** — household and co-parenting coordination with strict private-data boundaries.
- **NexusFamily** — FamilyOS and family-enterprise coordination; shared-chat behavior follows the FamilyOS consent contract.
- **Core** — neutral analysis without a relationship persona.

The same core recognizes FreeOS, LifeOS, LifeOS+, FounderOS, and LifeOS Infinite requests. The authenticated calling product—not the model—enforces subscriptions, permissions, and available actions.

## Executable capability domains

The native orchestration contract currently routes identity, scheduling, finance, health, learning, creation, relationships, family, home, career, emotional intelligence, documents, research, environment, business, and safety. These domains can be invoked through chat or as page/surface intelligence.

The AI proposes intelligence and actions. LifeOS owns authentication, database access, entitlement checks, confirmations, action execution, evidence, and audit logs. A model response alone never proves that an action occurred.

## Local profiles

| Profile | Model | Intended host |
| --- | --- | --- |
| `starter` | SmolLM2 135M Q2 | 512 MB latency-first bootstrap validation |
| `standard` | Qwen2.5 0.5B Q4 | 2 GB service |
| `pro` | Qwen3 4B Q3_K_S | 4 GB interactive service |
| `deep` | Qwen3 4B Q4_K_M | Higher-memory or queued background service |

Every model file is pinned by repository revision and SHA-256 checksum in `config/model_profiles.json`.

## Run locally

```bash
python -m venv .venv
pip install -r requirements.txt
python scripts/download_model.py
set ASCENSION_AI_TEST_TOKEN=choose-a-private-test-code
uvicorn src.serving.api:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000` and enter the private test code. The standalone page provides real token streaming, shell selection, and tier selection.

## API

- `GET /health` — public readiness without secrets.
- `GET /model/info` — protected runtime metadata.
- `GET /v1/capabilities` — protected shell, tier, and domain registry.
- `POST /v1/intelligence` — protected native inference.
- `POST /v1/stream` — protected SSE inference with real token deltas.
- `POST /v1/surface-plan` — protected deterministic domain-to-surface proposal.
- `POST /chat` — compatibility alias for native inference.
- `POST /generate` — legacy prompt compatibility.

Example request:

```json
{
  "shell": "lifeos",
  "tier": "lifeos_plus",
  "messages": [{"role": "user", "content": "Review this creation idea."}],
  "context": {"workspace": "software", "verified_evidence": []},
  "surface": "creation/software",
  "mode": "planning",
  "allowed_capabilities": ["creation", "research", "business", "safety"]
}
```

## Connect LifeOS

Deploy this repository as its own Render service. Configure the LifeOS service with:

```text
ASCENSION_AI_URL=https://ascension-ai.onrender.com
ASCENSION_AI_SERVICE_TOKEN=<same private service token>
ASCENSION_NATIVE_MODE=primary
ASCENSION_AI_TIMEOUT_MS=120000
```

Routing modes:

- `primary` — Ascension AI first, existing providers only if native inference fails.
- `fallback` — existing provider first, Ascension AI available afterward.
- `only` — native intelligence only; use after replacement evaluations pass.
- `off` — native routing disabled.

The LifeOS router sends the relevant shell, subscription tier, product surface, allowed capability domains, and permission-scoped context. AP chat, Academy program generation, culinary intelligence, workout intelligence, content enrichment, translation, and Creation workspace requests share that router.

## Verification

```bash
python scripts/native_conversation_eval.py
python scripts/replacement_contract_eval.py
set ASCENSION_AI_BASE_URL=https://ascension-ai.onrender.com
set ASCENSION_AI_TEST_TOKEN=<private test token>
python scripts/replacement_readiness_eval.py
```

The smoke set contains 30 human prompts across AP, LifeOS, NexusHome, NexusFamily, and Core. The replacement suite adds explicit required concepts, forbidden claims, response-length limits, provider-integrity checks, hidden-reasoning checks, and an interactive-latency gate. Passing the smoke set alone does not authorize provider replacement.

## Security boundaries

- The public web page never receives the service token.
- Requests require a test token or server-to-server service token.
- Context is bounded and supplied per request; the model does not directly query LifeOS databases.
- The runtime makes no external model call and performs no external action.
- Model files are checksum-verified on boot.
- CORS is allow-list based.
- Production replacement remains disabled until quality, safety, privacy, action-integrity, and shell-boundary evaluations pass.

## What is not production-proven yet

The repository contains earlier experimental modules and roadmap concepts. They are not loaded by the native production path and must not be treated as working merely because a file or feature name exists. Multimodal perception, autonomous execution, long-term model training, distributed inference, and most legacy specialist modules still require implementation and evaluation.

© 2026 The B.E.I.N.G Group LLC. All rights reserved.
