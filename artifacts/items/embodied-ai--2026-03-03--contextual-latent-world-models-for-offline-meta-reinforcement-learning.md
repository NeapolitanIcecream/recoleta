---
source: arxiv
url: http://arxiv.org/abs/2603.02935v1
published_at: '2026-03-03T12:45:20'
authors:
- Mohammadreza Nakheai
- Aidan Scannell
- Kevin Luck
- Joni Pajarinen
topics:
- offline-meta-rl
- world-model
- task-representation
- self-supervised-rl
- temporal-consistency
relevance_score: 0.34
run_id: materialize-outputs
---

# Contextual Latent World Models for Offline Meta Reinforcement Learning

## Summary
本文提出 SPC（Self-Predictive Contextual Offline Meta-RL），把任务上下文编码与条件化潜在世界模型联合训练，用时间一致性来学习更有用的任务表示。核心思想是：任务表示不只要区分任务，还要真正帮助预测该任务下未来的潜在状态与奖励，因此能更好泛化到未见任务。

## Problem
- 离线元强化学习要从固定数据中学会跨相关任务泛化，但没有在线交互时，**如何从少量上下文推断任务**变得非常关键。
- 现有上下文方法多依赖**对比学习**来学任务表示，通常只能“分开不同任务”，却**不强制表示包含长期的任务相关动力学和奖励信息**。
- 这会限制对未见任务的 few-shot / zero-shot 泛化，而这正是离线元 RL 最重要的目标之一。

## Approach
- 作者提出 **SPC**：先用上下文编码器把一组转移 \((s,a,r,s')\) 映射成任务表示 \(z\)，再让世界模型在预测未来时**显式条件化于这个任务表示**。
- 观测先经编码器得到潜在状态，再用 **FSQ 离散量化**成离散 code；随后任务条件化动力学模型根据当前 code、动作和任务表示，预测下一个离散 code，同时奖励模型预测奖励。
- 训练时使用**多步时间一致性损失**：让模型在潜空间中连续多步预测未来状态与奖励，而不是重建原始观测；这样任务表示必须携带能解释该任务动力学/奖励的关键信息。
- 为避免表示只学预测而不利于区分任务，方法还给上下文编码器加了 **InfoNCE 对比损失**，让同任务表示接近、异任务表示分开。
- 学到表示后，策略、Q 函数和值函数都条件化于“离散潜在状态 + 任务表示”，并用 **IQL** 做离线策略优化以减轻分布偏移问题。

## Results
- 论文声称在 **MuJoCo、Contextual-DeepMind Control、Meta-World** 三类基准上，SPC 对**未见任务泛化**明显优于现有离线元 RL 方法，覆盖 **few-shot 和 zero-shot** 设定。
- 摘要中的最强结论是：联合训练的**任务条件化潜在世界模型**比仅靠对比学习或一步重建目标能学到**更有表达力的任务表示**，从而显著提升泛化性能。
- 方法层面的关键经验结论包括：**多步潜在时间一致性**优于**重建式目标**；并且**离散 codebook / categorical dynamics** 对建模随机、多峰转移很重要。
- 提供的节选**没有给出具体数值结果**，因此无法准确列出指标、数据集分数、相对提升百分比或与各基线的精确差距。

## Link
- [http://arxiv.org/abs/2603.02935v1](http://arxiv.org/abs/2603.02935v1)
