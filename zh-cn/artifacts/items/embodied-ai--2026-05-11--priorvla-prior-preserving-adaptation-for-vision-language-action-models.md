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
PriorVLA 在不覆盖预训练中有用先验的情况下，对预训练的 VLA 机器人策略进行适配。它保留一个冻结的动作专家作为先验来源，并训练一个单独的适配专家，在分布外和小样本机器人操作任务上的提升最大。

## 问题
- 对预训练 VLA 做全量微调，可能会让模型在有限的下游机器人数据上过拟合，并削弱分布外泛化能力。
- 这很重要，因为新的机器人任务、场景、物体和本体形态往往只有少量示范；如果丢掉预训练得到的场景先验和运动先验，就浪费了昂贵的大规模预训练。

## 方法
- PriorVLA 以 pi0.5 为起点，把动作模型拆成两条路径：一个冻结的 Prior Expert 和一个从相同权重初始化的可训练 Adaptation Expert。
- 冻结的 Prior Expert 在去噪过程中运行，但它的最终动作预测会被丢弃；它的内部状态提供运动先验特征。
- 可学习的 Scene Queries 从 VLM 中读取与任务相关的视觉-语言特征，Motor Queries 读取冻结的动作去噪特征，Action Queries 把两者一起送入 Adaptation Expert。
- 训练使用和全量微调相同的 flow-matching MSE 动作损失，但只作用于 Adaptation Expert。
- 该方法训练 Adaptation Expert、Expert Queries 和 VLM 视觉编码器，同时冻结其余部分，更新的参数量约为全量微调的 25%。

## 结果
- 在 RoboTwin 2.0 的 13 个任务标准训练设置中，PriorVLA 达到 77% 的 Easy ID 成功率和 53% 的 Hard OOD 成功率，分别比 pi0.5 高 10 和 11 个百分点。
- 在 RoboTwin 2.0 的数据规模测试中，Hard OOD 相比 pi0.5 的提升在小样本、标准数据和大数据设置下分别为 11、11 和 6 个百分点；Easy ID 在小样本下为 41% 对 29%，在标准数据下为 77% 对 67%。
- 在 LIBERO 上，PriorVLA 在 Spatial、Object、Goal 和 Long 四个子集上的平均成功率为 99.1%，高于 OpenVLA-OFT 的 97.1% 和 pi0.5 的 96.9%。
- 在覆盖八个真实世界任务和两种机器人本体形态的标准数据测试中，PriorVLA 的 ID 成功率为 81%，OOD 成功率为 57%，分别比 pi0.5 高 12 和 16 个百分点。
- 在每个真实世界任务只有 10 个示范时，PriorVLA 的 ID 成功率为 48%，OOD 成功率为 32%，分别比 pi0.5 高 24 和 22 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.10925v1](https://arxiv.org/abs/2605.10925v1)
