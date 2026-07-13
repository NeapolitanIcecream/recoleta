---
source: arxiv
url: https://arxiv.org/abs/2607.09590v1
published_at: '2026-07-10T16:42:17'
authors:
- Yujie Pang
- Zudong Li
topics:
- robot-foundation-model
- generalist-robot-policy
- reinforcement-learning
- action-chunking
- contact-manipulation
- sim2real
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# PAC-ACT: Post-training Actor-Critic for Action Chunking Transformers

## Summary
PAC-ACT post-trains pretrained Action Chunking Transformer policies with chunk-level PPO and behavior-prior regularization. It improves contact-task success and force safety while retaining the low latency and lower memory cost of ACT-style policies.

## Problem
- Behavior-cloned action-chunking policies accumulate errors under pose disturbances and contact-state distribution shift.
- Precision contact tasks require reliable completion and force control; forces above 60N can indicate unsafe contact.
- Step-wise reinforcement learning poorly matches policies that generate and execute temporally coupled action chunks.

## Approach
- Reformulate the control problem so each RL decision contains an 8-step action chunk, while rewards are collected at each environment step and aggregated at chunk boundaries.
- Reuse the pretrained ACT visual encoder, Transformer encoder, and action decoder as the actor, remove the CVAE, and model each chunk with a diagonal Gaussian policy.
- Build the critic from the ACT encoder plus a pooled value head, without the action decoder.
- Train with PPO using chunk-level probability ratios and generalized advantage estimation, an adjacent-policy KL penalty, and a reward penalty for deviating from the frozen pretrained ACT policy.

## Results
- On the Contour precision-contact task, PAC-ACT significantly reduces median peak contact force; the excerpt does not provide the absolute median values.
- The share of force readings above 60N decreases by 46 times compared with the pretrained or comparison policy; the excerpt does not specify the exact denominator or absolute rates.
- The method improves task success, contact stability, and force safety on the Metal Touch benchmark, which randomizes object position within plus or minus 2cm, and is also evaluated on Square Assembly; complete success-rate tables are absent from the provided excerpt.
- A critic that retains the action decoder performs about 12 percentage points worse at the same training budget than the encoder-only critic.
- A sparse-reward ablation shows that task-success reward plus the behavior-prior constraint still supports exploration under randomized initial poses.

## Link
- [https://arxiv.org/abs/2607.09590v1](https://arxiv.org/abs/2607.09590v1)
