---
source: arxiv
url: https://arxiv.org/abs/2606.10305v1
published_at: '2026-06-09T01:46:23'
authors:
- Qianzhong Chen
- Hau Zheng
- Justin Yu
- Suning Huang
- Jiankai Sun
- Ken Goldberg
- Chuan Wen
- Pieter Abbeel
- Yide Shentu
- Philipp Wu
- Mac Schwager
topics:
- vision-language-action
- robot-reward-modeling
- long-horizon-manipulation
- self-improving-robots
- robot-data-scaling
- mixture-of-experts
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# SARM2: Multi-Task Stage Aware Reward Modeling for Self Improving Robotic Manipulation

## Summary
SARM2 is a multi-task dense reward model for long-horizon robotic manipulation, paired with SPIRAL, an on-policy VLA improvement loop that uses autonomous rollouts. The paper claims better reward accuracy on a 10-task benchmark and large real-robot success gains on folding shorts and cleaning a whiteboard.

## Problem
- Long-horizon VLA fine-tuning still depends on expensive demonstrations, and behavior cloning has trouble recovering when the policy leaves the demo distribution.
- Sparse rewards give weak credit assignment over multi-stage robot tasks, while large VLM reward models are too coarse for per-step progress.
- Existing stage-aware reward models can be accurate, but they usually need task-specific stage labels and retraining for each task.

## Approach
- SARM2 predicts the current action primitive from recent robot observations, using 3 camera views, proprioception, frozen SigLIP-2 features, and a 4-layer causal Transformer.
- The stage estimator classifies each segment into 22 classes: 21 action primitives plus a null class. The primitive data comes from 200 hours across 100 real-world manipulation tasks, with 66 balanced hours used for primitive training.
- A separate 6-layer causal Transformer value model estimates normalized remaining steps to completion in the range [-1, 0].
- The value head uses a multi-gate Mixture-of-Experts decoder. The predicted primitive selects a gate, and the gate routes the state through shared MLP experts.
- SPIRAL starts from a BC-fine-tuned VLA, adapts the reward model once with about 100 labeled rollouts, then alternates autonomous rollout collection, SARM2 relabeling, and residual TD3-style RL updates.

## Results
- On the 10-task reward benchmark, SARM2 gets the best overall demo MSE: 0.020, compared with ReWiND 0.036, TOPReward 0.107, Robometer 0.093, and LoRA-finetuned Robometer 0.043.
- On the classic subset S1, SARM2 reaches 0.006 demo MSE. On the unconventional subset S2, it reaches 0.031 demo MSE.
- Removing the stage estimator raises overall demo MSE from 0.020 to 0.034. Removing the multi-gate design raises it to 0.026.
- On rollout ranking, SARM2 reaches rho 0.833 on Folding Shorts and 0.667 on Cleaning Whiteboard, the best score on the harder whiteboard task.
- With SPIRAL, Folding Shorts Flat improves to 12/12 successes, and Folding Shorts Crumpled reaches 8/12 successes after three rounds.
- On Cleaning Whiteboard, SPIRAL with SARM2 reaches 18/20 successes and 97.5% progress, compared with 13/20 for finetuned Robometer rewards and 10/20 at 81.3% progress for demo-only RL-Dense.

## Link
- [https://arxiv.org/abs/2606.10305v1](https://arxiv.org/abs/2606.10305v1)
