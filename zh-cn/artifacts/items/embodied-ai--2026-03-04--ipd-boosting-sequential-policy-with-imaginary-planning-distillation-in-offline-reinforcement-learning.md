---
source: arxiv
url: http://arxiv.org/abs/2603.04289v1
published_at: '2026-03-04T17:05:39'
authors:
- Yihao Qin
- Yuanfei Wang
- Hang Zhou
- Peiran Liu
- Hao Dong
- Yiding Ji
topics:
- offline-rl
- decision-transformer
- world-model
- model-predictive-control
- policy-distillation
relevance_score: 0.28
run_id: materialize-outputs
language_code: zh-CN
---

# IPD: Boosting Sequential Policy with Imaginary Planning Distillation in Offline Reinforcement Learning

## Summary
IPD 是一种面向离线强化学习的框架，用“想象规划”增强 Transformer 顺序策略。它把世界模型、价值函数和 MPC 规划结合起来，先生成更优的虚拟轨迹，再把这些规划知识蒸馏进策略中。

## Problem
- 论文解决的是**离线 RL 中基于 Decision Transformer 的顺序策略难以从次优静态数据中拼接出最优行为**的问题，这会限制策略性能上限。
- 传统 Transformer 式方法更像条件模仿，**缺少显式规划与动态规划机制**，因此对次优数据利用不足。
- 这很重要，因为离线 RL 不能在线试错；若只能依赖固定数据，如何从有限、含噪、次优数据中提炼更优策略，直接决定实际可用性与安全性。

## Approach
- 先从离线数据学习一个**准最优价值函数**和 **Q 函数**，用接近 IQL 的方式降低 OOD 过估计；同时训练带**不确定性估计**的世界模型。
- 用价值函数比较真实轨迹回报与“想象回报”，找出**次优状态/轨迹片段**；对这些片段，用世界模型内的 **MPC** 生成更优的虚拟 rollout。
- 用**集成概率世界模型**刻画 aleatoric + epistemic uncertainty，并用 **GJS divergence** 做模型分歧度量；只保留低不确定性的 imagined 数据，避免模型误差累积。
- 用增强后的数据训练 Transformer 顺序策略，并加入**价值引导目标**，把价值函数/规划得到的偏好蒸馏进动作预测中。
- 推理时不用手工设定 return-to-go，而是用学习到的**准最优价值函数**作为条件信号，提高决策稳定性与效果。

## Results
- 论文声称在 **D4RL benchmark** 上，IPD **显著优于** 多种 SOTA 的**value-based** 与 **transformer-based** 离线 RL 方法。
- 提供了系统的**消融实验**，验证了三类关键组件的作用：**MPC 驱动数据增强**、**价值引导动作模仿**、**return-to-go 预测/替换**。
- 论文还声称分析了**imaginary data augmentation volume** 与性能的关系，并观察到一种**scaling law**。
- 但在当前提供的摘录中，**没有给出具体数值结果**，因此无法明确列出任务名、分数、提升幅度、基线差值等定量指标。最强的具体主张是：IPD 在 D4RL 多任务上取得一致性能提升，并且把规划整合进训练和推理全流程。

## Link
- [http://arxiv.org/abs/2603.04289v1](http://arxiv.org/abs/2603.04289v1)
