---
source: arxiv
url: https://arxiv.org/abs/2606.24472v1
published_at: '2026-06-23T12:02:36'
authors:
- Yue Peng
- Yongzhe Zhao
- Artur Habuda
- Khuyen Pham
- Yanheng Zhu
- Tran Nguyen Le
- Fares Abu-Dakka
- Li Guo
topics:
- vision-language-action
- robot-foundation-model
- multi-camera-geometry
- geometric-distillation
- sim2real
- robot-manipulation
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# G$^3$VLA: Geometric inductive bias for Vision-Language-Action Models

## Summary
## 摘要
G3VLA 把相机标定信息加入预训练视觉-语言-动作策略的视觉 token，从而提升依赖物体位置、空间关系和相机视角变化的机器人操作任务表现。

## 问题
- pi0、pi0.5 和 GR00T 1.5 等标准 VLA 策略主要把相机图像当作 2D token 流处理，因此必须从动作标签中间接学习相机内参、外参和跨视角几何。
- 这一点在多相机机器人设置中影响最大，因为相机标定已知，并且有助于估计物体在 3D 空间中的位置。
- 既有 3D 操作方法通常需要深度、点云、体素、修改后的动作空间或面向特定任务的模型设计，因此更难接入预训练 VLA 策略。

## 方法
- G3VLA 在动作预测前，把一个感知相机的几何模块插入视觉 token 流。它保留预训练 VLA 主干、动作空间和模仿学习目标不变。
- 该模块加入由内参条件化的射线嵌入：每个图像 patch token 都获得一个由 K^-1 推导出的方向，使模型能够区分外观相似但对应不同相机射线的像素。
- 它使用 Projective Positional Encoding，即 PRoPE，为跨视角注意力提供基于内参和外参的相机标定信号。
- 它通过双向跨视角注意力融合不同视角的 token，然后把融合后的 token 传给基础 VLA 使用的同一动作路径。
- 训练采用两阶段方案。第 1 阶段使用来自真实深度或置信度门控 pi3X 教师预测的密集点图监督，训练新的几何模块。第 2 阶段用原始动作损失加较小的几何蒸馏损失，对完整策略进行微调。

## 结果
- 在使用 pi0 的 LIBERO 上，真实值几何监督把平均成功率从 84.6% 提高到 88.1%，增益为 +3.5 个百分点。各套件中增益最大的是 Object，从 89.4% 到 94.4%（+5.0），以及 Spatial，从 85.2% 到 89.2%（+4.0）。使用 pi3X 监督时，平均成功率为 87.0%。
- 在使用 pi0 的 RoboCasa24 上，成功率从 34.2% 提高到 37.1%（真实值监督），使用 pi3X 监督时提高到 36.5%。
- 在使用 pi0 的 RoboTwin2.0 handover_block 上，真实值监督把成功率从 44.0% 提高到 49.0%。pi3X 版本下降到 41.0%，论文将其归因于合成域中教师点图不可靠。
- 在 pi0.5 LIBERO 上，复现基线平均为 95.85%，而使用 pi3X 的 G3VLA 达到 97.0%。由于基线已经接近饱和，增益较小。
- 在 GR00T 1.5 LIBERO 上，结果不一致：基线平均为 94.90%，使用真实值监督的 G3VLA 达到 94.50%，使用 pi3X 的 G3VLA 达到 95.25%。
- pi0 LIBERO 上的消融显示，移除射线嵌入会使平均成功率从 87.0% 降到 85.0%，移除 PRoPE 会降到 85.9%，用单阶段训练替换两阶段训练会降到 86.3%。在真实世界倒液任务中，pi0 OOD 成功率从 70.8-75.0% 提高到 83.3-87.5%，总体成功率从 82.5-85.0% 提高到 90.0-92.5%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.24472v1](https://arxiv.org/abs/2606.24472v1)
