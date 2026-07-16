---
kind: trend
trend_doc_id: 790
granularity: day
period_start: '2026-07-02T00:00:00'
period_end: '2026-07-03T00:00:00'
topics:
- robot learning
- vision-language-action policies
- world models
- test-time control
- robot data
run_id: materialize-outputs
aliases:
- recoleta-trend-790
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-policies
- topic/world-models
- topic/test-time-control
- topic/robot-data
language_code: en
pass_output_id: 328
pass_kind: trend_synthesis
---

# Robot policies are being rebuilt around control-loop evidence

## Overview
Robot learning is being judged inside the control loop. The strongest papers add future-change priors, drift monitors, critics, world-model rollouts, and cheaper motion data to make vision-language-action (VLA) policies survive contact, camera changes, and limited demonstrations. Bridge-WA, VLA-Corrector, and TAP give the clearest measured claims.

## Findings

### Future-change and motion forecasts
Several papers make prediction more action-specific. Bridge-WA distills a 5B future-change teacher into future tokens, change maps, and motion-flow maps, then removes the teacher at deployment. It reports 52.8% average success on VLABench, compared with 43.1% for the strongest listed success-rate baseline, and stronger Dobot hard-track results under distractors, lighting changes, and tablecloth changes.

PhysMani applies the same pressure to dynamic 3D manipulation. It models scenes with 30,000 3D Gaussians and predicts local velocity fields for moving targets. On PhysMani-Bench, it reports 45.9% mean simulation success, ahead of the listed 3D policy and Gaussian baselines, while still losing on some tasks such as Insert Peg.

#### Sources
- [Bridge-WA: Predicting Where and How the World Changes for Robotic Action](../Inbox/2026-07-02--bridge-wa-predicting-where-and-how-the-world-changes-for-robotic-action.md): Bridge-WA summary, method, and VLABench/Dobot results.
- [PhysMani: Physics-principled 3D World Model for Dynamic Object Manipulation](../Inbox/2026-07-02--physmani-physics-principled-3d-world-model-for-dynamic-object-manipulation.md): PhysMani summary, 3D Gaussian method, benchmark results, and task caveats.

### Test-time steering for action chunks and plans
Inference-time control is a major theme. VLA-Corrector keeps the VLA backbone frozen, monitors expected versus observed visual-latent change, cuts off stale action chunks, and guides the next flow-matching denoising step. On MetaWorld, pi0.5 rises from 48.70% to 64.35% average success, and SmolVLA at horizon 10 improves success while reducing policy calls.

Guided Action Flow uses a learned action-chunk critic to steer a frozen SmolVLA sampler. The gains are strongest in local settings: one LIBERO spatial task improves by 14 points, while the locked held-out gain is 2.5 points. ACID adds a separate check for world-model planning by asking whether predicted latent transitions are consistent with the conditioned actions; it improves success across Le-WM and PLDM manipulation tasks without retraining the world model.

#### Sources
- [VLA-Corrector: Lightweight Detect-and-Correct Inference for Adaptive Action Horizon](../Inbox/2026-07-02--vla-corrector-lightweight-detect-and-correct-inference-for-adaptive-action-horizon.md): VLA-Corrector detect-and-correct method and MetaWorld/LIBERO results.
- [Guided Action Flow: Q-Guided Inference for Flow-Matching Vision-Language-Action Policies](../Inbox/2026-07-02--guided-action-flow-q-guided-inference-for-flow-matching-vision-language-action-policies.md): Guided Action Flow critic-guided inference and LIBERO validation/held-out results.
- [ACID: Action Consistency via Inverse Dynamics for Planning with World Models](../Inbox/2026-07-02--acid-action-consistency-via-inverse-dynamics-for-planning-with-world-models.md): ACID inverse-dynamics consistency cost and planning results across world models.

### Lower-cost robot experience
Data cost is being attacked with unlabeled motion and generated rollouts. TAP pretrains a VLA with inverse dynamics on task-agnostic trajectories before language-conditioned behavior cloning. In SIMPLER, TAP-20k reaches 33.32% Avg-All success, compared with 23.15% for the same architecture trained with standard behavior cloning. In real WidowX tests, it improves the push-pumpkin task under background and viewpoint changes.

WorldSample uses real rollouts to seed local action perturbations, generates future observations with an adapted Cosmos-Predict2.5 world model, labels them with a reward model, and feeds selected synthetic transitions into real-robot reinforcement learning. Across five manipulation tasks, it reports 82% average success, compared with 56% for HIL-SERL, while reducing average training steps from 56K to 23K.

#### Sources
- [Learning to Move Before Learning to Do: Task-Agnostic pretraining for VLAs](../Inbox/2026-07-02--learning-to-move-before-learning-to-do-task-agnostic-pretraining-for-vlas.md): TAP task-agnostic pretraining method and SIMPLER/real-world results.
- [WorldSample: Closed-loop Real-robot RL with World Modelling](../Inbox/2026-07-02--worldsample-closed-loop-real-robot-rl-with-world-modelling.md): WorldSample real-synthetic training loop, success rates, and training-step reduction.

### Camera and layout generalization data
The Moving Eye isolates camera and object-position shortcuts in VLA training data. Its dual-arm setup uses one robot for manipulation and another as a moving environmental camera, then mixes moving-camera episodes with static multi-view episodes. On the pen task, fixed-view training reaches 85.0% in-distribution success but only 43.0% under moving-camera evaluation. Mixed data reaches 86.0% in-distribution success and 83.0% under the moving-camera test.

The object-position test shows the same pattern. A multi-fixed baseline drops from 95.0% to 71.9% after shifting the holder, while the mixed 1:3 setting reports 91.9% and 90.6%. The best Gr00t pen-task ratio in the excerpt is Moving:Multi-Fixed = 1:3.

#### Sources
- [The Moving Eye: Enhancing VLA Spatial Generalization via Hybrid Dynamic Data Collection](../Inbox/2026-07-02--the-moving-eye-enhancing-vla-spatial-generalization-via-hybrid-dynamic-data-collection.md): The Moving Eye data setup, shortcut analysis, moving-camera results, and object-position results.
