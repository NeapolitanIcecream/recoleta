---
source: arxiv
url: https://arxiv.org/abs/2606.06832v1
published_at: '2026-06-05T02:16:50'
authors:
- Abhiroop Ajith
- Constantinos Chamzas
topics:
- visual-task-planning
- symbolic-world-models
- strips-planning
- robot-manipulation
- neuro-symbolic-planning
relevance_score: 0.58
run_id: materialize-outputs
language_code: zh-CN
---

# STRIPS-WM: Learning Grounded Propositional STRIPS-style World Models from Images

## Summary
## 摘要
STRIPS-WM 从 RGB 动作转移中学习一个命题式 STRIPS 世界模型，然后用学到的谓词和算子做从图像到计划的机器人操作。

## 问题
- 它针对长时程视觉操作任务，机器人看到的是图像，但规划依赖离散事实，例如动作是否可用、动作会带来什么变化。
- 训练数据只有当前图像、高层动作 ID 和下一张图像的三元组。不使用物体标签、位姿、掩码、手写谓词或符号目标。
- 之所以重要，是因为只靠预测未来图像来规划，会把容量浪费在和任务成败无关的视觉细节上。

## 方法
- 一个学生-教师视觉动力学模型把图像映射到有限的标量量化代码。唯一代码成为抽象任务图节点，观测到的动作转移成为带标签的图边。
- 一个逆动力学头根据当前和下一步代码预测动作，这会推动代码保留与动作相关的信息。
- 一个 CP-SAT 求解器给图节点分配二元谓词向量，并为每个动作 ID 学习一个有落地的 STRIPS 算子，包含正负前置条件以及 add/delete 效果。
- 从可信图状态中缺失的动作提供前置条件的负证据。松弛变量处理抽象误差和噪声别名。
- 一个视觉谓词分类器把新的起始图像和目标图像映射到学到的谓词向量，然后经典规划器在谓词空间中搜索。

## 结果
- 摘要提到 3 个领域：BlocksWorld、DinnerTable 和 DinnerTable Real。
- BlocksWorld 使用 18 个动作和 5,000 条图像转移。STRIPS-WM 恢复了 16 个学到的图状态，对应 16 个真实状态，使用 9 个谓词，transition slack 为 0，applicability slack 为 0。
- DinnerTable 使用 70 个动作和 12,000 条图像转移。它恢复了 101 个学到的图状态，对应 101 个真实状态，使用 35 个谓词，transition slack 为 0，applicability slack 有 9 个案例。
- DinnerTable Real 使用 64 个动作和 3,000 条图像转移。它学到 111 个图状态，把它们压缩成 71 个学到的谓词状态，对应 71 个真实状态，使用 35 个谓词，transition slack 为 0，applicability slack 有 13 个案例。
- 论文声称它的从图像到计划成功率优于 WM-Rollout、WM-BFS、LSR 和 LatPlan-AMA3，但给出的摘要片段没有包含成功率表或准确数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.06832v1](https://arxiv.org/abs/2606.06832v1)
