---
source: arxiv
url: http://arxiv.org/abs/2604.11757v1
published_at: '2026-04-13T17:30:01'
authors:
- Jinhui Ye
- Ning Gao
- Senqiao Yang
- Jinliang Zheng
- Zixuan Wang
- Yuxin Chen
- Pengguang Chen
- Yilun Chen
- Shu Liu
- Jiaya Jia
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- benchmarking
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# StarVLA-$α$: Reducing Complexity in Vision-Language-Action Systems

## Summary
## 总结
StarVLA-α 的观点是，一个朴素的 VLM 到动作方案，已经足以在多个机器人基准上达到顶尖的 VLA 表现。论文的核心主张是方法论层面的：许多常见的 VLA 额外设计，对结果的影响没有骨干模型选择和干净训练设置那么大。

## 问题
- VLA 论文很难直接比较，因为它们混用了不同的骨干模型、机器人数据集、具身配置、预处理和针对基准的调参。
- 这让人难以判断系统里到底是哪一部分提升了机器人性能，哪些收益只是来自围绕某个基准做工程优化。
- 这很重要，因为这个领域想要的是通用机器人策略，但碎片化的评测会掩盖方法是否真的能跨任务、跨具身配置迁移。

## 方法
- 作者构建了 **StarVLA-α**，一个简单的基线：预训练的 **Qwen3-VL** 骨干加一个小型 **MLP 动作头**，从动作 token 预测连续动作块。
- 他们把数据流程保持得很简洁：原始 RGB 图像、语言指令、按训练集划分做动作归一化，以及使用官方基准评测，不做针对基准的调优。
- 他们在 **LIBERO、SimplerEnv、RoboTwin 2.0 和 RoboCasa-GR1** 上用同一套设置做测试，也训练了一个联合的通用模型，动作维度用零填充到 32。
- 在骨干、数据、训练条件一致时，他们比较了不同动作头：离散的 FAST 风格 token、直接连续回归、diffusion/flow-matching，以及双系统的 GR00T 风格设计。
- 他们还做了机器人数据预训练和常见数据工程选项的消融，包括本体感知、历史帧、delta 动作和相对动作。

## 结果
- **主要基准结果（专用版 StarVLA-α）：** LIBERO 上 Spatial/Object/Goal/Long 分别是 **99.0 / 99.8 / 98.5 / 94.1**，四项平均 **98.8**；SimplerEnv 上 WidowX 为 **64.6**，Google VA 为 **70.2**，Google VM 为 **76.0**；RoboTwin 2.0 上 clean 为 **50.3**，clean* 为 **88.2**；RoboCasa-GR1 为 **53.8**。表中结果显示，它超过了 **OpenVLA-OFT** 在 LIBERO 上的平均 **97.9**，超过了 **π0.5** 在 RoboTwin clean 上的 **60.2** 和 clean* 上的 **82.7**，也超过了 **GR00T-N1.6** 在 RoboCasa 上的 **47.6**。
- 摘要声称这个单一通用模型在公开真实世界 **RoboChallenge** 基准上比 **π0.5** 高 **20%**，但节选内容没有给出这项比较的原始数值。
- **动作头消融：** 简单的 MLP 头与更复杂的连续动作头表现相当。在 RoboCasa-GR1 上，MLP 达到 **53.8**，GR00T 风格为 **52.8**，diffusion 风格 π 为 **48.9**；离散 FAST 较弱，为 **45.0**。在 SimplerEnv 的 Google VM 上，MLP 为 **76.0**，FAST 为 **60.1**。
- **机器人预训练消融：** 额外的动作数据预训练没有稳定收益。基线 StarVLA-α 在 RoboTwin clean 上为 **50.3**，在 RoboCasa 上为 **53.8**；**+OXE** 分别降到 **30.2** 和 **27.8**；**+InternData-A1** 把 RoboTwin clean 提高到 **63.6**，但把 RoboCasa 降到 **35.4**；**+RoboTwin-Rand** 把 RoboTwin clean 提高到 **79.7**，但把 RoboCasa 降到 **33.3**。
- **数据工程消融：** 在低数据设置下，一些额外设计有帮助，但随着任务数据增多，收益会缩小。在 RoboCasa **24×10** 下，基线为 **9.8**，delta 动作达到 **15.8**，相对动作 **13.6**，本体感知 **12.5**。在 **24×1000** 下，基线为 **53.8**，各变体接近：本体感知 **54.2**，delta **54.8**，相对动作 **55.5**。
- 论文声称的突破不是一种新架构，而是：一个强的预训练 VLM 加一个小型连续动作头，在一个受控配方下，可以在多个基准上与近期 VLA 系统持平甚至更好。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11757v1](http://arxiv.org/abs/2604.11757v1)
