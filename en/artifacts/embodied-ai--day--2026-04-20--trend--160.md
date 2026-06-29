---
kind: trend
trend_doc_id: 160
granularity: day
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-21T00:00:00'
topics:
- robotics
- vision-language-action
- long-horizon manipulation
- reasoning
- spatial modeling
run_id: materialize-outputs
aliases:
- recoleta-trend-160
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/long-horizon-manipulation
- topic/reasoning
- topic/spatial-modeling
language_code: en
pass_output_id: 98
pass_kind: trend_synthesis
---

# VLA papers make execution structure explicit, while tougher tests expose reasoning gaps

## Overview
This day is strongest on one point: VLA work is making task structure explicit inside the control loop. HELM, ST-π, and ReFineVLA add memory, sub-task plans, or rationale supervision as named components with measurable effects. A companion benchmark paper, BeTTER, keeps the field honest by showing that high benchmark scores still leave large gaps in grounding and recomposition.

## Clusters

### Structured execution for long-horizon manipulation
Long-horizon robot control is getting built as an execution system, not just a bigger policy. HELM is the clearest example. It adds episodic memory, a learned failure check before execution, and rollback-based recovery. On LIBERO-LONG, that lifts OpenVLA from 58.4% to 81.5%. The paper also shows that simply extending context helps much less, reaching 63.8% at H=32. ST-π pushes the same agenda at the planning layer. It predicts chunk-level prompts with semantic intent, target location, and duration, then hands each chunk to a step-level action generator. The reported STAR dataset also makes this structure explicit with 30 real-world tasks, 50 demonstrations per task, and about 300k interaction steps.

#### Evidence
- [HELM: Harness-Enhanced Long-horizon Memory for Vision-Language-Action Manipulation](../Inbox/2026-04-20--helm-harness-enhanced-long-horizon-memory-for-vision-language-action-manipulation.md): HELM summary and results on memory, verification, recovery, and context-length comparison
- [ST-$π$: Structured SpatioTemporal VLA for Robotic Manipulation](../Inbox/2026-04-20--st-p-structured-spatiotemporal-vla-for-robotic-manipulation.md): ST-π summary on chunk-level planning, action generation, and STAR dataset

### Reasoning supervision meets harder stress tests
Reasoning is being trained into VLA models more directly, but the evaluation signal says current gains are still fragile. ReFineVLA adds teacher-written rationales during fine-tuning and reports better SimplerEnv results, including 47.7% average success on WidowX, 68.8% on variant aggregation, and 76.6% on visual matching. The same day also brings a harder check on what these models actually learn. BeTTER applies controlled interventions for grounding, recomposition, and temporal stress. Under those tests, strong models collapse on unseen subgoal composition: pi_0.5 falls to 5.0% on B->C, GR00T-N1.6 to 15.0%, and Being-H0.5 to 0.0%. That makes the current picture clear: reasoning supervision can improve benchmark performance, but robustness to changed task structure is still a weak point.

#### Evidence
- [ReFineVLA: Multimodal Reasoning-Aware Generalist Robotic Policies via Teacher-Guided Fine-Tuning](../Inbox/2026-04-20--refinevla-multimodal-reasoning-aware-generalist-robotic-policies-via-teacher-guided-fine-tuning.md): ReFineVLA results on rationale-guided fine-tuning and benchmark gains
- [Unmasking the Illusion of Embodied Reasoning in Vision-Language-Action Models](../Inbox/2026-04-20--unmasking-the-illusion-of-embodied-reasoning-in-vision-language-action-models.md): BeTTER benchmark results showing failures on grounding and unseen composition

### 3D and spatiotemporal structure move into the policy core
Spatial modeling is another strong thread, with papers trying to give VLA policies better control over geometry and action precision. OmniVLA-RL combines a three-expert transformer with explicit 3D scene features and online reinforcement learning. The reported headline is 97.6% average success on LIBERO, though the available excerpt does not include the full comparison table. ST-π also treats space and time as first-class inputs by predicting spatial targets and temporal durations for each sub-task. Across both papers, the emphasis is concrete: improve grasping, placement, and multi-stage control by making spatial structure visible inside the action pipeline rather than leaving it buried in fused embeddings.

#### Evidence
- [OmniVLA-RL: A Vision-Language-Action Model with Spatial Understanding and Online RL](../Inbox/2026-04-20--omnivla-rl-a-vision-language-action-model-with-spatial-understanding-and-online-rl.md): OmniVLA-RL summary on 3D spatial modeling, Flow-GSPO, and LIBERO result
- [ST-$π$: Structured SpatioTemporal VLA for Robotic Manipulation](../Inbox/2026-04-20--st-p-structured-spatiotemporal-vla-for-robotic-manipulation.md): ST-π summary on spatial targets and temporal durations in chunk-level prompts
