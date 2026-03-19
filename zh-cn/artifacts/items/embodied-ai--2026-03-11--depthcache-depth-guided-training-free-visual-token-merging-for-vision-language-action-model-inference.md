---
source: arxiv
url: http://arxiv.org/abs/2603.10469v1
published_at: '2026-03-11T06:40:44'
authors:
- Yuquan Li
- Lianjie Ma
- Han Ding
- Lijun Zhu
topics:
- vision-language-action
- token-merging
- depth-guided
- training-free
- robot-inference
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# DepthCache: Depth-Guided Training-Free Visual Token Merging for Vision-Language-Action Model Inference

## Summary
DepthCache 是一种面向视觉-语言-动作（VLA）模型推理加速的免训练视觉 token 压缩方法。它利用深度信息优先保留近处操作区与关键边界，在尽量不伤害机器人操控成功率的前提下降低推理延迟。

## Problem
- VLA 模型在机器人操控中很有潜力，但视觉 token 数量大、语言主干重，导致推理延迟高，难以满足实时闭环控制。
- 现有 token 剪枝或统一比例合并会破坏空间关系，尤其伤害抓取、对位等依赖精细几何推理的任务。
- 现有合并方法常需改动视觉编码器、缺乏跨架构可移植性，也没有利用机器人场景天然可得的深度结构先验。

## Approach
- 用深度图把未保护的图像 patch 按距离分区：近处工作区少合并，远处背景多合并；被保护的 token 不压缩。
- 用“双保护”机制保留关键 token：一部分来自语言模型跨注意力，表示语义上重要；另一部分来自深度边缘，表示几何边界重要。
- 不在单帧里一次性做完合并，而是把合并分摊到连续多帧中，利用时序冗余保持表示稳定，减少每一步计算。
- 监测深度变化，若某区域变动态则恢复为全分辨率；对腕部相机再加一个基于末端执行器运动的状态机，动态决定是否强压缩。
- 整个方法在视觉编码器外部运行，不改模型、不重训，可直接用于不同 VLA 架构。

## Results
- 在 LIBERO 基准、3 个不同 VLA 模型上，DepthCache 达到 **1.07×–1.28×** 推理加速，同时平均成功率下降 **小于 1%**。
- 对 **OpenVLA**：基线平均成功率 **76.7%**；DepthCache 为 **75.7%（-1.0）**，速度 **1.21×**，token 保留率 **78.9%**。相比之下，FastV 为 **64.0%（-12.7）/1.39×**，SP-VLA 为 **71.9%（-4.8）/1.50×**。
- 对 **π0.5**：基线 **97.9%**；DepthCache **97.6%（-0.3）/1.28×**，token 保留率 **68.2%**。而 FastV 为 **77.6%（-20.3）/1.30×**，ToSA 为 **73.8%（-24.1）/0.94×**。
- 对 **GR00T**：基线 **93.1%**；DepthCache **92.9%（-0.2）/1.07×**，token 保留率 **87.5%**。
- 稳态下，双相机总 patch token 从 **512** 降到约 **300**。
- 真实机器人 3 个核心任务上（基于 **π0.5**），总成功数从 **55/60** 变为 **52/60**，平均延迟从 **191 ms** 降到 **143 ms**，达到 **1.33×** 加速。

## Link
- [http://arxiv.org/abs/2603.10469v1](http://arxiv.org/abs/2603.10469v1)
