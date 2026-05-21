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
## 摘要
本文测试 RAG 流水线中哪些部分对 Python 软件工程任务影响最大。论文的主要结论是，检索相关选择，尤其是检索器，通常比生成器更影响最终质量。

## 问题
- 面向软件任务的 RAG 系统需要在查询处理、检索、上下文精炼和生成上做选择，但实践者缺少针对具体任务的证据来指导这些选择。
- 以往工作主要研究代码生成或单个检索组件，对代码摘要和代码修复的指导较弱。
- 组件选择不当可能把无关代码或文档输入 LLM，并增加反复试错的成本。

## 方法
- 作者构建了一个模块化 Code RAG 测试平台，将查询处理、检索、上下文精炼和生成分离，使每个部分都可以单独测试。
- 他们评估了 3 项任务：代码生成、代码摘要和代码修复。
- 他们比较了 4 种查询处理技术、覆盖稀疏检索、密集检索和混合检索的 7 个检索模型、4 种上下文精炼方法，以及 6 个生成器。
- 检索语料库结合了 Stack Overflow、Python API 文档、LeetCode、CodeSearchNet 和 Code-Contests，并进行了精确匹配的测试解答去污染处理。
- 他们还构建了一个由 LLM 驱动的自适应配置系统，使用从实验中得到的规则，将任务特征映射到组件选择。

## 结果
- 摘录没有给出最终的 W-Pass@1、CodeBLEU 或嵌入相似度分数，因此无法根据所提供文本用数字核验其性能提升主张。
- 研究覆盖超过 21 个模型和方法：4 种查询处理技术、7 个检索模型、4 种上下文精炼方法和 6 个生成器模型。
- 评估使用 4 个数据集或数据集变体：包含 300 道题的 APPS 子集、100 个较长的 CodeXGLUE Python 片段、一个混淆版 CodeXGLUE 变体，以及包含 300 个样本的 DebugBench 子集。
- 检索语料库包含 232,633 篇文档：164,085 篇来自 Stack Overflow，38,352 篇来自 Python API 文档，3,174 篇来自 LeetCode，13,590 篇来自 CodeSearchNet，13,432 篇来自 Code-Contests。
- 主要实证结论是，在许多设置中，检索器侧组件对最终 RAG 性能的影响大于生成器选择，并且 BM25 在测试的软件任务中表现良好。
- 压缩设置报告的平均上下文大小为：10 个分块 1,533.47 个 token，20 个分块 3,578.81 个 token，40 个分块 7,818.43 个 token，80 个分块 17,105.42 个 token。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.14503v1](https://arxiv.org/abs/2605.14503v1)
