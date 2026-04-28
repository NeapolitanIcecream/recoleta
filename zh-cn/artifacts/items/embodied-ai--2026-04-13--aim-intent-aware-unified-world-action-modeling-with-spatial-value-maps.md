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
## 摘要
AIM 是一个面向机器人操作的统一世界-动作模型，它在未来视频预测和动作生成之间加入了显式空间价值图。论文称，这比直接从未来视觉特征中读取动作更可靠。

## 问题
- 现有世界-动作模型可以预测未来视觉场景，但要产生可靠动作，仍需要大量针对特定机器人的训练。
- 未来 RGB 特征描述的是场景外观和运动，但控制还需要空间意图：机器人应该在哪里动作，以及该区域为什么与任务相关。
- 这个缺口在杂乱场景、长时程任务和接触敏感的操作中最明显，因为与动作相关的线索很稀疏。

## 方法
- AIM 同时预测未来 RGB 帧和对齐的空间价值图，然后基于价值图而不是原始未来 RGB 潜变量来预测动作。
- 价值图是与图像对齐的交互先验。它标出未来场景中与任务相关的区域，并给动作头提供更简单的控制信号。
- 该模型采用共享的 mixture-of-transformers 设计，建立在预训练视频模型 Wan2.2-TI2V-5B 之上。RGB、价值图和动作流共享 masked self-attention，但各自保留独立的前馈层。
- intent-causal attention mask 阻止动作分支直接读取未来 RGB token。未来信息通过预测出的价值图 token 传到动作分支。
- 在监督预训练之后，自蒸馏 RL 阶段会冻结视频分支和价值图分支，只用 GRPO 更新动作头，奖励由稀疏任务奖励和来自投影价值图响应的稠密奖励组成。

## 结果
- 论文构建了一个仿真数据集，包含 **30K manipulation trajectories**，其中有同步的多视角观测、动作和价值图标注。
- 在 **RoboTwin 2.0** 基准上，AIM 报告 **94.0% average success**（**Easy**）和 **92.1%**（**Hard**）。
- 摘要称，AIM 明显优于此前的统一世界-动作基线，在长时程任务和接触敏感任务上的提升更大。
- 在给出的表格中，AIM 经常达到或超过强基线以及仅监督训练的消融版本（**Stage1**）。例如：**Move Can Pot** 达到 **100% / 98%**，而 Stage1 为 **99% / 97%**；**Pick Diverse Bottles** 达到 **100% / 98%**，而 Stage1 为 **99% / 97%**；**Scan Object** 达到 **100% / 98%**，而 Stage1 为 **98% / 97%**。
- AIM 在一些任务上接近满分，包括 **Open Laptop 100% / 100%**、**Place Bread Skillet 100% / 100%**、**Place Object Stand 100% / 100%** 和 **Rotate QRcode 100% / 98%**。
- 一些任务的表现仍然较弱，这说明该方法没有解决所有操作场景。表中的例子包括 **Hanging Mug 43% / 42%**、**Blocks Ranking Size 47% / 43%** 和 **Place Phone Stand 82% / 80%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11135v1](http://arxiv.org/abs/2604.11135v1)
