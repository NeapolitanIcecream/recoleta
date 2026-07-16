---
source: arxiv
url: https://arxiv.org/abs/2607.13818v1
published_at: '2026-07-15T13:25:52'
authors:
- Xiaopeng Zhang
- Yueyang Weng
- Qi Liu
- Yongjin Mu
- Yanjie Li
topics:
- robot-foundation-model
- vision-language-action
- generalist-robot-policy
- reinforcement-learning
- failure-recovery
- sim2real
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Learning Robust Execution in Robotic Manipulation with Agentic Reinforcement Learning

## Summary
The paper adds a high-level reinforcement-learning execution manager to frozen robotic manipulation policies. On LIBERO, it improves success under nominal conditions and substantially improves recovery under injected disturbances without retraining the underlying policy.

## Problem
- Long-horizon manipulation policies can drift because of perception errors, contact uncertainty, disturbances, and compounding execution failures.
- Vision-language-action and imitation policies generally generate actions but do not explicitly monitor execution stability or select recovery behavior, which matters because small deviations can become irreversible task failures.

## Approach
- It computes local execution quality from recent end-effector effectiveness and motion smoothness, and global execution quality from the distance between the current execution prefix and stage-matched successful reference trajectories.
- A lightweight high-level policy observes a history of proprioception, low-level actions, and quality scores, then selects one of four modes: Execute, Retry, Repair, or Reset.
- Retry and Repair use operational-space control to roll the robot back to recent high-quality states; Reset restarts the episode. The low-level VLA or diffusion policy remains frozen.
- The agentic policy is trained with PPO using task success, failure, time, and recovery costs; the reported setup uses 50 successful reference trajectories per task, 10 progress bins, 5 nearest neighbors, a history length of 20, and a decision interval of 5 low-level steps.

## Results
- On the LIBERO suites, the average success-rate gains under nominal conditions were +5.1 percentage points on Spatial, +5.4 on Object, +6.6 on Goal, and +13.7 on Long.
- Under random kinematic disturbances, the corresponding average gains were +25.7, +27.4, +28.3, and +39.2 percentage points.
- In the nominal LIBERO-Long setting, OpenVLA improved from 54.0% to 74.5% success, while Diffusion Policy improved from 50.5% to 72.4%; in the disturbance setting, OpenVLA improved from 33.4% to 67.6% and Diffusion Policy from 30.5% to 60.5%.
- The method also preserved near-saturated performance for stronger policies such as pi_0 and pi_0.5, but the provided excerpt does not include the full ablation, cost, or real-robot evaluation results.

## Link
- [https://arxiv.org/abs/2607.13818v1](https://arxiv.org/abs/2607.13818v1)
