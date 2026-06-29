---
source: arxiv
url: http://arxiv.org/abs/2604.04539v1
published_at: '2026-04-06T09:03:41'
authors:
- Donghu Kim
- Youngdo Lee
- Minho Park
- Kinam Kim
- I Made Aswin Nahendra
- Takuma Seno
- Sehee Min
- Daniel Palenicek
- Florian Vogt
- Danica Kragic
- Jan Peters
- Jaegul Choo
- Hojoon Lee
topics:
- off-policy-rl
- soft-actor-critic
- high-dimensional-control
- sim-to-real
- humanoid-locomotion
- dexterous-manipulation
relevance_score: 0.81
run_id: materialize-outputs
language_code: en
---

# FlashSAC: Fast and Stable Off-Policy Reinforcement Learning for High-Dimensional Robot Control

## Summary
FlashSAC is an off-policy reinforcement learning method for high-dimensional robot control that aims to match or beat PPO while training faster and staying stable. The paper claims the biggest gains on dexterous manipulation, humanoid locomotion, and sim-to-real humanoid walking.

## Problem
- Standard on-policy RL methods such as PPO are stable, but they throw away past data and become inefficient when robot tasks have large state and action spaces or expensive simulation.
- Standard off-policy methods can reuse replay data, but in high-dimensional control they often train slowly and become unstable because critic errors compound through bootstrapped value updates.
- This matters for modern robot learning tasks such as dexterous hands, humanoids, and vision-based control, where broad data coverage and wall-clock speed both matter for sim and sim-to-real training.

## Approach
- FlashSAC builds on Soft Actor-Critic and changes the training regime: it uses many parallel simulators, a large replay buffer, larger actor/critic networks, large batches, and very few gradient updates per amount of new data.
- The main idea is to trade frequent updates for higher data throughput and larger models. In the GPU setup, it uses 1024 parallel environments, a replay buffer up to 10M transitions, 2.5M-parameter 6-layer actor and critic networks, batch size 2048, and an update-to-data ratio of 2/1024.
- To keep the critic stable under bootstrapping, it constrains several norms: RMS normalization on features, pre-activation batch normalization, cross-batch value prediction so current and target Q-values share batch statistics, and post-update weight projection to bounded norms.
- It also uses a distributional critic with adaptive reward scaling to keep return targets within a fixed support and reduce sensitivity to noisy targets.
- For exploration, it uses a unified entropy target based on action standard deviation (`σ_tgt = 0.15`) and a simple temporally correlated exploration method called noise repetition, where sampled noise is held for a random number of steps.

## Results
- The paper evaluates FlashSAC on more than 60 tasks across 10 simulators, covering low- and high-dimensional state-based control, vision-based control, and sim-to-real humanoid locomotion.
- On 25 GPU-based state-control tasks, off-policy methods are trained for 50M environment steps, while PPO is trained for 200M steps, which the paper says uses about 3× the compute of FlashSAC.
- On high-dimensional GPU tasks such as dexterous manipulation and humanoid locomotion, the paper claims FlashSAC consistently reaches higher final return than PPO and does so in less wall-clock time. The excerpt gives this as a qualitative claim and does not provide exact per-task return numbers.
- On low-dimensional GPU tasks, FlashSAC is reported as roughly comparable to PPO, with slight gains in some cases.
- Against FastTD3, the paper claims FlashSAC is more stable and converges on tasks where FastTD3 often fails or underperforms, with the largest gains on humanoid locomotion.
- In sim-to-real humanoid locomotion on the Unitree G1, the paper claims training time drops from hours with PPO to minutes with FlashSAC. The excerpt does not give an exact minute count or a quantitative real-world performance table.

## Link
- [http://arxiv.org/abs/2604.04539v1](http://arxiv.org/abs/2604.04539v1)
