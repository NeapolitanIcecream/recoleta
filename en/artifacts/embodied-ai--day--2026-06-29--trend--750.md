---
kind: trend
trend_doc_id: 750
granularity: day
period_start: '2026-06-29T00:00:00'
period_end: '2026-06-30T00:00:00'
topics:
- robot learning
- vision-language-action models
- manipulation
- test-time RL
- tactile sensing
- navigation
- autonomous driving
run_id: materialize-outputs
aliases:
- recoleta-trend-750
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action-models
- topic/manipulation
- topic/test-time-rl
- topic/tactile-sensing
- topic/navigation
- topic/autonomous-driving
language_code: en
pass_output_id: 322
pass_kind: trend_synthesis
---

# Robot policies are being judged by execution mechanics, not benchmark scores alone

## Overview
Robot learning work centered on making policies executable under real control constraints. ZR-0, T2VLA, and Chronos show the main emphasis: cross-embodiment supervision, reward-free test-time improvement, and memory over full trajectories.

## Findings

### Vision-language-action policy training
Vision-language-action (VLA) papers focused on the parts of policy learning that decide whether a high-level model can control a robot. ZR-0 trains a 2.6B-parameter VLA model with dense embodied chain-of-thought labels, then skips text generation at inference while a diffusion action expert outputs continuous action chunks. It reports 97.8% average success on LIBERO and uses ProcCorpus-60M, with about 60M frames and ECoT labels for 96.8% of frames.

T2VLA adds reinforcement learning (RL) at test time using the policy’s own confidence as the reward signal. On LIBERO, it raises OpenVLA-OFT from 91.0% to 97.2% average success, π0 from 57.7% to 81.9%, and π0.5 from 77.1% to 85.1%. SA-VLA attacks a lower-level failure point: fixed action-token decoding. Its state-aware tokenizer lifts RoboTwin average success to 0.56, compared with 0.29 for the strongest listed tokenizer baseline.

