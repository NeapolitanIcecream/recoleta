---
source: arxiv
url: http://arxiv.org/abs/2603.28740v1
published_at: '2026-03-30T17:50:54'
authors:
- Yichi Zhang
- Weihao Yuan
- Yizhuo Zhang
- Xidong Zhang
- Jia Wan
topics:
- vision-language-action
- robot-manipulation
- attention-mechanism
- dexterous-manipulation
- sim2real
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# FocusVLA: Focused Visual Utilization for Vision-Language-Action Models

## Summary
## 摘要
FocusVLA 是一个用于机器人操作的视觉-语言-动作模型，它改进了策略在生成动作时使用视觉 token 的方式。它针对自回归 VLA 策略在细粒度操作中的失误，通过把注意力集中到与任务相关的图像区域，并过滤无关的视觉内容，来提升表现。

## 问题
- 现有的自回归 VLA 策略常常会漏掉精确操作所需的细节视觉信息，因为它们的注意力结构允许策略依赖 action-query 捷径，而不是图像证据。
- 大量视觉 token 会让注意力过于分散，背景内容也会带来噪声，从而降低动作精度。
- 论文认为，性能瓶颈更多来自视觉信息的使用方式，而不是视觉表征本身的原始质量。这一点对构建更强的机器人基础模型很重要，因为这说明不能只靠扩大编码器规模。

## 方法
- FocusVLA 用 **Modality Cascaded Attention** 替代混合注意力。动作潜变量分别关注 self state、action-query 特征和视觉特征，然后再融合。这样去掉了模型忽略视觉细节的捷径。
- 它加入了**补丁级 Focus**：根据 action-to-vision 注意力分数，只保留 top-K 个视觉补丁，让策略使用与任务最相关的图像区域。
- 它加入了**通道级 Focus**：对视觉注意力输出施加逐元素门控，抑制有噪声的特征通道，同时保留有用通道。
- 在视觉 value 上，它使用较浅视觉骨干网络的特征来保留精细空间细节，同时用更深层的 VLM 特征来引导哪些区域更重要。
- 论文还在不同注意力结构和视觉表征之间做了受控对比，说明约束视觉信息的使用方式，比更换编码器更重要。

## 结果
- 在 **LIBERO 的 multi-weight 设置**中，FocusVLA 以 **0.5B 参数**达到 **98.7% 平均成功率**，对比 **VLA-Adapter-Pro (0.5B)** 的 **98.5%**、**Spatial Forcing (7B)** 的 **98.5%**、**X-VLA (0.9B)** 的 **98.1%**，以及 **OpenVLA-OFT (7B)** 的 **97.1%**。
- 在 **LIBERO 的 single-weight 设置**中，FocusVLA 取得 **97.0% 平均成功率**，高于 **VLA-Adapter-Pro: 95.6%**、**EVO-1: 94.8%**、**NORA-1.5: 95.0%** 和 **Pi0.5: 96.9%**。
- 在 LIBERO 的 multi-weight 细分结果中，FocusVLA 分别报告了 **99.6 Spatial**、**100.0 Object**、**98.8 Goal** 和 **96.2 Long**。与 VLA-Adapter-Pro 相比，分别是 **+0.0**、**+0.4**、**+0.6** 和 **-0.2** 个点。
- 在一项 LIBERO 消融实验中，使用 VLM 特征且不加 gate 时，从 **mixed attention** 切换到 **cascaded attention**，平均成功率从 **93.6%** 提升到 **97.0%**；Spatial/Object/Goal/Long 四个套件的分数从 **94.4/95.6/93.2/91.0** 提升到 **98.0/98.6/96.2/95.0**。
- 论文称训练收敛更快：在 LIBERO 上，相比 VLA-Adapter，整体速度提升 **1.5x**；在 **LIBERO-Spatial** 上提升 **5x**。
- 对于 **RoboTwin**，摘录给出了定性结论，称 FocusVLA 优于 Diffusion Policy、pi0 和 VLA-Adapter，尤其是在 **Hugging Mug** 这类细粒度任务上，但提供的文本没有给出逐任务数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28740v1](http://arxiv.org/abs/2603.28740v1)
