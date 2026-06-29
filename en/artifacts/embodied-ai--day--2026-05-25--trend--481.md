---
kind: trend
trend_doc_id: 481
granularity: day
period_start: '2026-05-25T00:00:00'
period_end: '2026-05-26T00:00:00'
topics:
- robot learning
- vision-language-action models
- world models
- reinforcement learning
- robot deployment
- adversarial reliability
run_id: materialize-outputs
aliases:
- recoleta-trend-481
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/world-models
- topic/reinforcement-learning
- topic/robot-deployment
- topic/adversarial-reliability
language_code: en
pass_output_id: 230
pass_kind: trend_synthesis
---

# Robot learning work centers on deployable control and measurable failure modes

## Overview
The day’s strongest signal is practical robot control. Vision-language-action (VLA) work pairs fast real-robot fine-tuning with action-space geometry, and world-model papers tighten latent planning and policy search. EXPO-FT, OASIS, and MBDPO carry the main empirical claims; deployment and adversarial studies add reliability checks.

## Clusters

### VLA manipulation fine-tuning
VLA manipulation papers put more weight on real execution metrics. EXPO-FT keeps a pretrained π0.5 policy and trains a lightweight edit policy with off-policy reinforcement learning. It reports 30/30 final successes on each of 8 real-world manipulation tasks after an average of 19.1 minutes of online robot data.

OASIS attacks the action decoding problem directly. It predicts an 8-step SE(3) end-effector trajectory, meaning 3D position and rotation, before producing 6-DoF actions and gripper commands. The paper reports 97.6% average success on LIBERO and 89.2% average success in real-world tests on Franka Research 3 and Kinova Gen3 robots.

#### Evidence
- [EXPO-FT: Sample-Efficient Reinforcement Learning Finetuning for Vision-Language-Action Models](../Inbox/2026-05-25--expo-ft-sample-efficient-reinforcement-learning-finetuning-for-vision-language-action-models.md): EXPO-FT summary gives the pretrained VLA fine-tuning setup, 8 real-world tasks, 30/30 success, and 19.1 minutes of online data.
- [OASIS: Observation-Action Space Alignment via SE(3) Trajectory Prediction for Robotic Manipulation](../Inbox/2026-05-25--oasis-observation-action-space-alignment-via-se-3-trajectory-prediction-for-robotic-manipulation.md): OASIS summary gives the SE(3) trajectory predictor, action-chunk decoder, LIBERO score, and real-robot success rate.

### Factory deployment and attack checks
The deployment evidence is more operational than architectural. The Siemens factory-floor case study fine-tunes Pi0.5 for transparent accessory-bag packaging, using 2,535 episodes and about 10 hours of data. Its failure breakdown is concrete: in unconstrained trials, bag contents left above the product account for 65% of failed episodes, with multiple-bag grasps at 23% and poor or failed grasps at 15%.

A separate VLA reliability paper gives an information-theoretic bound for capability and adversarial reliability. It cites OpenVLA-7B dropping from above 95% LIBERO success to under 5% under a 16/255 PGD image attack, then validates the bound with zero violations across 320 cells covering Gaussian proxies, OpenVLA, LIBERO suites, attack types, horizons up to 10, and two action-head designs.

#### Evidence
- [A Factory-Floor Deployment Case Study of VLA Pipelines for Industrial Packaging Task: Workflow, Failures, and Lessons](../Inbox/2026-05-25--a-factory-floor-deployment-case-study-of-vla-pipelines-for-industrial-packaging-task-workflow-failures-and-lessons.md): Factory case summary provides the Pi0.5 packaging task, dataset size, training workflow, and failure-rate breakdown.
- [Capability and Robustness Cannot Both Be Free: An Information-Theoretic Bound for Vision-Language-Action Models](../Inbox/2026-05-25--capability-and-robustness-cannot-both-be-free-an-information-theoretic-bound-for-vision-language-action-models.md): Reliability-bound summary provides the OpenVLA attack example, formal bound scope, and 320-cell validation result.

### World-model control
World-model papers focus on state representations that support planning and policy improvement. TC-WM compresses frozen visual foundation features and proprioception into task-centric latents, then trains action-conditioned dynamics for planning or reinforcement learning. The reported coverage spans 9 benchmarks across Robomimic, D4RL, navigation, locomotion, manipulation, and simulated plus real-world settings, though the summary does not include exact score tables.

MBDPO trains a diffusion action policy inside a latent world model, so imagined rollouts guide the same policy distribution used at execution time. Its strongest numeric claims are scale and breadth: model size grows from 1.7M to 340M parameters, online experiments cover 4 benchmark suites and 121 tasks, and an 8-task drift study reports lower action drift than TD-MPC2.

LeJEPA adds theory for when a learned representation is a usable world model. Under Gaussian latent variables and stationary additive-noise positive pairs, the optimum recovers the latent state up to an orthogonal transform. The paper also links that recovery to finite-horizon planning when costs are invariant under such transforms.

#### Evidence
- [Back to Parsimonious Latents: Learning Task-Centric World Models from Visual Foundations](../Inbox/2026-05-25--back-to-parsimonious-latents-learning-task-centric-world-models-from-visual-foundations.md): TC-WM summary gives the compact latent design, planning uses, benchmark coverage, and missing exact metric caveat.
- [Scaling World-Model Reinforcement Learning Through Diffusion Policy Optimization](../Inbox/2026-05-25--scaling-world-model-reinforcement-learning-through-diffusion-policy-optimization.md): MBDPO summary gives the diffusion policy inside a world model, scaling range, benchmark breadth, and action-drift comparison.
- [When Does LeJEPA Learn a World Model?](../Inbox/2026-05-25--when-does-lejepa-learn-a-world-model.md): LeJEPA summary gives the Gaussian identifiability conditions, theorem statements, and planning link.
