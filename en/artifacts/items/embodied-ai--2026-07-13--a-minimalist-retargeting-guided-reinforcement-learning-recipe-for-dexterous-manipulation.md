---
source: arxiv
url: https://arxiv.org/abs/2607.11874v1
published_at: '2026-07-13T17:56:08'
authors:
- Yunhai Feng
- Natalie Leung
- Jiaxuan Wang
- Lujie Yang
- Haozhi Qi
- Preston Culbertson
topics:
- dexterous-manipulation
- motion-retargeting
- reinforcement-learning
- sim2real
- tool-use
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# A Minimalist Retargeting-Guided Reinforcement Learning Recipe for Dexterous Manipulation

## Summary
Regrind learns contact-rich dexterous manipulation from one human demonstration by preserving hand-object relationships during motion retargeting and refining the result with residual reinforcement learning in simulation. It transfers zero-shot to two robot hands on scissors and screwdriver tasks, with simulation success rates above 98.7% across four hand-task settings.

## Problem
- Dexterous manipulation needs precise finger coordination, contact transitions, friction, and force regulation, which make direct human-motion retargeting and sim-to-real transfer difficult.
- Purely hand-centric retargeting can create collisions or physically implausible grasps because it ignores the robot hand's relationship with the object.
- Collecting large amounts of robot-specific dexterous manipulation data is expensive, while RL faces exploration and reward-design problems.

## Approach
- Retarget human hand and object motion with interaction meshes that preserve spatial and contact relationships between corresponding hand and object keypoints.
- Train a residual RL policy in simulation to track object-centric keypoints, using the retargeted trajectory as both a motion reference and a restart-state distribution.
- Generate diverse training trajectories by perturbing the initial object pose by up to ±5 cm and ±30 degrees, then smoothly warping the trajectory back to its original goal.
- Reduce transfer errors with domain randomization, observation noise, push and gravity curricula, low-noise actor observations, and hardware system identification.

## Results
- Across LEAP and WUJI hands on scissors and screwdriver tasks, Regrind achieved simulation object-tracking errors of 5.3-6.5 mm and success rates of 98.7-99.8%.
- The four evaluated settings were LEAP-Scissors, LEAP-Screwdriver, WUJI-Scissors, and WUJI-Screwdriver; Regrind's reported success rates were 99.8% ± 0.3%, 99.7% ± 0.0%, 98.7% ± 1.3%, and 98.8% ± 1.3%, respectively.
- Qualitative comparisons show that Mink IK + RL and DexMachina can produce hand-object penetrations or unstable grasps, while interaction-aware retargeting produces more usable contact structures for RL initialization.
- The paper claims zero-shot hardware transfer and fluid tool-use behavior on both robot hands, but the provided excerpt does not include the hardware success-rate table or numerical hardware comparison.
- The strongest reported mechanism-level result is that preserving interaction structure improves the retargeted reference used for downstream RL; the excerpt does not provide complete ablation numbers for each component.

## Link
- [https://arxiv.org/abs/2607.11874v1](https://arxiv.org/abs/2607.11874v1)
