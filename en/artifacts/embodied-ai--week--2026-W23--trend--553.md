---
kind: trend
trend_doc_id: 553
granularity: week
period_start: '2026-06-01T00:00:00'
period_end: '2026-06-08T00:00:00'
topics:
- robotics
- vision-language-action
- 3D grounding
- world models
- policy evaluation
- action representation
- robot adaptation
run_id: materialize-outputs
aliases:
- recoleta-trend-553
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action
- topic/3d-grounding
- topic/world-models
- topic/policy-evaluation
- topic/action-representation
- topic/robot-adaptation
language_code: en
pass_output_id: 264
pass_kind: trend_synthesis
---

# Robot VLA progress is being measured by executable control

## Overview
This week, robot Vision-Language-Action (VLA) work is judged by executable control. The strongest evidence ties gains to 3D grounding, closed-loop world models, and action heads that reduce real robot error. Dex-BEV, PiL-World, and ActionMap show the pattern across benchmarks and hardware.

## Clusters

### 3D grounding for VLA manipulation
Spatial alignment is a main performance lever. Dex-BEV puts visual geometry, proprioception, and output actions into a shared bird’s-eye-view coordinate frame. It reports 97.8% average success on official LIBERO, 76.0% on RoboTwin 2.0 Clean, and 89.9% on modified LIBERO camera and pose settings where listed 2D baselines fall below 10%.

GeoAlign adds RGB-derived geometry features queried by robot state. The gains are clearest on geometry-sensitive tasks: real ALOHA average success is 78.8%, versus 65.0% for the RGB-only baseline, with transparent-bottle success at 75.0% versus 35.0%. 3DThinkVLA takes a lighter deployment route. It trains latent 3D perception and reasoning adapters, then runs on 2D images at inference while reaching 98.7% on LIBERO and 81.0% on LIBERO-PLUS.

#### Evidence
- [Dexterity-BEV: Aligning 3D World and Actions for Generalizable Robot Policies Learning](../Inbox/2026-06-01--dexterity-bev-aligning-3d-world-and-actions-for-generalizable-robot-policies-learning.md): Dex-BEV results and shared 3D/BEV alignment design.
- [GeoAlign: Beyond Semantics with State-Guided Spatial Alignment in VLA Models](../Inbox/2026-06-02--geoalign-beyond-semantics-with-state-guided-spatial-alignment-in-vla-models.md): GeoAlign geometry-conditioned VLA design and LIBERO, SimplerEnv, real ALOHA results.
- [3DThinkVLA: Endowing Vision-Language-Action Models with Latent 3D Priors via 3D-Thinking-Guided Co-training](../Inbox/2026-06-03--3dthinkvla-endowing-vision-language-action-models-with-latent-3d-priors-via-3d-thinking-guided-co-training.md): 3DThinkVLA latent 3D training method and LIBERO/LIBERO-PLUS results.

### World models for control and policy evaluation
World Action Models (WAMs) are being tested by their effect on action choice, latency, and real rollout agreement. GeoSem-WAM trains future RGB, geometry, and semantic prediction heads, then removes those heads at deployment. The reported results are practical: 98.55% average success on LIBERO and 95.4% average success on real Franka tasks, compared with 88.9% for Fast-WAM.

PiL-World uses a policy-in-the-loop setup. A frozen VLA predicts an action chunk, the world model predicts the next multi-view observation, and that generated observation becomes the next policy input. Across three real dual-arm tasks, it cuts the average real-versus-imagined success-rate gap to 12.0%, compared with 63.2% for Ctrl-World, and reports 0.94 Pearson correlation between real and imagined success rates.

#### Evidence
- [GeoSem-WAM: Geometry- and Semantic-Aware World Action Models](../Inbox/2026-06-02--geosem-wam-geometry-and-semantic-aware-world-action-models.md): GeoSem-WAM structured future prediction targets, deployment design, and LIBERO/Franka results.
- [PiL-World: A Chunk-Wise World Model for VLA Policy-in-the-Loop Evaluation](../Inbox/2026-06-04--pil-world-a-chunk-wise-world-model-for-vla-policy-in-the-loop-evaluation.md): PiL-World closed-loop imagined rollout method and real-imagined success-rate agreement.

### Action heads and adapters as deployment levers
Several papers improve policy behavior by changing the action interface or adaptation route while keeping the main VLA mostly fixed. ActionMap replaces single-point action decoding with voxel heatmaps over translation, rotation, and gripper commands. On LIBERO with OpenVLA-OFT, it reaches 97.3% average success versus 89.1% for L1 regression at matched training steps. On real Franka tasks, it succeeds in 20 of 30 trials versus 7 of 30 for the regression head.

WIZARD targets task adaptation. It predicts task-specific LoRA weights from a language instruction and a short demonstration video, then runs a frozen VLA with the generated adapter. On held-out LIBERO-Spatial, it reaches 0.40 average success, compared with 0.19 for the strongest listed multi-task VLA baseline and 0.02 for nearest-neighbor adapter retrieval. The remaining gap to task-specific experts is large, but the evidence shows that adaptation speed and data requirements are now part of the control story.

#### Evidence
- [ActionMap: Robot Policy Learning via Voxel Action Heatmap](../Inbox/2026-06-05--actionmap-robot-policy-learning-via-voxel-action-heatmap.md): ActionMap voxel heatmap action head, LIBERO gains, low-data results, and real Franka trials.
- [Robotic Policy Adaptation via Weight-Space Meta-Learning](../Inbox/2026-06-05--robotic-policy-adaptation-via-weight-space-meta-learning.md): WIZARD generated LoRA adaptation method and held-out LIBERO results.
