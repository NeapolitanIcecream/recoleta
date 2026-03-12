---
source: hn
url: https://www.simplenews.ai/news/poet-x-enables-billion-parameter-llm-training-on-single-h100-gpu-ktw3
published_at: '2026-03-06T23:31:33'
authors:
- goldkey
topics:
- llm-training
- memory-efficient-optimization
- single-gpu-training
- orthogonal-transformations
relevance_score: 0.08
run_id: materialize-outputs
---

# Poet-X Enables Billion-Parameter LLM Training on Single H100 GPU

## Summary
POET-X是一种面向大语言模型预训练的高内存效率优化方法，声称可在单张NVIDIA H100上完成十亿参数级模型训练。它通过正交等价变换替代传统AdamW式状态存储，目标是显著降低训练显存门槛并提升吞吐。

## Problem
- 现有LLM预训练通常依赖多GPU集群，因为Adam/AdamW需要为每个参数额外保存一阶与二阶状态，显存开销很高。
- 这使十亿参数级模型训练对小团队和预算有限的研究者几乎不可及，限制了AI开发的可获得性。
- 当硬件仅有单张H100时，标准AdamW在文中描述的十亿参数训练设置下会直接OOM，成为实际瓶颈。

## Approach
- POET-X建立在POET（Reparameterized Orthogonal Equivalence Training）之上，用**正交等价变换**来优化权重矩阵，而不是像AdamW那样给每个参数维护额外优化器状态。
- 其核心机制是在**保持谱性质**的框架下对权重做重参数化/变换，从而减少显存占用，同时尽量保留训练稳定性与泛化能力。
- 与原始POET相比，POET-X进一步做了实现与计算上的优化，避免了高强度矩阵乘法带来的额外计算负担。
- 用最简单的话说：它通过“换一种表示和更新权重的方式”，省掉了传统优化器最耗显存的那部分辅助变量。

## Results
- 论文摘要性报道的核心结果是：**十亿参数级LLM可在单张NVIDIA H100上完成预训练**；而在相同硬件配置下，**标准AdamW会OOM**。
- 文中明确声称POET-X相较传统方法带来**显著的内存效率提升**与**吞吐提升**，但给定摘录**没有提供具体百分比、tokens/s、峰值显存或训练时长数字**。
- 方法据称在实现上述显存节省的同时，**保持了原POET的训练稳定性和泛化优势**，但摘录中**没有给出具体数据集、评测指标或相对基线数值**。
- 最强的具体对比结论是：**单H100上，POET-X成功训练；AdamW失败（OOM）**。这一点直接支持其“降低LLM训练硬件门槛”的主张。

## Link
- [https://www.simplenews.ai/news/poet-x-enables-billion-parameter-llm-training-on-single-h100-gpu-ktw3](https://www.simplenews.ai/news/poet-x-enables-billion-parameter-llm-training-on-single-h100-gpu-ktw3)
