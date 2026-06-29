---
source: arxiv
url: https://arxiv.org/abs/2605.26282v1
published_at: '2026-05-25T19:06:51'
authors:
- Xiaoyuan Cheng
- Wenxuan Yuan
- Zhancun Mu
- Yuanzhao Zhang
- Yiming Yang
- Hai Wang
- Zhuo Sun
- Che Liu
topics:
- world-model-rl
- diffusion-policy
- model-based-rl
- policy-optimization
- offline-to-online-rl
- robot-policy-scaling
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Scaling World-Model Reinforcement Learning Through Diffusion Policy Optimization

## Summary
MBDPO trains a diffusion action policy inside a latent world model so policy search and policy learning use the same distribution. The paper claims this fixes a scaling bottleneck in model-based RL and improves over TD-MPC2 in offline, online, and offline-to-online settings.

## Problem
- Existing world-model RL often trains a value function on actions from a non-search policy, then improves behavior with a separate search policy. This mismatch makes the value function unreliable on searched actions.
- Search can exploit overestimated values in out-of-distribution action regions, which hurts long-horizon control and weakens scaling with larger world models.
- The problem matters because pretrained world models only help control if larger models and more data lead to better policies.

## Approach
- MBDPO represents the policy as a diffusion process over action sequences, then executes actions in a receding-horizon style.
- A latent world model rolls out sampled action sequences and scores them by predicted reward plus terminal value.
- The method estimates the diffusion score field from these imagined rollouts, so denoising steps move action sequences toward higher-return actions.
- A learned implicit energy function estimates the behavior-policy density from replay data and adds a KL-style trust region, keeping the optimized policy close to the data distribution.
- The world model, value function, energy function, and diffusion policy are trained together for offline pretraining, online learning, and offline-to-online fine-tuning.

## Results
- In multi-task offline pretraining, MBDPO reports higher performance than TD-MPC2 and shows monotonic gains as model size increases from 1.7M to 340M parameters.
- In online-from-scratch experiments, the paper reports superior or competitive results across 4 benchmark suites with 121 tasks.
- The paper evaluates action drift and cross-TD error on 8 online tasks; MBDPO has lower drift than TD-MPC2, and the contrastive variant with η=0.1 stays closest to the base policy.
- The theory gives a value-iteration gap bounded by γ‖Q̂‖∞√(2D_KL^max(π‖β)), linking search-policy drift to value error.
- The excerpt gives no exact return, success-rate, or normalized-score values, so the strongest numeric claims are the 1.7M-to-340M scaling range, 4 benchmarks, 121 tasks, 8-task drift study, and η=0.1 variant comparison.

## Link
- [https://arxiv.org/abs/2605.26282v1](https://arxiv.org/abs/2605.26282v1)
