---
source: arxiv
url: https://arxiv.org/abs/2606.04436v1
published_at: '2026-06-03T04:34:07'
authors:
- Jiaxin Shi
- Xidong Zhang
- Fucai Zhu
- Zhe Li
- Siyu Zhu
- Weihao Yuan
topics:
- vision-language-action
- robot-foundation-model
- 3d-spatial-reasoning
- latent-distillation
- robot-manipulation
- 2d-to-3d
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# 3DThinkVLA: Endowing Vision-Language-Action Models with Latent 3D Priors via 3D-Thinking-Guided Co-training

## Summary
## 摘要
3DThinkVLA 是一种 VLA 训练方法，它把潜在的 3D 几何和空间推理注入动作预测，同时推理阶段仍只使用 2D 图像。文中报告，基于 Qwen3-VL-2B 和 OFT 风格动作头，它在 LIBERO 和 LIBERO-PLUS 上达到最优或接近最优的成功率。

## 问题
- 标准 VLA 模型根据 2D 图像预测机器人动作，因此常常会遗漏物体位置、距离和朝向等 3D 关系。
- 直接使用点云或深度图等 3D 输入会增加传感器和模型需求，直接做特征对齐也可能破坏预训练 VLM 的视觉-语言对齐。
- 在动作数据和 3D 推理数据上联合训练时，动作提示词仍可能让模型跳过空间推理，转而学习动作捷径。

## 方法
- 模型在真实世界图像上构建的 VLA 动作数据和 3D VLM 问答数据上联合训练。
- 几何适配器把 Qwen3-VL 的中间视觉特征映射到潜在空间，并用余弦相似度与 VGGT 3D 基础模型特征对齐。
- 一个共享的 reasoning-anchor token 传递空间信息。教师分支接收显式的 3D 推理提示，学生分支接收普通动作提示。
- 推理适配器训练学生的 anchor 在潜在空间中匹配教师的 anchor，这样动作预测就能使用空间推理，而不需要生成 chain-of-thought 文本。
- 动作头接收普通的 action-query 特征，以及通过加性融合加入的投影几何特征和推理特征；在推理阶段，VGGT 教师路径被移除。

## 结果
- 在 LIBERO 上，3DThinkVLA 的平均成功率达到 98.7%，高于 SpatialForcing 的 98.5%、3D-CAVLA 的 98.1%、GeoVLA 的 97.7% 和 OpenVLA-OFT 的 97.1%。
- LIBERO 套件分项得分为：Spatial 100.0%，Object 100.0%，Goal 98.8%，Long 95.8%。
- 在 LIBERO-PLUS 上，它的平均成功率达到 81.0%，高于 ABot-M0 的 80.5%、Qwen3-VL-OFT 的 75.0% 和 OpenVLA-OFT 的 69.9%。
- LIBERO-PLUS 的扰动分项得分为：Camera 73.8%、Robot 64.5%、Language 78.0%、Light 98.4%、Background 94.8%、Noise 84.7%、Layout 81.5%。
- 摘要还声称它在 SimplerEnv 和真实世界操作任务上达到最优性能，但给出的文本里没有这些数值结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.04436v1](https://arxiv.org/abs/2606.04436v1)
