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
- world-models
- representation-learning
- task-conditioning
- reinforcement-learning
relevance_score: 0.34
run_id: materialize-outputs
---

# Contextual Latent World Models for Offline Meta Reinforcement Learning

## Summary
本文提出 SPC（Self-Predictive Contextual Offline Meta-RL），把任务上下文编码与任务条件潜在世界模型联合训练，以提升离线元强化学习对未见任务的泛化。核心思想是用“预测未来潜在状态和奖励”的时序一致性信号，而不只是做任务对比区分。

## Problem
- 离线元强化学习需要仅凭固定离线数据，学到能泛化到未见相关任务的策略，这对真实世界中无法反复在线交互的场景很重要。
- 现有基于 context encoder 的方法通常主要依赖对比学习，只会“区分任务”，却未必学到真正决定控制效果的任务相关动力学与奖励结构。
- 一步重建或观测重建信号往往不足以捕获长时程、任务相关的动态变化，因此限制了 few-shot / zero-shot 泛化。

## Approach
- 用上下文编码器从一小段转移 (s,a,r,s') 中聚合出任务表示 `z`，把它作为隐式任务标识提供给世界模型、价值函数和策略。
- 用观测编码器把状态映射到离散潜在码 `c`，再通过**任务条件**潜在动力学模型 `D(c,a,z)` 预测未来潜在状态，并用奖励模型 `R(c,a,z)` 预测奖励。
- 训练时采用多步时序一致性目标：对未来潜在码使用交叉熵损失、对奖励使用平方误差；这样迫使任务表示必须包含能解释未来演化与奖励的任务信息。
- 为避免表示坍塌并增强任务可分性，再给上下文编码器加入 InfoNCE 对比损失；最终上下文编码器联合优化“时序一致性 + 对比学习”。
- 下游策略学习阶段采用 IQL，在离散潜在状态 `c` 和任务表示 `z` 上做离线策略优化，以减少离线 RL 的分布偏移问题。

## Results
- 论文声称在 **MuJoCo、Contextual-DeepMind Control、Meta-World** 三类基准上，SPC 对未见任务的 **few-shot 和 zero-shot 泛化** 均显著优于现有 SOTA 离线元强化学习方法。
- 摘要与给定节选没有提供具体数值表格、均值/方差、百分比提升、或逐基线对比数字，因此**无法从提供文本中提取定量结果**。
- 最强的具体主张是：与仅用对比学习或基于重建的表征学习相比，SPC 学到的任务表示更能捕获**任务相关动力学**，而不是仅仅把不同任务分开。
- 论文还主张：离散代码本潜在空间 + 任务条件动力学，对学习**随机/多峰转移动态**更有表达力，并对性能有明显影响，但节选中未给出量化幅度。

## Link
- [http://arxiv.org/abs/2603.02935v1](http://arxiv.org/abs/2603.02935v1)
