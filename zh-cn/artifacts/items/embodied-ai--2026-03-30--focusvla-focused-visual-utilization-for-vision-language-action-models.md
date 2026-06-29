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
## 总结
FocusVLA 是一个用于机器人操作的视觉-语言-动作模型，改进了策略在动作生成时使用视觉 token 的方式。它通过把注意力强制放到与任务相关的图像区域，并过滤无关视觉内容，来解决自回归 VLA 策略在精细操作中的失误。

## 问题
- 现有的自回归 VLA 策略经常会遗漏精细操作所需的视觉细节，因为它们的注意力结构让策略更容易依赖动作查询的捷径，而不是图像证据。
- 大量视觉 token 会让注意力分散，背景内容也会带来噪声，从而降低动作准确性。
- 论文认为，性能受限更多的是视觉信息的使用方式，而不是视觉表示本身的原始质量。这一点对构建更强的机器人基础模型很重要，不能只靠扩大编码器规模。

## 方法
- FocusVLA 用 **模态级级联注意力** 替代混合注意力。动作潜变量分别关注自身状态、动作查询特征和视觉特征，再将它们融合。这样就去掉了模型可以忽略视觉细节的捷径。
- 它加入了 **patch 级聚焦**：根据动作到视觉的注意力分数，只保留排名前 K 的视觉 patch，让策略使用最相关的图像区域。
- 它加入了 **通道级聚焦**：对视觉注意力输出施加逐元素门控，压制噪声特征通道，同时保留有用通道。
- 在视觉 value 上，它使用较浅的视觉骨干特征来保留细粒度空间细节，同时用更深的 VLM 特征来指示哪些区域更重要。
- 论文还对注意力结构和视觉表示做了控制比较，说明调节视觉信息的使用方式，比更换编码器更重要。

## 结果
- 在 **LIBERO 多权重设置**下，FocusVLA 的**平均成功率为 98.7%**，参数量为 **0.5B**。对比之下，**VLA-Adapter-Pro（0.5B）** 为 **98.5%**，**Spatial Forcing（7B）** 为 **98.5%**，**X-VLA（0.9B）** 为 **98.1%**，**OpenVLA-OFT（7B）** 为 **97.1%**。
- 在 **LIBERO 单权重设置**下，FocusVLA 的**平均成功率为 97.0%**，高于 **VLA-Adapter-Pro：95.6%**、**EVO-1：94.8%**、**NORA-1.5：95.0%** 和 **Pi0.5：96.9%**。
- 在 LIBERO 多权重分解结果中，FocusVLA 的成绩是 **99.6 Spatial**、**100.0 Object**、**98.8 Goal** 和 **96.2 Long**。与 VLA-Adapter-Pro 相比，分别是 **+0.0**、**+0.4**、**+0.6** 和 **-0.2** 分。
- 在 LIBERO 的消融实验中，把 **混合注意力** 改成带 VLM 特征且不使用门控的 **级联注意力** 后，平均成功率从 **93.6%** 提升到 **97.0%**；Spatial/Object/Goal/Long 的套件分数从 **94.4/95.6/93.2/91.0** 变为 **98.0/98.6/96.2/95.0**。
- 论文声称训练收敛更快：在 LIBERO 上相对 VLA-Adapter 的整体速度提升为 **1.5 倍**，在 **LIBERO-Spatial** 上为 **5 倍**。
- 对于 **RoboTwin**，摘录部分给出的定性结论是 FocusVLA 优于 Diffusion Policy、pi0 和 VLA-Adapter，尤其是在 **Hugging Mug** 这类细粒度任务上，但提供的文本没有逐任务数值。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.28740v1](http://arxiv.org/abs/2603.28740v1)
