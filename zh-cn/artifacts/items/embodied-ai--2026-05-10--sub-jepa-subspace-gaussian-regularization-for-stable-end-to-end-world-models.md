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
Sub-JEPA 是一种 JEPA 风格的潜在世界模型，在避免过于严格的全空间高斯先验的同时减少坍塌。它报告了在四个基于像素的连续控制任务上，比 LeWorldModel 有更高的规划成功率。

## 问题
- JEPA 世界模型在端到端训练中可能坍塌，因为编码器可能把不同观测映射到相似的潜在向量。
- LeWorldModel 通过在完整潜在空间上使用各向同性高斯正则化来防止坍塌，但这可能把低维控制动力学强制成高秩形状。
- 这个问题会影响规划：失真的潜在几何会降低模型预测控制在长 rollout 中的准确性。

## 方法
- 该模型保留 LeWorldModel 设置：编码器把 RGB 观测映射为潜在向量，预测器根据当前潜在向量和动作学习下一个潜在状态。
- Sub-JEPA 用多个低维投影子空间内的高斯检验替代全空间高斯正则化。
- 每个投影矩阵只采样一次，通过 QR 分解变为行正交归一，并在训练期间冻结。
- 对每个子空间，该方法采样随机一维方向并应用 Epps-Pulley 正态性统计量，然后在方向和子空间上平均损失。
- 主要训练损失是潜在预测误差加子空间高斯正则项；实验使用潜在维度 D=192，多数任务使用 K=32，PushT 使用 K=16。

## 结果
- 相比 LeWorldModel，Sub-JEPA 在全部四个任务上提高了规划成功率：Two-Room 从 84.33±4.23% 提高到 95.00±2.76%，Reacher 从 82.67±4.42% 提高到 84.00±4.00%，PushT 从 84.67±6.53% 提高到 89.00±5.33%，OGB-Cube 从 67.33±5.01% 提高到 76.33±5.99%。
- 相比 PLDM，Sub-JEPA 在 Two-Room 上低 2.00 个点，在 Reacher 上高 6.00 个点，在 PushT 上高 11.00 个点，在 OGB-Cube 上高 11.33 个点。
- 相比不使用本体感受的 DINO-WM，Sub-JEPA 在 Two-Room 上低 5.00 个点，在 OGB-Cube 上低 9.67 个点，但在 Reacher 上高 5.00 个点，在 PushT 上高 15.00 个点。
- 投影消融显示，冻结正交投影表现最好：Two-Room 为 95.00±2.76%，Reacher 为 84.00±4.00%，PushT 为 89.00±5.33%，OGB-Cube 为 76.33±5.99%。随机冻结投影分别降至 53.00±8.44%、68.00±5.29%、13.33±5.61% 和 61.00±5.55%。
- 论文报告称，Sub-JEPA 比 LeWorldModel 更大幅降低有效秩，并且更大的秩降低对应更大的规划收益，但摘录没有提供具体的有效秩数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09241v1](https://arxiv.org/abs/2605.09241v1)
