---
source: arxiv
url: http://arxiv.org/abs/2603.10451v1
published_at: '2026-03-11T06:10:03'
authors:
- Yushan Bai
- Fulin Chen
- Hongzheng Sun
- Yuchuang Tong
- En Li
- Zhengtao Zhang
topics:
- dexterous-manipulation
- imitation-learning
- sim2real
- residual-policy
- data-augmentation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# FAR-Dex: Few-shot Data Augmentation and Adaptive Residual Policy Refinement for Dexterous Manipulation

## Summary
FAR-Dex针对灵巧操作中“示教太少、控制太难、真实部署不稳”三个核心瓶颈，提出了一个由少样本数据扩增和自适应残差控制组成的分层框架。它面向机械臂与多指手协同控制，在仿真与真实世界都报告了较强的成功率与实时性。

## Problem
- 该工作要解决的是**少量人类示教下的机械臂-灵巧手协同操作**问题；这很重要，因为高质量灵巧操作示教稀缺，而真实任务需要精细接触与长时序稳定控制。
- 现有数据生成方法往往缺少细粒度手-物体交互细节，导致**sim-to-real迁移差**，而现有残差策略又缺少明确的时空建模，难以在长时程任务中稳定纠错。
- 机械臂与多指手联合控制的动作空间维度高，若不能同时提升**数据质量**与**在线修正能力**，就很难实现可靠的真实世界灵巧操作。

## Approach
- FAR-Dex包含两部分：**FAR-DexGen**先把极少量示教分解成“运动段”和“技能段”，再在IsaacLab中通过改变物体初始位姿、结合运动规划与逆运动学，生成大量物理可行的新轨迹。
- 方法的核心思想可以简单理解为：**手的精细接触动作尽量保留原示教，机械臂轨迹随物体位置变化而重算**，这样既扩充了数据，又保住了接触细节。
- 训练阶段把真实示教与仿真生成数据合并，用DP3式基础策略学习动作；同时用**consistency model蒸馏**把原本多步采样的扩散/去噪推理压缩成单步推理，以降低时延。
- 在线执行时，**FAR-DexRes**再学习一个残差策略：利用多步轨迹片段与当前观测，通过交叉注意力生成逐维权重 \(\sigma_t\)，对基础动作做“该修多少就修多少”的自适应校正。
- 残差策略通过PPO暖启动训练，目标是在保持基础策略平滑性的同时，针对接触阶段和分布外状态进行更精细的误差补偿。

## Results
- 数据生成方面，在Insert Cylinder任务上，**FAR-DexGen**的轨迹生成时间为 **10.3 ms/trajectory**，相比 **MimicGen 8.3 ms**、**DemoGen 9.1 ms** 略慢，但仍接近同量级。
- 数据质量方面，按“用生成数据训练统一DP3后得到的成功率”作为代理指标，FAR-DexGen达到 **87.9%**，高于 **MimicGen 68.3%** 和 **DemoGen 74.5%**；分别提升 **19.6%** 和 **13.4%**。
- 仿真任务成功率方面，**FAR-DexRes**在四个任务上分别达到：**Insert Cylinder 93%**、**Pinch Pen 83%**、**Grasp Handle 88%**、**Move Card 95%**。
- 与最强对比方法之一 **ResiP** 相比，FAR-DexRes在四个任务上的成功率分别从 **85%→93%**、**79%→83%**、**80%→88%**、**87%→95%**，平均约提升 **7 个百分点**，与摘要中的主张一致。
- 与纯模仿学习基线相比，FAR-DexRes也显著更强，例如相对 **DP3**：**83%→93%**、**77%→83%**、**80%→88%**、**53%→95%**；其中Move Card提升最明显，为 **+42 个百分点**。
- 推理时延方面，FAR-DexRes每步仅 **3.0/4.3/3.8/4.3 ms**，显著低于 **DP3 的 29.1/31.5/29.8/29.6 ms** 与 **ResiP 的 29.3/32.5/31.9/30.2 ms**。摘要还声称真实世界任务成功率**超过80%**，但摘录中未给出更细的逐任务真实实验数字。

## Link
- [http://arxiv.org/abs/2603.10451v1](http://arxiv.org/abs/2603.10451v1)
