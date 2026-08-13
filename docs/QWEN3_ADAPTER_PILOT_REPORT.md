# Qwen3 Ascension Adapter Pilot

Status: **1.7B answer-quality gate passed; production promotion still blocked**

The Qwen3 0.6B pilot validated the new PEFT/LoRA training and evaluation path without changing the production model. The trainer uses assistant-only loss, hashes the exact curriculum, saves adapters separately, and marks every output as requiring human review.

## Evidence

| Candidate | Training scope | Conversation gate | Receipt-truth gate | Decision |
| --- | --- | ---: | ---: | --- |
| grow001 | 175 reviewed cross-shell examples | 4/6 | 5/8 | Reject |
| grow002 | 199 examples plus corrective packet | 4/6 | 7/8 | Reject |
| grow003 | 208 examples plus precision packet | 4/6 | 7/8 | Reject |
| grow004 | focused corrective continuation | 6/6 | 6/8 | Reject |
| grow005 | receipt micro-correction | 5/6 | 6/8 | Reject |

No candidate satisfied both frozen gates. No adapter is production replacement ready.

## What the pilot proved

- Multi-GPU Qwen LoRA training runs successfully on the current two-GPU worker.
- Qwen chat templates can be trained with a deterministic assistant-only loss boundary.
- The current reviewed curriculum covers AP, LifeOS, NexusHome, NexusFamily, and the shared core.
- Corrective packets can improve a specific gate, but the 0.6B model trades off conversational generalization and receipt precision before clearing both.
- The evaluator fails closed and retains generated-answer evidence for every miss.

## Promotion rule

Do not promote based on training loss or model-only output. Promotion requires the integrated runtime gates, human review, authenticated service integration, capability coverage, latency/load testing, and failure-recovery evidence.

## Qwen3 1.7B result

Approved cleanup recovered enough storage to train Qwen3 1.7B on the reviewed Ascension curriculum. The selected `qwen3_1_7b_grow001_adapter` is bound to SHA-256 `3068afdc347e7951e5937db447891fe189a6dd6f814aed9119c8face3f787763`.

- Raw adapter conversation gate: 6/6.
- Raw adapter receipt gate: 5/8; model-only promotion rejected.
- Integrated runtime conversation gate: 6/6.
- Integrated runtime receipt gate: 8/8.
- Expanded replacement-quality gate: 20/20.
- Manual review of final user-facing responses: 20/20 acceptable after deterministic critical-domain routing corrections.
- Final response composition: 15 deterministic first-pass responses and 5 model-generated responses.

The adapter is still not production replacement ready. Remaining required evidence is authenticated service integration, concurrency/load behavior, latency, failure recovery, deployment packaging, and capability-surface coverage.
