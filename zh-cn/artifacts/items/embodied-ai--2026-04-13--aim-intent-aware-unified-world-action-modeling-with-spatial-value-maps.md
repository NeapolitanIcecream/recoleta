---
source: arxiv
url: http://arxiv.org/abs/2604.11135v1
published_at: '2026-04-13T07:48:58'
authors:
- Liaoyuan Fan
- Zetian Xu
- Chen Cao
- Wenyao Zhang
- Mingqi Yuan
- Jiayu Chen
topics:
- vision-language-action
- world-model
- robot-manipulation
- spatial-value-map
- generalist-robot-policy
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# AIM: Intent-Aware Unified world action Modeling with Spatial Value Maps

## Summary
## 总结
AIM 是一个面向机器人操作的统一 world-action 模型，它在未来视频预测和动作生成之间加入了显式的空间价值图。论文认为，这样比直接从未来视觉特征里解码动作更可靠。

## 问题
- 现有 world-action 模型可以预测未来视觉场景，但要输出可靠动作，仍然需要大量机器人特定训练。
- 未来 RGB 特征描述的是场景外观和运动，但控制还需要空间意图：机器人应该在哪里作用，以及为什么该区域与任务相关。
- 这个差距在杂乱、长时程和接触敏感的操作任务里最明显，因为与动作相关的线索很稀疏。

## 方法
- AIM 同时预测未来 RGB 帧和对齐的空间价值图，然后基于价值图来预测动作，而不是直接依赖原始未来 RGB 潜表示。
- 价值图是与图像对齐的交互先验。它标出未来场景里与任务相关的区域，并给动作头提供更简单的控制信号。
- 模型采用共享的 mixture-of-transformers 设计，建立在预训练视频模型 Wan2.2-TI2V-5B 上。RGB、价值图和动作流共享 masked self-attention，但保留各自的前馈层。
- intent-causal attention mask 阻止动作分支直接读取未来 RGB token。未来信息只能通过预测出的价值图 token 进入动作分支。
- 在监督式预训练之后，self-distillation RL 阶段冻结视频分支和价值图分支，只用 GRPO 更新动作头，并结合稀疏任务奖励和来自投影价值图响应的密集奖励。

## 结果
- 论文构建了一个包含 **30K 条操作轨迹** 的仿真数据集，带有同步的多视角观测、动作和价值图标注。
- 在 **RoboTwin 2.0** 基准上，AIM 报告的 **Easy** 平均成功率为 **94.0%**，**Hard** 为 **92.1%**。
- 摘要称 AIM 显著优于先前的统一 world-action 基线，在长时程和接触敏感任务上的提升更大。
- 在给出的表格里，AIM 经常与强基线和仅监督学习的消融版本（**Stage1**）持平或更好。例子包括：**Move Can Pot** 达到 **100% / 98%**，Stage1 为 **99% / 97%**；**Pick Diverse Bottles** 达到 **100% / 98%**，Stage1 为 **99% / 97%**；**Scan Object** 达到 **100% / 98%**，Stage1 为 **98% / 97%**。
- 一些任务上，AIM 接近满分，包括 **Open Laptop 100% / 100%**、**Place Bread Skillet 100% / 100%**、**Place Object Stand 100% / 100%** 和 **Rotate QRcode 100% / 98%**。
- 也有一些任务仍然较弱，说明这个方法还不能解决所有操作场景。表格中的例子包括 **Hanging Mug 43% / 42%**、**Blocks Ranking Size 47% / 43%** 和 **Place Phone Stand 82% / 80%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11135v1](http://arxiv.org/abs/2604.11135v1)
