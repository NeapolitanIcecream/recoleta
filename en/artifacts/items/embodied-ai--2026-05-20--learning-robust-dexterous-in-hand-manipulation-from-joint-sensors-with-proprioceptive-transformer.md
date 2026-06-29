---
source: arxiv
url: https://arxiv.org/abs/2605.21330v1
published_at: '2026-05-20T15:57:27'
authors:
- Senlan Yao
- Chenyu Yang
- Jaehoon Kim
- Aristotelis Sympetheros
- Robert K. Katzschmann
topics:
- dexterous-manipulation
- proprioceptive-control
- transformer-policy
- in-hand-rotation
- sim2real
- joint-sensing
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Learning Robust Dexterous In-Hand Manipulation from Joint Sensors with Proprioceptive Transformer

## Summary
Proprioceptive Transformer learns continuous cube rotation on a tendon-driven ORCA hand using only joint position and velocity histories. The paper claims joint-only control can beat vision-based and PPO baselines on real hardware.

## Problem
- Dexterous in-hand rotation often needs cameras or tactile sensors to track the object, which adds occlusion, calibration, compute, and sim-to-real failure points.
- Joint sensing exists on most robot hands, yet motor encoders can misread the real finger state on tendon-driven hands because of cable stretch, friction, and backlash.
- The task matters because a hand that can infer object state from its own joints can manipulate objects without external pose tracking.

## Approach
- A teacher policy is trained in Isaac Lab with PPO and privileged object pose, using 8192 parallel ORCA hand simulations.
- A student policy, Proprioceptive Transformer, receives only noisy joint positions and velocities over a time window, plus the previous action, previous command, and goal command.
- The Transformer uses self-attention over joint history to infer hidden contact and object information from motion patterns.
- Training combines behavior cloning from the teacher with auxiliary reconstruction losses for object position, clean joint position, and clean joint velocity.
- The real ORCA hand uses 16 AS5600 magnetic angle sensors at the finger joints, and the paper compares these direct joint readings with motor encoder readings.

## Results
- On the 55 mm cube, PT-Joint reaches 11.83 ± 0.52 RPM, compared with 3.83 ± 0.51 RPM for Proprio-PPO and 3.08 ± 0.12 RPM for Extero-PPO.
- On the 55 mm cube, PT-Joint reports 100 ± 0% rotation accuracy, 100 ± 0% drop-free success rate, and 0 drops across 3 trials of 60 seconds.
- On the 65 mm cube, PT-Joint reaches 11.33 ± 0.12 RPM, compared with 5.17 ± 0.12 RPM for Proprio-PPO, 4.83 ± 0.12 RPM for Extero-PPO, and 8.53 ± 1.48 RPM for PT-Motor.
- Direct joint sensing improves speed over motor encoders on the 55 mm cube: 11.83 RPM for PT-Joint versus 9.33 RPM for PT-Motor, a 26.8% gain.
- For object position reconstruction from joint history, the Transformer reaches 13.70 ± 4.62 mm RMSE across 32 simulated environments, compared with 17.87 ± 4.60 mm for MLP and 15.64 ± 4.46 mm for LSTM.
- For clean joint state reconstruction, the Transformer reports 0.098 rad joint position RMSE and 0.070 rad/s velocity RMSE, compared with LSTM at 0.110 rad and 0.112 rad/s.

## Link
- [https://arxiv.org/abs/2605.21330v1](https://arxiv.org/abs/2605.21330v1)
