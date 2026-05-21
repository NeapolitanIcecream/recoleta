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
本文比较了四种用潜在动作监督训练视觉-语言-动作模型的方法。核心结论是，离散潜在动作 token 预测提供最强的训练信号；其中，基于图像的 token 有助于长时程任务，基于动作的 token 有助于复杂运动控制。

## 问题
- VLA 数据集混合了机器人平台、动作格式和人类视频，因此原始动作标签在不同数据源之间可能含义不一致。
- 以往 VLA 论文以不同方式使用潜在动作，导致研究者难以判断收益来自潜在动作类型、集成方法，还是基础模型。
- 这个问题重要，因为通用机器人策略需要能跨不同机器人和任务工作的监督信号，同时不能增加额外推理步骤。

## 方法
- 作者使用一个基于 Qwen3-VL-2B 的 VLA 基线，在所有变体中保持相同的 backbone、占位符、聚合方式和连续动作头。
- 他们比较了基于图像的潜在动作和基于动作的潜在动作；前者从视觉转移中学习，后者通过对连续动作片段进行 token 化学习。
- 他们测试了四种策略：LA-Align 将隐藏状态对齐到图像潜在嵌入；LA-Direct 预测图像潜在 token；LA-Cond 预测图像潜在 token，并用它们作为动作解码的条件；LA-Tok 预测动作潜在 token。
- 所有潜在动作模型在 VLA 训练期间保持冻结，四种策略在测试时都只需一次前向传递。

## 结果
- 在 LIBERO 上，基线平均成功率为 93.1%。LA-Direct 达到 97.1%（+4.0），LA-Align 达到 97.0%（+3.9），LA-Cond 达到 96.6%（+3.5），LA-Tok 达到 95.5%（+2.4）。
- 在 LIBERO-Long 上，LA-Direct 得分为 96.6%，基线为 85.8%，提升 +10.8 个百分点。LA-Align 得分为 94.8%（+9.0），LA-Cond 得分为 94.2%（+8.4），LA-Tok 得分为 92.6%（+6.8）。
- 在 RoboTwin 2.0 上，基线平均成功率为 60.5%。LA-Tok 达到 78.0%（+17.5），LA-Cond 达到 73.8%（+13.3），LA-Direct 达到 71.8%（+11.3），LA-Align 达到 70.5%（+10.0）。
- RoboTwin 任务收益支持论文关于表述方式与任务的对应关系这一结论：LA-Tok 将 Move playingcard away 从 73% 提高到 89%（+16），将 Move Can Pot 从 46% 提高到 70%（+24）；LA-Cond 将 Pick Dual Bottles 从 37% 提高到 78%（+41）。
- 作者还报告了真实世界 JAKA 实验，每个模型-任务进行 10 次 rollout，并在 0-100 分量表上给出完成分数，但所提供的摘录没有包含足够完整的数值结果，无法比较所有方法。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04678v1](https://arxiv.org/abs/2605.04678v1)
