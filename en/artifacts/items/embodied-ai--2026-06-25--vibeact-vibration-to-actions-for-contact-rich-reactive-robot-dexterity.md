---
source: arxiv
url: https://arxiv.org/abs/2606.27344v1
published_at: '2026-06-25T17:50:07'
authors:
- Yuemin Mao
- Uksang Yoo
- Jean Oh
- Jonathan Francis
- Jeffrey Ichnowski
topics:
- dexterous-manipulation
- vibrotactile-sensing
- sim2real
- tactile-policy-learning
- contact-rich-manipulation
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# VibeAct: Vibration to Actions for Contact-Rich Reactive Robot Dexterity

## Summary
VibeAct uses piezoelectric fingertip microphones to add contact-onset, slip-presence, and slip-magnitude feedback to dexterous robot policies trained in simulation. Its main claim is that this compact tactile signal improves contact-rich hand control without simulating raw vibration audio.

## Problem
- Dexterous hands need fast contact and slip feedback because key events are local, brief, and often hidden from cameras.
- Raw vibro-acoustic signals are hard to simulate because they depend on finger material, mounting, object texture, electronics, and motor noise.
- Training dexterous policies directly from real tactile data would need large real-world datasets or unsafe online exploration.

## Approach
- The robot uses 8 piezoelectric microphones, 2 in each fingertip, recorded at 48 kHz.
- Real teleoperation data is replayed in a calibrated MuJoCo digital clone to label a 12-D tactile vector: per-finger contact onset, binary slip, and slip magnitude.
- A tactile estimator maps 200 ms log-mel microphone windows to that vector using separate per-finger networks.
- PPO policies are trained in MuJoCo with proprioception, a fixed-camera point cloud, and the same 12-D tactile vector; at deployment, the estimator supplies the tactile input.

## Results
- Tactile estimator, full VibeAct: contact-onset F1 0.597 ± 0.101, slip-presence F1 0.913 ± 0.054, slip-magnitude MAE 4.736 ± 0.658 mm/s on a held-out moving-object split.
- Compared with pretraining only, full VibeAct improved contact-onset F1 from 0.384 to 0.597, slip-presence F1 from 0.781 to 0.913, and reduced slip-magnitude MAE from 6.417 to 4.736 mm/s.
- In simulation over 5 tasks and 100 trials across 3 seeds, full VibeAct beat the proprioception plus point-cloud baseline on every task: Box Climb 50.0% vs 46.7%, Nut Rotation 44.0% vs 28.5%, Peg in Hole 30.0% vs 6.5%, Cube Rotation 57.0% vs 6.0%, Can Climb 76.0% vs 60.0%.
- The largest simulation gains were Cube Rotation +51.0 points and Peg in Hole +23.5 points, which require sustained tactile correction.
- On hardware, VibeAct improved success over Prop+PC on Box Climb 12/20 vs 4/20, Can Climb 19/20 vs 11/20, and Nut Rotation 8/20 vs 1/20.

## Link
- [https://arxiv.org/abs/2606.27344v1](https://arxiv.org/abs/2606.27344v1)
