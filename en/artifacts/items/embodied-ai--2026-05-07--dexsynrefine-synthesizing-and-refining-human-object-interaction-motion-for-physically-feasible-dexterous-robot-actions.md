---
source: arxiv
url: https://arxiv.org/abs/2605.05925v1
published_at: '2026-05-07T09:31:43'
authors:
- Hyesung Lee
- Hyunwoo Jung
- Si-Hwan Heo
- Sungwook Yang
topics:
- dexterous-manipulation
- human-object-interaction
- residual-rl
- sim-to-real
- motion-synthesis
- contact-adaptation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# DexSynRefine: Synthesizing and Refining Human-Object Interaction Motion for Physically Feasible Dexterous Robot Actions

## Summary
DexSynRefine turns a small set of human-object interaction recordings into executable dexterous robot actions. It combines motion synthesis, residual reinforcement learning, and contact/dynamics adaptation for five manipulation tasks.

## Problem
- Dexterous teleoperation datasets are costly to collect, while human-object interaction recordings are easier to scale.
- HOI data gives wrist, hand, and object motion, but not the contact forces and dynamics needed for robot execution; human and robot hands also differ in shape and actuation.
- Sparse HOI demos often lack a matching reference for a new initial object pose, so raw retargeting fails outside the recorded cases.

## Approach
- The method collects 7 HOI demos per task across five tasks and expands them with object-centric SE(2) augmentation to about 300 trajectories per task, each with horizon T=220.
- HOI-MMFP learns a latent motion manifold with a Transformer autoencoder, then uses conditional flow matching to generate wrist, hand-keypoint, and object trajectories from a task text embedding and the initial object pose.
- A PPO teacher policy learns task-space residuals added to the generated wrist and fingertip targets; inverse kinematics converts these targets to 7-DoF arm and 16-DoF hand commands at 120 Hz.
- A deployable student policy uses 30-step proprioceptive histories with a GRU contact estimator and a dynamics latent predictor to replace privileged simulation state.

## Results
- Under ±20 cm x/y and ±30° yaw initial-pose perturbations, HOI-MMFP gets first-frame wrist error of 0.015 m / 2.50°, compared with DiT-Full at 0.018 m / 2.65° and TC-VAE at 0.121 m / 12.88°.
- HOI-MMFP has lower wrist jerk: 29.83±4.78 m/s^3 and 101.08±17.12 rad/s^3, compared with TC-VAE at 37.00±8.52 / 139.14±45.21 and DiT-Full at 41.03±8.23 / 189.52±33.82.
- On Pick Up and Hammer, HOI-MMFP as the reference gives 52.6±3.04% simulated success, compared with DiT-Full at 49.10±4.12%; object translation error is 0.041 m vs 0.057 m, and object orientation error is 46.29° vs 51.42°.
- Task-space residual actions give the best mean simulated success rate across five tasks: 68.1%. Per-task success rates are Pringles 71.5%, Watering Can 52.4%, Bowl 94.8%, Hammer 60.3%, and Book 61.6%; kinematic retargeting stays at 0.0-5.8%.
- The full student policy beats adaptation ablations: on Hammer, 44.3% success vs 17.2% without contact and 7.5% without dynamics; on Watering Can, 51.8% vs 0.0% and 4.4%.
- The abstract claims real-robot transfer on all five tasks, with a 50-70 percentage point gain over kinematic retargeting.

## Link
- [https://arxiv.org/abs/2605.05925v1](https://arxiv.org/abs/2605.05925v1)
