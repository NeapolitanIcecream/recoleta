---
source: arxiv
url: http://arxiv.org/abs/2603.01452v1
published_at: '2026-03-02T05:07:43'
authors:
- Shaohuai Liu
- Weirui Ye
- Yilun Du
- Le Xie
topics:
- model-based-rl
- multi-task-learning
- humanoid-control
- sample-efficiency
- world-models
relevance_score: 0.18
run_id: materialize-outputs
---

# Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning

## Summary
本文提出 EZ-M，一种面向多任务在线学习的人形控制模型式强化学习方法，核心主张是应当扩展**任务数量**而不是单任务样本数。作者认为共享物理动力学让多任务数据可共同训练世界模型，从而在 HumanoidBench 上实现更高样本效率和更强性能。

## Problem
- 现有机器人“基础模型”路线更依赖大参数量和离线数据，但机器人必须通过**在线交互**学习，单靠离线数据难以纠错、适应变化和持续改进。
- 多任务在线强化学习里，模型自由方法常因不同任务在相似状态下需要相反动作而出现**梯度冲突/负迁移**，导致随着任务数增加性能退化或停滞。
- 人形控制尤其困难，因为全身、接触丰富的高维动力学学习本身就是主要瓶颈；如果不能高效共享动力学知识，样本成本会很高。

## Approach
- 提出 **EfficientZero-Multitask (EZ-M)**：在 EfficientZero-v2 基础上扩展到多任务在线 MBRL，用一个**共享世界模型**学习任务无关的物理动力学，再通过任务条件化完成各任务控制。
- 直观机制是：虽然任务奖励和最优动作不同，但**物理规律不变**；因此多任务数据可一起训练动力学模型，任务多样性反而成为一种“动力学正则化”。
- 具体设计包括：可学习任务嵌入、动作编码统一不同动作空间、观测 padding、动作 masking、每任务独立 replay buffer，以及平衡式任务采样。
- 训练时结合 Gumbel tree search 生成改进策略目标，并用监督方式学习策略；奖励/价值采用**categorical prediction** 以缓解跨任务尺度差异。
- 为稳定多步想象与价值学习，加入两类一致性约束：**temporal consistency**（预测潜状态对齐真实编码潜状态）和 **path consistency**（约束 value ≈ reward + γ·next value）。

## Results
- 在 **HumanoidBench** 上，作者声称 EZ-M 达到 **state-of-the-art**，且**无需极端参数扩展**即可获得显著更高样本效率。
- 图 1 的明确结论是：在 **HumanoidBench-Hard** 上，将环境交互限制为 **1 million** 时，EZ-M 仍能**匹配并超过强基线**；所有结果基于 **3 random seeds**。
- 摘要与引言都声称：随着任务数增加，EZ-M 表现出**正迁移**，而模型自由基线会**退化或平台期**；这支持“扩展任务数”是更可扩展的在线机器人学习轴。
- 理论部分给出渐近结论：当任务数 **K → ∞** 时，模型式方法的每任务样本复杂度趋于 **d_rew**，而模型自由方法趋于 **d_dyn + d_rew**，其中作者假设 **d_dyn ≫ d_rew**，据此论证多任务 MBRL 具有结构性样本效率优势。
- 提供的摘录里**缺少更完整的定量表格/具体分数提升百分比**，因此无法准确列出各数据集、指标和基线间的详细数值差距。

## Link
- [http://arxiv.org/abs/2603.01452v1](http://arxiv.org/abs/2603.01452v1)
