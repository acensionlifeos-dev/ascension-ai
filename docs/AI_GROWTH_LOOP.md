# Ascension AI Growth Loop

Ascension AI grows through evaluated apprenticeship packets, not through unreviewed self-modification.

Each run processes at most one packet from `evals/growth_packet_queue.json`:

1. Load the next packet and a small, de-identified lesson packet.
2. Submit the canonical growth curriculum to the live native service.
3. Grade completeness, truthfulness, context judgment, action boundaries, conversational humanity, and latency.
4. Record the evidence and failures. A failed answer is evaluation evidence, never a positive training example.
5. Mark the packet complete only when its pass conditions are satisfied. Otherwise revise and repeat it.
6. Load the next packet only after the current packet reaches a terminal evaluated state.

Personal memories and sensitive values never enter this repository. Weight training and production-model promotion require separate reviewed workflows.
