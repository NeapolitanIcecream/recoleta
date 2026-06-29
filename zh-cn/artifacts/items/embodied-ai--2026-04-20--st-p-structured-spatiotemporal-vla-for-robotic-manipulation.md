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
## 总结
ST-$\pi$ 是一个用于机器人操作的视觉-语言-动作模型，它把明确的时空结构加入任务规划和动作生成中。它面向长时程、多阶段操作，这类任务里标准 VLA 模型常会漂移，或者丢失子任务边界。

## 问题
- 现有 VLA 和 4D-VLA 系统通常从融合后的观测中以隐式方式预测动作，这让长序列子任务很难清晰分开，也难以稳定执行。
- 精细操作同时需要两件事：规划层面要有明确的子任务边界，子任务内部又要有稳定的逐步控制。
- 这对装配和家务任务很重要，因为错误会在各阶段之间累积，后续动作又依赖前面动作在正确的位置和顺序完成。

## 方法
- 这个模型有两部分：**ST-VLM** 用于 chunk 级规划，**ST-AE** 用于 step 级控制。
- ST-VLM 从图像序列、几何特征和时间戳构建 4D 表示，然后预测一串 chunk 级动作提示。每个提示都包含一个语义意图、一个空间目标和一个子任务的时间持续时间。
- 规划模块在这些提示之间使用因果注意力，让后续子任务依赖前面的子任务，从而把长任务拆成一个明确的有序分解。
- ST-AE 一次接收一个 chunk 级提示，并用两个生成器产生低层动作步骤：一个空间生成器负责轨迹形状，一个时间生成器负责步骤顺序和一致性。
- 动作生成使用 flow matching，并通过随时间变化的融合，在去噪早期更偏向空间形状，后期更偏向时间细化。

## 结果
- 论文引入了 **STAR**，这是一个在 Franka Research 3 机器人上的真实世界数据集，包含 **30 个操作任务**、**每个任务 50 次示范**，以及大约 **30 万步交互**。它包含子任务描述、目标位置和执行时长。
- 在给出的基准表中，**4D-VLA** 是列出的最强基线，平均成功率为 **88.6%**。ST-$\pi$ 声称相较于之前的 VLA 基线有稳定提升，但提供的摘要片段 **没有** 给出完整的 ST-$\pi$ 结果行，所以这里看不到它的准确平均提升。
- 可见的基线数字说明长时程设置为什么难：**OpenVLA** 在 Long 套件上的成功率是 **53.7%**，**Octo** 是 **51.1%**，**SpatialVLA** 是 **55.5%**，**TraceVLA** 是 **54.1%**，而 **4D-VLA** 达到 **79.1%**。
- 摘要片段还报告了若干基线的完成时间。平均完成时间方面，**OpenVLA** 是 **8.0s**，**Octo** 是 **7.0s**，**SpatialVLA** 是 **6.6s**。提供的文本里没有显示 ST-$\pi$ 的完成时间数字。
- 这个方法的明确结论是：它把 chunk 级的显式子任务规划和双生成器的 step 级动作细化结合起来，而不是只依赖隐式时空表示，从而提升了长时程操作能力。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17880v1](http://arxiv.org/abs/2604.17880v1)
