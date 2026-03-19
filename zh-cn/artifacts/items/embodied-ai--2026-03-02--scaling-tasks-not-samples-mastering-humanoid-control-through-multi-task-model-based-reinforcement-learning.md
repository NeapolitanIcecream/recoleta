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
- world-model
- sample-efficiency
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Scaling Tasks, Not Samples: Mastering Humanoid Control through Multi-Task Model-Based Reinforcement Learning

## Summary
这篇论文提出 **EZ-M**，主张在在线机器人强化学习中应优先扩展**任务数量**而不是单任务样本量。核心观点是：多任务下，共享世界模型能利用跨任务不变的物理动力学获得更高样本效率，尤其适合高维人形控制。

## Problem
- 现有机器人“基础模型”路线更强调**大模型 + 大规模离线数据**，但机器人学习本质上需要**在线交互**，仅靠离线数据难以持续纠错和适应环境变化。
- 在多任务在线强化学习里，**模型无关（model-free）**方法容易因不同任务在相似状态下要求相反动作而出现**梯度冲突/负迁移**，导致扩展任务数后性能变差或停滞。
- 人形控制尤其困难，因为其**高维、接触丰富、动力学复杂**；如果不能高效复用跨任务共享的物理规律，学习成本会很高。这很重要，因为通用机器人需要在多技能场景中稳定扩展。

## Approach
- 提出 **EfficientZero-Multitask (EZ-M)**：基于 EfficientZero 的**多任务模型式强化学习**框架，学习一个**共享世界模型**，并用任务嵌入对策略、价值、奖励和动力学预测进行条件化。
- 核心机制很简单：不同任务虽然目标不同，但**物理运动规律相同**。因此把多个任务的数据合在一起训练动力学模型，相当于让模型更好地学“世界怎么运转”，而不是为每个任务单独记动作。
- 采用 **Gumbel search / tree search** 在潜在空间里规划动作，并把搜索得到的改进策略蒸馏回策略头；同时使用**分类式 reward/value 建模**来缓解不同任务奖励尺度不一致的问题。
- 加入两类一致性约束来稳定多任务训练：**temporal consistency** 让想象 rollout 的潜在状态贴近真实编码状态；**path consistency** 约束价值预测与“即时奖励 + 下一状态价值”的递推关系一致。
- 工程上还使用**独立任务回放池、平衡任务采样、动作 masking、观测 padding**，以适配不同任务的观测/动作空间并减少任务不平衡。

## Results
- 在 **HumanoidBench** 上，作者声称 **EZ-M 达到 SoTA**，并且比强基线具有**显著更高样本效率**。
- 图 1 的明确设定显示：在 **HumanoidBench-Hard** 上，**环境交互限制为 1 million**、**3 个随机种子** 时，EZ-M **匹配并超过**所有强基线，且“**significantly outperforms all baselines**”。
- 摘要与引言中的强结论是：随着**任务数量增加**，EZ-M 表现出**正迁移**，而模型无关基线会**退化或平台化**；这支持“扩展任务数”是可扩展在线机器人学习的关键轴。
- 理论部分给出样本复杂度主张：当任务数 **K -> ∞** 时，模型式方法的**每任务**样本复杂度趋近于 **d_rew**，而模型无关方法趋近于 **d_dyn + d_rew**，并强调 **d_dyn >> d_rew**，说明共享动力学可带来渐近优势。
- 提供的节选**没有给出更细的表格数值**（如具体平均分、提升百分比、逐基线差值），因此无法进一步列出完整定量对比；但最强的可核实数字是 **1M interactions** 和 **3 seeds** 的设定。

## Link
- [http://arxiv.org/abs/2603.01452v1](http://arxiv.org/abs/2603.01452v1)
