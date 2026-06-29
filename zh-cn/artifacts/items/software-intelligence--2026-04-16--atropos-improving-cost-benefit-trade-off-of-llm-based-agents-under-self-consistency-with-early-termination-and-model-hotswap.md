---
source: arxiv
url: http://arxiv.org/abs/2604.15075v1
published_at: '2026-04-16T14:39:36'
authors:
- Naryeong Kim
- Shin Yoo
topics:
- llm-agents
- software-engineering
- early-termination
- model-hotswap
- self-consistency
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Atropos: Improving Cost-Benefit Trade-off of LLM-based Agents under Self-Consistency with Early Termination and Model Hotswap

## Summary
## 摘要
Atropos 通过预测运行中途的失败，并把这些运行从便宜的小模型切换到更强的大模型，降低了自洽式 LLM 代理的成本。它面向软件工程代理，这类方法会通过多个采样轨迹提升质量，但也会让推理变得昂贵。

## 问题
- 自洽会让同一个代理运行多次，再对输出投票，这会抬高 token、工具和模型成本。
- 开放权重的小语言模型更便宜、速度更快，但在软件工程代理上的失败率高于更强的专有模型。
- 如果没有早期信号，用户只能在付完整条轨迹的成本后才知道一次 SLM 运行失败了，因此成本和质量之间的权衡仍然很差。

## 方法
- Atropos 将代理的多个采样轨迹合并成一个 **语义流图（Semantic Flow Graph）**，其中节点是推理或工具使用步骤，边记录这些步骤彼此跟随的频率。
- 它训练一个 **3 层图卷积网络（Graph Convolutional Network）**，在完整推理结束前，把部分图分类为更可能成功或更可能失败。
- 对于 AutoFL 和 AutoCodeRover，节点编码工具调用和结构化参数；对于 RepairAgent，语义上相似的非结构化步骤会用 FastText 嵌入和余弦相似度阈值聚类。
- 当部分运行被预测会在源 SLM 上失败时，Atropos 要么提前停止以节省成本，要么通过回放当前上下文 **hotswap** 到更强的目标 LLM，因为 LLM 查询上下文是无状态的。
- 论文研究了覆盖所有采样轨迹的 **并行** 截断/hotswap，以及覆盖已完成运行的 **顺序** 截断/hotswap。

## 结果
- 在推理的中点，Atropos 预测最终失败的准确率最高达到 **0.85**，**AUROC 0.85**。
- 论文还报告了一项技术贡献结果：对错误结果的中点预测达到 **85.4% 准确率** 和 **85.45% AUROC**。
- hotswap 可以挽回最多 **27.57%** 原本会在小模型上失败的运行。
- 相比闭源专有 LLM 运行，Atropos 只用 **23.90%** 的货币成本，就达到它们 **74.35%** 的性能。
- 按论文的另一种表述，Atropos 相比专有 LLM 最多把货币成本降低 **76.1%**，同时保留 **74.35%** 的性能。
- 评估覆盖三个软件工程代理：**AutoFL**、**AutoCodeRover** 和 **RepairAgent**，在 **10 次采样** 的自洽设置下进行。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15075v1](http://arxiv.org/abs/2604.15075v1)
