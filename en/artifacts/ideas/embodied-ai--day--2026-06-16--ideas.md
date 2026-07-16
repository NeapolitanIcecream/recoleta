---
kind: ideas
granularity: day
period_start: '2026-06-16T00:00:00'
period_end: '2026-06-17T00:00:00'
run_id: e34d6d67-1db5-4b16-9ed0-00a3429a66c1
status: succeeded
topics:
- robot manipulation
- vision-language-action models
- world models
- robot evaluation
- multimodal sensing
- policy adaptation
tags:
- recoleta/ideas
- topic/robot-manipulation
- topic/vision-language-action-models
- topic/world-models
- topic/robot-evaluation
- topic/multimodal-sensing
- topic/policy-adaptation
language_code: en
pass_output_id: 293
pass_kind: trend_ideas
upstream_pass_output_id: 292
upstream_pass_kind: trend_synthesis
---

# Robot Policy Readiness Checks

## Summary
Robot teams can add pre-execution checks, make mixed-robot training data easier to combine, and test policies with capability-level diagnostics before putting them on hardware. The concrete gains in the evidence come from action verification at inference time, cross-embodiment state-action alignment, and benchmarks that expose failures hidden by one overall success rate.

## Pre-execution action verification and uncertainty logging for VLA rollouts
A robot team running π0-style or other stochastic VLA policies can add a small runtime layer that samples several short action chunks, scores them before motion, executes the best candidate, and logs the rejected candidates with the final outcome. VERITAS gives the most concrete recipe: generate N candidate chunks, use a visual verifier tied to pixel-space waypoints, and keep successful verified rollouts for later behavior-cloning fine-tuning. The reported setting used N = 5 at 15 Hz, with less than 1 ms geometric verification overhead after the one-time VLM trace generation.

This is a practical fit for manipulation cells where a wrong first motion is expensive but a few extra policy samples are cheap. The same logging layer can include velocity-field disagreement for flow-based VLAs, so uncertain starts are routed to an expert demonstration queue. That turns deployment telemetry into a triage list: successful verified rollouts become self-training data, and high-disagreement cases become the next demonstrations to collect.

### Sources
- [Visual Verification Enables Inference-time Steering and Autonomous Policy Improvement](../Inbox/2026-06-16--visual-verification-enables-inference-time-steering-and-autonomous-policy-improvement.md): VERITAS samples short action chunks, verifies them visually before execution, reports success gains across policies, and logs verified rollouts for fine-tuning.
- [Uncertainty Quantification for Flow-Based Vision-Language-Action Models](../Inbox/2026-06-16--uncertainty-quantification-for-flow-based-vision-language-action-models.md): The uncertainty paper uses velocity-field disagreement across flow-based VLA action-head ensembles for failure detection and active fine-tuning case selection.

## Canonical state-action templates for multi-robot manipulation datasets
Teams with demonstrations spread across Franka, UR, ALOHA, ARX, or similar arms should treat data formatting as part of model training. Qwen-RobotManip maps different robots into one state-action template, applies per-dimension binary masks for missing joints or grippers, predicts camera-frame delta end-effector poses, and uses recent execution history as a clue about the current embodiment.

The immediate build is a dataset adapter that converts each robot log into a shared schema before pretraining or fine-tuning. A cheap validation run can train on two or three robot families and hold out one embodiment, then compare zero-shot transfer and few-shot adaptation against a per-robot action encoding. Qwen-RobotManip reports a 38,100-hour corpus and real-robot validation across AgileX ALOHA, Franka, UR, and ARX, so the schema choices are now concrete enough to copy in smaller labs.

### Sources
- [Qwen-RobotManip Technical Report: Alignment Unlocks Scale for Robotic Manipulation Foundation Models](../Inbox/2026-06-16--qwen-robotmanip-technical-report-alignment-unlocks-scale-for-robotic-manipulation-foundation-models.md): Qwen-RobotManip describes canonical state-action alignment, binary masks, camera-frame delta end-effector actions, execution-history conditioning, a 38,100-hour corpus, and real-robot validation across several platform families.
- [Qwen-RobotManip Technical Report: Alignment Unlocks Scale for Robotic Manipulation Foundation Models](../Inbox/2026-06-16--qwen-robotmanip-technical-report-alignment-unlocks-scale-for-robotic-manipulation-foundation-models.md): The source text says the system builds a roughly 38,100-hour corpus using open-source robot datasets and human demonstration videos, with human-to-robot synthesis across 15 platforms.

## Capability-level acceptance tests for generalist manipulation policies
A lab choosing a generalist manipulation policy should add a pre-deployment test sheet that splits success by task type, precision, horizon, operating mode, and distribution shift. EBench shows why this matters: π0, π0.5, XVLA, and InternVLA-A1 land in a close overall test-success band of 24.4% to 29.5%, while InternVLA-A1 drops to 5.8% success on dexterous fixed-base tasks despite stronger mobile manipulation results.

Industrial teams handling wires or cables need an extra contact-rich test. WireCraft shows that privileged state RL can solve Ethernet connector insertion in simulation, with State PPO at 95.86% insert success, while Vision PPO reaches 17.74% insert success on the same task and simulation-only ACT gives 0/10 real UR5 insertions in the reported run. Acceptance testing should include staged metrics such as reach, align, insert, route, and seat, so a policy that reaches the port but fails contact alignment is caught before a hardware trial.

### Sources
- [EBench: Elemental Diagnosis of Generalist Mobile Manipulation Policies](../Inbox/2026-06-16--ebench-elemental-diagnosis-of-generalist-mobile-manipulation-policies.md): EBench defines capability axes and generalization shifts and reports close overall success rates that hide large skill-profile differences across generalist policies.
- [WireCraft: A Simulation Benchmark for Industrial DLO Manipulation](../Inbox/2026-06-16--wirecraft-a-simulation-benchmark-for-industrial-dlo-manipulation.md): WireCraft reports a large gap between privileged state RL and vision-based policies on industrial wire and connector tasks, including real UR5 insertion results.
