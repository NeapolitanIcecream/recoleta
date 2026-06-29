---
source: arxiv
url: https://arxiv.org/abs/2606.24448v1
published_at: '2026-06-23T11:35:13'
authors:
- Danze Chen
- Yanzhe Chen
- Qiming Huang
- Zhijun Cao
- Chen Gao
- Mike Zheng Shou
topics:
- vision-language-action
- robot-foundation-model
- synthetic-robot-videos
- geometry-supervision
- robot-data-scaling
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Supervise What Survives: Geometry-Guided VLA Adaptation from Synthetic Robot Videos

## Summary
GRA adapts VLA models with synthetic robot videos by using those videos for 2D geometry supervision, while training actions only on real robot demonstrations. On three Franka pick-and-place tasks, it raises matched-budget success from 61.1% for Real-only to 68.9% and beats pseudo-action baselines.

## Problem
- VLA policies need paired video-action data, but real teleoperation is slow and hardware-specific.
- Human-to-robot video generators can create robot-looking videos, yet they do not provide reliable motor commands.
- Prior pseudo-action methods train the action head on actions recovered from generated pixels; the paper argues this adds control noise and lowers real-robot success.

## Approach
- GRA uses generated videos only for spatial geometry supervision.
- It extracts future 2D end-effector waypoints from the source human video using Grounding DINO, SAM2, HaMeR, retargeting, MuJoCo simulation, and calibrated camera projection.
- Stage 1 trains the OpenVLA-OFT vision backbone and a 3-layer MLP 2D waypoint head for 5K steps on 75 generated videos per task; the language model and action head are excluded.
- Stage 2 trains the action head for 10K steps on 25 real demos per task with L1 delta-action loss, while a waypoint loss on real frames keeps the vision features tied to end-effector geometry.
- The action output is a 24-step chunk of 7D delta actions; the waypoint horizon is K=8.

## Results
- On 3 real Franka tasks with 30 trials each, GRA reaches 68.9% mean success with 25 real demos and 75 generated videos per task, compared with 61.1% for Real-only, 48.9% for DreamGen-style pseudo-actions, and 54.4% for MimicDreamer-style retargeted pseudo-actions.
- Per task, GRA scores 66.7% on cube→pad, 56.7% on cup→coaster, and 83.3% on mango→plate; Real-only scores 60.0%, 46.7%, and 76.7%.
- The 100-demo Real-only reference reaches 75.6% mean success. GRA cuts the gap to this reference from 14.5 points to 6.7 points while using 4x fewer real demos.
- Frozen-probe diagnostics show generated-to-real transfer is much worse for delta actions than waypoints: waypoint error is 0.41σ, while delta-action error is 1.38σ on the Stage-1 backbone.
- Teacher-forced action evaluation reports GRA at 9.26 mm position error and 0.060 total L1 error, better than Real-only at 11.09 mm and 0.090 and MimicDreamer-style at 13.36 mm and 0.071.
- On cup→coaster ablations, full GRA reaches 56.7% success; removing Stage 1 gives 43.3%, removing the waypoint anchor gives 46.7%, and replacing geometry with delta-action targets gives 36.7%.

## Link
- [https://arxiv.org/abs/2606.24448v1](https://arxiv.org/abs/2606.24448v1)
