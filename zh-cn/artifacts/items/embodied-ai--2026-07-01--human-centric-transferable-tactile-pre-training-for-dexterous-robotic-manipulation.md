---
source: arxiv
url: https://arxiv.org/abs/2607.01067v1
published_at: '2026-07-01T15:26:26'
authors:
- Chi Zhang
- Penglin Cai
- Ziheng Xi
- Haoqi Yuan
- Hao Luo
- Wanpeng Zhang
- Sipeng Zheng
- Chaoyi Xu
- Zongqing Lu
topics:
- vision-language-action
- dexterous-manipulation
- tactile-pretraining
- human-to-robot-transfer
- robot-data-scaling
- cross-embodiment
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Human-Centric Transferable Tactile Pre-Training for Dexterous Robotic Manipulation

## Summary
## 摘要
TTP 先在大规模人类触觉-动作数据上预训练视觉-语言-动作机器人策略，再将其适配到灵巧机器人操作。摘录中的主要具体贡献是 H-Tac：一个 160 小时的数据集，包含触觉、动作、视觉和语言信号。

## 问题
- 富接触操作需要触觉反馈，因为视觉可能漏掉力、滑移、遮挡和细小接触变化。
- 机器人触觉数据集规模小，因为不同机械手的触觉硬件不同，而面向灵巧接触任务的遥操作采集成本高。
- 现有触觉 VLA 工作通常在后训练阶段加入触觉，这限制了模型在机器人任务训练前学习接触动力学的程度。

## 方法
- 作者收集了 H-Tac：160 小时的第一视角人类及机器人相关触觉-动作数据，覆盖 300+ 个任务和 135k+ 个片段。
- TTP 使用 BeingH-0.5 作为基础 VLA 模型，并加入一个触觉专家来预测未来触觉读数，同时用一个动作专家预测未来动作块。
- 人类和机器人数据共享 200 维动作空间和 351-taxel UniTacHand 触觉空间，因此预训练和后训练使用相同的目标格式。
- 训练对动作和未来触觉都使用流匹配，并使用动作预测和触觉预测损失。
- 一个保持流形的门控机制使用切片 Wasserstein 距离，将观测特征与动作锚点和触觉锚点进行比较；当特征看起来不可靠时，它会减少上下文更新。

## 结果
- H-Tac 总计 160 小时、300+ 个任务和 135k+ 个片段。
- HOI-Tac 来自公开的手-物体、手-脸和手-场景数据集，贡献约 11.5M 帧、约 106 小时和 124.8K 个序列。
- DeskTask-Tac 来自真实桌面双手任务，贡献 37.2 小时的 30 Hz 数据、947 个片段和约 4M 帧。
- InternData-Tac 覆盖 Genie1、Lift2 和 Split ALOHA 机器人配置，贡献 17.8 小时的 30 Hz 数据、9,563 个片段和约 1.9M 帧。
- 摘录称该方法在仿真和真实机器人触觉任务中表现更好，并支持跨本体迁移，但没有给出下游成功率、指标表或具名基线数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.01067v1](https://arxiv.org/abs/2607.01067v1)
