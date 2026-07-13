---
source: arxiv
url: https://arxiv.org/abs/2607.09190v1
published_at: '2026-07-10T08:32:19'
authors:
- Suting Ni
- Hanbing Zhang
- Zhenyu Wei
- Guo Chen
- Chixuan Zhang
- Ye Shi
- Jingya Wang
topics:
- dexterous-manipulation
- tactile-sensing
- robot-data-scaling
- sim2real
- human-to-robot-transfer
- robot-foundation-model
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# TactiDex: A Real-World Tactile-Guided Benchmark for Human-Like Dexterous Manipulation

## Summary
## 摘要
TactiDex 是一个面向真实世界的基准，用触觉监督将人类灵巧操作迁移到机器人上，减少对运动轨迹的单独依赖。TactiSkill 使用同步采集的人手压力数据训练机器人手部，使其更接近人类的接触形成方式和力度调节方式。

## 问题
- 人到机器人的灵巧操作迁移通常只匹配手部和物体的运动，忽略接触时序、力的分布和抓取稳定性。
- 现有手物交互数据集很少同时包含真实触觉测量、精确的手部运动和物体运动数据，限制了具有物理依据的策略学习。
- 这一缺口会影响接触密集型任务：仅匹配轨迹可能导致抓取不稳定、施力过大，或产生不符合物理规律的交互。

## 方法
- TactiDex 在同步的真实世界演示中记录整手压力图、灵巧手运动学数据、腕部和物体的 6D 位姿、任务阶段以及文本描述。
- 数据集包含 757 段单手和双手序列，共 510 万帧数据，涉及 49 个经过标定的物体和 10 名受试者。
- TactiSkill 以冻结的运动学模仿策略为起点，学习一个残差策略，通过调整关节指令来调节接触力。
- 其触觉奖励结合了接触事件引导、人类手指受力模式对齐，以及对超过人类数据推导安全上限的力进行惩罚。
- 非对称 Actor-Critic 设置在训练期间向 critic 提供模拟接触力，actor 则使用部署时可获得的人类触觉参考；生成的策略通过 sim-to-real 迁移进行测试。

## 结果
- 该基准通过 162 个压力元件提供整手触觉感知，力分辨率最高可达 0.01 N，采样率为 17 Hz，并与 120 Hz 的运动和位姿数据流同步。
- TactiDex 将真实世界触觉数据、高精度运动学数据、文本标注和长时域双手操作结合起来；对比表列出的数据集规模为 510 万帧、49 个物体和 757 段序列。
- 论文声称，在单手和双手任务中，与仅使用运动学的迁移方法相比，TactiDex 在操作成功率、接触保真度、物理真实性、几何鲁棒性和交互稳定性方面表现更好。
- 提供的摘录没有实验表中的数值成功率、指标数值、数据集划分或基线比较，因此不足以支持量化的性能提升结论。
- 作者报告了在灵巧操作机器人硬件上的真实世界部署，包括接触密集型操作中的稳定接触和零样本 sim-to-real 迁移，但摘录没有给出硬件操作的数值成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.09190v1](https://arxiv.org/abs/2607.09190v1)
