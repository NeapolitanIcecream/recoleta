---
kind: trend
trend_doc_id: 825
granularity: day
period_start: '2026-07-07T00:00:00'
period_end: '2026-07-08T00:00:00'
topics:
- robotics
- vision-language-action models
- world models
- 3D manipulation
- imitation learning
- dexterous manipulation
- robot planning
run_id: materialize-outputs
aliases:
- recoleta-trend-825
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/world-models
- topic/3d-manipulation
- topic/imitation-learning
- topic/dexterous-manipulation
- topic/robot-planning
language_code: en
pass_output_id: 340
pass_kind: trend_synthesis
---

# Robot policy work is concentrating on geometry, generated demonstrations, and control latency

## Overview
The day’s robot papers put physical detail inside policy pipelines. Vision-language-action (VLA) models add 3D structure, reusable demonstrations, cached action chunks, and explicit handoff checks. RynnWorld-4D, RynnWorld-Teleop, and Lift3D-VLA show the clearest emphasis: make robot control faster and more spatially grounded while reducing dependence on raw physical data collection.

## Findings

### 4D world models for manipulation and teleoperation
RynnWorld-4D treats future prediction as RGB, depth, and optical flow together. Depth lifts pixels into 3D points, and optical flow links them over time, giving the policy a scene-flow view of contact and motion. The reported data scale is large for this period: Rynn4DDataset 1.0 has more than 254.4 million frames. The policy path still costs 1,106 ms per planning pass on an RTX 5090, with the world model taking 990 ms, so latency remains a central constraint.

RynnWorld-Teleop uses an action-conditioned video model as a data engine. Operator hand poses drive robot-centric egocentric video, and the generated dataset pairs frames with 54-dimensional robot actions for dual arms and dexterous hands. The distilled model reports 40+ FPS on one H100, which makes interactive generation plausible. The paper claims zero-shot sim-to-real transfer using generated data, but the available excerpt does not include the success-rate table.

### 3D geometry inside VLA policies
Lift3D-VLA adds point-cloud reasoning to a VLA policy while reusing a pretrained 2D vision encoder. It projects 3D points onto six virtual planes, tokenizes 1024 points into 256 tokens, and trains the encoder to reconstruct current geometry and predict next-frame geometry. The action decoder also spreads action-chunk prediction across LLaMA2-7B layers.

The reported gains are concrete: 10.8 percentage points higher mean success on MetaWorld, 11.1 points on RLBench, and 4 points over the strongest real-world baseline in the excerpt. This cluster matters because the day’s strongest manipulation claims are tied to reachability, occlusion, contact, and future geometry, not only language-conditioned image features.

### Efficient VLA training and inference
ActionCache attacks inference cost in flow-based VLA models by reusing past action chunks. A compact key retrieves a cached action, then the system executes it directly or refines it with one or two flow steps. On VLABench with π0.5, the full model gets 38.8% success at 18.8 ms action-head latency; ActionCache with no refinement gets 32.9% at 1.6 ms. With one refinement step, it reaches 32.4% at 3.6 ms, while direct one-step generation falls to 6.8%.

SIEVE addresses the training side. It segments demonstrations at gripper or hand-state changes, clusters reusable visuo-motor primitives, and selects central trajectories within primitive-sequence buckets. On Bridge-V2 with Qwen3-VL-4B-GR00T, 50% of the demonstrations and 25K steps reach 56.3% average success, above full-data training at 51.8% with 50K steps. The evidence supports a practical message: selection and reuse can improve robot policy quality without scaling every dataset and every forward pass.

### Deployment failures expose weak skill boundaries
The BEHAVIOR-1K handoff study shows why high single-skill scores do not guarantee long-horizon robot success. Several isolated skills score well, including pick_up_from at 96.5% and place_on at 100.0%, yet end-to-end task predicate success is described as near zero. Across 30 rollouts, mean progress is 19.5%. A 10-rollout trace records 130 failed skill attempts, including grasp control, placement, target-grounding, and navigation-readiness failures.

LAMP shows a complementary route for real hardware: constrain dexterous hand exploration with a learned 2-D latent motion prior. Starting with small demonstration sets, it reaches 56.25% average imitation-learning success and 98.75% average final success after online reinforcement learning across four real robot tasks. The ablations are sharp: removing the low-dimensional bottleneck drops final success to 55.0%, and raw behavior cloning averages 3.75% after reinforcement learning.
