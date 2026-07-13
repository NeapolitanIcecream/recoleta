---
source: arxiv
url: https://arxiv.org/abs/2607.09648v1
published_at: '2026-07-10T17:46:32'
authors:
- Xiaoshen Han
- Haoyu Xiong
- Haonan Chen
- Chaoqi Liu
- Antonio Torralba
- Yuke Zhu
- Yilun Du
topics:
- robot-policy
- fast-manipulation
- action-representation
- trajectory-smoothing
- imitation-learning
- temporal-rescaling
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# B-spline Policy: Accelerating Manipulation Policies via B-spline Action Representations

## Summary
## 摘要
B-spline Policy 用连续的 B 样条动作曲线替代固定的离散动作块。控制器可以高频采样这些曲线，并以不同速度执行。真实机器人测试显示，任务完成时间缩短，同时成功率相当或更高；速度提升过大时，可能超出控制器的跟踪能力。

## 问题
- 视觉运动策略完成操作任务的速度通常远低于人类。论文引用的数据显示，机器人折叠 T 恤约需 60 秒，人类约需 10 秒。
- 固定长度的动作块在整个任务中使用相同的时间分辨率，连续动作块连接时还可能产生不连续。
- 执行速度较高时，稀疏或不连续的指令更容易造成跟踪误差和任务失败。

## 方法
- 对示范轨迹拟合三次 B 样条，在曲率较高的区域放置更多节点，在平滑区域放置更少节点。
- 训练标准模仿学习策略预测局部样条参数，包括控制点和节点，替代离散动作序列。
- 在较高的底层控制频率下采样每条连续曲线，并通过时间重缩放改变执行速度，无需针对每种速度重新训练策略。
- 通过寻找新曲线上与上一段已执行动作差异最小的点，使每个新预测的样条片段与上一段动作对齐。
- 将该表示接入 Diffusion Policy 和 ACT 风格的回归策略，替代标准动作分块机制。

## 结果
- 在真实世界的 Cube Picking 任务中，Diffusion+BSP 在 4X 速度下以 2.45 秒完成任务，成功率为 20/20；4X Diffusion 基线以 3.52 秒完成任务，成功率同为 20/20。Regression+BSP 在 4X 速度下以 2.08 秒完成任务，成功率为 19/20；基线以 3.74 秒完成任务，成功率同为 19/20。
- 在长时序的 Table Cleaning 任务中，Regression+BSP 在 4X 速度下将平均完成时间从 23.57 秒降至 11.80 秒，减少 50%；成功次数从 13/20 变为 14/20。
- 在 Speed Stacking 任务中，Regression+BSP 在 1X 速度下将成功次数从 8/20 提高到 16/20，在 2X 速度下从 4/20 提高到 13/20；对应完成时间分别为 17.61 秒和 10.98 秒。
- 在扩散策略和回归策略的对比中，BSP 在 18 个设置中的 14 个设置里保持或提高了成功率，并且通常缩短了完成时间。
- 速度提升过大时，性能可能崩溃：Regression+BSP 在 Speed Stacking 任务的 4X 速度下取得 0/20。论文将其归因于底层控制器的跟踪能力限制。
- 在 Push-T、RoboMimic 和 RoboCasa 的仿真结果中，报告任务的成功率相当或更高。例如，Diffusion+BSP 将 Turn off microwave 的成功率从 77% 提高到 89%，将 Close door 的成功率从 27% 提高到 46%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.09648v1](https://arxiv.org/abs/2607.09648v1)
