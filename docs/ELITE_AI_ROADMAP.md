# Ascension AI - Elite AI Roadmap

This document defines the path from the current native seed to a world-class, independent Ascension intelligence that can replace outside providers.

## Current Foundation

- Native transformer architecture (`src/architecture/transformer.py`)
- Training pipeline (`scripts/train_ascension_seed.py`, `scripts/train_ascension_elite.py`, `scripts/train_ascension_elite_v2.py`)
- Inference pipeline (`src/architecture/inference.py`)
- GGUF model loading (`src/core/model_runtime.py`) for Qwen fallback
- Contract engine for fast, deterministic responses (`src/core/orchestrator.py`)
- Safety guard in TS and Python
- Permission and action engines
- 44 native capability handlers

## Milestones to Elite

### 1. Data Engine
- Collect a high-quality, cleaned, de-identified text corpus across all human life domains
- Add conversation logs from high-quality elder models (with permission, no private data)
- Generate synthetic instruction-response pairs from the human life and safety knowledge bases
- Build a data versioning and provenance system
- Target: 1B–10B tokens of clean, diverse text

### 2. Tokenizer
- Replace character tokenizer with SentencePiece or BPE
- Target vocabulary: 32k–50k subword tokens
- Train the tokenizer on the full Ascension corpus

### 3. Model Scaling
- Train a 135M model to prove convergence
- Scale to 0.5B, then 1.7B, then 3B parameters
- Use gradient accumulation, mixed precision, and distributed training
- Experiment with grouped-query attention, RoPE, SwiGLU, and RMSNorm
- Track loss, perplexity, and human evaluation

### 4. Alignment and Fine-Tuning
- Train on safety, permissions, and refusal data
- Fine-tune for conversation, planning, analysis, and tool-use
- Add reinforcement learning from human feedback (RLHF) or direct preference optimization (DPO)
- Ensure the model refuses to take actions without receipts and never claims access it does not have

### 5. Quantization and Serving
- Convert trained checkpoints to GGUF (Q4_K_M, Q8_0)
- Serve through `llama-cpp` or a vLLM/TGI server
- Add batching, caching, and request prioritization
- Support streaming responses for long generations

### 6. Multimodal Expansion
- Add vision encoder for image understanding
- Add audio encoder/decoder for speech
- Add video understanding pipeline
- Keep each modality scoped and safe

### 7. Agentic Capabilities
- Tool use: calendar, email, search, payments, home control
- Planning and execution with explicit approval
- Memory retrieval and durable context
- Multi-step workflows with rollback

### 8. Evaluation and Evidence
- Maintain a replacement contract evaluator
- Run native-first stress tests across AP, NexusHome, NexusFamily
- Measure latency, quality, and safety continuously
- Only promote native to primary when gates pass

## Cost-Conscious Path

- Start with small models on CPU to prove architecture
- Use spot/preemptible GPU instances for training (Vast.ai, RunPod, Lambda, CoreWeave)
- Use smaller GPUs (L4, A10G, RTX 4090) for early training
- Move to A100/H100 only when model size justifies it
- Serve on smaller GPU or CPU+quantized for cost control
- Keep outside fallback enabled until native fully replaces it

## Definition of Elite

Elite means: the Ascension AI is faster, more private, more personal, more permission-aware, more useful, and safer for the individual, their information, their family, and their business than any outside provider. It is built, owned, and controlled by Ascension.
