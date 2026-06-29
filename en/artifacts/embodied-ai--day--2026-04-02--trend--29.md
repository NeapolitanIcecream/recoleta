---
kind: trend
trend_doc_id: 29
granularity: day
period_start: '2026-04-02T00:00:00'
period_end: '2026-04-03T00:00:00'
topics:
- world-models
- vla-finetuning
- autonomous-driving
- uav-tracking
- robot-control
- adversarial-robustness
run_id: materialize-outputs
aliases:
- recoleta-trend-29
tags:
- recoleta/trend
- topic/world-models
- topic/vla-finetuning
- topic/autonomous-driving
- topic/uav-tracking
- topic/robot-control
- topic/adversarial-robustness
language_code: en
pass_output_id: 10
pass_kind: trend_synthesis
---

# Action learning is getting sharper, while VLA robustness still lags

## Overview
The day’s strongest pattern is practical action learning. Papers improve robot and driving systems by tightening the link between prediction, action, and control details. The clearest gains come from verified world models, smoother action distributions, and geometry-aware planning. At the same time, Tex3D shows that current VLA models remain easy to derail with object-level visual attacks.

## Clusters

### Verified world models and geometry-grounded planning
World-model work in this period is getting more concrete about where predictions fail and how to use that signal for training. WAV treats verification as two simpler checks: whether a future state looks plausible and whether the action could actually reach it. That design is aimed at the sparse-data regime that hurts action-conditioned dynamics models most. The headline numbers are strong for a single-day crop: 2x sample efficiency across nine tasks and an 18% downstream policy gain. The same period also extends world-action modeling into driving. DriveDreamer-Policy predicts depth, future video, and action in one stack, with depth generated first as the geometric scaffold. On Navsim, it reports 89.2 PDMS on v1 and 88.7 EPDMS on v2, alongside better future-video quality.

#### Evidence
- [World Action Verifier: Self-Improving World Models via Forward-Inverse Asymmetry](../Inbox/2026-04-02--world-action-verifier-self-improving-world-models-via-forward-inverse-asymmetry.md): WAV summary with method and headline results
- [DriveDreamer-Policy: A Geometry-Grounded World-Action Model for Unified Generation and Planning](../Inbox/2026-04-02--drivedreamer-policy-a-geometry-grounded-world-action-model-for-unified-generation-and-planning.md): DriveDreamer-Policy summary with geometry-first design and Navsim metrics

### Training objectives are getting closer to action tolerance
VLA finetuning papers are focusing on action distributions, not just bigger backbones. The FAN prior paper argues that many robot states admit a small set of near-equivalent good actions, so training should keep probability mass over that neighborhood. In ManiSkill supervised finetuning with OpenVLA, it raises in-distribution success from 78.1 to 89.8 and lifts average OOD success from 58.1 to 63.3. A separate control paper makes a related point lower in the stack: controller gains change how easy policies are to learn and transfer. Its behavior-cloning results favor compliant, overdamped gains, and its retargeting setup keeps at least 90% success with joint-position MSE below 1e-3 across gain settings up to 25x decimation. Taken together, the practical emphasis is clear: action tolerance and control interface choices are becoming first-order training variables.

#### Evidence
- [Boosting Vision-Language-Action Finetuning with Feasible Action Neighborhood Prior](../Inbox/2026-04-02--boosting-vision-language-action-finetuning-with-feasible-action-neighborhood-prior.md): FAN prior summary with concrete ManiSkill/OpenVLA gains
- [Tune to Learn: How Controller Gains Shape Robot Policy Learning](../Inbox/2026-04-02--tune-to-learn-how-controller-gains-shape-robot-policy-learning.md): Controller-gain study summary with learnability framing and reported metrics

### VLA designs are specializing for drones and driving
Embodied VLA work is spreading into new operating domains, with speed and structure built into the model. UAV-Track VLA adds temporal compression, spatial grounding, and a 25-step flow-matching action head for instruction-following drone tracking. It is backed by a large CARLA benchmark with 892,756 frames, 176 tasks, and 85 objects, and reports 61.76% success on long-distance pedestrian tracking with 33.4% lower per-step latency. Driving papers are also organizing VLA systems by role. UniDriveVLA splits understanding, perception, and planning into separate transformer experts to reduce interference between language reasoning and spatial perception. Its excerpt does not expose the final headline row, but it claims state-of-the-art results on nuScenes and Bench2Drive and gives stronger baseline context than earlier driving VLA reports.

#### Evidence
- [UAV-Track VLA: Embodied Aerial Tracking via Vision-Language-Action Models](../Inbox/2026-04-02--uav-track-vla-embodied-aerial-tracking-via-vision-language-action-models.md): UAV-Track VLA summary with benchmark scale, success rate, and latency
- [UniDriveVLA: Unifying Understanding, Perception, and Action Planning for Autonomous Driving](../Inbox/2026-04-02--unidrivevla-unifying-understanding-perception-and-action-planning-for-autonomous-driving.md): UniDriveVLA summary with expert separation design and benchmark claims

### Physical attack surfaces are still wide open
Robustness remains a hard limit for current VLA systems. Tex3D shows that adversarial 3D textures on manipulated objects can break policies at rates that are hard to dismiss as edge cases. The attack is physically grounded at the object surface, optimized through a differentiable rendering path, and stabilized across long episodes with trajectory-aware weighting. Reported failure rates rise from 24.1% to 88.1% on OpenVLA, from 4.7% to 76.0% on OpenVLA-OFT, and from 4.6% to 71.8% on pi0 under untargeted attack. On OpenVLA spatial tasks, failure reaches 96.7% under targeted attack. This is a useful counterweight to the period's capability gains: better training and better planning do not remove large visual attack surfaces.

#### Evidence
- [Tex3D: Objects as Attack Surfaces via Adversarial 3D Textures for Vision-Language-Action Models](../Inbox/2026-04-02--tex3d-objects-as-attack-surfaces-via-adversarial-3d-textures-for-vision-language-action-models.md): Tex3D summary with method and failure-rate increases across VLA models
