---
source: arxiv
url: http://arxiv.org/abs/2604.05323v1
published_at: '2026-04-07T01:52:42'
authors:
- Chuhang Liu
- Yayun He
- Zuheng Kang
- Xiaoyang Qu
- Jianzong Wang
topics:
- vision-language-action
- inference-acceleration
- token-pruning
- kv-cache
- robot-policy
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# VLA-InfoEntropy: A Training-Free Vision-Attention Information Entropy Approach for Vision-Language-Action Models Inference Acceleration and Success

## Summary
## 总结
VLA-InfoEntropy 是一种面向视觉-语言-行动模型的免训练推理方法，它通过 KV cache 保留更有用的视觉 token，并复用较少有用的 token。它的目标是在保持或提升 LIBERO 上任务成功率的同时，加快 OpenVLA 的测试时推理速度。

## 问题
- VLA 模型在每一步都会处理大量视觉 token，其中许多 token 对任务相关信息贡献很小。这会增加延迟和计算开销，影响机器人实时使用。
- 以往的加速方法常只依据单一信号进行裁剪，比如视觉冗余或注意力信号，容易漏掉指令关键区域，或者在整个 rollout 过程中缺乏自适应能力。
- 这篇论文希望在不重新训练模型的情况下实现更快推理，这对在算力有限的硬件上部署大型机器人策略很重要。

## 方法
- 该方法从每个图像 token 的灰度直方图计算 **visual entropy**。高熵 token 来自纹理丰富或边缘信息较多的区域，被视为更有信息量。
- 它还从文本到视觉的 cross-attention 计算 **attention entropy**。如果某个视觉 token 收到任务文本的集中注意力，那么它的 attention entropy 较低，归一化后的信息分数就较高。
- 一个 timestep 调度会在整个 rollout 中调整 token 选择：较早步骤保留更多全局上有信息的视觉 token，较晚步骤保留更多与指令相关的 token。
- 被选中的重要 token 会从可复用的静态集合中排除，而价值较低的静态 token 则通过 VLA-Cache 机制复用缓存的 KV 状态。
- 完整的选择规则是视觉熵最高的 token 与 attention 信息分数最高的 token 的并集，数量由与 timestep 相关的超参数控制。

## 结果
- 在 **LIBERO** 上，该方法的 **平均成功率为 76.4%**，对比 **OpenVLA** 基线的 **75.0%**、**VLA-Cache** 的 **74.7%**、**SP-VLA** 的 **74.9%** 和 **Spec-VLA** 的 **75.0%**。
- **VLA-InfoEntropy** 在各子集上的成功率分别为：**LIBERO-Spatial 86.4**、**LIBERO-Object 87.6**、**LIBERO-Goal 79.4**、**LIBERO-Long 52.2**。它在 Spatial、Object、Goal 和平均分上领先，但在 Long 上不是最高，**Spec-VLA** 的结果是 **55.0**。
- 相比 **OpenVLA** 的效率数据：**latency 31.25 vs 51.91**、**FLOPs 1.214 vs 1.864**、**speedup 1.53x vs 1.00x**。论文还给出 **34.9% fewer FLOPs** 和 **39.8% lower CUDA latency**。
- 消融实验中，只有 visual entropy 时平均成功率为 **69.8**，只有 attention entropy 时为 **73.9**，静态的 visual+attention 组合为 **75.8**，完整的 timestep-aware 方法为 **76.4**。延迟则从 **33.82** 和 **33.24** 降到 **32.26**，再到 **31.25**。
- 在不同 token 预算下，**100 tokens** 时成功率为 **76.4%**，延迟 **31.25**，**1.205 FLOPs**。使用 **60 tokens** 时成功率降到 **71.6%**，而 **140 tokens** 时延迟升到 **36.64**，成功率为 **76.8%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05323v1](http://arxiv.org/abs/2604.05323v1)
