---
source: arxiv
url: https://arxiv.org/abs/2606.18697v1
published_at: '2026-06-17T05:24:18'
authors:
- Yibin Hu
- Xiaolin Sun
- Zizhan Zheng
topics:
- world-model
- data-poisoning
- model-based-rl
- planning-security
- continuous-control
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Stealthy World Model Manipulation via Data Poisoning

## Summary
SWAAP is a two-stage data poisoning attack against learned world models used for model-based planning. It shows that changing a bounded subset of fine-tuning transition targets can push a world model toward harmful dynamics while keeping the poisoned data close to normal prediction errors.

## Problem
- Learned world models are updated from collected trajectories, so a compromised fine-tuning buffer can change future planning behavior without direct access to deployed model weights.
- Existing supervised-learning poisoning methods do not fit this setting because next-state targets are structured, high-dimensional, and affect long-horizon rollouts.
- The risk matters for robotics, autonomous systems, and other model-based agents that rely on world-model adaptation after deployment.

## Approach
- Stage 1 searches for a target world model that lowers true-environment return while staying close to clean dynamics.
- The paper uses a first-order bilevel method and a transition-gradient theorem to update transition-model parameters without differentiating through the full planner or policy optimizer.
- Stage 2 poisons data by changing only selected next-state targets in the fine-tuning set, leaving states, actions, and rewards unchanged.
- It selects the top-rp fraction of transitions with the largest residual under the target model, then optimizes poisoned targets so their training gradient matches the gradient that would move the victim model toward the Stage 1 target.
- A prediction-error regularizer keeps poisoned targets near the clean model’s natural one-step error, and a trajectory-consistent variant changes shared intermediate states consistently across adjacent transitions.

## Results
- The excerpt gives no quantitative return drops, poisoning rates, or defense success rates from the experiments.
- The paper claims SWAAP is the first data poisoning attack built for learned world-model dynamics in deep model-based RL.
- It evaluates 2 world-model agents: TD-MPC2 and DINO-WM.
- It reports experiments across 3 benchmark suites: DMControl, MyoSuite, and MetaWorld.
- It evaluates stealth against 3 defense stages: pre-training transition detection, robust fine-tuning with TRIM, and test-time model monitoring.
- The stated qualitative result is that poisoning a small fraction of fine-tuning data causes large performance drops while evading evaluated residual, CUSUM, and TRIM-style defenses, but the excerpt does not provide the numeric margins.

## Link
- [https://arxiv.org/abs/2606.18697v1](https://arxiv.org/abs/2606.18697v1)
