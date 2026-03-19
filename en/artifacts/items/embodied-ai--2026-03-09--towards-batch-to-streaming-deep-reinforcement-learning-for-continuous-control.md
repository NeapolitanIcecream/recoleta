---
source: arxiv
url: http://arxiv.org/abs/2603.08588v1
published_at: '2026-03-09T16:40:06'
authors:
- Riccardo De Monte
- Matteo Cederle
- Gian Antonio Susto
topics:
- streaming-rl
- continuous-control
- actor-critic
- sim2real
- online-finetuning
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Towards Batch-to-Streaming Deep Reinforcement Learning for Continuous Control

## Summary
This paper proposes two streaming deep reinforcement learning algorithms for continuous control, S2AC and SDAC, to migrate common batch-style SAC/TD3 methods to a purely online update setting. The goal is to make continual learning on resource-constrained devices and Sim2Real finetuning more feasible, while maintaining performance comparable to existing streaming methods.

## Problem
- Existing high-performance continuous-control DRL methods typically rely on replay buffers, mini-batch updates, and target networks, leading to substantial compute and memory overhead that is unsuitable for edge devices or onboard real-time learning.
- Although purely streaming/online RL is more lightweight, it is incompatible with the SAC and TD3 pretrained policies commonly used in robotics, making the transition from batch training to online finetuning difficult in practice.
- This matters because real robots often need to keep adapting to environmental changes under limited compute, especially in Sim2Real, Real2Sim, and continual deployment scenarios.

## Approach
- Proposes **S2AC**: a streaming version of SAC that removes the replay buffer, batch updates, and target network, and performs online updates directly on the current sample.
- Proposes **SDAC**: a streaming adaptation of TD3/deterministic actor-critic ideas, using deterministic policy gradients for actor updates and adding target action noise to smooth Q-value targets.
- Both methods incorporate engineering choices for stable training: eligibility traces, the ObGD optimizer, sparse initialization, LayerNorm, online state normalization, and reward scaling.
- A key mechanism in S2AC is changing the entropy coefficient from fixed \(\alpha\) to \(\alpha/\sigma_r\), which varies with reward scaling, to keep the “reward vs. entropy” tradeoff stable.
- The paper also discusses practical issues in switching from batch RL to streaming finetuning and proposes preliminary strategies to address them.

## Results
- Experiments are conducted on **MuJoCo Gym** and **DM Control Suite**; the streaming methods trained from scratch run for **20M steps**, all curves are based on **10 random seeds**, evaluation is performed every **10,000 steps**, and each evaluation uses **10 episodes**.
- The paper explicitly claims that **S2AC and SDAC achieve performance comparable to the strongest current streaming baseline, Stream AC(\lambda)**, across multiple standard continuous-control benchmark environments.
- The paper also claims that, compared with AVG, **S2AC does not require environment-specific fine-tuning of the optimizer/hyperparameters**; SDAC likewise **does not introduce environment-specific hyperparameters**.
- The excerpt does not provide final scores, success rates, or percentage improvements on specific tasks, so more detailed numerical comparisons cannot be quoted here; the strongest quantitative information is mainly the experimental setup of **20M steps, 10 seeds, 10k-step eval, and 10-episode eval**.
- The paper further claims that ablation studies validate two points: the adaptive entropy coefficient \(\alpha/\sigma_r\) in S2AC provides practical benefits, and target noise in SDAC is important for stability/performance, though the excerpt does not provide specific numbers.

## Link
- [http://arxiv.org/abs/2603.08588v1](http://arxiv.org/abs/2603.08588v1)
