# Ascension AI Native Runtime Readiness

## Canonical architecture

Ascension AI is the shared intelligence core. It is not another consumer screen and it is not a hosted-model router.

- **AP** is the private, person-level relationship and action shell.
- **LifeOS** is the personal-domain intelligence and surfacing shell.
- **NexusHome** is the household and co-parenting coordination shell.
- **NexusFamily** is the FamilyOS and family-enterprise coordination shell.
- Each shell owns authorization, private-data boundaries, execution, evidence, and UI placement.
- Ascension AI receives a permission-scoped context packet, returns reasoning and proposed actions, and never silently widens access.

## Executable in native alpha 2.1

- Local GGUF inference through llama.cpp with no hosted AI provider.
- Pinned model revisions and SHA-256 verification.
- Seed, Standard, and Pro model profiles selected by one environment variable.
- Private test and service credentials.
- AP, LifeOS, NexusHome, NexusFamily, and neutral-core role contracts.
- Cross-domain capability detection and screen/surface routing.
- A proposal-only orchestration endpoint for non-chat intelligence surfaces.
- A private ChatGPT-style evaluation screen with real token streaming plus selectable shell and tier behavior.
- A stable API contract wired into the LifeOS central AI router for AP chat and existing router-backed domain services.
- Direct Creation workspace intelligence that receives room evidence and renders its response in the Creation surface.

## Model profiles

| Profile | Model | Quantized size | Minimum target | Purpose |
|---|---|---:|---|---|
| `starter` | SmolLM2 135M Q2 | 88 MB | Render Free/Starter, 512 MB | Prove native boot, privacy, API, and shell routing with a responsive bootstrap. Quality is limited. |
| `standard` | Qwen2.5 0.5B Q4_K_M | 491 MB | Render Standard, 2 GB | Better instruction following and conversation. |
| `pro` | Qwen3 1.7B Q8_0 | 1.83 GB | Render Pro, 4 GB | Responsive multilingual conversation, planning, structured cognition, and tool selection. |
| `deep` | Qwen3 4B Q4_K_M | 2.50 GB | Pro 4 GB background worker | Queued research, synthesis, evaluation, and apprenticeship distillation where interactive latency is not required. |

The service must be redeployed after changing `ASCENSION_MODEL_PROFILE`. Model selection does not change the API or shell contracts.

## Measured local evidence (2026-08-11)

- Starter profile: 30/30 native smoke prompts passed across AP, LifeOS, NexusHome, NexusFamily, and Core; median 2,558 ms and p95 3,409 ms; no outside provider.
- The earlier 3B test passed five shell smoke requests but was too slow for ordinary conversation.
- Production candidate 2.2 now runs the pinned Qwen3 1.7B Q8 profile on Render Pro with real SSE streaming and bounded mode-specific output budgets.
- Replacement readiness remains false until the rubric-based live suite, concurrency/recovery checks, and native-primary canary all pass.

## Capability surfacing rule

Capabilities are available to the intelligence core regardless of a consumer's subscription. The calling Ascension shell supplies the user's tier, permissions, live context, and allowed actions. The shell decides what UI and execution paths the user can access. This keeps one capable core while preserving product tiers and clean interfaces.

The native core does not execute bank transfers, messages, purchases, filings, medical actions, family decisions, or external submissions itself. It proposes or prepares; the authenticated shell validates, asks for approval where required, executes, and returns evidence.

## Inherited Devin repository audit

- The previous Render service used random model weights and a character tokenizer.
- The previous public page displayed unsupported parameter and training-data claims.
- The TypeScript provider router was not the runtime Render launched.
- The dependency list contained a nonexistent `@types/path` package.
- Thirty of forty-two inherited Python modules fail syntax parsing, usually because roadmap bullets were pasted into source files as executable text.
- Most claimed capabilities are sketches, heuristics, registries, or roadmap notes—not trained or production-tested systems.
- No native checkpoint, benchmark evidence, red-team report, provenance record, or comprehensive test suite was present.

Those files remain research references. Production imports only the new native runtime path until a legacy module is repaired, tested, and deliberately promoted.

## Required gates before AP replacement

1. Pro model boots inside the 4 GB instance without memory pressure.
2. At least 30 natural conversation prompts pass a blinded AP-vs-native comparison.
3. Shell-isolation tests prove personal, household, and family context never cross boundaries.
4. Structured tool proposals pass schema validation and never self-execute.
5. Domain tests cover finance, schedule, health, learning, creation, relationships, identity, career, home, and family.
6. Latency, crash recovery, concurrency, and degraded-mode behavior meet product thresholds.
7. Safety, privacy, correction, memory, and audit tests pass.
8. Native runs in primary-with-fallback mode before `only` mode removes outside-provider fallback.
9. Rollback to the current AP intelligence path is one configuration change.
10. Replacement occurs domain by domain, never as an unmeasured all-at-once cutover.
