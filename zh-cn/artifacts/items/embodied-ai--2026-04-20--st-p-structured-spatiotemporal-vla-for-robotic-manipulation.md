---
source: arxiv
url: http://arxiv.org/abs/2604.17880v1
published_at: '2026-04-20T06:48:47'
authors:
- Chuanhao Ma
- Hanyu Zhou
- Shihan Peng
- Yan Li
- Tao Gu
- Luxin Yan
topics:
- vision-language-action
- robotic-manipulation
- spatiotemporal-reasoning
- long-horizon-control
- hierarchical-policy
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# ST-$π$: Structured SpatioTemporal VLA for Robotic Manipulation

## Summary
## 摘要
ST-$\pi$ 是一个用于机器人操作的视觉-语言-动作模型，在任务规划和动作生成两层都加入了显式的时空结构。它面向长时程、多阶段操作任务，这类任务中标准 VLA 模型常会逐渐偏离目标，或丢失对子任务边界的跟踪。

## 问题
- 现有 VLA 和 4D-VLA 系统通常以隐式方式从融合后的观测中预测动作，这使得长序列子任务难以清晰划分，也难以稳定执行。
- 细粒度操作同时需要两点：规划层面的显式子任务边界，以及每个子任务内部稳定的逐步控制。
- 这对装配和家务任务很重要，因为错误会在多个阶段中累积，后续动作还依赖前面的动作在正确的位置、按正确的顺序完成。

## 方法
- 模型分为两部分：用于 chunk 级规划的 **ST-VLM**，以及用于 step 级控制的 **ST-AE**。
- ST-VLM 从图像序列、几何特征和时间戳构建 4D 表征，然后预测一系列 chunk 级动作提示。每个提示包含一个子任务的语义意图、空间目标和时间长度。
- 规划模块在这些提示之间使用因果注意力，因此后续子任务会依赖前面的子任务，从而对长任务进行显式且有序的分解。
- ST-AE 每次接收一个 chunk 级提示，并通过两个生成器生成底层动作步骤：空间生成器负责轨迹形状，时间生成器负责步骤顺序和一致性。
- 动作生成使用 flow matching，并采用随时间变化的融合方式：在去噪早期更侧重空间引导，后期再加强时间上的细化。

## 结果
- 论文提出了 **STAR**，这是一个基于 Franka Research 3 机器人的真实世界数据集，包含 **30 个操作任务**、每个任务 **50 条演示**，以及约 **30 万个交互步骤**。数据集包含子任务描述、目标位置和执行时长。
- 在展示的基准表中，**4D-VLA** 是列出的最强基线，**平均成功率为 88.6%**。ST-$\pi$ 声称相较以往 VLA 基线有持续提升，但给出的摘录**没有**包含完整的 ST-$\pi$ 结果行，因此这里看不到其确切的平均提升幅度。
- 已展示的基线数字说明了长时程设置的难度：**OpenVLA** 在 Long 套件上的成功率为 **53.7%**，**Octo** 为 **51.1%**，**SpatialVLA** 为 **55.5%**，**TraceVLA** 为 **54.1%**，而 **4D-VLA** 达到 **79.1%**。
- 摘录还报告了部分基线的完成时间。平均完成时间方面，**OpenVLA** 为 **8.0s**，**Octo** 为 **7.0s**，**SpatialVLA** 为 **6.6s**。给出的文本中看不到 ST-$\pi$ 的完成时间数据。
- 一个明确的结论是：该方法通过结合显式的 chunk 级子任务规划和双生成器的 step 级动作细化，提高了长时程操作表现，而不是只依赖隐式的时空表征。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17880v1](http://arxiv.org/abs/2604.17880v1)
