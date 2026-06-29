---
source: arxiv
url: https://arxiv.org/abs/2606.20104v1
published_at: '2026-06-18T11:25:16'
authors:
- Petr Ivashkov
- Randall Balestriero
- "Bernhard Sch\xF6lkopf"
topics:
- latent-world-models
- inverse-dynamics
- representation-learning
- offline-robot-data
- model-predictive-control
- controllable-state
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# Sensorimotor World Models: Perception for Action via Inverse Dynamics

## Summary
## 摘要
SMWM 使用逆动力学作为唯一的防坍塌正则项，从像素和连续动作训练潜在世界模型。该方法旨在学习紧凑状态，保留与动作相关的变量，并丢弃不可控干扰项。

## 问题
- JEPA 风格的潜在世界模型如果只用下一个嵌入的预测目标来训练编码器和动力学模型，可能会坍塌；常量嵌入可以得到零前向损失。
- 像素重建会促使模型保留可能无助于控制的视觉细节，例如背景或随机干扰项。
- 这对离线、无奖励的控制数据很重要，因为学习到的状态必须在没有任务标签、奖励、冻结编码器或预训练视觉模型的情况下支持规划。

## 方法
- 模型使用编码器 \(f_\theta\) 将观测映射为嵌入，使用前向模型 \(g_\phi\) 根据 \(z_t\) 和动作 \(a_t\) 预测 \(z_{t+1}\)，并使用逆模型 \(h_\psi\) 根据 \((z_t,z_{t+1})\) 预测 \(a_t\)。
- 训练最小化 \(\mathcal{L}=\mathcal{L}_{\text{fwd}}+\lambda\mathcal{L}_{\text{inv}}\)，其中两个损失都会更新编码器。
- 逆损失会阻止完全坍塌，因为常量嵌入对只能预测常量动作；要降低逆损失，嵌入必须保留可预测动作的信息。
- 学到的表示偏向可控的状态变化，因为这些变化有助于恢复动作，也有助于前向模型预测未来嵌入。
- 在控制阶段，论文冻结编码器和前向模型，然后使用带滚动时域 MPC 的 CEM，优化朝向目标嵌入的动作序列。

## 结果
- 在 dot-world 测试平台中，观测是 \(64\times64\) RGB 图像，潜在大小是 \(d=64\)，PCA 显示，对于真实的 2D 状态，2 个主成分承载了有用方差；其余 62 个方向实际上已经坍塌。
- 在 dot-world 示例中，5 步潜在 rollout 能跟踪编码后的真实嵌入，这支持了动作在潜在空间中大致表现为平移的说法。
- 在四个 dot-world 变体中，有效潜在维度与可控维度一致：Independent = 4，Coupled = 2，Distractor = 2，Combined = 6。
- 在干扰项设置中，编码器会忽略一个随机移动的不可控点，即使它在观测中可见。
- 规划评估覆盖 4 个环境：TwoRoom、Reacher、Push-T 和 OGBench-Cube，并使用 SIGReg、forward-only 和 random-action 基线。
- 提供的摘录没有包含成功率或回报等定量规划指标；它声称在 2D 和 3D 控制任务中，相比 SIGReg 具有有竞争力的规划性能。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.20104v1](https://arxiv.org/abs/2606.20104v1)
