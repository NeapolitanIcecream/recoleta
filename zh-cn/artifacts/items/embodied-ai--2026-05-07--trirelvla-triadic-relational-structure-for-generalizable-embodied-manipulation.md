---
source: arxiv
url: https://arxiv.org/abs/2605.05714v1
published_at: '2026-05-07T05:57:49'
authors:
- Hanyu Zhou
- Chuanhao Ma
- Gim Hee Lee
topics:
- vision-language-action
- robot-manipulation
- relational-reasoning
- generalist-robot-policy
- robot-data-scaling
- sim2real
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# TriRelVLA: Triadic Relational Structure for Generalizable Embodied Manipulation

## Summary
## 摘要
TriRelVLA 是一种视觉-语言-动作模型，通过显式的物体-手-任务关系来进行动作预测。它的目标是让机器人操作更好地迁移到未见过的场景、物体和任务组合。

## 问题
- 现有 VLA 策略可能会把动作绑定到物体外观、背景纹理和场景布局上，导致它们难以迁移到新的视觉条件。
- 结构化 VLA 方法通常编码物体或场景语义，而该论文认为，操作任务需要目标物体、机器人手部和任务约束之间的关系。

## 方法
- 它从多视角视觉特征构建物体 token，从由本体感知锚定的视觉特征构建手部 token，并构建 4 个任务 token，分别对应动作、角色、约束和阶段。
- 它将 SigLIP 语义特征与 VGGT 3D 几何特征融合，为腕部视角和第三人称视角形成 3D 视觉隐变量。
- 它构建一个以任务为基础的图，包含物体、手部和任务节点，以及 4 种关系类型：任务-物体、任务-手部、物体-手部和物体-物体。
- 一个关系感知图 transformer 将边特征注入注意力，然后由瓶颈层把关系增强后的节点压缩成 token，并传递给 Qwen3-4B LLM 动作头。
- 训练分为 3 个阶段，使用 OXE、DROID、LIBERO 和新的 CSOT-Bench 数据集，损失包括动作损失以及物体和手部注意力掩码损失。

## 结果
- 给定摘录没有包含定量成功率、基准表或消融实验数字。
- 它声称在可泛化机器人任务上达到最先进性能，但摘录没有给出该说法对应的指标、数据集划分或相对基线的差距。
- 它声称在 3 种泛化设置中取得提升：跨场景、跨物体和跨任务操作。
- CSOT-Bench 被介绍为一个真实世界数据集，包含 3 个评估套件：场景推理、物体理解和任务目标。
- 该模型使用 4 个任务提示 token 和 4 种边关系类型，这是摘录中可见的主要具体机制数量。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05714v1](https://arxiv.org/abs/2605.05714v1)
