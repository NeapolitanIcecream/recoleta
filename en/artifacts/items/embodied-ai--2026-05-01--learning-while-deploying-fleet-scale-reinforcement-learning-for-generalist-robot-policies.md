---
source: arxiv
url: https://arxiv.org/abs/2605.00416v1
published_at: '2026-05-01T05:20:26'
authors:
- Yi Wang
- Xinchen Li
- Pengwei Xie
- Pu Yang
- Buqing Nie
- Yunuo Cai
- Qinglin Zhang
- Chendi Qu
- Jeffrey Wu
- Jianheng Song
- Xinlin Ren
- Jingshun Huang
- Mingjie Pan
- Siyuan Feng
- Zhi Chen
- Jianlan Luo
topics:
- vision-language-action
- generalist-robot-policy
- fleet-scale-rl
- robot-data-scaling
- offline-to-online-rl
- long-horizon-manipulation
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# Learning while Deploying: Fleet-Scale Reinforcement Learning for Generalist Robot Policies

## Summary
LWD trains a single VLA robot policy during deployment by mixing offline robot data with new fleet rollouts. On 16 dual-arm robots and 8 real-world manipulation tasks, it reports 95% average success after a few hours of online interaction.

## Problem
- Offline VLA pretraining misses distribution shifts, long-tail failures, task variants, and human corrections seen after deployment.
- Pure imitation learning cannot use failed autonomous trials, partial progress, sparse rewards, and recoveries as RL signals.
- Existing robot RL often improves one short-horizon or task-specific policy, so it does not solve continual post-training for a shared generalist policy.

## Approach
- Start with a pretrained flow-based Vision-Language-Action policy that outputs action chunks from observations and language instructions.
- Deploy current checkpoints to a shared fleet, collect autonomous rollouts plus optional human interventions, add them to an online replay buffer, and retrain on mixed offline and online replay.
- Use Distributional Implicit Value Learning: fit a distribution over replay action-values, then use a high quantile as the TD bootstrap target instead of a scalar expectile value.
- Adapt the quantile level with value-distribution entropy, using lower optimism when the value distribution is diffuse.
- Extract the policy with Q-learning via Adjoint Matching, which turns critic action gradients into local training targets for the flow action generator.

## Results
- The real-world evaluation uses 16 dual-arm robots across 8 manipulation tasks.
- The task set includes semantic grocery restocking and long-horizon tasks such as Gongfu tea, cocktails, and fruit juice, with reported execution times of 3–5 minutes for the long-horizon tasks.
- A single generalist policy reaches an average success rate of 95% across all tasks.
- The paper says LWD improves over the pretrained VLA and beats relevant baselines by large margins, but the excerpt does not provide baseline success rates.
- The largest gains are reported on long-horizon tasks, where sparse rewards can be propagated across partial progress with dynamic programming.
- The online improvement phase is reported to need only a few hours of real-world interaction.

## Link
- [https://arxiv.org/abs/2605.00416v1](https://arxiv.org/abs/2605.00416v1)
