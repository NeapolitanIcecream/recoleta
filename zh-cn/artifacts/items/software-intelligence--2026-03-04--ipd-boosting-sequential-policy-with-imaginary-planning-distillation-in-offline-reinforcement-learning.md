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
- offline-reinforcement-learning
- decision-transformer
- model-predictive-control
- world-model
- policy-distillation
relevance_score: 0.24
run_id: materialize-outputs
language_code: zh-CN
---

# IPD: Boosting Sequential Policy with Imaginary Planning Distillation in Offline Reinforcement Learning

## Summary
IPD是一种离线强化学习方法，目标是让Transformer式序列策略不再只会模仿离线数据，而是能从“想象中的规划”里学到更优决策。它把世界模型、价值函数和MPC生成的高质量虚拟轨迹蒸馏进策略训练与推理流程中。

## Problem
- 现有Decision Transformer类离线RL方法主要做条件模仿，**难以把多个次优片段“拼接”成更优策略**。
- 纯离线数据常含大量次优轨迹，且分布外动作会导致**价值高估与不稳定决策**。
- 这很重要，因为现实场景里在线探索代价高、风险大，离线RL若不能从静态数据中提炼更优行为，实际部署价值会受限。

## Approach
- 先用离线数据学习一个**带不确定性估计的世界模型**，以及一个基于IQL风格训练的**准最优价值函数/Q函数**，减少分布外高估。
- 用价值函数比较真实轨迹回报与“想象轨迹”回报，找出**最值得改写的次优状态/片段**。
- 对这些片段，利用**MPC在学习到的世界模型中做规划**，生成更优的虚拟rollout；再用不确定性阈值过滤，只保留可靠样本加入增强数据集。
- 训练Transformer策略时，不只拟合增强后的序列，还加入**价值引导目标**，把动态规划与MPC的知识蒸馏进策略。
- 推理时，用学习到的**准最优价值函数替代手工设定的return-to-go**作为条件信号，以提升稳定性和性能。

## Results
- 论文声称在**D4RL benchmark**上，IPD“显著优于”多种**SOTA value-based和transformer-based offline RL**方法。
- 摘要与引言明确给出的是**定性结论**：在多样任务上取得一致提升，并通过消融验证了MPC数据增强、价值引导动作模仿、return-to-go预测等模块的贡献。
- 论文还声称分析了**imaginary data augmentation volume**与性能之间的**scaling law**关系。
- **当前提供的摘录没有具体数值结果**，因此无法列出精确的分数、提升百分比、对应基线或任务级别对比数字。

## Link
- [http://arxiv.org/abs/2603.04289v1](http://arxiv.org/abs/2603.04289v1)
