---
source: arxiv
url: https://arxiv.org/abs/2605.10925v1
published_at: '2026-05-11T17:56:02'
authors:
- Xinyu Guo
- Bin Xie
- Wei Chai
- Xianchi Deng
- Tiancai Wang
- Zhengxing Wu
- Xingyu Chen
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- vla-adaptation
- robot-data-scaling
- dexterous-manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# PriorVLA: Prior-Preserving Adaptation for Vision-Language-Action Models

## Summary
## 摘要
PriorVLA 在不覆盖有用预训练先验的情况下适配预训练 VLA 机器人策略。它保留一个冻结的动作专家作为先验来源，并训练一个独立的适配专家，在 OOD 和少样本机器人操作中收益最大。

## 问题
- 对预训练 VLA 进行全量微调可能会过拟合有限的下游机器人数据，并降低 OOD 泛化能力。
- 这一点很重要，因为新的机器人任务、场景、物体和具身形态通常只有少量演示；如果丢失预训练得到的场景先验和运动先验，就会浪费成本高昂的大规模预训练。

## 方法
- PriorVLA 从 pi0.5 出发，将动作模型拆成两条路径：冻结的 Prior Expert，以及用相同权重初始化、可训练的 Adaptation Expert。
- 冻结的 Prior Expert 在去噪过程中运行，但其最终动作预测会被丢弃；它的内部状态提供运动先验特征。
- 可学习的 Scene Queries 从 VLM 读取与任务相关的视觉语言特征，Motor Queries 读取冻结的动作去噪特征，Action Queries 将两者输入 Adaptation Expert。
- 训练使用与全量微调相同的 flow-matching MSE 动作损失，并且只作用于 Adaptation Expert。
- 该方法训练 Adaptation Expert、Expert Queries 和 VLM 视觉编码器，同时冻结其余部分；更新的参数量约为全量微调的 25%。

## 结果
- 在 RoboTwin 2.0 的 13 个任务标准训练中，PriorVLA 达到 77% Easy ID 成功率和 53% Hard OOD 成功率，分别比 pi0.5 高 +10 和 +11 个百分点。
- 在 RoboTwin 2.0 数据规模实验中，Hard OOD 相比 pi0.5 的提升为：少样本 +11 个百分点、标准数据 +11 个百分点、大数据设置 +6 个百分点；Easy ID 在少样本下为 41% 对 29%，在标准数据下为 77% 对 67%。
- 在 LIBERO 上，PriorVLA 报告在 Spatial、Object、Goal 和 Long 上的平均成功率为 99.1%，高于 OpenVLA-OFT 的 97.1% 和 pi0.5 的 96.9%。
- 在覆盖 8 个任务和 2 种机器人具身形态的真实世界标准数据测试中，PriorVLA 达到 81% ID 和 57% OOD 成功率，相比 pi0.5 分别提高 +12 和 +16 个百分点。
- 每个真实世界任务只有 10 次演示时，PriorVLA 达到 48% ID 和 32% OOD 成功率，比 pi0.5 高 +24 和 +22 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10925v1](https://arxiv.org/abs/2605.10925v1)
