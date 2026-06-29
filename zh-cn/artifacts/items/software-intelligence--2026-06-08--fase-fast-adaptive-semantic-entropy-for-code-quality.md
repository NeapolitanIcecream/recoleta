---
source: arxiv
url: https://arxiv.org/abs/2606.09800v1
published_at: '2026-06-08T17:53:05'
authors:
- Shizhe Lin
- Ladan Tahvildari
topics:
- code-quality-estimation
- semantic-entropy
- code-generation
- multi-agent-systems
- uncertainty-quantification
- software-foundation-models
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# FASE: Fast Adaptive Semantic Entropy for Code Quality

## Summary
## 摘要
FASE 通过衡量多个代码样本之间的一致性，来估计生成代码是否可能正确，而不依赖真实测试用例。它用嵌入、图距离和自适应聚类替代基于 LLM 的等价性检查，在提升与 Pass@1 相关性的同时降低了运行成本。

## 问题
- 多智能体代码生成会把带幻觉或有错误的代码在各个代理之间传递，所以在错误扩散前需要一个低成本的质量信号。
- 标准语义熵按功能等价性对输出分组，但基于 LLM 蕴含的检查成本高，而且不同评估模型的结果不稳定。
- 结构熵更快，但语法不同的代码可能完成同一任务，而语法相近的代码也可能表现不同。

## 方法
- 每个任务生成 10 个代码样本，用 Qwen3-Embedding-8B 这类仅编码器模型为每个样本生成嵌入，并计算所有样本对之间的余弦距离。
- 在样本对距离图上构建最小生成树，保留样本之间最近的关系，并暴露聚类边界。
- 用 MST 边权的众数设定聚类阈值，再按 MST 平均边权与完整样本对距离均值的比值进行缩放。
- 将得到的聚类当作语义等价类，再在这些等价类上计算熵。

## 结果
- 在 HumanEval 的 164 个 Python 任务和 BigCodeBench-hard 的 148 个 Python 任务上，使用 Qwen3-Embedding-8B 的 FASE，相比基于 LLM 蕴含的语义熵，在与 Pass@1 的 Spearman 相关性上平均提升 25%。
- 它在 ROC-AUC 对 Pass@1 的指标上，比同样的 LLM 蕴含基线提升 19%。
- 运行成本约为传统语义熵方法的 0.3%，因为它去掉了基于 LLM 的成对等价性检查。
- 在中间 Pass@1 任务中，正确与失败代码样本之间的 MST 边距离比约为 3.4-3.6，而完整样本对距离矩阵中这一比值约为 1.7-1.8。
- 评估使用了四个 7B coder 模型：Mistral-7B、CodeLlama-7B、DeepSeek-Coder-7B 和 Qwen2.5-Coder-7B。在报告的设置里，Qwen2.5-Coder 在 101 个 HumanEval 任务上达到 Pass@1 = 1，在 BigCodeBench-hard 上只有 2 个任务达到这一结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09800v1](https://arxiv.org/abs/2606.09800v1)
