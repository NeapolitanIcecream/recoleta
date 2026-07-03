---
source: arxiv
url: https://arxiv.org/abs/2607.01212v1
published_at: '2026-07-01T17:51:21'
authors:
- Chenyang Ma
- Yue Yang
- Radu Corcodel
- Siddarth Jain
- Andrew Wu
- Chiori Hori
- Diego Romeres
topics:
- vision-language-action
- bimanual-manipulation
- robot-furniture-assembly
- long-horizon-control
- robot-data-scaling
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# FurnitureVLA: Learning Long-Horizon Bimanual Furniture Assembly with Vision-Language-Action Model

## Summary
## 摘要
FurnitureVLA 训练一种视觉-语言-动作策略，用于真实尺寸的双臂家具组装，并用子任务进度预测处理长时程任务。它在三个宜家风格家具任务中，将平均模拟组装成功率从整体式微调 VLA 的 48% 提高到 80%。

## 问题
- 机器人家具组装需要长序列的精确动作；本文测试的任务包含 4 到 7 个子任务、650 到 1550 个控制步，并采用严格的部件对齐阈值：小部件 1 cm，大部件 2 cm，每个旋转轴约 4 度。
- 以往工作主要覆盖玩具尺度或单臂组装，因此没有处理需要双臂协调、可达性检查和遮挡处理的大型部件。
- 整体式 VLA 在长 rollout 中可能漂移：小的动作误差会把机器人带到训练中少见或没有出现过的状态，导致后续子任务失败。

## 方法
- 系统将每个组装过程分解为由语言条件控制的子任务，例如抓取、对齐、插入、抬起、旋转和撤离。
- VLA 为两台 Kinova Gen3 机械臂预测一个 14 维双臂动作，外加一个标量进度值，因此每一步输出 15 维。
- 进度在每个子任务内从 0 连续变化到 1，并通过动作原语赋值；推理时，进度阈值触发切换到下一个子任务。
- 子任务边界设置在机械臂脱离接触之后，因此下一个子任务从比富接触插入状态更稳定的状态开始。
- 论文还构建了一个 Isaac Gym 仿真流水线，用于专家演示和评估，并构建了一个 VR 遥操作系统，让一名操作员采集双臂真实机器人演示。

## 结果
- 在仿真中，zero-shot π0.5 在 LACK、KALLAX 和 IVAR 上的成功率为 0.00；整体式微调分别达到 0.91、0.11 和 0.41；FurnitureVLA 分别达到 0.98、0.85 和 0.56。
- 平均模拟完整组装成功率从整体式微调的 0.48 提高到 FurnitureVLA 的 0.80，在三类家具上提升 32 个百分点。
- 设计因素研究报告的最佳设置平均成功率为 0.80；较弱设置包括：不使用后置相机设置时为 0.50，使用前视深度替换时为 0.47，输入分辨率为 224×224 时为 0.60。
- 在报告的扫描实验中，λ = -0.1 的时间集成取得最佳平均成功率 0.80；不使用集成时为 0.65，λ = -0.25 时为 0.75。
- 数据规模扩大能提高成功率：使用 25% 演示时平均成功率为 0.50，使用 50% 时为 0.68，使用 100% 时为 0.80。
- 离散进度消融在三个模拟家具任务上都失败，成功率为 0.00；真实机器人 IVAR 验证相对最难仿真任务只下降 16 个百分点，如果与 0.56 的模拟 IVAR 结果比较，对应约 0.40 的真实成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01212v1](https://arxiv.org/abs/2607.01212v1)
