---
source: arxiv
url: https://arxiv.org/abs/2605.14503v1
published_at: '2026-05-14T07:47:44'
authors:
- Qiang Ke
- Yanjie Zhao
- Hongjin Leng
- Shengming Zhao
- Haoyu Wang
topics:
- retrieval-augmented-generation
- code-intelligence
- software-engineering
- empirical-study
- rag-optimization
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Not All RAGs Are Created Equal: A Component-Wise Empirical Study for Software Engineering Tasks

## Summary
## 总结
这篇论文测试了 RAG 流水线中哪些部分对 Python 软件工程任务最重要。它的核心结论是，检索端的选择，尤其是检索器，往往比生成器更影响最终质量。

## 问题
- 面向软件任务的 RAG 系统需要在查询处理、检索、上下文精炼和生成之间做选择，但实践者缺少针对这些选择的任务级证据。
- 以往工作主要研究代码生成或单个检索组件，对代码摘要和代码修复的指导更弱。
- 组件选错会把无关的代码或文档送进 LLM，增加反复试错的成本。

## 方法
- 作者搭建了一个模块化的 Code RAG 测试平台，把查询处理、检索、上下文精炼和生成分开，便于逐项测试。
- 他们评估了 3 个任务：代码生成、代码摘要和代码修复。
- 他们比较了 4 种查询处理技术、7 种覆盖稀疏检索、稠密检索和混合检索的检索模型、4 种上下文精炼方法和 6 种生成器。
- 检索语料结合了 Stack Overflow、Python API 文档、LeetCode、CodeSearchNet 和 Code-Contests，并做了与测试解的精确匹配去污染。
- 他们还构建了一个由 LLM 驱动的自适应配置系统，使用从实验中归纳出的规则，把任务特征映射到组件选择。

## 结果
- 这段摘录没有给出最终的 W-Pass@1、CodeBLEU 或 embedding-similarity 分数，所以无法从提供的文本里用数值核对宣称的性能提升。
- 这项研究覆盖了 21 个以上的模型和方法：4 种查询处理技术、7 种检索模型、4 种上下文精炼方法和 6 种生成器模型。
- 评估使用了 4 个数据集或数据集变体：300 题的 APPS 子集、100 条较长的 CodeXGLUE Python 片段、一个混淆后的 CodeXGLUE 变体，以及 300 条样本的 DebugBench 子集。
- 检索语料包含 232,633 篇文档：其中 164,085 篇来自 Stack Overflow，38,352 篇来自 Python API 文档，3,174 篇来自 LeetCode，13,590 篇来自 CodeSearchNet，13,432 篇来自 Code-Contests。
- 主要的实证结论是，在很多设置下，检索端组件对最终 RAG 性能的影响大于生成器选择，而 BM25 在测试的软件任务上表现稳定。
- 压缩设置报告的平均上下文长度为：10 个 chunk 时 1,533.47 个 token，20 个 chunk 时 3,578.81 个，40 个 chunk 时 7,818.43 个，80 个 chunk 时 17,105.42 个。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14503v1](https://arxiv.org/abs/2605.14503v1)