#### Sources
- [Training Vision-Language-Action Models with Dense Embodied Chain-of-Thought Supervision](../Inbox/2026-06-29--training-vision-language-action-models-with-dense-embodied-chain-of-thought-supervision.md): ZR-0 architecture, ProcCorpus-60M scale, and LIBERO results.
- [Trust Your Instincts: Confidence-Driven Test-Time RL for Vision-Language-Action Models](../Inbox/2026-06-29--trust-your-instincts-confidence-driven-test-time-rl-for-vision-language-action-models.md): T2VLA confidence-driven test-time RL method and LIBERO gains.
- [SA-VLA: State-aware tokenizer for improving Vision-Language-Action Models' performance](../Inbox/2026-06-29--sa-vla-state-aware-tokenizer-for-improving-vision-language-action-models-performance.md): SA-VLA state-aware tokenizer design and RoboTwin results.

### Long-horizon manipulation and geometric execution
Several systems make task phase, object geometry, and recovery explicit. Chronos treats the full observation history as the policy state for long-horizon manipulation where the same camera view can require different actions. It reports 73.6% average success on RMBench and 78% average success across four real-world dual-arm tasks.

OpenSPM stores object-relative key poses from demonstrations and transfers them using 6D object pose estimates. Its 0.24M-parameter action model reports 85.6% success on 10 LIBERO-GOAL tasks and 4.8 ms action-chunk generation latency. Spark uses one LLM-generated behavior tree, then spends test-time compute on object grounding and retry logic. It reaches 43.7% mean success on six Libero-Pro perturbation cells and 68% mean success across 11 physical robot task cells.

#### Sources
- [Chronos: A Physics-Informed Full-History Framework for Non-Markovian Long-Horizon Manipulation](../Inbox/2026-06-29--chronos-a-physics-informed-full-history-framework-for-non-markovian-long-horizon-manipulation.md): Chronos full-history policy state and RMBench/real-world success rates.
- [OpenSPM: An Environment-Transferable Robotic Key Spatial Pose Memory and Closed-Loop High-Frequency Flow-Matching Action Generation Model](../Inbox/2026-06-29--openspm-an-environment-transferable-robotic-key-spatial-pose-memory-and-closed-loop-high-frequency-flow-matching-action-generation-model.md): OpenSPM key-pose memory, model size, latency, and LIBERO-GOAL results.
- [Sequential Planning via Anchored Robotic Keypoints](../Inbox/2026-06-29--sequential-planning-via-anchored-robotic-keypoints.md): Spark behavior-tree planning, perception retries, and simulation/real-robot results.

### Validation, deployment, and touch sensing
The period also exposed how much policy iteration depends on measurement and sensing. Critical Interval MSE scores only task-critical trajectory segments and aligns action sequences before comparing predictions with expert actions. On LBM-Eval, it reaches Spearman ρ = -0.87 against rollout success, compared with -0.61 for raw MSE.

The UR5e case study shows a separate deployment problem. OpenVLA inference ran at about 3 Hz on an A100, and the authors report unstable closed-loop behavior when action semantics, coordinate frames, timing, preprocessing, and data coverage are misaligned. Heterogeneous Tactile Transformer extends this engineering focus to contact sensing, training one tactile backbone across optical and array sensors. In camera-free real-world tests with unseen Sharpa fingertips, it reaches 95% success on toy screw and 55% on grasp tofu.

#### Sources
- [Critical Interval MSE: Toward Reliable Offline Validation for Robot Manipulation Policies](../Inbox/2026-06-29--critical-interval-mse-toward-reliable-offline-validation-for-robot-manipulation-policies.md): CI-MSE definition and correlation results against rollout success.
- [Vision-Language-Action Models: Experimental Insights from a Real-World UR5 Platform](../Inbox/2026-06-29--vision-language-action-models-experimental-insights-from-a-real-world-ur5-platform.md): UR5e VLA deployment pipeline, inference speed, and closed-loop instability findings.
- [Heterogeneous Tactile Transformer](../Inbox/2026-06-29--heterogeneous-tactile-transformer.md): HTT paired tactile pretraining and real-world tactile manipulation results.

### World models for navigation and driving
World-model work appeared in navigation and autonomous driving, with plans tied to predicted future observations. SWAM generates intermediate RGB-D sequences and 2D actions in one diffusion pass for visual navigation. It cuts RECON absolute trajectory error to 0.93 versus 1.53 for NWM+NoMaD x16, and runs in 16.91 seconds per episode versus 245.98 seconds for that sampled planner.

LWDrive uses a vision-language model (VLM) for a coarse driving trajectory, then refines candidate trajectories with world-model-supervised features and bird’s-eye-view geometry. It reports 92.0 PDMS on NAVSIM and 89.6 EPDMS on NAVSIM-v2. X-Morph covers a different control setting: it maps human motion into quadruped, hexapod, and quadruped-manipulator behaviors. On Go2 clips, its physics corrector reduces foot slip by 27.2% and penetration p95 by 46.9%.

#### Sources
- [Pondering the Way: Spatial-perceiving World Action Model for Embodied Navigation](../Inbox/2026-06-29--pondering-the-way-spatial-perceiving-world-action-model-for-embodied-navigation.md): SWAM joint observation-action generation and navigation metrics.
- [LWDrive: Layer-Wise World-Model-Guided Vision-Language Model Planning for Autonomous Driving](../Inbox/2026-06-29--lwdrive-layer-wise-world-model-guided-vision-language-model-planning-for-autonomous-driving.md): LWDrive VLM planning method and NAVSIM/NAVSIM-v2 scores.
- [X-Morph: Human Motion Priors for Scalable Robot Learning Across Morphologies](../Inbox/2026-06-29--x-morph-human-motion-priors-for-scalable-robot-learning-across-morphologies.md): X-Morph cross-morphology motion transfer and physics-correction metrics.
