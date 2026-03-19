---
source: arxiv
url: http://arxiv.org/abs/2603.07083v1
published_at: '2026-03-07T07:41:28'
authors:
- Michael Hauri
- Friedemann Zenke
topics:
- model-based-rl
- world-model
- dreamer
- self-supervised-learning
- reconstruction-free
relevance_score: 0.38
run_id: materialize-outputs
language_code: zh-CN
---

# Dreamer-CDP: Improving Reconstruction-free World Models Via Continuous Deterministic Representation Prediction

## Summary
Dreamer-CDP提出一种**无重建**的世界模型训练方法，用连续确定性表征预测替代像素重建，在Crafter上把这类方法的性能提升到与Dreamer相当。核心结论是：仅靠内部离散状态预测不够，但加入JEPA式连续表征预测后，无需重建也能学到有效世界模型。

## Problem
- 现有Dreamer类MBRL通常靠**像素重建**学习表征，但这会让表示过度关注任务无关的视觉细节。
- 已有无重建替代方案（如动作预测、视角增强）在**Crafter**这类长时程、稀疏奖励基准上明显落后于重建式Dreamer。
- 这很重要，因为如果能去掉解码/重建目标，世界模型有望更高效、更聚焦任务相关信息，并降低复杂视觉环境下的计算负担。

## Approach
- 将DreamerV3的观测编码拆成两部分：先把图像映射为**连续确定性embedding** `u_t`，再由随机编码器结合隐藏状态生成潜变量 `z_t`。
- 去掉原本的**观测重建损失**，新增一个JEPA/BYOL风格的预测头，用隐藏状态 `h_t` 预测未来连续表征 `\hat{u}_t = g(h_t)`。
- 训练目标使用**负余弦相似度**，让预测表征对齐真实表征：`L_CDP = -cos(SG(u_t), \hat{u}_t)`，其中目标分支停止梯度以避免塌缩。
- 保留Dreamer的奖励、continuation，以及 `L_dyn/L_rep` 对齐项；作者还通过给序列模型/预测器更高学习率，代替EMA目标网络来稳定训练。
- 直观上，这个方法不是去“重建像素”，而是去“预测下一步高层特征”，从而让模型学会对控制更有用的抽象动态。

## Results
- 在**Crafter**上，Dreamer-CDP达到**16.2 ± 2.1** Crafter score，和重建式 **DreamerV3 14.5 ± 1.6** 基本持平；带优先经验回放的Dreamer可到 **19.4 ± 1.6**。
- 相比已有无重建方法，Dreamer-CDP明显更强：**MuDreamer 7.3 ± 2.6**，**DreamerPro 4.7 ± 0.5**，而Dreamer-CDP为 **16.2 ± 2.1**。
- 若移除 `L_CDP`（相当于无重建、也无连续表征预测），性能降到**3.2 ± 1.2**，说明连续确定性表征预测是关键。
- 若去掉奖励预测头对世界模型的梯度，分数变为**12.7 ± 1.6**，说明奖励学习有帮助，但不是主要来源。
- 若去掉 `L_dyn/L_rep` 对齐项，性能降到**6.3 ± 1.9**，表明**CDP本身必要但不充分**，仍需Dreamer的潜变量对齐机制。
- 累积奖励方面，Dreamer-CDP为**9.8 ± 0.4**，低于Dreamer的**11.7 ± 1.9**，但高于MuDreamer的**5.6 ± 1.6**；实验基于**1M环境步数**、**单张Nvidia V100**、**n=7**。

## Link
- [http://arxiv.org/abs/2603.07083v1](http://arxiv.org/abs/2603.07083v1)
