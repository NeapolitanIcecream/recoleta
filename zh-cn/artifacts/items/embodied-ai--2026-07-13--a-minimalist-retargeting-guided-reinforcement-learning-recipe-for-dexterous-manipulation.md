---
source: arxiv
url: https://arxiv.org/abs/2607.11874v1
published_at: '2026-07-13T17:56:08'
authors:
- Yunhai Feng
- Natalie Leung
- Jiaxuan Wang
- Lujie Yang
- Haozhi Qi
- Preston Culbertson
topics:
- dexterous-manipulation
- motion-retargeting
- reinforcement-learning
- sim2real
- tool-use
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# A Minimalist Retargeting-Guided Reinforcement Learning Recipe for Dexterous Manipulation

## Summary
## 摘要
Regrind通过在运动重定向过程中保留手与物体的关系，并在仿真中用残差强化学习优化结果，仅凭一段人类演示学习接触密集型灵巧操作。该方法可零样本迁移到两种机器人手上，完成剪刀和螺丝刀任务；在四种手-任务组合中，仿真成功率均超过98.7%。

## 问题
- 灵巧操作需要精确的手指协调、接触转换、摩擦力和力调节，这使直接重定向人类动作以及仿真到现实的迁移变得困难。
- 仅以手为中心的重定向会忽略机器人手与物体之间的关系，因此可能产生碰撞或不符合物理规律的抓取姿态。
- 收集大量针对特定机器人的灵巧操作数据成本高，而强化学习还面临探索和奖励设计问题。

## 方法
- 使用交互网格重定向人类手部和物体的运动，保留对应手部关键点与物体关键点之间的空间关系和接触关系。
- 在仿真中训练残差强化学习策略，使其跟踪以物体为中心的关键点；重定向轨迹同时作为运动参考和重启状态分布。
- 将物体初始姿态扰动至多±5厘米和±30度，再让轨迹平滑地回到原始目标，以生成多样化的训练轨迹。
- 通过域随机化、观测噪声、推力与重力课程、低噪声执行器观测以及硬件系统辨识来减少迁移误差。

## 结果
- 在LEAP和WUJI手执行剪刀与螺丝刀任务时，Regrind的仿真物体跟踪误差为5.3至6.5毫米，成功率为98.7%至99.8%。
- 评估的四种设置为LEAP-Scissors、LEAP-Screwdriver、WUJI-Scissors和WUJI-Screwdriver；Regrind报告的成功率分别为99.8% ± 0.3%、99.7% ± 0.0%、98.7% ± 1.3%和98.8% ± 1.3%。
- 定性比较显示，Mink IK + RL和DexMachina可能产生手与物体相互穿透或不稳定抓取，而考虑交互关系的重定向能为强化学习初始化提供更可用的接触结构。
- 论文声称该方法可零样本迁移到硬件，并能让两种机器人手流畅地使用工具，但所提供的摘录没有包含硬件成功率表或硬件数值对比。
- 报告中最明确的机制层面结果是：保留交互结构可以改善供后续强化学习使用的重定向参考；该摘录没有给出每个组件的完整消融实验数据。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.11874v1](https://arxiv.org/abs/2607.11874v1)
