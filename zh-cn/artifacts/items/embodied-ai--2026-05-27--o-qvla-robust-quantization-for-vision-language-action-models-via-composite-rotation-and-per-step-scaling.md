---
source: arxiv
url: https://arxiv.org/abs/2605.28803v1
published_at: '2026-05-27T17:55:01'
authors:
- Xinyu Wang
- Mingze Li
- Sicheng Lyu
- Dongxiu Liu
- Kaicheng Yang
- Ziyu Zhao
- Yufei Cui
- Xiao-Wen Chang
- Peng Lu
topics:
- vision-language-action
- vla-quantization
- robot-policy-compression
- diffusion-action-head
- post-training-quantization
- bimanual-manipulation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Ω-QVLA: Robust Quantization for Vision-Language-Action Models via Composite Rotation and Per-step Scaling

## Summary
## 总结
Ω-QVLA 是一种无需训练的后训练量化方法，面向 VLA 机器人策略。它把语言骨干和 DiT 动作头都量化到统一的 W4A4，同时让 LIBERO 上的成功率接近 FP16。

## 问题
- Pi 0.5 和 GR00T N1.5 等 VLA 模型使用十亿参数级骨干和扩散式动作头，这让机器人端部署在内存和算力上都很昂贵。
- 现有 PTQ 方法常把 DiT 注意力或动作头保留在更高精度，因为动作误差会影响连续机器人控制。
- 统一的 W4A4 量化很重要，因为等价的 4 位权重和激活可以减少内存，并支持更低精度计算，而不需要混合精度处理。

## 方法
- 在量化前应用正交旋转，使每个线性层可以按 `(X R)(R^T W)` 计算，然后再对旋转后的张量进行量化。
- 使用 SVD 旋转来减小权重通道能量不均衡；论文给出的一个示例里，权重行范数跨度从 26 倍降到 6 倍。
- 在 SVD 之后加入 Hadamard 旋转，以分散激活异常值；同一个示例里，激活跨度从 20 倍降到 1.6 倍。
- 使用块大小为 64 的分块 SVD-Hadamard 旋转，并按权重范数做之字形通道置换，以控制开销。
- 用 10 条未标注轨迹和 8 个 Euler 去噪步，对 DiT 激活尺度按层、按去噪步、按通道进行校准。

## 结果
- 在 LIBERO 上，Ω-QVLA 的 W4A4 在 Pi 0.5 上达到 98.0% 的平均成功率，对比 FP16 的 97.1%；各任务得分分别为 Goal 100.0、Spatial 99.0、Object 97.0、Long 96.0。
- 在 LIBERO 上，Ω-QVLA 的 W4A4 在 GR00T N1.5 上达到 87.8% 的平均成功率，对比 FP16 的 87.0%；各任务得分分别为 Goal 91.0、Spatial 86.0、Object 92.0、Long 82.0。
- 与 Pi 0.5 上的 W4A4 全量 QuantVLA 相比，平均成功率从 82.0% 提升到 98.0%，Long 从 56.0% 提升到 96.0%。
- 与 GR00T N1.5 上的 W4A4 全量基线相比，Ω-QVLA 的平均得分为 87.8%，高于 SmoothQuant 的 84.0%、DuQuant 的 70.0% 和 QuantVLA 的 69.8%。
- 该方法报告的静态内存占用减少了 71.3%。
- 在 ARX R5 双臂机器人上的真实世界 Pi 0.5 W4A4 测试中，Ω-QVLA 在 5 个任务上的平均进度得分为 51.0，FP16 Pi-0.5 Base 为 49.6，QuantVLA 为 25.0。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.28803v1](https://arxiv.org/abs/2605.28803v1)
