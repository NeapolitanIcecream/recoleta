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
## 摘要
VLA-InfoEntropy 是一种用于视觉-语言-动作模型的免训练推理方法。它保留更有用的视觉 token，并通过 KV cache 复用价值较低的 token。它的目标是在测试时让 OpenVLA 更快，同时在 LIBERO 上保持或提高任务成功率。

## 问题
- VLA 模型在每一步都会处理大量视觉 token，其中很多 token 几乎不包含与任务相关的信息。这会增加延迟和计算成本，不利于实时机器人应用。
- 现有加速方法通常只依据单一信号进行剪枝，例如视觉冗余或注意力，因此可能漏掉对指令关键的区域，或者无法在整个 rollout 过程中自适应调整。
- 论文的目标是在不重新训练模型的情况下加快推理速度，这对在有限硬件上部署大型机器人策略很重要。

## 方法
- 该方法根据每个图像 token 的灰度直方图计算 **视觉熵**。高熵 token 通常来自纹理丰富或边缘明显的区域，因此被视为信息量更高。
- 它还根据文本到视觉的交叉注意力计算 **注意力熵**。如果某个视觉 token 从任务文本中获得的注意力更集中，那么它的注意力熵就更低，对应的归一化信息分数就更高。
- 一个随时间步变化的调度策略会在 rollout 过程中调整 token 选择：早期步骤保留更多全局信息丰富的视觉 token，后期步骤保留更多与指令相关的 token。
- 选出的重要 token 不会被放入可复用的静态集合，而价值较低的静态 token 则通过 VLA-Cache 机制复用缓存的 KV 状态。
- 完整的选择规则是高视觉熵 token 和高注意力信息 token 的并集，具体数量由依赖时间步的超参数控制。

## 结果
- 在 **LIBERO** 上，该方法报告的**平均成功率**为 **76.4%**，对比 **OpenVLA** 基线的 **75.0%**、**VLA-Cache** 的 **74.7%**、**SP-VLA** 的 **74.9%** 和 **Spec-VLA** 的 **75.0%**。
- **VLA-InfoEntropy** 在各子套件上的成功率分别为：**LIBERO-Spatial** 上 **86.4**、**LIBERO-Object** 上 **87.6**、**LIBERO-Goal** 上 **79.4**、**LIBERO-Long** 上 **52.2**。它在 Spatial、Object、Goal 和平均分上领先，但在 Long 上不是最优；**Spec-VLA** 在该项上的结果是 **55.0**。
- 相对 **OpenVLA** 的效率指标为：**latency 31.25 vs 51.91**、**FLOPs 1.214 vs 1.864**、**speedup 1.53x vs 1.00x**。论文还写到，**FLOPs 减少 34.9%**，**CUDA 延迟降低 39.8%**。
- 在消融实验中，仅使用视觉熵时平均成功率为 **69.8**，仅使用注意力熵时为 **73.9**，使用静态视觉+注意力组合时为 **75.8**，完整的时间步感知方法为 **76.4**。延迟从 **33.82** 和 **33.24** 改善到 **32.26**，再到 **31.25**。
- 在不同 token 预算下，**100 tokens** 对应 **76.4%** 成功率、**31.25** 延迟和 **1.205 FLOPs**。使用 **60 tokens** 会将成功率降到 **71.6%**，而 **140 tokens** 会把延迟提高到 **36.64**，成功率为 **76.8%**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05323v1](http://arxiv.org/abs/2604.05323v1)
