---
kind: trend
trend_doc_id: 730
granularity: day
period_start: '2026-06-25T00:00:00'
period_end: '2026-06-26T00:00:00'
topics:
- robotics
- vision-language-action models
- behavior cloning
- test-time scaling
- robot safety
- contact-rich manipulation
run_id: materialize-outputs
aliases:
- recoleta-trend-730
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/behavior-cloning
- topic/test-time-scaling
- topic/robot-safety
- topic/contact-rich-manipulation
language_code: en
pass_output_id: 312
pass_kind: trend_synthesis
---

# Robot VLA papers are converging on rollout-grounded reliability

## Overview
Robot vision-language-action (VLA) research is focused on real manipulation evidence: open rollouts, deployment checks, and safety metrics. ABC makes behavior cloning more reproducible. E-TTS adds inference-time candidate scoring. ForesightSafety-VLA scores unsafe success during full trajectories.

## Findings

### Open manipulation data and denser action supervision
ABC raises the reproducibility bar for behavior cloning by releasing data, code, hardware details, model weights, simulation assets, and real rollout scores. Its ABC-130K dataset contains 3,553 hours, 134,806 episodes, and 195 tasks, with more than 100 hours of real policy rollouts in ABC-Eval. The paper also reports that simulation and some offline diagnostics track real-world success, giving researchers cheaper signals for model choices.

LA4VLA attacks a different data problem inside VLA pretraining. Long demonstrations often pair one high-level instruction with many image-action frames, so the language signal is sparse. LA4VLA cuts demonstrations into short language-action segments, keeps 33,116 human-verified episodes, and trains a 1B model with image-free language, proprioception, and action trajectories before VLA training. Its mixed language-action and VLA pretraining reports 83.3% real-world manipulation success and a 45.0 point gain over no pretraining on real tasks.

#### Sources
- [Scalable Behavior Cloning with Open Data, Training, and Evaluation](../Inbox/2026-06-25--scalable-behavior-cloning-with-open-data-training-and-evaluation.md): ABC dataset scale, released stack, rollout evaluation, and diagnostic correlations.
- [LA4VLA: Learning to Act without Seeing via Language-Action Pretraining](../Inbox/2026-06-25--la4vla-learning-to-act-without-seeing-via-language-action-pretraining.md): LA4VLA language-action dataset construction and reported simulation and real-world gains.

### Inference-time checks for deployed policies
Several papers treat a frozen or trained VLA policy as one component inside a monitored execution loop. E-TTS samples reasoning-action pairs, scores them with vision-language verifiers, stores recent history, and asks for feedback when candidates fail. Across its reported settings, it gives an average simulated success gain of 13.52 points and a maximum gain of 33.14 points.

PhysReflect-VLA adds physical-feasibility scoring before action execution and compares predicted next states with observed next states after execution. If the mismatch is large, a reflector generates corrective guidance. On five real-robot tasks, Phys-OVLA improves average success by 5.4 points over OVLA-FT, and Phys-OFT improves by 3.0 points over OVLA-OFT.

RouterVLA shows that pre-deployment smoke tests can also guide policy choice. On LIBERO-Plus, a simple probe-success rule selects among frozen experts and reaches 0.6149 held-out success, compared with 0.4686 for the global best expert.

#### Sources
- [E-TTS: A New Embodied Test-Time Scaling Framework for Robotic Manipulation](../Inbox/2026-06-25--e-tts-a-new-embodied-test-time-scaling-framework-for-robotic-manipulation.md): E-TTS reasoning-action sampling, verifier scoring, history buffer, and success gains.
- [PhysReflect-VLA: Physical Feasibility and Self-Reflective Regulation for Reliable Vision-Language-Action Policies](../Inbox/2026-06-25--physreflect-vla-physical-feasibility-and-self-reflective-regulation-for-reliable-vision-language-action-policies.md): PhysReflect-VLA feasibility checks, reflection mechanism, and real-robot gains.
- [RouterVLA: Turning Smoke Tests into Supervision for Heterogeneous VLA Selection](../Inbox/2026-06-25--routervla-turning-smoke-tests-into-supervision-for-heterogeneous-vla-selection.md): RouterVLA smoke-test routing protocol and held-out success improvement.

### Action modules are becoming phase and contact aware
PAMAE modifies flow-matching VLA policies with phase-aware mixture-of-experts action heads. The router uses execution cues such as gripper state, gripper change, previous action norm, and progress. On five simulated multi-stage tasks, PAMAE improves π0 average success by 9.2 points and π0.5 by 5.6 points.

VibeAct adds a compact tactile channel for dexterous control. Piezoelectric fingertip microphones feed a contact and slip estimator, which supplies a 12-D tactile vector to policies trained in MuJoCo. On hardware, it improves success over a proprioception plus point-cloud baseline on Box Climb, Can Climb, and Nut Rotation.

The LeHome garment-folding system gives a competition-scale example for deformable objects. It combines a flow-matching VLA policy with reinforcement learning, replay, human corrections, and sim-to-real tuning, placing first in the online simulation round and second in the real-world final.

#### Sources
- [PAMAE: Phase-Aware-MoE Action Experts Towards Reliable Flow-Matching Vision-Language-Action Policies](../Inbox/2026-06-25--pamae-phase-aware-moe-action-experts-towards-reliable-flow-matching-vision-language-action-policies.md): PAMAE phase-aware expert routing and simulated multi-stage task gains.
- [VibeAct: Vibration to Actions for Contact-Rich Reactive Robot Dexterity](../Inbox/2026-06-25--vibeact-vibration-to-actions-for-contact-rich-reactive-robot-dexterity.md): VibeAct tactile sensing setup and simulation and hardware results.
- [Learning to Fold: prizewinning solution at LeHome Challenge 2026 (1st place online, 2nd offline)](../Inbox/2026-06-25--learning-to-fold-prizewinning-solution-at-lehome-challenge-2026-1st-place-online-2nd-offline.md): LeHome folding system components and competition outcomes.

### Safety evaluation is tracking unsafe success, not only task success
ForesightSafety-VLA makes safety the main measurement target for VLA policies. It defines 13 safety categories across physical interaction, instruction handling, and perception. The benchmark builds 66 safety-augmented RoboTwin scenarios across five robot embodiments, then separates safe success, unsafe success, safe failure, and unsafe failure.

The reported baselines all show remaining risk. OpenVLA-oft has the best listed safety-adjusted success rate at 0.35, while unsafe success still appears at 0.06. Among successful episodes, the unsafe share is 12.5% for OpenVLA-oft and 37.5% for ACT. That scoring choice matters because a robot can complete an instruction while colliding with objects, entering hot zones, or violating clearance limits.

#### Sources
- [ForesightSafety-VLA: A Unified Diagnostic Safety Benchmark for Vision-Language-Action Models](../Inbox/2026-06-25--foresightsafety-vla-a-unified-diagnostic-safety-benchmark-for-vision-language-action-models.md): ForesightSafety-VLA safety taxonomy, benchmark design, and baseline safety metrics.
