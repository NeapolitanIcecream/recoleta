---
source: arxiv
url: http://arxiv.org/abs/2603.11110v1
published_at: '2026-03-11T11:27:08'
authors:
- Jseen Zhang
- Gabriel Adineera
- Jinzhou Tan
- Jinoh Kim
topics:
- world-model
- visual-rl
- model-based-rl
- continuous-control
- residual-action
- dmcontrol
relevance_score: 0.86
run_id: materialize-outputs
---

# ResWM: Residual-Action World Model for Visual RL

## Summary
ResWM提出一种用于视觉强化学习的世界模型改造：不再直接预测绝对动作，而是预测相对上一步动作的“残差动作”。这样把控制变成小步平滑调整，并结合相邻观测差分编码，提升样本效率、长期规划稳定性和动作平滑性。

## Problem
- 现有视觉世界模型通常直接以**绝对动作**为条件，这会让策略优化面对任务相关、非平稳且高方差的动作分布，容易训练不稳。
- 在连续控制和机器人场景中，这种设定常导致**动作抖动/振荡**、长时域规划误差累积、控制低效，影响安全性与能耗。
- 该问题重要，因为视觉RL和机器人数据昂贵，若世界模型不稳定，就会削弱模型式RL在样本效率和真实部署上的核心价值。

## Approach
- 将动作重参数化为**残差动作**：策略先预测增量 \(\delta a_t\)，再与前一时刻动作组合得到当前动作 \(a_t=\tanh(a_{t-1}+\delta a_t)\)。最简单理解：模型每一步只做“小修正”，而不是每次都重新猜完整动作。
- 在世界模型的潜在动力学中，也改为用**残差动作而非绝对动作**驱动状态转移与想象滚动，从而让规划和策略学习都在同一种更平滑的动作空间中进行。
- 提出**Observation Difference Encoder (ODL)**，直接编码相邻两帧的差异 \(o_t-o_{t-1}\)，提取“环境变化”而非静态内容，得到更紧凑、与残差控制更匹配的动态表征。
- 保持Dreamer式RSSM框架基本不变，且声称**无需额外超参数**；再配合对残差动作的KL约束和可选能量惩罚，抑制过大、抖动的控制更新。

## Results
- 在 **DMControl 6个常见任务、100K steps** 下，ResWM平均分 **828.7**，高于 **DeepRAD 695.1**、**RAD 663.6**、**DeepMDP 460.5**、**pixel SAC 167.3**。
- 在 **DMControl 6个常见任务、500K steps** 下，ResWM平均分 **925.0**，高于 **DeepRAD 890.8**、**RAD 872.5**、**DeepMDP 764.6**、**pixel SAC 216.8**。
- 单任务示例：**Reacher Easy @100K**，ResWM **942 ± 43**，优于 **DeepRAD 792 ± 77**、**RAD 894 ± 32**；**Finger Spin @100K**，ResWM **986 ± 86**，优于 **DeepRAD 832 ± 101**。
- 文中相关段落还声称：在更广泛比较中，ResWM在DMControl平均分达到 **925.0**，超过 **TACO 887.1**、**MaDi 885.1**；在困难任务上 **1M steps** 平均 **644.8 vs. ResAct 630.2**。
- 论文还声称动作轨迹更稳定、更平滑、更节能，且长期预测误差更小；但在给定摘录中，**动作平滑性/能耗**没有看到更细的明确量化表格。

## Link
- [http://arxiv.org/abs/2603.11110v1](http://arxiv.org/abs/2603.11110v1)
