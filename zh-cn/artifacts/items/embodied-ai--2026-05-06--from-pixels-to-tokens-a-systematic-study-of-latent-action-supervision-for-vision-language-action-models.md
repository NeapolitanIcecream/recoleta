---
source: arxiv
url: https://arxiv.org/abs/2605.04678v1
published_at: '2026-05-06T09:27:07'
authors:
- Yihan Lin
- Haoyang Li
- Yang Li
- Haitao Shen
- Yihan Zhao
- Chao Shao
- Jing Zhang
topics:
- vision-language-action
- latent-actions
- robot-policy-learning
- action-tokenization
- generalist-robot-policy
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# From Pixels to Tokens: A Systematic Study of Latent Action Supervision for Vision-Language-Action Models

## Summary
## 摘要
本文比较了用潜在动作监督训练 Vision-Language-Action 模型的四种方法。核心结论是，离散潜在动作 token 预测提供了最强的训练信号；基于图像的 token 更适合长时程任务，基于动作的 token 更适合复杂的运动控制。

## 问题
- VLA 数据集混合了机器人平台、动作格式和人类视频，因此原始动作标签在不同数据源之间可能有不一致的含义。
- 以往的 VLA 论文对潜在动作的用法不同，难以判断收益来自潜在动作类型、集成方式还是基础模型。
- 这个问题很重要，因为通用机器人策略需要一种监督方式，能跨不同机器人和任务工作，同时不增加额外推理步骤。

## 方法
- 作者使用一个基于 Qwen3-VL-2B 的 VLA 基线，在所有变体中保持相同的主干、占位符、聚合方式和连续动作头。
- 他们比较了两类潜在动作：基于图像的潜在动作由视觉转移学习得到，基于动作的潜在动作通过对连续动作片段进行分词得到。
- 他们测试了四种策略：LA-Align 将隐藏状态对齐到图像潜在嵌入；LA-Direct 预测图像潜在 token；LA-Cond 预测图像潜在 token，并用它们来条件化动作解码；LA-Tok 预测动作潜在 token。
- 训练 VLA 时，所有潜在动作模型都被冻结，测试时这四种策略都在一次前向传播中运行。

## 结果
- 在 LIBERO 上，基线平均成功率为 93.1%。LA-Direct 达到 97.1%（+4.0），LA-Align 达到 97.0%（+3.9），LA-Cond 达到 96.6%（+3.5），LA-Tok 达到 95.5%（+2.4）。
- 在 LIBERO-Long 上，LA-Direct 得分为 96.6%，而基线为 85.8%，提升了 10.8 个百分点。LA-Align 得分 94.8%（+9.0），LA-Cond 得分 94.2%（+8.4），LA-Tok 得分 92.6%（+6.8）。
- 在 RoboTwin 2.0 上，基线平均成功率为 60.5%。LA-Tok 达到 78.0%（+17.5），LA-Cond 达到 73.8%（+13.3），LA-Direct 达到 71.8%（+11.3），LA-Align 达到 70.5%（+10.0）。
- RoboTwin 任务上的提升支持论文的“形式-任务”判断：LA-Tok 将 Move playingcard away 从 73% 提升到 89%（+16），将 Move Can Pot 从 46% 提升到 70%（+24）；LA-Cond 将 Pick Dual Bottles 从 37% 提升到 78%（+41）。
- 作者还报告了真实世界的 JAKA 实验，每个模型-任务组合有 10 次 rollout，并给出 0-100 分的完成度分数，但提供的摘要没有包含足够完整的数值结果，无法比较所有方法。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04678v1](https://arxiv.org/abs/2605.04678v1)
