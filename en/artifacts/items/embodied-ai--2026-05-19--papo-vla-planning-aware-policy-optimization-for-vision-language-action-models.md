---
source: arxiv
url: https://arxiv.org/abs/2605.19580v1
published_at: '2026-05-19T09:22:49'
authors:
- Peizheng Guo
- Jingyao Wang
- Changwen Zheng
- Wenwen Qiang
topics:
- vision-language-action
- robot-policy-optimization
- grpo
- causal-credit-assignment
- manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# PAPO-VLA: Planning-Aware Policy Optimization for Vision-Language-Action Models

## Summary
PAPO-VLA fine-tunes Vision-Language-Action robot policies by giving extra update weight to key decision actions in a trajectory. The excerpt explains the method, but it does not include PAPO-VLA's final quantitative scores.

## Problem
- VLA robot policies act in a closed loop, so one bad decision can change later observations and make the task fail.
- Standard imitation learning copies all actions, and GRPO-style fine-tuning assigns the same trajectory advantage to every action in a rollout.
- This matters for manipulation because actions such as grasping, switching to transport, or releasing often determine whether later continuous control can finish the task.

## Approach
- PAPO-VLA treats a trajectory as a mix of planning actions and execution actions.
- It scores planning actions using action change magnitude, normalized by the trajectory's average action change, then gates the score with the trajectory reward.
- It selects the top-k planning actions from each trajectory.
- It estimates each selected action's causal sufficiency by comparing expected reward when keeping the action against expected reward after a feasible perturbation.
- It estimates causal necessity with a similar perturbation test, combines sufficiency and necessity with a harmonic-mean form, and adds the result to GRPO's action-level advantage.

## Results
- The excerpt claims experiments on multiple benchmarks show PAPO-VLA improves VLA policy reliability, but the provided text cuts off before PAPO-VLA's reported scores.
- The visible LIBERO-style baseline table reports OpenVLA-OFT at 0.91 average success, with 0.91 Spatial, 0.95 Object, 0.90 Goal, and 0.86 Long.
- OpenVLA reports 0.76 average success, with 0.85 Spatial, 0.88 Object, 0.79 Goal, and 0.53 Long.
- Octo reports 0.75 average success, and GRAPE reports 0.80 average success in the visible rows.
- The strongest concrete claim available in the excerpt is methodological: PAPO-VLA changes GRPO by replacing the trajectory-only advantage A_i with an action-level planning-aware advantage A_i,t + ηC_i,t^plan.

## Link
- [https://arxiv.org/abs/2605.19580v1](https://arxiv.org/abs/2605.19580v1)
