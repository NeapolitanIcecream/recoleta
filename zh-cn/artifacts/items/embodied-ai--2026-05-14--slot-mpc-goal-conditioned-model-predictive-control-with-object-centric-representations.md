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
Slot-MPC 使用对象级视觉槽位和可微的动作条件动力学模型，规划机器人动作以接近目标图像。主要主张是，在模拟任务中，基于对象中心潜变量的规划比整体式世界模型基线有更高的操作成功率和规划效率。

## 问题
- 它面向视觉目标条件机器人操作，机器人必须根据图像和目标图像选择动作。
- 离线学习的反应式策略在起始状态或对象布局不同于训练数据时可能失败，这会影响长时程操作。
- 基于采样的 MPC 在每个控制步可能需要数百或数千条候选 rollout，这会提高规划成本。

## 方法
- SAVi 风格的场景解析器将每张图像映射为槽位，每个槽位旨在编码一个对象或实体。
- 条件对象中心视频预测器 cOCVP 根据当前槽位和动作序列，自回归地预测未来槽位。
- 测试时，目标图像被编码为目标槽位；MPC 搜索动作，使预测的最终槽位在 L2 代价下接近目标槽位。
- 该方法在计算槽位空间代价前使用匈牙利匹配，使预测槽位和目标槽位按最佳对象对齐进行比较。
- 它测试了 MPPI 采样式 MPC 和基于梯度的 MPC；梯度版本通过可微世界模型进行反向传播，并且可以从用专家演示训练的行为克隆策略开始。

## 结果
- 摘录报告了 4 个模拟操作环境上的实验：Meta-World Button Press 和 Lever Pull，以及 robosuite Stack 和 Square。
- 训练在每个环境中使用 2 类离线数据集：用于场景解析器和动力学模型的随机探索轨迹，以及用于热启动策略的小规模专家集合。
- 论文称，与基于 patch 的 DINO-WM 相比，槽位表示将潜变量维度降低了 99%，从而提高了规划效率。
- 论文称，Slot-MPC 相比非对象中心世界模型基线提高了任务性能和规划效率，其中包括 DINO-WM，并与 GC-BC 和 Dreamer-v3 进行了比较。
- 摘录不包含成功率表或具体任务成功百分比，因此可用的最强数值主张是 4 个环境、2 类数据集、完整 episode 评估协议，以及 99% 的潜变量大小降低。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14937v1](https://arxiv.org/abs/2605.14937v1)
