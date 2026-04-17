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
language_code: zh-CN
---

# FlashSAC: Fast and Stable Off-Policy Reinforcement Learning for High-Dimensional Robot Control

## Summary
## 摘要
FlashSAC 是一种用于高维机器人控制的离策略强化学习方法，目标是在保持稳定的同时，以更快的训练速度达到或超过 PPO 的表现。论文称，最大的收益出现在灵巧操作、人形机器人运动，以及仿真到现实的人形行走任务上。

## 问题
- 标准的在策略强化学习方法，如 PPO，稳定性较好，但会丢弃过去的数据；当机器人任务具有较大的状态空间和动作空间，或者仿真成本较高时，这种做法效率较低。
- 标准离策略方法可以复用回放数据，但在高维控制中往往训练缓慢且不稳定，因为 critic 误差会通过自举式价值更新不断累积。
- 这对现代机器人学习任务很重要，例如灵巧手、人形机器人和基于视觉的控制；在这些任务中，数据覆盖范围和实际训练时间都会影响仿真训练与仿真到现实训练的效果。

## 方法
- FlashSAC 基于 Soft Actor-Critic，并调整了训练方式：它使用大量并行模拟器、大型回放缓冲区、更大的 actor/critic 网络、大批量训练，以及相对于新增数据量而言很少的梯度更新。
- 核心思路是用更高的数据吞吐和更大的模型，换掉高频更新。在 GPU 设置中，它使用 1024 个并行环境、最高 10M transitions 的回放缓冲区、参数量为 250 万的 6 层 actor 和 critic 网络、2048 的 batch size，以及 2/1024 的 update-to-data ratio。
- 为了在自举训练下保持 critic 稳定，它约束了多个范数：对特征使用 RMS normalization，使用 pre-activation batch normalization，采用 cross-batch value prediction，使当前 Q 值和目标 Q 值共享 batch 统计量，并在每次更新后将权重投影到有界范数内。
- 它还使用 distributional critic 和 adaptive reward scaling，把回报目标限制在固定支撑范围内，并降低对噪声目标的敏感性。
- 在探索方面，它使用基于动作标准差的统一熵目标（`σ_tgt = 0.15`），以及一种简单的时间相关探索方法 noise repetition，即将采样得到的噪声保持若干个随机步数。

## 结果
- 论文在 10 个模拟器上的 60 多个任务上评估了 FlashSAC，覆盖低维和高维的基于状态控制、基于视觉的控制，以及仿真到现实的人形机器人运动。
- 在 25 个基于 GPU 的状态控制任务上，离策略方法训练 50M environment steps，而 PPO 训练 200M steps；论文称这大约是 FlashSAC 计算量的 3 倍。
- 在灵巧操作和人形机器人运动等高维 GPU 任务上，论文称 FlashSAC 的最终回报持续高于 PPO，而且实际训练时间更短。摘录中这是定性表述，没有给出各任务的精确回报数值。
- 在低维 GPU 任务上，FlashSAC 据称与 PPO 大致相当，部分任务略有提升。
- 与 FastTD3 相比，论文称 FlashSAC 更稳定，并且能在 FastTD3 经常失败或表现较差的任务上收敛，其中最大收益出现在人形机器人运动任务。
- 在 Unitree G1 的仿真到现实人形机器人运动任务中，论文称训练时间从 PPO 的数小时降到 FlashSAC 的数分钟。摘录没有给出精确分钟数，也没有提供量化的真实世界性能表。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04539v1](http://arxiv.org/abs/2604.04539v1)
