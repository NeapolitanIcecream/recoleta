---
source: arxiv
url: https://arxiv.org/abs/2605.26478v1
published_at: '2026-05-26T02:35:08'
authors:
- Haoxiang You
- Yilang Liu
- Davis Zong
- Qian Wang
- Teeratham Vitchutripop
- Qi Wang
- Daniel Rakita
- Ian Abraham
topics:
- visual-rl
- robot-learning
- sim2real
- dexterous-manipulation
- policy-gradient
- visuomotor-control
relevance_score: 0.66
run_id: materialize-outputs
language_code: en
---

# Efficient On-policy Visual-RL via Stochastic Decoupled Policy Gradient

## Summary
SDPG trains visual robot control policies end-to-end with far less rendered simulation than standard on-policy visual RL. The paper’s main claim is that random action-sequence perturbations can replace full trajectory differentiation while keeping training fast on one RTX 4080 GPU.

## Problem
- Visual RL is slow and memory-heavy because image rendering and visual encoders make large on-policy batches expensive.
- Differentiable first-order RL can reduce samples, but long-horizon backpropagation is unstable in contact-rich tasks and requires differentiable simulators and rewards.
- Teacher-student distillation can train fast, but visual students can fail when teacher data misses states that appear during deployment.

## Approach
- SDPG rolls out a small set of nominal visual environments, then runs multiple physics-only auxiliary rollouts with random perturbations added to the nominal action sequence.
- It estimates the action-sequence gradient from return differences: better perturbations push the policy toward similar actions, worse perturbations push it away.
- The policy update is written as a supervised loss that moves the visual policy output toward `action + estimated gradient`, with stop-gradient on the target.
- The method adapts the exploration scale `delta`, normalizes by return standard deviation, and uses short-horizon rollouts to reduce variance and improve throughput.
- The actor uses visual observations, while the critic can use privileged low-dimensional state for faster value learning.

## Results
- On Visual MuJoCo Hopper, Walker, Ant, and Humanoid, SDPG reports the highest rewards in the shown training curves and matches state-based performance, though the excerpt does not give exact reward values.
- SDPG trains with 64 batch-rendered environments, while the PPO memory estimate uses 4096 environments.
- Memory use for SDPG is 10.2 GB on Hopper, 10.3 GB on Walker, 10.3 GB on Ant, and 10.5 GB on Humanoid.
- PPO memory is estimated at 48 GB on Hopper, 48 GB on Walker, 49 GB on Ant, and 50 GB on Humanoid, about 4.7x to 4.8x higher than SDPG in the table.
- SDPG memory is comparable to DrQv2, DreamerV3, and distillation in the table: DrQv2 ranges from 8.2 GB to 11.6 GB, DreamerV3 from 10.8 GB to 10.9 GB, and distillation from 10.3 GB to 10.7 GB.
- The paper claims end-to-end training for locomotion and manipulation tasks within a few hours on a single NVIDIA RTX 4080 GPU, and reports sim-to-real deployment on a Unitree Go2 robot.

## Link
- [https://arxiv.org/abs/2605.26478v1](https://arxiv.org/abs/2605.26478v1)
