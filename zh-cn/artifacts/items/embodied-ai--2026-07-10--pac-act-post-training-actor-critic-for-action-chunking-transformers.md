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
language_code: zh-CN
---

# PAC-ACT: Post-training Actor-Critic for Action Chunking Transformers

## Summary
## 摘要
PAC-ACT 使用分块级 PPO 和行为先验正则化，对预训练的动作分块变换器策略进行后训练。在保留 ACT 类策略低延迟和较低内存成本的同时，该方法提升了接触任务成功率和力安全性。

## 问题
- 通过行为克隆训练的动作分块策略在位姿扰动和接触状态分布偏移下会累积误差。
- 精密接触任务要求可靠完成任务并控制接触力；超过 60N 的力可能表示接触不安全。
- 逐步强化学习与生成和执行时间耦合动作分块的策略匹配较差。

## 方法
- 重新表述控制问题，使每个强化学习决策包含一个 8 步动作分块，同时在每个环境步收集奖励，并在分块边界进行聚合。
- 复用预训练 ACT 的视觉编码器、Transformer 编码器和动作解码器作为演员网络，移除 CVAE，并用对角高斯策略对每个分块建模。
- 使用 ACT 编码器和池化价值头构建评论家网络，不使用动作解码器。
- 使用 PPO 训练，采用分块级概率比率和广义优势估计，并加入相邻策略 KL 惩罚，以及偏离冻结预训练 ACT 策略的奖励惩罚。

## 结果
- 在 Contour 精密接触任务中，PAC-ACT 显著降低了接触力峰值的中位数；摘录没有提供中位数的绝对值。
- 与预训练策略或对比策略相比，超过 60N 的力读数比例降低了 46 倍；摘录没有说明确切的分母或绝对比例。
- 在 Metal Touch 基准测试中，该方法提升了任务成功率、接触稳定性和力安全性。该测试会在正负 2cm 范围内随机化物体位置；方法还在 Square Assembly 上进行了评估。提供的摘录没有包含完整的成功率表格。
- 在相同训练预算下，保留动作解码器的评论家网络表现约低 12 个百分点于仅使用编码器的评论家网络。
- 稀疏奖励消融实验表明，即使使用任务成功奖励和行为先验约束，在随机初始位姿下仍能支持探索。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.09590v1](https://arxiv.org/abs/2607.09590v1)
