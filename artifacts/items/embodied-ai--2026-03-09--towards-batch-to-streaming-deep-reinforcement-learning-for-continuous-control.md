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
---

# Towards Batch-to-Streaming Deep Reinforcement Learning for Continuous Control

## Summary
本文提出两种面向连续控制的流式深度强化学习算法 S2AC 和 SDAC，用于把常见的批量式 SAC/TD3 迁移到纯在线更新场景。其目标是让资源受限设备上的持续学习与 Sim2Real 微调更可行，同时保持与现有流式方法相当的性能。

## Problem
- 现有高性能连续控制 DRL 方法通常依赖 replay buffer、mini-batch 更新和 target network，算力与内存开销较大，不适合边缘设备或机载实时学习。
- 纯流式/在线 RL 虽更轻量，但与机器人中常用的 SAC、TD3 预训练策略不兼容，导致从批量训练切换到在线微调在实践中很困难。
- 这很重要，因为真实机器人往往需要在有限算力下继续适应环境变化，尤其是 Sim2Real、Real2Sim 和持续部署场景。

## Approach
- 提出 **S2AC**：把 SAC 改造成流式版本，去掉 replay buffer、batch update 和 target network，直接对当前样本做在线更新。
- 提出 **SDAC**：把 TD3/确定性 actor-critic 思想改造成流式版本，使用确定性策略梯度进行 actor 更新，并加入目标动作噪声来平滑 Q 值目标。
- 两个方法都结合了稳定训练的工程设计：eligibility traces、ObGD 优化器、稀疏初始化、LayerNorm、在线状态归一化和奖励缩放。
- S2AC 的一个关键机制是把熵系数从固定 \(\alpha\) 改为随奖励缩放变化的 \(\alpha/\sigma_r\)，以保持“奖励 vs 熵”权衡稳定。
- 论文还讨论了从批量 RL 切换到流式微调时的实际问题，并提出初步应对策略。

## Results
- 实验在 **MuJoCo Gym** 和 **DM Control Suite** 上进行；从头训练的流式方法训练 **20M steps**，所有曲线基于 **10 个随机种子**，每 **10,000 steps** 评估一次，每次评估 **10 个 episode**。
- 论文明确声称：**S2AC 和 SDAC 的性能与当前最强流式基线 Stream AC(\lambda) 可比**，覆盖多个标准连续控制基准环境。
- 论文还声称：相比 AVG，**S2AC 不需要按环境精细调 optimizer/hyperparameter**；SDAC 也**不引入环境特定超参数**。
- 文段未提供具体任务上的最终分数、成功率或相对提升百分比，因此无法在此摘录更细的数值比较；最强定量信息主要是 **20M steps、10 seeds、10k-step eval、10-episode eval** 这一实验设置。
- 论文进一步声称消融实验验证了两点：S2AC 中自适应熵系数 \(\alpha/\sigma_r\) 有实际收益；SDAC 中目标噪声对稳定性/性能重要，但节选未给出具体数字。

## Link
- [http://arxiv.org/abs/2603.08588v1](http://arxiv.org/abs/2603.08588v1)
