---
source: arxiv
url: http://arxiv.org/abs/2603.12243v1
published_at: '2026-03-12T17:56:29'
authors:
- Amber Xie
- Haozhi Qi
- Dorsa Sadigh
topics:
- dexterous-manipulation
- sim2real
- residual-reinforcement-learning
- robot-piano-playing
- bimanual-control
relevance_score: 0.77
run_id: materialize-outputs
---

# HandelBot: Real-World Piano Playing via Fast Adaptation of Dexterous Robot Policies

## Summary
HandelBot旨在让通用双手机器人实现真实世界钢琴演奏，通过“仿真预训练 + 现实快速适配”来解决高精度灵巧操作中的sim2real难题。它把毫米级对位问题拆成先做结构化轨迹校正，再用少量真实交互做残差强化学习微调。

## Problem
- 真实世界双手钢琴演奏要求**毫米级空间精度、精确时序和多指协同**，直接从仿真迁移的策略很容易因微小误差而失败。
- 高自由度灵巧手的数据采集很难扩展：遥操作困难，而人类数据到机器人又存在显著**形体差距**。
- 因此，需要一种**几乎不依赖大规模真实示教**、但又能快速跨越sim-to-real gap的方法，这对高精度灵巧操作很重要。

## Approach
- 先在仿真中用RL训练基础策略，学习双手弹琴的**粗粒度手指协同**；再从该策略提取一个开环轨迹用于真实部署。
- 第一阶段做**结构化策略精修**：根据真实钢琴MIDI反馈，比较“目标键”和“实际按下的键”，迭代调整每根手指的**横向关节**，并使用分块更新和前瞻窗口让修正更平滑。
- 第二阶段做**残差强化学习**：冻结精修后的基础轨迹，只学习小幅修正量，把下一步目标关节位置改为“基础动作 + 残差动作”，从而更安全、样本效率更高。
- 真实世界奖励直接来自钢琴的**MIDI按键输出**；算法使用TD3，并加入受目标按键方向启发的**guided noise**来帮助探索正确横向移动。
- 系统部署在两只Tesollo DG-5F灵巧手 + 两台Franka机械臂上，每只手只对3根活动手指学习残差，以降低动作维度和适配难度。

## Results
- 论文声称这是**首个基于学习的真实世界双手钢琴演奏系统**，并在**5首知名乐曲**上进行了硬件评测：Twinkle Twinkle、Ode to Joy、Hot Cross Buns、Fur Elise、Prelude in C。
- 相比直接sim-to-real部署，HandelBot整体性能**提升1.8×**，且只需**30分钟**真实交互数据即可完成快速适配（摘要与贡献中明确给出）。
- 评测指标为**F1 score**（文中图3与表格均报告F1×100）；作者指出HandelBot在**全部5首曲目上都是最优方法**，优于纯仿真、仿真+残差RL、以及从零开始真实RL等基线。
- 已给出的具体数字包括：在**Twinkle Twinkle**上，HandelBot达到**81 ± 4.1** F1×100；其消融版本中，γ=0.75为**73 ± 2.5**，γ=0.9为**69 ± 0.2**，guided noise概率=0时为**81 ± 0.7**，概率=1时为**77 ± 0.9**。
- 针对仿真策略部署方式，表1显示闭环\(\pi_{sim}\)(CL)普遍较差，例如**Ode to Joy: 5 ± 2.46 vs 12 ± 2.6**（Hybrid）、**Prelude in C: 29 ± 2.2 vs 40 ± 1.0**，说明直接使用真实观测闭环执行会明显受动力学偏差影响。
- 文本未在摘录中给出图3所有方法在5首曲目上的完整数值表，但最强的具体主张是：**HandelBot在所有歌曲上取得最高F1，并稳定超过不使用真实数据的方法**。

## Link
- [http://arxiv.org/abs/2603.12243v1](http://arxiv.org/abs/2603.12243v1)
