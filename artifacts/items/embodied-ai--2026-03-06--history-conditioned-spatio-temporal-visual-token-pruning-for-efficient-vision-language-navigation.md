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
- vision-language-action
- token-pruning
- spatio-temporal-reasoning
- efficient-inference
relevance_score: 0.78
run_id: materialize-outputs
---

# History-Conditioned Spatio-Temporal Visual Token Pruning for Efficient Vision-Language Navigation

## Summary
本文提出一种面向视觉-语言导航（VLN）的**免训练时空视觉token剪枝**方法，在不改动预训练VLA模型的前提下，降低推理延迟并尽量保留导航性能。核心思想是对当前帧与历史帧采用不同剪枝策略：当前帧保留空间覆盖，历史帧按与当前任务相关性进行时空压缩。

## Problem
- 视觉-语言-动作（VLA）模型在VLN中表现强，但Transformer视觉token很多，导致推理延迟高，难以满足机器人**实时闭环导航**需求。
- 现有视觉token剪枝方法多面向单帧或通用视觉模型，**没有显式利用VLN对历史观察和时空关系的依赖**。
- 在高剪枝率下，若只看显著性或只看文本相关性，容易保留**冗余但相似**的token，丢失对导航决策关键的互补信息。

## Approach
- 对所有视觉patch先计算基础重要性：用视觉编码器中全局`[CLS]` token与各patch token的余弦相似度，作为该patch的显著性分数。
- 对**当前帧**，使用自适应最大边际相关（A-MMR）迭代选token：每次选择“**重要且与已选token不同**”的token，简单说就是同时保留关键目标和多样背景，避免重复。
- 对**历史帧**，先用当前帧剪枝后的token作为查询，计算每个历史token与当前视图的最大相似度，再把这个相关性和基础重要性相乘得到新分数。
- 再对历史token应用同样的A-MMR，得到一个**紧凑但信息充分的记忆池**，最后送入投影层和LLM预测导航动作。
- 整个方法**无需重训练、无需修改预训练模型**，可直接插入现有VLA导航系统中。

## Results
- 在 **R2R val-unseen**、**90%剪枝**（保留72/729 token）下，本文方法达到 **SR 47.63、SPL 36.36、OS 68.46、NE 5.69**；对比 **SparseVLM 31.08 SPL**、**DivPrune 18.55 SPL**、**VisPruner 29.27 SPL**，SPL分别提升 **5.28、17.81、7.09** 个点。
- 在 **RxR val-unseen**、**90%剪枝** 下，本文方法达到 **SR 45.71、SPL 32.91、nDTW 47.69、NE 6.90**；对比 **SparseVLM 20.87 SPL**、**DivPrune 14.56 SPL**、**VisPruner 25.34 SPL**，SPL分别提升 **12.04、18.35、7.57** 个点。
- 延迟方面，文中称在 **90%剪枝** 时，CUDA推理延迟从未剪枝的 **231.34 ms** 降到 **213.40 ms**，并比 **SparseVLM、DivPrune、VisPruner** 进一步快 **6.09 ms、7.31 ms、10.96 ms**。
- 与未剪枝模型比较，90%剪枝时性能仍有下降，但保持相对稳健：例如 **R2R SPL 从 49.66 降到 36.36**，**RxR SPL 从 47.26 降到 32.91**，说明该方法在极高压缩下比现有剪枝更能保留任务相关信息。
- 消融实验（R2R）显示“语义重要性+多样性”组合最有效：在 **90%剪枝** 下，完整设置 **SPL 36.51**，优于仅多样性 **36.18**，显著优于仅语义 **27.80**；说明同时考虑“重要”与“去冗余”是关键。
- 论文还报告了在 **Unitree Go2 四足机器人** 上的真实部署，声称实现了可靠、低延迟的指令跟随导航，但摘录中**未提供真实机器人定量指标**。

## Link
- [http://arxiv.org/abs/2603.06480v1](http://arxiv.org/abs/2603.06480v1)
