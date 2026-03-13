---
source: arxiv
url: http://arxiv.org/abs/2603.08588v1
published_at: '2026-03-09T16:40:06'
authors:
- Riccardo De Monte
- Matteo Cederle
- Gian Antonio Susto
topics:
- reinforcement-learning
- continuous-control
- streaming-rl
- online-learning
- sim2real
relevance_score: 0.18
run_id: materialize-outputs
---

# Towards Batch-to-Streaming Deep Reinforcement Learning for Continuous Control

## Summary
本文提出两种面向连续控制的流式深度强化学习算法 S2AC 和 SDAC，用于把依赖回放缓冲区与批量更新的 SAC/TD3 迁移到纯在线更新场景。其目标是支持资源受限设备上的持续学习与从 batch 到 streaming 的微调，同时保持接近现有流式方法的性能。

## Problem
- 现有连续控制 DRL 方法如 SAC、TD3 通常依赖 replay buffer、mini-batch 和 target network，计算开销较大，不适合边缘设备或板载实时学习。
- 纯流式深度 RL 虽更适合在线部署，但现有方法与主流 batch RL 预训练策略不兼容，难以用于 Sim2Real 等实际微调场景。
- 从 batch 训练切换到 streaming 微调时会遇到稳定性、尺度变化和超参数敏感等实际问题，这很重要，因为真实机器人往往需要在线适应且计算预算有限。

## Approach
- 提出 **S2AC**：把 SAC 改造成流式版本，去掉 replay buffer、batch update 和 target network，直接用当前样本在线更新 soft Q，并保留最大熵策略优化。
- 提出 **SDAC**：把 TD3/确定性 actor-critic 改造成流式版本，使用确定性策略梯度、在线 Q 学习，并在目标动作中加入高斯噪声以平滑价值估计。
- 两种方法都使用相同的稳定化设计：稀疏初始化、LayerNorm、在线状态归一化、奖励缩放、以及带资格迹的 ObGD 来更新 critic，以减轻单样本在线更新的高噪声与大步长不稳定。
- S2AC 的一个关键机制是把熵系数从固定 \(\alpha\) 改为随奖励标准差变化的 \(\alpha/\sigma_r\)，以在奖励被动态缩放时维持“奖励 vs 熵”的相对权重。
- 论文还讨论如何把 batch 预训练策略切换到 streaming 微调，并声称这些为流式兼容而做的简单改动也能提升 batch SAC/TD3 的表现。

## Results
- 实验在 **MuJoCo Gym** 和 **DM Control Suite** 上进行；从零开始训练时，策略训练 **20M steps**，每个实验使用 **10 个随机种子**，每 **10,000 steps** 评估一次，并在 **10 个评估 episode** 上取平均回报。
- 论文明确声称：**S2AC 和 SDAC 的性能与当前 SOTA 流式基线 Stream AC(\(\lambda\)) 可比**，覆盖标准连续控制基准；但给出的摘录中**没有提供具体任务级分数、均值/方差或相对提升百分比**。
- 与 AVG 相比，作者声称 **S2AC 不需要按环境单独调 optimizer/hyperparameter**；同时 **SDAC 不引入环境特定超参数**，强调了 Q-based 流式算法的实用性。
- 消融实验被描述为验证两项关键设计：S2AC 中的 **自适应熵系数 \(\alpha/\sigma_r\)** 与 SDAC 中的 **target noise** 都对稳定训练和性能有实际帮助；但摘录里**没有给出具体数值结果**。
- 论文还声称自己是**首批**系统研究从 **batch 到 streaming** 微调实际挑战并提出具体策略的工作之一，面向 **Sim2Real**、**Real2Sim** 和动态计算预算切换等应用场景。

## Link
- [http://arxiv.org/abs/2603.08588v1](http://arxiv.org/abs/2603.08588v1)
