---
source: arxiv
url: https://arxiv.org/abs/2605.14937v1
published_at: '2026-05-14T15:12:15'
authors:
- Jonathan Spieler
- Angel Villar-Corrales
- Sven Behnke
topics:
- object-centric-world-model
- model-predictive-control
- robot-manipulation
- visual-planning
- offline-robot-data
- goal-conditioned-control
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Slot-MPC: Goal-Conditioned Model Predictive Control with Object-Centric Representations

## Summary
## 摘要
Slot-MPC 使用基于对象的视觉 slot 和可微的动作条件动力学模型，围绕目标图像规划机器人动作。核心结论是，在模拟任务中，基于对象的潜变量规划比整体式世界模型基线更能提高操作成功率和规划效率。

## 问题
- 它面向视觉目标条件下的机器人操作，机器人需要根据图像和目标图像选择动作。
- 离线学到的反应式策略在起始状态或物体布局与训练数据不同时容易失效，这对长时程操作很重要。
- 基于采样的 MPC 在每个控制步可能需要数百到数千个候选 rollout，这会增加规划成本。

## 方法
- 一个 SAVi 风格的场景解析器把每张图像映射为多个 slot，每个 slot 设计上编码一个物体或实体。
- 一个条件式对象中心视频预测器 cOCVP 根据当前 slots 和动作序列，自回归地预测未来 slots。
- 测试时，将目标图像编码为目标 slots；MPC 通过 L2 代价搜索让预测的最终 slots 接近目标 slots 的动作。
- 该方法在 slot 空间代价之前使用 Hungarian matching，使预测 slots 和目标 slots 按最佳对象对齐进行比较。
- 它同时测试了基于采样的 MPPI-MPC 和基于梯度的 MPC；梯度版本通过可微世界模型反向传播，并且可以从用专家示范训练的行为克隆策略开始。

## 结果
- 摘要段报告了 4 个模拟操作环境上的实验：Meta-World 的 Button Press 和 Lever Pull，以及 robosuite 的 Stack 和 Square。
- 每个环境使用 2 类离线数据集进行训练：用于场景解析器和动力学模型的随机探索轨迹，以及用于热启动策略的小规模专家集。
- 论文声称，与基于 patch 的 DINO-WM 相比，slot 表示将潜变量维度降低了 99%，从而提高了规划效率。
- 论文声称，Slot-MPC 在任务表现和规划效率上都优于非对象中心的世界模型基线，包括 DINO-WM，并与 GC-BC 和 Dreamer-v3 进行了比较。
- 摘要未给出成功率表或具体任务成功百分比，因此目前能直接确认的最强数值结论是 4 个环境、2 类数据集、全回合评估流程，以及 99% 的潜变量规模缩减。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14937v1](https://arxiv.org/abs/2605.14937v1)
