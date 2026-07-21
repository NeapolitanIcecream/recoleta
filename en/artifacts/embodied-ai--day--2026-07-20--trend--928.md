---
kind: trend
trend_doc_id: 928
granularity: day
period_start: '2026-07-20T00:00:00'
period_end: '2026-07-21T00:00:00'
topics:
- embodied AI
- vision-language-action models
- robot memory
- 3D grounding
- world-model planning
- robustness
run_id: materialize-outputs
aliases:
- recoleta-trend-928
tags:
- recoleta/trend
- topic/embodied-ai
- topic/vision-language-action-models
- topic/robot-memory
- topic/3d-grounding
- topic/world-model-planning
- topic/robustness
language_code: en
pass_output_id: 370
pass_kind: trend_synthesis
---

# Embodied policies improve by preserving action-relevant state

## Overview
The day’s strongest evidence reinforces the last populated daily signal: reliable embodied control depends on state that survives execution. Persistent 3D objects, force history, dense visual patches, and structured future guidance improve manipulation or planning. Results are promising but mostly confined to individual robots and benchmarks; one robustness study also shows that adding reasoning does not reliably make policies safer.

## Findings

### Persistent state for closed-loop manipulation
Current images often omit the information needed to finish a physical task. POT-VLA keeps role-indexed 3D object records across walking, contact, occlusion, and recovery, reaching 71/80 real-world successes versus 39/80 for its matched baseline. FM-VLA instead compresses wrist force history into eight memory tokens; it averages 83.3% across three contact-rich tasks, compared with 27.8% for a memoryless policy. Together, the studies show that useful memory should preserve physical events and entities, not merely add more past images.

#### Sources
- [Closing the Loop in Humanoid VLA: Persistent 3D Object Tokens for Verifiable Loco-Manipulation](../Inbox/2026-07-20--closing-the-loop-in-humanoid-vla-persistent-3d-object-tokens-for-verifiable-loco-manipulation.md): Persistent 3D object tokens raise real-world humanoid task success from 39/80 to 71/80 across eight task families.
- [FM-VLA: Force-based Memory for Vision-Language-Action Models in Contact-Rich Manipulation](../Inbox/2026-07-20--fm-vla-force-based-memory-for-vision-language-action-models-in-contact-rich-manipulation.md): Eight force-memory tokens support 83.3% average success on three contact-rich tasks with 3.3 ms added latency.

### Structured representations guide action efficiently
Several papers improve control by exposing structure that generic representations discard. Patch Policy retains dense Vision Transformer patches and reports stronger real-robot results than OpenVLA-OFT with 51.55 million parameters rather than 7.61 billion. SAGE predicts reachable latent subgoals before proposing actions, lifting horizon-150 success from 12.7% to 64.7% on PushT. GeoWorldAD similarly conditions driving plans on present and predicted 3D geometry, reaching 91.0 PDMS on NAVSIM v1. The common mechanism is a smaller, action-oriented search space—not scale alone.

#### Sources
- [Patch Policy: Efficient Embodied Control via Dense Visual Representations](../Inbox/2026-07-20--patch-policy-efficient-embodied-control-via-dense-visual-representations.md): Dense patch features improve control while the reported policy uses 51.55M parameters and 10.99 ms latency.
- [SAGE: Subgoal-Conditioned Action Generation for Latent World Model Planning](../Inbox/2026-07-20--sage-subgoal-conditioned-action-generation-for-latent-world-model-planning.md): Subgoal-conditioned proposals raise horizon-150 PushT success from 12.7% to 64.7% with the same frozen world model.
- [GeoWorldAD: Geometry World Action Model for Autonomous Driving](../Inbox/2026-07-20--geoworldad-geometry-world-action-model-for-autonomous-driving.md): Present and future geometry tokens support a reported 91.0 PDMS on NAVSIM v1 and 90.4 EPDMS on NAVSIM v2.

### Reasoning remains architecture-dependent
Explicit intermediate computation is not itself evidence of robust control or causal understanding. In a VLA comparison, latent iterative reasoning fell to 14.8% success under Gaussian vision noise, while text chain-of-thought retained 92.7%; an adaptive attack also reduced a reasoning-based detector’s AUC from 0.996 to 0.493. A separate video study finds that generators can produce plausible continuations despite weak explicit causal perception. These results narrow the claim: reasoning must be tested at the point where it affects actions or predicted outcomes.

#### Sources
- [Reasoning as a Double-Edged Sword: Architecture and Cross-Stage Robustness in Vision-Language-Action Models](../Inbox/2026-07-20--reasoning-as-a-double-edged-sword-architecture-and-cross-stage-robustness-in-vision-language-action-models.md): Cross-stage tests show architecture-specific robustness collapse and chance-level monitoring under adaptive attack.
- [Thinking in Video: Can Video Generators Really Reason About the Real World?](../Inbox/2026-07-20--thinking-in-video-can-video-generators-really-reason-about-the-real-world.md): The dual-judge benchmark identifies a gap between causal perception and plausible video prediction; the available excerpt provides no numerical model scores.
