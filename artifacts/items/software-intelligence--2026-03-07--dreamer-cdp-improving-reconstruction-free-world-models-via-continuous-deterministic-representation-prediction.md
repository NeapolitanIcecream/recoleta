---
source: arxiv
url: http://arxiv.org/abs/2603.07083v1
published_at: '2026-03-07T07:41:28'
authors:
- Michael Hauri
- Friedemann Zenke
topics:
- model-based-rl
- world-models
- reconstruction-free-learning
- self-supervised-learning
- dreamer
- representation-learning
relevance_score: 0.34
run_id: materialize-outputs
---

# Dreamer-CDP: Improving Reconstruction-free World Models Via Continuous Deterministic Representation Prediction

## Summary
本文提出 Dreamer-CDP，一种用于高维观测下模型化强化学习的无重建世界模型训练方法。它用连续确定性表征预测替代像素重建，在 Crafter 上首次把这类无重建 Dreamer 变体性能提升到接近甚至略高于标准 Dreamer。

## Problem
- 现有 Dreamer 这类世界模型常依赖**像素重建**来学习表征，但这会让表示过度关注与决策无关的视觉细节。
- 先前的**无重建**替代方案通常依赖动作预测或视图增强，但在 **Crafter** 这类稀疏奖励、长时程任务上明显落后于重建式 Dreamer。
- 这很重要，因为如果能去掉解码重建，世界模型有望更高效、更聚焦任务相关信息，并减少复杂环境中的计算负担。

## Approach
- 核心方法是把观察先编码成一个**连续、确定性嵌入** `u_t`，再让世界模型的隐藏状态 `h_t` 去预测它的下一步表示 `\hat{u}_t`，而不是重建下一帧像素。
- 训练目标加入一个 **JEPA/BYOL 风格** 的表示预测损失：用**负余弦相似度**让预测表示靠近真实表示，并对目标分支使用 **stop-gradient** 防止塌缩。
- 与 Dreamer 原版不同，Dreamer-CDP **去掉 reconstruction loss**，但保留奖励、continuation、以及 Dreamer 的动态/表示 KL 对齐项。
- 与一些相关方法不同，它**不使用 EMA 目标网络**，而是通过让序列模型/预测器使用更高学习率，使动态模型更快接近稳定点。
- 设计上它同时满足：**reconstruction-free、non-contrastive、no action prediction、no view augmentation**，只靠内部表征预测学习世界模型。

## Results
- 在 **Crafter** 上，Dreamer-CDP 达到 **16.2±2.1** 的 **Crafter score**，相比标准 **DreamerV3 的 14.5±1.6** 为同一量级，论文主张其已**匹配 Dreamer** 的表现。
- 相比以往无重建 Dreamer 变体，Dreamer-CDP 明显更强：**MuDreamer 7.3±2.6**，**DreamerPro 4.7±0.5**，而 Dreamer-CDP 为 **16.2±2.1**。
- 若移除 **CDP 损失**（相当于无重建、也无该预测目标），Crafter score 降到 **3.2±1.2**，说明连续确定性表征预测是关键。
- 若不让奖励头反向传播到世界模型，性能降到 **12.7±1.6**，说明奖励学习有帮助，但不是主要来源。
- 若移除 **dyn/rep KL 对齐项**，性能降到 **6.3±1.9**，说明 **CDP 必要但不足够**，还需要 Dreamer 的潜变量对齐机制共同工作。
- 累积奖励上，Dreamer-CDP 为 **9.8±0.4**，低于 Dreamer 的 **11.7±1.9**，但高于 MuDreamer 的 **5.6±1.6**；因此其主要突破体现在 **Crafter score** 而非所有指标全面领先。

## Link
- [http://arxiv.org/abs/2603.07083v1](http://arxiv.org/abs/2603.07083v1)
