---
source: arxiv
url: https://arxiv.org/abs/2607.13429v1
published_at: '2026-07-15T04:13:54'
authors:
- Dwip Dalal
- Shivansh Patel
- Chahit Jain
- Jeonghwan Kim
- Utkarsh Mishra
- Alex Baratian
- Hyeonjeong Ha
- Heng Ji
- Svetlana Lazebnik
- Unnat Jain
topics:
- vision-language-action
- robot-foundation-model
- representation-anchoring
- language-action-alignment
- sim2real
- robot-data-scaling
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Generalizable VLA Finetuning via Representation Anchoring and Language-Action Alignment

## Summary
## 摘要
Anchor-Align 通过保留预训练的视觉-语言表征，并训练语言预测与机器人动作保持一致，改进了 VLA 微调。在仿真环境和实体 xArm7 机器人上，该方法相较于标准行为克隆及多个 VLA 基线，展现出更强的语义、感知和长时域泛化能力。

## 问题
- 行为克隆微调可能覆盖支撑泛化能力的视觉和语义表征，使策略记忆训练场景，而不是对变化后的物体、位置或指令作出响应。
- 在通用图文数据上进行联合训练，并不能直接约束机器人观测上的表征，还可能导致语言预测与动作预测不一致。
- 这一问题很重要，因为标准操作基准可能无法暴露空间重排、语义变化、感知扰动和长时域执行过程中出现的失败。

## 方法
- 视觉-语言锚定保留预训练 VLM 的冻结副本，并在每个解码器层将其视觉和文本隐藏状态蒸馏到可训练的主干网络中。
- 语言-动作对齐将每个示范动作块转换为六种运动方向标签之一——上、下、左、右、前或后，并使用与动作预测相同的机器人观测来预测该标签。
- 该方法联合优化标准行为克隆损失、逐层锚定损失和语言-动作对齐损失，无需额外数据或架构改动。
- 评估涵盖使用回归动作的 VLA-Adapter，以及使用流匹配动作头的 StarVLA，覆盖两种架构和动作生成机制。

## 结果
- 在 LIBERO-PRO 上，Anchor-Align 的平均成功率达到 71.9%，而 VLA-Adapter 为 61.0%；在 LIBERO-Plus 上达到 90.3%，而 VLA-Adapter 为 85.1%。在两个基准的所有报告维度上，该方法均有所提升。
- 在难度较高的 LIBERO-PRO 位置交换测试中，Anchor-Align 得分为 22.6%，而 VLA-Adapter 为 2.3%，MolmoAct、OpenVLA-OFT 以及报告中的联合训练基线均为 0%。
- 在 CALVIN ABC→D 上，完成五条指令的比例从 VLA-Adapter 的 73.1% 提升至 77.9%；平均 rollout 长度从 4.3 个任务增加到 4.5 个任务。
- 根据摘要，在实体 xArm7 实验中，两个受评估的 VLA 架构的成功率分别从 28% 提升至 54%，以及从 37% 提升至 60%。
- 消融实验显示出互补作用：仅使用锚定时，LIBERO-PRO 和 LIBERO-Plus 的得分分别为 68.1% 和 87.3%；仅使用对齐时分别为 65.9% 和 88.6%；完整方法则分别达到 71.9% 和 90.3%。
- 摘录未提供完整的实体机器人任务分项结果或所有统计细节，因此应将这些提升限定在所列出的基准、架构和评估设置内加以理解。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.13429v1](https://arxiv.org/abs/2607.13429v1)
