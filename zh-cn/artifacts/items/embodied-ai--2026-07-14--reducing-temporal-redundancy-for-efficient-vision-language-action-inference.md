---
source: arxiv
url: https://arxiv.org/abs/2607.12287v1
published_at: '2026-07-14T02:48:31'
authors:
- Yuzhou Wu
- Yuxin Zheng
- Muchun Niu
- Yishan Yang
- Tianhao Liu
- hanwen kang
- Jiajian Jing
- Linfeng Zhang
- Chuan Wen
topics:
- vision-language-action
- generalist-robot-policy
- efficient-inference
- temporal-token-reuse
- flow-policy-compression
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# Reducing Temporal Redundancy for Efficient Vision-Language-Action Inference

## Summary
## 摘要
该论文通过消除视觉编码和基于流的动作生成中的冗余计算，加速视觉-语言-动作推理。在 LIBERO 和 RoboTwin 上，论文报告了约 2.4 倍的推理加速，同时保持相近的操作成功率；其中在 LIBERO 上达到 8.2 FPS 和 93.8% 的成功率。

## 问题
- 大型 VLA 模型会反复编码几乎没有变化的视频帧，并执行 8–10 个迭代式策略采样步骤，从而产生延迟，限制机器人进行高频闭环控制。
- 现有加速方法通常只优化感知模块或语言模块，而动作专家仍是主要的延迟瓶颈。
- 这一问题之所以重要，是因为部署需要在不牺牲任务成功率、也不改变预训练骨干网络的情况下获得更快的响应。

## 方法
- 在连续帧之间复用缓存的视觉 token 表示，只重新计算余弦相似度变化最大的 token，并在后续 ViT 层中使用选出的 token 索引。论文报告称，每帧约有 60% 的 token 会被重新计算。
- 利用流匹配速度轨迹的低秩结构：大部分速度变化集中在两个主导方向上。
- 训练一个轻量级适配器，用 2 步调度替代原始的 8–10 步流求解器，以重建最终的动作轨迹。
- 联合应用这两种机制，在系统层面降低感知和动作生成的计算成本。

## 结果
- 在 LIBERO 上，将该方法应用于 $\pi_{0.5}$ 后，采样步数从 10 步降至 2 步，延迟从 286.9 ms 降至 121.2 ms，吞吐量从 3.5 FPS 提升至 8.2 FPS；平均成功率为 93.8%，而原始 $\pi_{0.5}$ 为 94.4%。
- 在 LIBERO 的详细效率表中，该方法达到 121.8 ms 的总延迟、8.2 FPS 和 1.23 TFLOPs；相比之下，$\pi_{0.5}$ 基线为 293.2 ms、3.4 FPS 和 4.48 TFLOPs。
- 在 RoboTwin 2.0 上，该方法报告的延迟为 125.4 ms、吞吐量为 8.0 FPS、计算量为 2.80 TFLOPs，TOP10 成功率为 81.5%；相比之下，$\pi_{0}$ 为 298.46 ms、3.35 FPS、4.38 TFLOPs 和 82.2%。
- 论文报告称，该方法在仿真中实现了接近 2.6 倍的端到端加速，在真实机器人平台上实现了 1.6 倍加速，同时保持了相当的任务性能；但摘要摘录没有提供详细的真实机器人成功率表格。
- 报告中最显著的收益来自将动作专家的延迟降至基线的约 19%；ViT 和 LLM 的延迟则仍接近原始水平。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.12287v1](https://arxiv.org/abs/2607.12287v1)
