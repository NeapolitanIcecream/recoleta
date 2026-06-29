---
source: arxiv
url: https://arxiv.org/abs/2606.19784v1
published_at: '2026-06-18T04:36:57'
authors:
- Thien-Loc Ha
- Quang-Tan Nguyen
- Trong-Bao Ho
- Long Dinh
- Minh Duc Nguyen
- Gia-Binh Nguyen
- Pham Tri Quang
- Minh N. Vu
- Duy M. H. Nguyen
- An Thai Le
- Ngo Anh Vien
topics:
- vision-language-action
- robot-foundation-model
- equivariant-policy
- robot-manipulation
- data-efficient-robotics
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# EquiVLA: A General Framework for Rotationally Equivariant Vision-Language-Action Models

## Summary
## 摘要
EquiVLA 为由冻结的视觉-语言骨干网络和流匹配 Diffusion Transformer 动作头组成的 VLA 策略加入 SO(2) 旋转等变性。在 GR00T N1.5 上，它报告了在 LIBERO、CALVIN 和 Mobile ALOHA 真实机器人任务上的性能提升。

## 问题
- 当前 VLA 策略常常需要在多种物体朝向下重新学习同一种操作技能，这会增加数据需求，并降低其在旋转场景中的可用性。
- 数据增强可以让模型看到更多旋转情况，但它不能强制策略在观测发生旋转时输出相应旋转后的动作。
- 这对通用机器人操作很重要，因为物体姿态变化在桌面任务和真实部署中很常见。

## 方法
- EquiVLA 面向将冻结的 VLM 或 ViT 风格视觉骨干网络与流匹配 Diffusion Transformer 动作头配对的 VLA 系统。
- EquiPerceptor 通过有限旋转群旋转输入图像，运行冻结的 ViT，将 patch token 移回对齐后的网格位置，并对其取平均，以生成具有旋转感知能力的视觉 token。
- 它将不变 token 与语言和腕部相机输入一起送入冻结的 VLM，同时让等变 token 保留在单独的流中，以保留旋转结构。
- EquiActor 用 SO(2) 等变层替换标准 DiT 动作头，包括等变投影、注意力、状态编码和动作解码。
- 简单说，旋转后的场景应产生同一项预测技能，并让动作按匹配方向旋转。

## 结果
- 在采用相对控制的 LIBERO 上，EquiVLA 报告的平均成功率为 92.6%，相比之下，GR00T N1.5 为 78.1%，GR00T N1.5 + EquiActor 为 91.0%，pi0 为 86.0%，OpenVLA 为 76.8%，SmolVLA 为 65.6%。
- 在采用绝对控制的 LIBERO 上，EquiVLA 报告的平均成功率为 76.1%，相比之下，GR00T N1.5 为 62.6%，GR00T N1.5 + EquiActor 为 73.6%。
- 在使用单帧观测的 CALVIN ABCD→D 上，EquiVLA 报告的平均序列长度为 4.03/5，相比之下，GR00T N1.5 为 3.45，GR00T N1.5 + EquiActor 为 3.89。
- 在 CALVIN 任务位置成功率上，相比 GR00T N1.5，EquiVLA 将 Task 5 从 48.5% 提高到 64.3%，增加 15.8 个百分点。
- 在五个 Mobile ALOHA 真实机器人任务上，每个任务有 150 条演示和 20 次试验，EquiVLA 报告的平均成功率为 72%，相比之下，GR00T N1.5 为 54%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.19784v1](https://arxiv.org/abs/2606.19784v1)
