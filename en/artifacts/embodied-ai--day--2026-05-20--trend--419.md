---
kind: trend
trend_doc_id: 419
granularity: day
period_start: '2026-05-20T00:00:00'
period_end: '2026-05-21T00:00:00'
topics:
- embodied AI
- vision-language-action
- robot manipulation
- 3D perception
- dexterous hands
- world models
- robot evaluation
run_id: materialize-outputs
aliases:
- recoleta-trend-419
tags:
- recoleta/trend
- topic/embodied-ai
- topic/vision-language-action
- topic/robot-manipulation
- topic/3d-perception
- topic/dexterous-hands
- topic/world-models
- topic/robot-evaluation
language_code: en
pass_output_id: 188
pass_kind: trend_synthesis
---

# Robot research treats 3D contact and real testbeds as the main evidence

## Overview
Embodied AI is the clear center. Vision-language-action (VLA) papers are judged by 3D contact cues, real hardware, perturbation tests, and reproducible evaluation. GaussianDream, PointACT, and VLA-REPLICA give the strongest signal.

## Clusters

### 3D-aware VLA control
Several robot papers put geometry closer to the action output. GaussianDream trains a VLA policy with 3D Gaussian reconstruction and short-horizon scene-flow prediction, then removes the decoding heads at inference and keeps only learned prefix tokens. It reports 98.4% average success on LIBERO and 52.6% on RoboCasa Human-50.

PointACT makes the action decoder attend to multi-scale point-cloud features. Its reported LIBERO average is 96.0%, with a 17.9-point gain over SpatialVLA in the same table. DISC tackles a different grounding failure: the instruction generates a task-specific policy, while the control policy sees only observations. That design reaches 94.3% on LIBERO-90 and 86.4% on a real 9-task shared-context setup.

#### Evidence
- [GaussianDream: A Feed-Forward 3D Gaussian World Model for Robotic Manipulation](../Inbox/2026-05-20--gaussiandream-a-feed-forward-3d-gaussian-world-model-for-robotic-manipulation.md): GaussianDream training design and reported LIBERO, RoboCasa, and real-robot results.
- [PointACT: Vision-Language-Action Models with Multi-Scale Point-Action Interaction](../Inbox/2026-05-20--pointact-vision-language-action-models-with-multi-scale-point-action-interaction.md): PointACT point-cloud action interaction and LIBERO comparison results.
- [DISC: Decoupling Instruction from State-Conditioned Control via Policy Generation](../Inbox/2026-05-20--disc-decoupling-instruction-from-state-conditioned-control-via-policy-generation.md): DISC policy-generation design and simulated plus real manipulation results.

### Reproducible evaluation for robot policies and world models
Evaluation work is becoming more concrete and cheaper to repeat. VLA-REPLICA defines a real-world VLA testbed built from about $1050 of parts, with 10 manipulation tasks, 500 demonstrations, and 90 test scenes. In its in-distribution results, π0.5 leads the tested policies at 0.54 average success, which also shows how much room remains on low-cost physical setups.

stable-worldmodel addresses the world-model side with shared data loading, baseline training, model-predictive control planning, and evaluation across robotics and control tasks. Its Lance data layer reaches 4,815 Push-T samples per second locally, compared with 1,416 for HDF5. Lost in Fog adds a driving VLA stress test: Alpamayo R1’s chain-of-causation explanation changes correlate with much larger trajectory deviations under noise, lighting changes, and fog.

#### Evidence
- [VLA-REPLICA: A Low-Cost, Reproducible Benchmark for Real-World Evaluation of Vision-Language-Action Models](../Inbox/2026-05-20--vla-replica-a-low-cost-reproducible-benchmark-for-real-world-evaluation-of-vision-language-action-models.md): VLA-REPLICA hardware cost, task suite, demonstrations, scenes, and policy results.
- [stable-worldmodel: A Platform for Reproducible World Modeling Research and Evaluation](../Inbox/2026-05-20--stable-worldmodel-a-platform-for-reproducible-world-modeling-research-and-evaluation.md): stable-worldmodel data layer, included baselines, benchmark coverage, and loading results.
- [Lost in Fog: Sensor Perturbations Expose Reasoning Fragility in Driving VLAs](../Inbox/2026-05-20--lost-in-fog-sensor-perturbations-expose-reasoning-fragility-in-driving-vlas.md): Driving VLA perturbation study and link between explanation changes and trajectory deviation.

### Dexterous manipulation with local sensing and hard safety
Dexterous-hand papers focus on control signals that can survive hardware limits. Proprioceptive Transformer uses only joint position and velocity histories on a tendon-driven ORCA hand. On a 55 mm cube, its direct-joint-sensing policy reaches 11.83 RPM with 100% rotation accuracy and no drops across three 60-second trials.

SafePBDS adds explicit safety constraints to geometric motion policies. It solves for configuration-space acceleration while enforcing task-manifold safety conditions as hard constraints. On a Franka Panda plus Allegro Hand, it reports 92.5% success across 120 household-object grasping trials and more than 360° yaw reorientation in both directions.

#### Evidence
- [Learning Robust Dexterous In-Hand Manipulation from Joint Sensors with Proprioceptive Transformer](../Inbox/2026-05-20--learning-robust-dexterous-in-hand-manipulation-from-joint-sensors-with-proprioceptive-transformer.md): Proprioceptive Transformer joint-only sensing setup and real ORCA hand rotation results.
- [Safe and Steerable Geometric Motion Policies for Robotic Dexterous Manipulation](../Inbox/2026-05-20--safe-and-steerable-geometric-motion-policies-for-robotic-dexterous-manipulation.md): SafePBDS constraint formulation and hardware dexterous manipulation results.

### Cross-embodiment imitation through latent goals
Demo-JEPA treats a demonstration as a goal signal that the target robot must realize with its own dynamics. A V-JEPA-style encoder maps observations to latent states, a Dreamer Predictor estimates a target-compatible future latent goal, and the robot plans actions toward that goal with its own world model.

The results are strongest in transfer settings. In simulation, Demo-JEPA averages 0.45 success on cross-embodiment bridging and 0.36 on zero-shot generalization, ahead of VPP and XSkill in the reported comparisons. In-domain behavior grounding is weaker, with 0.31 success in RLBench simulation and 0.43 in real-world behavior grounding.

#### Evidence
- [Demo-JEPA: Joint-Embedding Predictive Architecture for One-shot Cross-Embodiment Imitation](../Inbox/2026-05-20--demo-jepa-joint-embedding-predictive-architecture-for-one-shot-cross-embodiment-imitation.md): Demo-JEPA latent-goal method and mixed cross-embodiment, zero-shot, and behavior-grounding results.
