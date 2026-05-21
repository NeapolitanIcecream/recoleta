---
source: arxiv
url: https://arxiv.org/abs/2605.05126v1
published_at: '2026-05-06T16:55:44'
authors:
- Wei Li
- Jizhihui Liu
- Li Yixing
- Junwen Tong
- Rui Shao
- Liqiang Nie
topics:
- vision-language-action
- robot-manipulation
- 3d-perception
- spatiotemporal-reasoning
- generalist-robot-policy
- efficient-inference
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation

## Summary
## 摘要
ConsisVLA-4D 是一个用于机器人操作的 VLA 模型，在动作预测中加入紧凑的多视角 3D 感知和未来场景推理。论文报告称，与 OpenVLA 相比，它在 LIBERO 和真实世界任务上的性能更高，同时使用的视觉 token 少得多。

## 问题
- 仅使用 2D 的 VLA 模型在操作过程中可能混淆物体身份、物体关系和场景变化。
- 深度图、点云或较长的帧历史会增加传感器和计算成本，这会影响真实机器人推理。
- 论文关注物体布局复杂或机器人移动后布局变化时的动作稳定性。

## 方法
- CV-Aligner 使用 SigLIP 图文相似度和 FiLM 条件控制，保留 Top-K 个与指令相关的视觉 token；默认 K 为 32。
- Single-Fusion 将这些物体 token 与 VGGT 3D 特征做交叉注意力，使同一物体能够在主视角、左视角和右视角之间匹配。
- CO-Fuser 融合三个视角中的 DINOv2 几何特征和 VGGT 特征，然后用紧凑的 latent token 存储跨物体几何信息。
- CS-Thinker 训练未来动态物体 token 和多视角深度 token 的辅助预测；推理时，这些学到的 token 会指导动作解码，不需要显式深度或物体 rollout。
- SC-Attn 并行解码动作块，并使用动作 L1 损失、动态物体损失和深度损失进行训练。

## 结果
- 与 OpenVLA 相比，论文称 ConsisVLA-4D 在 LIBERO 上性能提升 21.6%，推理速度提升 2.3 倍。
- 在真实世界机器人平台上，论文称它相较 OpenVLA 性能提升 41.5%，推理速度提升 2.4 倍。
- 经过指令引导的物体选择后，CV-Aligner 使用的视觉 token 约为原始数量的 1/8。
- CO-Fuser 将几何信息压缩到原始视觉 token 数量的约 1/12 到 1/8。
- 推理期间，CS-Thinker 学到的动态 token 和深度 token 占观察-指令序列的比例低于 10%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05126v1](https://arxiv.org/abs/2605.05126v1)
