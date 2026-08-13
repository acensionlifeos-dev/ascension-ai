# Qwen3 Ascension Adapter Pilot

Status: **completed, not promoted**

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

## Required next run

Run the same gated pipeline against the intended Qwen3 1.7B base. Do not promote based on training loss. Promotion remains blocked until one frozen adapter passes 6/6 conversation, 8/8 receipt truth, human review, integration tests, and runtime latency/load checks.

The GPU worker needs storage reclaimed before downloading and saving the 1.7B base and adapter. Preserve the approved scratch v7 checkpoint and production artifacts. Rejected scratch checkpoints and rejected pilot adapters may be removed only after an explicit artifact-retention decision.
