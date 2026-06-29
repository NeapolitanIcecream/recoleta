---
source: arxiv
url: https://arxiv.org/abs/2606.18043v1
published_at: '2026-06-16T15:19:09'
authors:
- "Ralf R\xF6mer"
- Maximilian Seeliger
- Saida Liu
- Ben Sturgis
- Marco Bagatella
- Daniel Marta
- Andreas Krause
- Angela P. Schoellig
topics:
- vision-language-action
- uncertainty-quantification
- flow-matching
- active-fine-tuning
- robot-data-scaling
- failure-detection
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Uncertainty Quantification for Flow-Based Vision-Language-Action Models

## Summary
## 摘要
这篇论文为基于流的视觉-语言-动作模型提供了实用的置信度信号。它使用流速度场中的集成分歧来检测可能的失败，并选择需要收集哪些机器人演示用于微调。

## 问题
- 当场景、物体或任务超出训练分布时，基于流的 VLA 可能在没有可靠预警的情况下执行动作，这会影响真实机器人部署和安全。
- 现有 VLA 微调通常需要大量专家演示，而这些演示的收集成本很高。
- 缺少的关键信号是认知不确定性：当模型获得合适的新数据后，这类不确定性应当下降。

## 方法
- 该方法训练一个小型的基于流的 VLA 动作头集成，并在动作生成过程中比较它们预测的速度场。
- 它推导出速度场分歧（VFD），作为一种易处理的估计量，与流模型之间的成对 KL 散度相关，同时避免通过 ODE 散度项进行昂贵的似然计算。
- 简单来说，模型先开始生成一个动作片段，检查各个集成成员在流路径上是否指向不同的动作方向，并将更大的分歧视为更高的不确定性。
- SAVE 主动微调方法按平均 VFD 对任务排序，选择不确定性最高的初始观测，请专家提供演示，并使用新数据加回放数据进行微调。

## 结果
- 在 LIBERO 基准上，论文称 VFD 给出的不确定性估计校准更好，并且比测试过的基线更能预测下游任务表现；摘录没有提供具体的校准或相关性数值。
- 论文称 VFD 在部署失败检测上表现良好；摘录没有提供 AUROC、精确率、召回率或阈值数值。
- 论文称在 LIBERO 的多任务适应中，SAVE 至少比基线少需要 22 个样本；摘录将单位呈现为“22”，没有说明这是 22 个演示还是 22%。
- 该方法在包含 K 个任务、每个任务 L 个候选初始观测的多任务池上评估，使用 R 轮主动学习以及每轮 n_e 次专家查询，但摘录没有给出具体的 K、L、R 或 n_e 数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.18043v1](https://arxiv.org/abs/2606.18043v1)
