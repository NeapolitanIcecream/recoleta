---
source: arxiv
url: http://arxiv.org/abs/2604.09824v1
published_at: '2026-04-10T18:56:48'
authors:
- Nastaran Darabi
- Amit Ranjan Trivedi
topics:
- vision-language-action
- robot-grounding
- ambiguity-detection
- generalist-robot-policy
- 3d-scene-representation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# ProGAL-VLA: Grounded Alignment through Prospective Reasoning in Vision-Language-Action Models

## Summary
## 总结
ProGAL-VLA 是一种视觉-语言-动作模型，它要求机器人在行动前先验证指令指向哪个三维场景实体。论文针对的是一种常见的 VLA 失败模式：策略忽略语言，只沿用视觉捷径。

## 问题
- 现有 VLA 系统常出现**语言忽视**：即使改了指令，行为变化也不够大，因为策略依赖视觉先验，而不是指令语义。
- 这会影响机器人操作，因为机器人可能拿错物体，无法执行空间或关系指令，或者在场景或相机变化时变得不稳定。
- 现有的多模态融合不会检查目标符号是否真的对应当前 3D 场景中的一个可执行实体。

## 方法
- ProGAL-VLA 把系统分成一个**慢速规划器**和一个**快速控制器**。规划器把指令和观测映射为一个简短的符号子目标，例如 `grasp_red_block`。
- 一个**Grounded State Module (GSM)** 构建以实体为中心的 3D 场景表示，包含跟踪到的物体和短期记忆，让模型围绕物体而不是原始图像块进行推理。
- 一个 **State Alignment Cross Attention (SACA)** 模块把符号子目标与 3D 实体匹配，并输出一个**已验证的目标嵌入** `g_t`。动作策略接收的是这个已验证嵌入，而不是原始语言。
- 训练时加入 **Grounding Alignment Contrastive (GAC)** 损失，这是一个 InfoNCE 风格目标，它把符号目标拉向正确的实体嵌入，并把它推离错误实体。
- 模型用实体上的注意力熵作为歧义分数。熵高表示指令没有清楚指向某一个物体，因此模型可以拒绝执行并请求澄清。

## 结果
- 在 **LIBERO-Plus** 鲁棒性评测中，ProGAL-VLA 的 **总分为 85.5**，而 **OpenVLA-OFT+** 为 **79.6**，基础 **OpenVLA** 为 **17.3**。
- 在 LIBERO-Plus 的**机器人扰动**条件下，性能从 **30.3** 提升到 **71.5**。论文还报告了其他类别分数：与 OpenVLA-OFT+ 相比，**相机**为 **93.2** 对 **92.8**，**语言**为 **93.6** 对 **85.8**，**布局**为 **86.7** 对 **77.6**。
- 论文称，在简单、空间和关系指令上，**语言忽视减少了 3 倍到 4 倍**。
- 在 **N=8** 个候选下，实体检索的 **Recall@1** 从 **0.41** 提升到 **0.71**。
- 在 **Custom Ambiguity Benchmark** 上，歧义检测的 **AUROC 为 0.81**，对比为 **0.52**，**AUPR 为 0.79**。
- 对于含糊输入，澄清行为从 **0.09** 提升到 **0.81**，而对清晰指令的成功率没有下降，这是论文的结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09824v1](http://arxiv.org/abs/2604.09824v1)
