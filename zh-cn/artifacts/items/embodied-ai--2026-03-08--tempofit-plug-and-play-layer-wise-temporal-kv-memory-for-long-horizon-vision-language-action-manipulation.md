---
source: arxiv
url: http://arxiv.org/abs/2603.07647v1
published_at: '2026-03-08T14:17:25'
authors:
- Jun Sun
- Boyu Yang
- Jiahao Zhang
- Ning Ma
- Chencheng Wu
- Siqing Zhang
- Yiou Huang
- Qiufeng Wang
- Shan Liang
- Yaran Chen
topics:
- vision-language-action
- long-horizon-manipulation
- temporal-memory
- kv-cache
- training-free
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# TempoFit: Plug-and-Play Layer-Wise Temporal KV Memory for Long-Horizon Vision-Language-Action Manipulation

## Summary
TempoFit 是一种面向预训练视觉-语言-动作（VLA）策略的**免训练**时间记忆插件，用于把原本“单帧决策”的模型改造成能利用历史信息的长时序操作策略。它直接复用模型内部注意力的层级 K/V 缓存，而不是堆叠历史图像或训练额外时序模块，因此更易插拔且保持接近实时推理。

## Problem
- 现有许多 VLA 在推理时基本是**无记忆**的：每一步只看当前观测，导致在遮挡、状态混淆、动作后变化细微等**非马尔可夫**长时序任务中容易重复操作、漏步骤、阶段衔接失败。
- 直接堆叠历史帧虽然能引入时间信息，但会增加视觉 token、推理延迟，并带来大量近重复像素，效率低。
- 训练额外记忆/融合模块通常需要再训练或微调，且会改变原有单帧推理图，难以对强预训练 VLA 做真正的即插即用升级。

## Approach
- 核心想法：把 Transformer 中前缀注意力的 **K/V** 看作模型原生的“状态记忆”。TempoFit 在若干**中间层**缓存过去时刻的前缀 K/V，而不是保存原始图像或添加新 token。
- 检索方式是**K-to-K 检索**：用当前时刻的 key 去和历史 key 做相似度匹配，再读出对应历史 K/V；整个过程**无额外参数、无新训练**，并与冻结骨干原有注意力几何保持一致。
- 为避免旧信息干扰当前决策，引入 **FGTB（Frame-Gap Temporal Bias）**：对时间更久远的历史添加固定衰减偏置，让检索更偏向“最近且相关”的内容。
- 将取回的历史上下文通过**残差方式**加回当前 K/V，而不是拼接虚拟 token；再做**保范数重缩放**，尽量避免在冻结权重下产生分布漂移。
- 方法是**plug-and-play**：不改模型参数、不改输入上下文长度、不依赖动作头结构，适配不同 VLA 主干。

## Results
- **LIBERO-Long**：在 **\(\pi_{0.5}\)** 基线上，平均成功率从 **92.6% 提升到 96.6%**，即 **+4.0 个百分点**；在 **QwenGR00T** 上，从 **90.8% 提升到 94.4%**，即 **+3.6 个百分点**。
- 与训练式时序方法对比，TempoFit 在 LIBERO-Long 上达到或超过代表方法：**MemoryVLA 93.4%**，**HiF-VLA 96.4%**；其中 **TempoFit+\(\pi_{0.5}\)** 达到 **96.6%**。
- 在困难子任务 **“Put both pots on stove”** 上，**\(\pi_{0.5}\)** 从 **58.0% 提升到 84.0%**，说明其对跨阶段时序关联尤其有效。
- **CALVIN D-D**：平均成功任务长度从 **3.78 提升到 3.84**（QwenGR00T → TempoFit）；分步成功率在后续指令上更明显改善，如第 5 个任务从 **59.8 提升到 62.3**。
- **CALVIN ABC-D**：平均成功任务长度从 **3.83 提升到 3.87**（\(\pi_{0.5}\) → TempoFit）；第 5 个任务从 **61.4 提升到 62.0**。
- 论文还声称该方法带来**可忽略的推理开销**并保持接近实时控制，但在给定摘录中未提供更细的延迟数值。

## Link
- [http://arxiv.org/abs/2603.07647v1](http://arxiv.org/abs/2603.07647v1)
