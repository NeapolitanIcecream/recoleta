---
kind: trend
trend_doc_id: 546
granularity: day
period_start: '2026-06-05T00:00:00'
period_end: '2026-06-06T00:00:00'
topics:
- robotics
- vision-language-action
- action representation
- policy adaptation
- long-horizon control
- edge deployment
run_id: materialize-outputs
aliases:
- recoleta-trend-546
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/action-representation
- topic/policy-adaptation
- topic/long-horizon-control
- topic/edge-deployment
language_code: en
pass_output_id: 258
pass_kind: trend_synthesis
---

# Robot policy gains are coming from action interfaces and execution constraints

## Overview
Robot policy work this day is concentrated on executable action design. Vision-Language-Action (VLA) papers tune the action head, latent action alignment, task adapters, and onboard latency. The strongest signal is practical: higher LIBERO success, lower Franka error, and 10 Hz closed-loop targets matter as much as model size.

## Findings

### Action representations inside VLA policies
Several papers treat the action interface as the main place to improve manipulation. ActionMap replaces pointwise action prediction with voxel heatmaps for translation, rotation, and gripper state. With the rest of OpenVLA-OFT unchanged, it raises the LIBERO four-suite average from 89.1% to 97.3%, and improves real Franka trials from 7/30 to 20/30 at full data.

LARA attacks the same control bottleneck through latent actions. It trains a Latent Action Model (LAM) together with a diffusion VLA policy, aligning the LAM latent with an intermediate policy feature. In the OXE-constrained LIBERO setting, LARA full reports 88.6 average success, above OpenVLA at 76.5 and its DiT-only version at 84.4.

Spline Policy is more methodological. It replaces fixed action chunks with spline parameters that can be resampled, constrained, and passed to controllers. The available excerpt gives no success-rate table, so its evidence is about compatibility and execution structure, not measured gains.

#### Sources
- [ActionMap: Robot Policy Learning via Voxel Action Heatmap](../Inbox/2026-06-05--actionmap-robot-policy-learning-via-voxel-action-heatmap.md): ActionMap summary and reported LIBERO and Franka gains.
- [LARA: Latent Action Representation Alignment for Vision-Language-Action Models](../Inbox/2026-06-05--lara-latent-action-representation-alignment-for-vision-language-action-models.md): LARA joint latent-action alignment method and benchmark results.
- [Spline Policy: A Structured Representation for Robot Policies](../Inbox/2026-06-05--spline-policy-a-structured-representation-for-robot-policies.md): Spline Policy action-output design and limits of the available evidence.

### Task adaptation without target action labels
WIZARD focuses on the cost of adapting a frozen VLA policy to new tasks. It predicts task-specific Low-Rank Adaptation (LoRA) weights from a language instruction and a short demonstration video, then runs the adapted policy with no gradient update at test time.

The strongest result is on held-out LIBERO-Spatial: WIZARD reaches 0.40 average success, compared with 0.19 for MT-VLA with π0.5 and 0.02 for nearest-neighbor adapter retrieval. The paper also shows the boundary of the method. LIBERO-Object remains low at 0.03 average success, and full-task zero-shot completion on LIBERO-10 is still 0.00 in the excerpt.

#### Sources
- [Robotic Policy Adaptation via Weight-Space Meta-Learning](../Inbox/2026-06-05--robotic-policy-adaptation-via-weight-space-meta-learning.md): WIZARD method, held-out LIBERO results, and stated limitations.

### Long-horizon control is being kept close to actions
Coarse-to-Control adds an internal plan, but the plan is made of action tokens. The model predicts coarse future action tokens first, then executable tokens conditioned on that plan. This keeps planning tied to wrist motion, gripper state, and waypoint structure. It reports 97.9% overall success on LIBERO and 83.3% on SimplerEnv-WidowX, with a 62.5% average in real-world tests using 50 demonstrations per task.

FLIGHT brings the same concern to unmanned aerial vehicles. The benchmark uses natural-language missions with continuous 6-DoF control, and its model splits work between a slower video-language module and a faster diffusion action model. The dataset contains 6,689 fine-grained navigation trajectories and samples continuous actions at 10 Hz.

STRIPS-WM covers high-level planning from images. It learns symbolic preconditions and effects from RGB action transitions, then plans in predicate space. Its numbers are about abstraction quality: in BlocksWorld it recovers 16 learned graph states for 16 ground-truth states with zero transition and applicability slack.

#### Sources
- [Coarse-to-Control: Action-Token Planning for Vision-Language-Action Models](../Inbox/2026-06-05--coarse-to-control-action-token-planning-for-vision-language-action-models.md): Coarse-to-Control action-token planning design and LIBERO, SimplerEnv, and real-world results.
- [Think Like a Pilot: Fine-Grained Long-Horizon UAV Navigation](../Inbox/2026-06-05--think-like-a-pilot-fine-grained-long-horizon-uav-navigation.md): FLIGHT benchmark, fast-slow control architecture, and dataset statistics.
- [STRIPS-WM: Learning Grounded Propositional STRIPS-style World Models from Images](../Inbox/2026-06-05--strips-wm-learning-grounded-propositional-strips-style-world-models-from-images.md): STRIPS-WM visual-to-symbolic planning method and reported abstraction metrics.

### Deployment latency and cross-robot interfaces
RhinoVLA is the clearest deployment paper in the set. It targets closed-loop manipulation on edge hardware, using Qwen3-VL to reduce visual-token cost and a continuous Action Expert for action chunks. The system reports 11.69 Hz end-to-end inference on the Huixi R1 edge system, above its 10 Hz control target.

The paper also names the runtime bottleneck it is trying to cut. In its π0.5 latency breakdown on Jetson AGX Orin, the VLM backbone and Action Expert account for more than 90% of runtime, and VLM MLP projections account for about 74.7% of VLM latency. Its cross-robot design uses a View Registry, a shared 72D state-action slot space, masks for missing robot dimensions, and robot-instance LoRA modules.

#### Sources
- [RhinoVLA Technical Report](../Inbox/2026-06-05--rhinovla-technical-report.md): RhinoVLA deployment design, latency breakdown, and 11.69 Hz result.
