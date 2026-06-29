---
source: arxiv
url: https://arxiv.org/abs/2605.09241v1
published_at: '2026-05-10T00:51:47'
authors:
- Kai Zhao
- Dongliang Nie
- Yuchen Lin
- Zhehan Luo
- Yixiao Gu
- Deng-Ping Fan
- Dan Zeng
topics:
- world-model
- jepa
- latent-dynamics
- gaussian-regularization
- continuous-control
- robot-manipulation
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Sub-JEPA: Subspace Gaussian Regularization for Stable End-to-End World Models

## Summary
## 摘要
Sub-JEPA 是一种 JEPA 风格的潜在世界模型，它在避免过强的全空间高斯先验的同时，减少了表示坍塌。论文报告，在四个基于像素的连续控制任务上，它的规划成功率高于 LeWorldModel。

## 问题
- JEPA 世界模型在端到端训练时可能发生坍塌，因为编码器会把不同观测映射到相近的潜在向量。
- LeWorldModel 用整个潜在空间上的各向同性高斯正则项来防止坍塌，但这会把低维控制动力学强行约束成高秩形状。
- 这个问题会影响规划：被扭曲的潜在几何会让模型预测控制在长时间展开时不够准确。

## 方法
- 该模型保留 LeWorldModel 的设置：编码器把 RGB 观测映射到潜在向量，预测器根据当前潜在状态和动作预测下一个潜在状态。
- Sub-JEPA 用多个低维投影子空间内的高斯检验，替代全空间高斯正则化。
- 每个投影矩阵只采样一次，用 QR 分解把行正交化，并在训练期间冻结。
- 在每个子空间里，方法采样随机的一维方向，应用 Epps-Pulley 正态性统计量，然后在方向和子空间上对损失取平均。
- 主要训练损失由潜在预测误差和子空间高斯正则项组成；实验中大多数任务使用潜在维度 D=192、K=32，PushT 使用 K=16。

## 结果
- 与 LeWorldModel 相比，Sub-JEPA 在四个任务上的规划成功率都更高：Two-Room 从 84.33±4.23% 提升到 95.00±2.76%，Reacher 从 82.67±4.42% 提升到 84.00±4.00%，PushT 从 84.67±6.53% 提升到 89.00±5.33%，OGB-Cube 从 67.33±5.01% 提升到 76.33±5.99%。
- 与 PLDM 相比，Sub-JEPA 在 Two-Room 上低 2.00 个百分点，在 Reacher 上高 6.00 个百分点，在 PushT 上高 11.00 个百分点，在 OGB-Cube 上高 11.33 个百分点。
- 与不使用本体感觉的 DINO-WM 相比，Sub-JEPA 在 Two-Room 上低 5.00 个百分点，在 OGB-Cube 上低 9.67 个百分点，但在 Reacher 上高 5.00 个百分点，在 PushT 上高 15.00 个百分点。
- 投影消融结果显示，冻结的正交投影效果最好：Two-Room 为 95.00±2.76%，Reacher 为 84.00±4.00%，PushT 为 89.00±5.33%，OGB-Cube 为 76.33±5.99%。随机冻结投影分别降到 53.00±8.44%、68.00±5.29%、13.33±5.61% 和 61.00±5.55%。
- 论文报告，Sub-JEPA 比 LeWorldModel 更能降低有效秩，而且更大的秩下降与更大的规划收益相对应，但摘要没有给出确切的有效秩数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09241v1](https://arxiv.org/abs/2605.09241v1)
