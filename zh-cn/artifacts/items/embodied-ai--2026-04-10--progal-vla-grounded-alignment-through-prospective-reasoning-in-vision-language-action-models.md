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
## 概要
ProGAL-VLA 是一种视觉-语言-动作模型，它要求机器人在执行动作前先确认指令指向的是 3D 场景中的哪个实体。论文针对的是 VLA 的一种常见失效模式：策略会忽略语言，转而依赖视觉捷径。

## 问题
- 现有 VLA 系统常出现**语言忽视**：即使改变指令，行为也不会充分改变，因为策略更依赖视觉先验，而不是指令本身的含义。
- 这会影响机器人操作：机器人可能抓错物体，无法执行空间或关系类指令，或者在场景和相机变化时变得不稳定。
- 标准的多模态融合不会检查目标符号是否真的对应当前 3D 场景中一个真实且可操作的实体。

## 方法
- ProGAL-VLA 将系统拆分为**慢速规划器**和**快速控制器**。规划器根据指令和观测生成一个简短的符号子目标，例如 `grasp_red_block`。
- **Grounded State Module (GSM)** 会构建一个以实体为中心的 3D 场景表示，包含被跟踪的物体和短期记忆，使模型围绕物体而不是原始图像块进行推理。
- **State Alignment Cross Attention (SACA)** 模块将符号子目标与 3D 实体匹配，并输出一个**已验证的目标嵌入** `g_t`。动作策略接收的是这个已验证嵌入，而不是原始语言。
- 训练时加入 **Grounding Alignment Contrastive (GAC)** loss，这是一种 InfoNCE 风格的目标函数，会将符号目标拉近到正确实体的嵌入，并与错误实体拉远。
- 针对实体的注意力熵被用作歧义分数。高熵表示指令没有清楚地指向单一物体，因此模型可以选择不执行并请求澄清。

## 结果
- 在 **LIBERO-Plus** 鲁棒性测试中，ProGAL-VLA 的**总分为 85.5**，对比 **OpenVLA-OFT+** 的 **79.6** 和基础 **OpenVLA** 的 **17.3**。
- 在 LIBERO-Plus 的**机器人扰动**条件下，性能从 **30.3** 提升到 **71.5**。论文还报告了其他类别分数：**camera 93.2** 对比 **92.8**，**language 93.6** 对比 **85.8**，**layout 86.7** 对比 **77.6**，比较对象为 OpenVLA-OFT+。
- 论文称，在简单、空间和关系类指令上，**语言忽视降低了 3x-4x**。
- 在 **N=8** 个候选项的设置下，基于实体的检索从 **0.41 Recall@1** 提升到 **0.71 Recall@1**。
- 在 **Custom Ambiguity Benchmark** 上，歧义检测达到 **AUROC 0.81**，对比 **0.52**，同时 **AUPR 为 0.79**。
- 论文称，在有歧义的输入上，请求澄清的行为从 **0.09** 提高到 **0.81**，同时不会降低对无歧义指令的成功率。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.09824v1](http://arxiv.org/abs/2604.09824v1)
