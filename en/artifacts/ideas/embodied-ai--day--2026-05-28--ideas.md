---
kind: ideas
granularity: day
period_start: '2026-05-28T00:00:00'
period_end: '2026-05-29T00:00:00'
run_id: 1c06e363-c98d-489c-b975-2263ff49b7ab
status: succeeded
topics:
- vision-language-action
- robot manipulation
- real-robot evaluation
- dexterous control
- spatial reasoning
- inference efficiency
tags:
- recoleta/ideas
- topic/vision-language-action
- topic/robot-manipulation
- topic/real-robot-evaluation
- topic/dexterous-control
- topic/spatial-reasoning
- topic/inference-efficiency
language_code: en
pass_output_id: 237
pass_kind: trend_ideas
upstream_pass_output_id: 236
upstream_pass_kind: trend_synthesis
---

# Real-Robot VLA Deployment Controls

## Summary
Real-robot VLA teams should add throughput-aware rollout logging, latency checks, and small adaptation layers before expanding task claims. The clearest operational changes are in evaluation protocol, per-step inference control, and dexterous post-training.

## Time-to-success logging for real-robot VLA comparisons
Robot labs comparing VLA policies should log every rollout as a completion time, hard failure, or safety stop, then report the time-to-success distribution with confidence intervals. PhAIL gives a concrete template: Kaplan-Meier CDFs, Human-Relative Throughput against same-fixture human teleoperation, and per-object KS tests for model comparisons.

This workflow addresses a common adoption blocker: two robot policies can show similar fixed-time success rates while one is much slower or has a worse failure tail. In PhAIL’s Franka FR3 benchmark, the best evaluated VLA was about seven times slower than the human reference by RMST ratio, and no inference model exceeded 19% Human-Relative Throughput on any object. A cheap first check is to reuse existing rollout videos and logs, add timestamps for task completion and unrecoverable failures, and see whether the ranking changes when success rate is replaced with the full completion-time distribution.

### Evidence
- [PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology](../Inbox/2026-05-28--phail-a-real-robot-vla-benchmark-and-distributional-methodology.md): PhAIL defines time-to-success CDF evaluation, Human-Relative Throughput, bootstrap confidence intervals, and reports the gap between evaluated VLAs and same-fixture human teleoperation.
- [PhAIL: A Real-Robot VLA Benchmark and Distributional Methodology](../Inbox/2026-05-28--phail-a-real-robot-vla-benchmark-and-distributional-methodology.md): The paper abstract describes the open Franka FR3 benchmark, per-rollout artifacts, and the distributional evaluation method.

## Per-step compute scheduling around frozen VLA policies
Teams deploying GR00T-like or CogACT-like policies should test a small scheduler that decides when to recompute the vision encoder, LLM, and action head, and when cached representations are safe to reuse. ElegantVLA keeps the base policy frozen and uses representation similarity, robot motion, and episode progress to choose compute modes at each control step.

The practical pain is control frequency. Running every component at every step can leave the robot late during moving-object tracking, contact, alignment, insertion, or placement. ElegantVLA reports GR00T-based real-world tests across six tasks with compute reduced by 2.18×, control frequency rising from 13.8 Hz to 26.3 Hz, and average success rising from 61.67% to 65.00%. VisualThink-VLA adds a related latency lesson: sparse visual evidence channels can keep reasoning in the sub-second range, with BridgeData V2 latency reported at 0.367 seconds per step versus 8.377 seconds for ECoT. A useful adoption test is to require both task success and measured Hz on the real controller, with separate checks for stable motion and contact-heavy phases.

### Evidence
- [ElegantVLA: Learning When to Think for Efficient Vision-Language-Action Models](../Inbox/2026-05-28--elegantvla-learning-when-to-think-for-efficient-vision-language-action-models.md): ElegantVLA describes a frozen-policy scheduler for vision, language, and action computation, with real-world gains in compute, control frequency, and success.
- [ElegantVLA: Learning When to Think for Efficient Vision-Language-Action Models](../Inbox/2026-05-28--elegantvla-learning-when-to-think-for-efficient-vision-language-action-models.md): The abstract states the per-step compute allocation mechanism and the GR00T real-world result of 13.8 Hz to 26.3 Hz.
- [VisualThink-VLA: Visual Intermediate Reasoning for Effective and Low-Latency Vision-Language-Action Policies](../Inbox/2026-05-28--visualthink-vla-visual-intermediate-reasoning-for-effective-and-low-latency-vision-language-action-policies.md): VisualThink-VLA reports sparse visual evidence routing with 0.367 s per step on BridgeData V2 versus 8.377 s for ECoT.

## Human-guided residual adaptation for dexterous VLA hands
Dexterous-hand deployments should separate the pretrained VLA from the real-robot correction layer. BORA freezes the base policy during online use and trains a small residual actor that adds chunk-level corrections, guided by an offline action-conditioned critic and human interventions during risky states.

This is useful for multi-DoF hands because contact errors accumulate quickly and full-model online RL can create unsafe exploration. On five Franka arm plus 12-DoF hand tasks, BORA-Full reached 86.0% average success versus 53.0% for the consistency-policy base. On unseen objects, it reached 70.0% versus 27.0% for the same base. The reported online stage converged within two RL rounds, with one to two human interventions per task and about 20% of online trajectory time under human control. A small validation run can start with one contact-rich task, freeze the base policy, and measure whether residual corrections reduce repeated grasp, slip, or alignment failures without retraining the VLA backbone.

### Evidence
- [BORA: Bridging Offline Reinforcement Learning and Online Residual Adaptation for Real-World Dexterous VLA Models](../Inbox/2026-05-28--bora-bridging-offline-reinforcement-learning-and-online-residual-adaptation-for-real-world-dexterous-vla-models.md): BORA defines the offline critic, frozen base VLA, human-guided residual actor, and reports success gains on real dexterous tasks and unseen objects.
- [BORA: Bridging Offline Reinforcement Learning and Online Residual Adaptation for Real-World Dexterous VLA Models](../Inbox/2026-05-28--bora-bridging-offline-reinforcement-learning-and-online-residual-adaptation-for-real-world-dexterous-vla-models.md): The abstract states the lightweight human-in-the-loop residual adaptation mechanism and the reported 33-point and 43-point success improvements.
