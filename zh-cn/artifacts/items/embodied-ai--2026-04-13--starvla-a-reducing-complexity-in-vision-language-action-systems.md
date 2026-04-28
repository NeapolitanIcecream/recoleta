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
## 摘要
StarVLA-α 认为，朴素的 VLM 到动作设置已经足以在多个机器人基准上达到第一梯队的 VLA 表现。论文的核心结论是方法论上的：在 VLA 系统中，许多常见附加设计对结果的影响，小于骨干模型选择和干净的训练设置。

## 问题
- VLA 论文很难直接比较，因为它们混用了不同的骨干模型、机器人数据集、具身配置、预处理方式，以及针对特定基准的调参。
- 这使人难以判断系统里哪些部分真的提升了机器人性能，哪些提升只是来自围绕某个基准做的工程优化。
- 这很重要，因为该领域想要的是通用机器人策略，而分散的评测会掩盖方法是否能跨任务和跨具身形态迁移。

## 方法
- 作者构建了 **StarVLA-α**，一个简单基线：预训练的 **Qwen3-VL** 骨干模型，加上一个小型 **MLP action head**，从动作 token 预测连续动作块。
- 他们把数据流程保持得很简单：原始 RGB 图像、语言指令、按训练集划分做动作归一化，并使用官方基准评测，不做针对基准的专门调参。
- 他们在 **LIBERO、SimplerEnv、RoboTwin 2.0 和 RoboCasa-GR1** 上测试同一套设置，还训练了一个联合的通才模型，用零填充把动作维度统一到 32。
- 在匹配骨干模型、数据和训练设置的条件下，他们比较了不同动作头选择：离散 FAST 风格 token、直接连续回归、diffusion/flow-matching，以及双系统的 GR00T 风格设计。
- 他们还做了机器人数据预训练消融，以及一些常见数据工程选择的消融，例如 proprioception、历史帧、delta actions 和 relative actions。

## 结果
- **主要基准结果（专才版 StarVLA-α）：** LIBERO 在 Spatial/Object/Goal/Long 上分别为 **99.0 / 99.8 / 98.5 / 94.1**，平均 **98.8**；SimplerEnv 在 WidowX 上为 **64.6**，在 Google VA 上为 **70.2**，在 Google VM 上为 **76.0**；RoboTwin 2.0 为 **50.3** clean、**88.2** clean*；RoboCasa-GR1 为 **53.8**。表中这些结果超过了 **OpenVLA-OFT** 在 LIBERO 上的平均 **97.9**、**π0.5** 在 RoboTwin 上的 clean **60.2** 和 clean* **82.7**，以及 **GR00T-N1.6** 在 RoboCasa 上的 **47.6**。
- 摘要称，单个通才模型在公开真实世界 RoboChallenge 基准上比 **π0.5** 高 **20%**，但给出的摘录没有提供这组比较的原始分数。
- **动作头消融：** 简单的 MLP 头与更复杂的连续动作头相比也有竞争力。在 RoboCasa-GR1 上，MLP 达到 **53.8**，GR00T 风格为 **52.8**，diffusion 风格 π 为 **48.9**；离散 FAST 较弱，为 **45.0**。在 SimplerEnv 的 Google VM 上，MLP 为 **76.0**，FAST 为 **60.1**。
- **机器人预训练消融：** 额外的动作数据预训练没有稳定带来帮助。基线 StarVLA-α 在 RoboTwin clean 上为 **50.3**，在 RoboCasa 上为 **53.8**；**+OXE** 降到 **30.2** 和 **27.8**；**+InternData-A1** 把 RoboTwin clean 提高到 **63.6**，但把 RoboCasa 降到 **35.4**；**+RoboTwin-Rand** 把 RoboTwin clean 提高到 **79.7**，但把 RoboCasa 降到 **33.3**。
- **数据工程消融：** 一些附加设计在低数据设置下有帮助，但任务数据更多时，收益会缩小。在 RoboCasa **24×10** 设置下，基线为 **9.8**，delta action 达到 **15.8**，relative action 为 **13.6**，proprioception 为 **12.5**。在 **24×1000** 设置下，基线为 **53.8**，各变体都很接近：proprioception **54.2**，delta **54.8**，relative **55.5**。
- 论文声称的突破不是新架构，而是这样一个结果：强预训练 VLM 加上一个小型连续动作头，在统一且受控的方案下，可以在多个基准上追平或超过近期的 VLA 系统。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.11757v1](http://arxiv.org/abs/2604.11757v1)
