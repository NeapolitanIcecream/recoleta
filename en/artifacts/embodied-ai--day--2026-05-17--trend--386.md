---
kind: trend
trend_doc_id: 386
granularity: day
period_start: '2026-05-17T00:00:00'
period_end: '2026-05-18T00:00:00'
topics:
- vision-language-action
- robot manipulation
- reinforcement learning
- affordance learning
- 3D planning
- interpretability
- autonomous driving safety
run_id: materialize-outputs
aliases:
- recoleta-trend-386
tags:
- recoleta/trend
- topic/vision-language-action
- topic/robot-manipulation
- topic/reinforcement-learning
- topic/affordance-learning
- topic/3d-planning
- topic/interpretability
- topic/autonomous-driving-safety
language_code: en
pass_output_id: 160
pass_kind: trend_synthesis
---

# Robot VLA papers demand contact-aware control and behavior-level validation

## Overview
Vision-language-action (VLA) robot work in this period is execution-centered. DyGRO-VLA protects multi-task policies during reinforcement learning. AffordVLA teaches contact regions without runtime modules. RoboFlow4D adds fast 3D motion plans for closed-loop control.

## Clusters

### Multi-task VLA control and contact grounding
DyGRO-VLA treats reinforcement learning as a controlled edit to a base robot policy. It freezes the base VLA and trains routed residual experts that add delta action chunks. On LIBERO, it reports 97.1% average success, a +4.4 point gain over its offline base, with a +9.8 point gain on LIBERO-Long.

AffordVLA attacks a different failure mode: the policy may choose the right object and still touch the wrong part. It aligns intermediate VLA visual tokens with a frozen affordance teacher during training, then removes the teacher at inference. The paper reports RoboTwin gains of 20.5% in Easy and 12.8% in Hard over the previous best baseline.

#### Evidence
- [DyGRO-VLA: Cross-Task Scaling of Vision-Language-Action Models via Dynamic Grouped Residual Optimization](../Inbox/2026-05-17--dygro-vla-cross-task-scaling-of-vision-language-action-models-via-dynamic-grouped-residual-optimization.md): DyGRO-VLA method and reported LIBERO, LIBERO-Long, and RoboTwin2 results.
- [AffordVLA: Injecting Affordance Representations into Vision-Language-Action Models via Implicit Feature Alignment](../Inbox/2026-05-17--affordvla-injecting-affordance-representations-into-vision-language-action-models-via-implicit-feature-alignment.md): AffordVLA training setup, affordance teacher removal at inference, and RoboTwin gains.

### 3D planning signals for closed-loop manipulation
RoboFlow4D uses predicted 3D gripper flows as an explicit plan that a policy can track. Its slow-fast loop plans lower-frequency trajectories and lets the action policy execute higher-frequency chunks. The paper reports LIBERO gains of +6.2 points with Diffusion Policy and +4.0 points with a DiT policy, plus under-one-second planning latency.

Visual Sculpting shows the same emphasis in deformable manipulation. It plans over dense 512×512 depth maps and spatial depth gradients, then replans with model predictive control after small batches of actions. The system produced long-horizon clay sequences with more than 100 actions, and its visual loss improved foam and dough deformation metrics in the reported held-out tests.

#### Evidence
- [RoboFlow4D: A Lightweight Flow World Model Toward Real-Time Flow-Guided Robotic Manipulation](../Inbox/2026-05-17--roboflow4d-a-lightweight-flow-world-model-toward-real-time-flow-guided-robotic-manipulation.md): RoboFlow4D 3D flow planning method, slow-fast control, benchmark gains, and latency claim.
- [Visual Sculpting: Visually-Aligned Planning Representations for Long-Horizon Robot Clay Sculpting](../Inbox/2026-05-17--visual-sculpting-visually-aligned-planning-representations-for-long-horizon-robot-clay-sculpting.md): Visual Sculpting dense depth representation, MPC loop, deformation results, and long-horizon runs.

### Behavior-level checks for VLA interpretability and safety
Event-Grounded Sparse Autoencoders adapts sparse autoencoders (SAEs) to robot policies by anchoring features to recurring rollout events. The pipeline extracts end-effector keyframes, clusters them by visual and robot-state cues, then tests features through closed-loop interventions. On OpenVLA layer 31, zeroing event-aligned features reduced success from 70.0% to 48.8%, a larger effect than window-mean, task-mean, or random-alive rankings.

The driving-safety paper tests whether Chain-of-Causation (CoC) explanations match scenes and trajectories in Alpamayo-R1-10B. Overall reasoning fidelity is 42.5% across inferences with obstacle context. The study also reports 94 missed pedestrians, 53.3% low reasoning-action consistency, and 37.9% of claimed stop cases continuing instead.

#### Evidence
- [Event-Grounded Sparse Autoencoders for Vision-Language-Action Policies](../Inbox/2026-05-17--event-grounded-sparse-autoencoders-for-vision-language-action-policies.md): Event-grounded SAE pipeline and closed-loop intervention results.
- [Is VLA Reasoning Faithful? Probing Safety of Chain-of-Causation](../Inbox/2026-05-17--is-vla-reasoning-faithful-probing-safety-of-chain-of-causation.md): VLA driving reasoning-fidelity evaluation, pedestrian misses, and reasoning-action mismatch results.
