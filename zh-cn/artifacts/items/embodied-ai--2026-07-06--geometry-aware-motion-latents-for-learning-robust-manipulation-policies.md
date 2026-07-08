---
source: arxiv
url: https://arxiv.org/abs/2607.04714v1
published_at: '2026-07-06T06:34:14'
authors:
- Yunchao Zhang
- Yijia Weng
- Ruizhe Liu
- Ming Hu
- Leonidas Guibas
- Yanchao Yang
topics:
- robot-manipulation
- motion-latents
- 3d-geometry
- diffusion-policy
- rgb-d
- sim2real
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Geometry-Aware Motion Latents for Learning Robust Manipulation Policies

## Summary
## 摘要
GeoMoLa 通过预测操作过程中的未来 3D 点云变化来学习离散运动代码。在 RLBench 单视角 RGB-D 任务上，摘录中报告的最高平均成功率是 84.7%。

## 问题
- 机器人策略需要可复用的运动抽象，但许多潜在动作方法从 2D 视频中学习这些抽象，遗漏了深度、姿态、接近角和物体几何。
- 这很关键，因为当策略无法处理视角变化、杂乱场景、遮挡或新的物体布局时，操作常会失败。
- 现有 3D 策略通常使用静态场景特征，因此不能直接学习 3D 场景如何随时间变化。

## 方法
- GeoMoLa 将 RGB-D 观测转换为 pointmaps，然后训练运动潜变量来预测未来 pointmaps。简单说，代码必须描述下一步会发生什么物理 3D 变化。
- 它使用带 VQ 风格离散代码的视觉语言编码器，因此相似运动可以映射到共享的潜在 token。
- pointmap 扩散模型根据最近的 pointmaps 和潜在代码预测未来 3D 几何。模型也训练了 RGB 预测分支，但论文称几何预测带来了主要增益。
- 一个单独的 3D 去噪 transformer 使用学到的运动代码、场景 token、本体感知信息和带噪动作片段，生成 6-DoF 末端执行器姿态以及夹爪命令。

## 结果
- 在覆盖 10 个任务和 166 个变体的 RLBench 单视角评估中，GeoMoLa 报告了 5 个随机种子下 84.7% 的平均成功率。
- 表中最强的 RLBench 基线是 RVT2，成功率为 80.4%；其他平均值为 3D Diffuser Actor 77.0%、SkillDiffuser 74.4%、Act3D 65.3%、ManiGaussian 44.8% 和 GNFactor 31.7%。
- GeoMoLa 在 10 个 RLBench 任务中的 8 个排名第一。
- 在 Stack Blocks 上，GeoMoLa 达到 54.2% 成功率，RVT2 为 34.8%，3D Diffuser Actor 为 4.0%。
- 在 Push Buttons 上，GeoMoLa 达到 93.0% 成功率，RVT2 为 85.4%，3D Diffuser Actor 为 84.0%。
- 摘录还称，在演示数量有限的杂乱环境中，真实世界 ALOHA 实验也有提升，但可见文本没有提供真实世界成功率数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.04714v1](https://arxiv.org/abs/2607.04714v1)
