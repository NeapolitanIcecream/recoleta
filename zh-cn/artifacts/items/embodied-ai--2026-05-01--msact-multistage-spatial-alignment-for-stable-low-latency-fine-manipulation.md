---
source: arxiv
url: https://arxiv.org/abs/2605.00475v1
published_at: '2026-05-01T07:35:15'
authors:
- Xianbo Cai
- Hideyuki Ichiwara
- Masaki Yoshikawa
- Tetsuya Ogata
topics:
- bimanual-manipulation
- fine-manipulation
- spatial-attention
- action-chunking
- imitation-learning
- low-latency-control
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# MSACT: Multistage Spatial Alignment for Stable Low-Latency Fine Manipulation

## Summary
## 摘要
MSACT 在 ACT 中加入显式的 2D 注意力点跟踪，用于双臂精细操作。它提高了真实世界任务成功率，同时保持接近 ACT 的推理延迟。

## 问题
- 精细操作需要快速控制和稳定的视觉定位；漂移会导致接触错失、交接失败和时机错误。
- ACT 速度快、数据效率高，但它的视觉特征没有强制空间一致性。
- 更大的 VLA 模型和扩散策略可能增加计算量或采样延迟，这会影响 50 Hz 机器人控制。

## 方法
- 该策略保留 ACT 的动作分块、时间集成、ResNet 图像编码器和 CVAE 训练损失。
- 多阶段空间注意力模块从顶部和前方摄像头的每个视角提取 6 个归一化 2D 点，然后将 12 个点转换为 Transformer token。
- 注意力图来自 3 个 CNN 阶段，经过平均后通过带温度控制的 2D softmax 生成坐标。
- 训练期间，解码器预测未来动作块和未来注意力点序列。
- 自监督 L1 对齐损失将预测的未来点与从未来真实帧中重新提取的点进行比较，因此不需要人工关键点标签。

## 结果
- 在 4 个任务的 400 次真实世界 ALOHA 试验中，MSACT 报告的总体成功率为 53.00%，99% CI 为 [46.58, 59.33]；相比之下，ACT 为 23.25% [18.27, 29.10]，SmolVLA 为 15.25%，π0.5 为 13.00%，Diffusion Policy 为 0.00%。
- 推理延迟接近 ACT：MSACT 为 45.40 ± 5.00 ms，ACT 为 45.34 ± 1.03 ms，SmolVLA 为 91.23 ± 1.34 ms，π0.5 为 112.1 ± 0.40 ms，Diffusion Policy 为 158.1 ± 14.9 ms。
- 论文使用 Fisher 精确检验报告称，在汇总的真实世界结果上，MSACT 相比 ACT 有统计显著提升，p < 0.001。
- 在真实世界最终阶段成功率上，MSACT 相比 ACT 的提升为：Detach Network Cable 从 26% 提高到 72%，Thread Velcro 从 8% 提高到 21%，Open Match Box 从 38% 提高到 63%；Insert Tea Bag 与 SmolVLA 同为 56%，高于 ACT 的 21%。
- 在使用人类数据的模拟 Cube Transfer 中，最终 Transfer 成功率从 ACT 的 50% 提高到 76%；使用脚本数据时，从 86% 提高到 100%。
- 在模拟 Bimanual Insertion 中，使用人类数据时，最终 Insert 成功率从 ACT 的 20% 提高到 26%；使用脚本数据时，从 32% 提高到 49%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00475v1](https://arxiv.org/abs/2605.00475v1)
