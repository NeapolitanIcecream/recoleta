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
## 总结
TriRelVLA 是一个视觉-语言-动作模型，通过显式的物体-手-任务关系来进行动作预测。它的目标是让机器人操作在未见过的场景、物体和任务组合上有更好的迁移能力。

## 问题
- 现有的 VLA 策略会把动作和物体外观、背景纹理、场景布局绑定在一起，这会削弱它们在新视觉条件下的迁移能力。
- 结构化 VLA 方法常常编码物体或场景语义，而论文认为，操作任务需要目标物体、机器人手和任务约束之间的关系。

## 方法
- 它从多视角视觉特征中构建物体 token，从由本体感觉锚定的视觉特征中构建手 token，并构建 4 个任务 token，分别表示动作、角色、约束和阶段。
- 它融合 SigLIP 语义特征和 VGGT 3D 几何特征，形成用于腕部视角和第三人称视角的 3D 视觉潜变量。
- 它构建一个以任务为基础的图，包含物体、手和任务节点，以及 4 种关系类型：任务-物体、任务-手、物体-手、物体-物体。
- 一个感知关系的图 Transformer 将边特征注入注意力，然后一个瓶颈层把增强了关系的信息压缩成 token，再送入 Qwen3-4B LLM 动作头。
- 训练分 3 个阶段，在 OXE、DROID、LIBERO 和新的 CSOT-Bench 数据集上进行，并使用动作损失以及物体和手的注意力掩码损失。

## 结果
- 这段摘要没有给出定量成功率、基准表或消融实验数值。
- 文中声称它在可泛化机器人任务上达到最先进性能，但这段摘要没有给出该结论对应的指标、数据集划分或相对基线差距。
- 文中声称它在 3 种泛化设置上有提升：跨场景、跨物体和跨任务操作。
- CSOT-Bench 被描述为一个真实世界数据集，包含 3 个评估套件：场景推理、物体理解和任务目标。
- 这个模型使用 4 个任务提示 token 和 4 种边关系类型，这是这段摘要里能直接确定的主要机制数量。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05714v1](https://arxiv.org/abs/2605.05714v1)
