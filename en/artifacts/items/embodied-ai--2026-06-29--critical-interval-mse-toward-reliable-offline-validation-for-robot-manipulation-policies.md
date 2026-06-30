---
source: arxiv
url: https://arxiv.org/abs/2606.29898v1
published_at: '2026-06-29T07:34:39'
authors:
- Haoxu Huang
- Tongsam Zheng
- Yifan Chen
- Jiacheng You
- Yang Gao
topics:
- offline-validation
- robot-manipulation
- vision-language-action
- policy-ranking
- robot-evaluation
- action-mse
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Critical Interval MSE: Toward Reliable Offline Validation for Robot Manipulation Policies

## Summary
Critical Interval MSE is an offline validation metric for robot manipulation policies that predicts rollout performance better than raw action MSE. It scores only task-critical trajectory segments and applies rollout-time action alignment before comparing predicted actions with expert actions.

## Problem
- Robot rollouts give the best policy evaluation signal, but they are costly, hard to reproduce, and too sparse for comparing nearby model variants.
- Raw validation MSE on expert demonstrations often ranks policies poorly because long transit or idle motions can dominate the error while brief contact, grasp, insertion, or alignment phases decide task success.
- Offline validation matters because faster policy iteration depends on a cheap metric that tracks real success rates or rollout rankings.

## Approach
- CI-MSE first identifies critical intervals in demonstration videos, such as grasping, contact, insertion, or fine alignment; the paper uses few-shot vision-language model prompting for this annotation.
- It filters the validation set to keep only timesteps inside those intervals, then computes action error only there.
- It applies the same action execution procedures used at rollout time, including temporal ensembling or real-time action chunking, before measuring error.
- It uses local dynamic time warping to avoid penalizing small timing offsets between predicted and expert action sequences.
- For limited real-world trials, the paper also recommends Elo-style pairwise policy ranking instead of relying only on scalar partial-progress scores.

## Results
- In simulation on LBM-Eval with 49 tasks, about 10k demonstrations, and 27 policy checkpoints, CI-MSE reaches Pearson r = -0.74 and Spearman ρ = -0.87 against rollout success rate; raw MSE reaches r = -0.56 and ρ = -0.61.
- Across model-variant families, CI-MSE matches or improves Spearman rank correlation versus raw MSE. For data scaling variants, raw MSE gives the wrong direction with r = 0.67 and ρ = 0.90, while CI-MSE gives r = -0.97 and ρ = -0.70.
- Under distribution shift, CI-MSE improves object-layout OOD rank correlation from raw MSE ρ = -0.77 to ρ = -0.88, and skill OOD from ρ = -0.36 to ρ = -0.69. Visual OOD remains hard, with CI-MSE ρ = -0.66 and raw MSE ρ = -0.68.
- In real-world Franka experiments, CI-MSE gives near-perfect cross-environment ranking for pour water with r = -0.99 and ρ = -1.00, and arrange mouse with r = -0.96 and ρ = -1.00.
- For fold-towel cross-object validation with mismatched collectors, CI-MSE improves over raw MSE: CI-MSE r = -0.87 and ρ = -1.00, while raw MSE r = -0.09 and ρ = 0.00.
- Sensitivity analysis reports temporal ensembling improves rank correlation from H = 1, ρ = -0.80, to H = 8, ρ = -0.87; the paper also claims less than 5% correlation degradation across a reasonable hyperparameter range.

## Link
- [https://arxiv.org/abs/2606.29898v1](https://arxiv.org/abs/2606.29898v1)
