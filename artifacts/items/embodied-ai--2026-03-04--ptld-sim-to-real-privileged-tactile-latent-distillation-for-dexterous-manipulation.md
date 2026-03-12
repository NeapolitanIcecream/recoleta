---
source: arxiv
url: http://arxiv.org/abs/2603.04531v1
published_at: '2026-03-04T19:17:42'
authors:
- Rosy Chen
- Mustafa Mukadam
- Michael Kaess
- Tingfan Wu
- Francois R Hogan
- Jitendra Malik
- Akash Sharma
topics:
- dexterous-manipulation
- sim-to-real
- tactile-learning
- privileged-distillation
- asymmetric-actor-critic
relevance_score: 0.94
run_id: materialize-outputs
---

# PTLD: Sim-to-real Privileged Tactile Latent Distillation for Dexterous Manipulation

## Summary
PTLD提出一种不必在仿真中建模触觉传感器的灵巧操作学习方法，通过先在仿真/真实中运行带“特权传感器”的策略，再把其潜变量蒸馏到真实可部署的触觉策略。它面向多指手触觉灵巧操作这一高难度、难示教且强依赖接触感知的问题。

## Problem
- 目标问题：学习多指手的触觉灵巧操作策略，尤其是**in-hand rotation**与更困难的**in-hand reorientation**。
- 重要性：这类接触丰富任务对家庭、工具使用等机器人能力关键，但高质量示教很难获取，尤其多指手遥操作/示教成本极高。
- 核心瓶颈：纯RL虽可在仿真中学，但**触觉仿真既慢又不真实**，导致触觉策略难以直接做sim-to-real；而仅靠本体感觉的“盲操”策略性能上限有限。

## Approach
- 先在仿真中训练一个使用**privileged sensors**（如物体位姿、形状等高可观测信息）的强策略，而不是去仿真触觉本身。
- 用**Asymmetric Actor-Critic + 在线潜变量蒸馏**简化传统两阶段privileged distillation：critic看特权状态，actor只看可部署观测，并通过潜变量对齐学习更好的表征。
- 在真实世界中搭建带4个相机和物体标记的**特权传感器系统**，部署该特权策略收集数据，同时记录真实触觉与策略潜变量。
- 之后用监督学习把“特权策略的潜变量”蒸馏到一个输入为**触觉+本体感觉**的编码器上，得到真实可部署的触觉策略。
- 为缓解离线蒸馏的分布偏移，作者使用**DAgger式迭代数据聚合**，用中间触觉编码器收集更多on-policy数据继续训练。

## Results
- 在**in-hand rotation**基准任务上，PTLD相对**proprioception-only policy**带来**182% improvement**（文中摘要明确声明，但摘录未给出绝对分数、数据集规模或方差）。
- 在更困难的**tactile in-hand reorientation**任务上，PTLD使**number of goals reached**相对仅用本体感觉提升**57%**。
- 作者声称PTLD在旋转任务上对**物体滑移、质量变化、手腕朝向变化**更鲁棒，但摘录中未提供这些鲁棒性实验的完整量化表格。
- 论文还声称其触觉策略不仅优于本体感觉策略，也优于**adaptation-based tactile policies**；但在当前摘录里没有给出具体数值比较。
- 对方法层面，作者声称单阶段的**AAC + 在线latent distillation**在仿真评估中与传统两阶段privileged latent distillation性能相近，同时训练更简化；摘录未提供详细数字。

## Link
- [http://arxiv.org/abs/2603.04531v1](http://arxiv.org/abs/2603.04531v1)
