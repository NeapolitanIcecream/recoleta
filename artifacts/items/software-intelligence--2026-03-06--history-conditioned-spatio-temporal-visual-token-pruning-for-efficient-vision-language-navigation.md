---
source: arxiv
url: http://arxiv.org/abs/2603.06480v1
published_at: '2026-03-06T17:03:16'
authors:
- Qitong Wang
- Yijun Liang
- Ming Li
- Tianyi Zhou
- Christopher Rasmussen
topics:
- vision-language-navigation
- token-pruning
- embodied-ai
- robot-navigation
- spatio-temporal-modeling
relevance_score: 0.63
run_id: materialize-outputs
---

# History-Conditioned Spatio-Temporal Visual Token Pruning for Efficient Vision-Language Navigation

## Summary
本文提出一种面向视觉-语言导航（VLN）的免训练视觉token剪枝方法，针对当前视图与历史记忆采用不同压缩策略，在极高剪枝率下仍尽量保持导航性能。其目标是降低VLA导航模型的推理延迟，使机器人更接近实时部署。

## Problem
- 该工作解决的是：**VLA驱动的VLN模型推理太重，难以在真实机器人上低延迟闭环运行**；这会直接影响导航响应速度与部署可靠性。
- 现有视觉token剪枝多按单帧处理，**没有显式利用VLN依赖历史观测的时空结构**，因此在长时程导航中容易丢失关键信息。
- 问题之所以重要，是因为VLN是具身机器人执行自然语言指令导航的核心能力，适用于家庭辅助、办公引导和搜救等场景。

## Approach
- 方法是一个**training-free / plug-and-play**的时空视觉token剪枝框架，不需要重训或修改预训练VLA模型。
- 对**当前帧**：先用[CLS]与patch token的相似度估计token重要性，再用 **Adaptive Maximal Marginal Relevance (A-MMR)** 迭代选token，同时兼顾“重要”与“彼此不重复”。
- 对**历史帧**：先用当前帧已保留token作为查询，计算每个历史token与当前视图的相关性；再把原始重要性与这种相关性做重加权，保留“既重要又和当前决策有关”的历史信息。
- 简单说，核心机制就是：**当前画面保留空间覆盖，过去画面只保留与当前决策最相关的记忆，并且避免重复token**。
- 最后将剪枝后的token送入原VLA的projector和LLM预测导航动作，从而减少长序列视觉输入的计算量。

## Results
- 在 **R2R val-unseen**、**90%剪枝**（保留72/729 token）下，方法达到 **SR 47.63、SPL 36.36、OS 68.46、NE 5.69**；对比 **SparseVLM** 的 **SPL 31.08**、**DivPrune** 的 **18.55**、**VisPruner** 的 **29.27**，分别高 **5.28、17.81、7.09** 个点。
- 在 **RxR val-unseen**、**90%剪枝** 下，方法达到 **SR 45.71、SPL 32.91、nDTW 47.69、NE 6.90**；对比 **SparseVLM 20.87 SPL**、**DivPrune 14.56**、**VisPruner 25.34**，分别高 **12.04、18.35、7.57** 个点。
- 延迟方面，论文声称在 **90%剪枝** 时，CUDA推理延迟从未剪枝的 **231.34 ms** 降到 **213.40 ms**；并且比 **SparseVLM / DivPrune / VisPruner** 分别再快 **6.09 / 7.31 / 10.96 ms**。
- 在较低剪枝率下也保持领先：例如 **R2R 80%剪枝** 时，本文 **SPL 46.44**，高于 **SparseVLM 40.63**、**DivPrune 28.64**、**VisPruner 43.92**；**RxR 80%剪枝** 时，本文 **SPL 43.64**，高于 **30.10 / 23.92 / 40.15**。
- 消融实验表明“语义重要性 + 多样性”都必要：在 **R2R 90%剪枝** 上，完整设置 **SPL 36.51**；仅多样性为 **36.18**，仅语义为 **27.80**，说明只看语义会导致冗余，只看多样性会偏离任务相关区域。
- 论文还报告在 **Unitree Go2** 四足机器人上的真实部署，声称实现了可靠、低延迟的指令跟随导航，但摘录中未给出机器人实验的量化指标。

## Link
- [http://arxiv.org/abs/2603.06480v1](http://arxiv.org/abs/2603.06480v1)
