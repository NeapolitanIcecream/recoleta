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
Atropos 通过在运行中途预测失败，并把这些运行从便宜的小模型切换到更强的大模型，来降低采用自洽性的 LLM 智能体成本。它面向软件工程智能体，这类系统通过采样多条轨迹来提高质量，但推理成本也会随之上升。

## 问题
- 自洽性会多次运行同一个智能体，再对输出进行投票，这会提高 token、工具和模型成本。
- 开放权重的小语言模型更便宜、速度更快，但在软件工程智能体上，它们比更强的专有模型更容易失败。
- 如果没有早期信号，用户只有在为整条轨迹付费后才会知道一次 SLM 运行失败，因此成本与质量之间的权衡仍然较差。

## 方法
- Atropos 将智能体采样得到的多条轨迹合并为一个 **Semantic Flow Graph**，其中节点表示推理步骤或工具使用步骤，边表示某一步骤后接另一步骤的频率。
- 它训练一个 **3-layer Graph Convolutional Network**，在完整推理结束前，将部分图分类为可能成功或可能失败。
- 对于 AutoFL 和 AutoCodeRover，节点编码工具调用及其结构化参数；对于 RepairAgent，则用 FastText embeddings 和 cosine-similarity thresholds 对语义相近的非结构化步骤进行聚类。
- 当部分运行被预测为会在源 SLM 上失败时，Atropos 会提前停止以节省成本，或者通过重放当前上下文 **hotswap** 到更强的目标 LLM，依据是 LLM 的查询上下文是无状态的。
- 论文同时研究了在所有采样轨迹上进行的 **parallel** 截断/热切换，以及在已完成运行之间进行的 **sequential** 截断/热切换。

## 结果
- 在推理中点，Atropos 对最终失败的预测准确率最高达到 **0.85**，**AUROC 0.85**。
- 论文还报告了一组技术贡献数据：在中点预测错误结果时，准确率为 **85.4%**，**AUROC** 为 **85.45%**。
- **hotswapping** 最多可挽救 **27.57%** 原本如果继续停留在小模型上就会失败的运行。
- 与封闭的专有 LLM 运行相比，Atropos 以仅 **23.90%** 的金钱成本达到其 **74.35%** 的性能。
- 按论文中的另一种表述，Atropos 相比专有 LLM 最多可将金钱成本降低 **76.1%**，同时保留其 **74.35%** 的性能。
- 评估覆盖三个软件工程智能体：**AutoFL**、**AutoCodeRover** 和 **RepairAgent**，并在自洽性设置下使用 **10 samples**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.15075v1](http://arxiv.org/abs/2604.15075v1)
