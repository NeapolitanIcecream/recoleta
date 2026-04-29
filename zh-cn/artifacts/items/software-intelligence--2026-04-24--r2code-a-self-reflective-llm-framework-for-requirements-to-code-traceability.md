---
source: arxiv
url: http://arxiv.org/abs/2604.22432v1
published_at: '2026-04-24T10:47:56'
authors:
- Yifei Wang
- Jacky Keung
- Xiaoxue Ma
- Zhenyu Mao
- Kehui Chen
- Yishu Li
topics:
- requirements-traceability
- code-intelligence
- llm-for-software-engineering
- retrieval-augmented-generation
- software-maintenance
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# R2Code: A Self-Reflective LLM Framework for Requirements-to-Code Traceability

## Summary
## 概要
R2Code 是一个基于 LLM 的框架，用于把自然语言需求与实现这些需求的代码关联起来。它通过结合结构化的需求-代码对齐、自检和自适应检索，来提高追踪链接的准确率并降低 LLM 的上下文成本。

## 问题
- 论文关注需求到代码的可追踪性：给定一条需求，找出实现它的文件、类或方法。
- 这对软件维护、变更影响分析和程序理解很重要，因为缺失或过时的追踪链接会增加人工工作量。
- 以往的 IR、嵌入和简单 RAG 方法通常依赖词语重叠，容易漏掉需求与代码之间跨层级的语义匹配，并且因为向 LLM 传入过宽的上下文而浪费 token。

## 方法
- R2Code 将每条需求拆成四部分：意图、动作、条件和输出。它也将每个代码实体概括为四个对应部分：功能意图、控制流、变量影响和返回状态。
- 双向对齐网络（BAN）从两个方向为需求-代码对打分：自上而下检查代码是否覆盖需求，自下而上检查代码逻辑是否与需求匹配。最终的 BAN 分数是两个方向的加权组合。
- 自反一致性验证（SRCV）步骤会让 LLM 解释某个链接为什么成立，然后判断这段解释是否与原始需求保持一致。这个一致性分数会调整初始链接置信度，以减少误报。
- 动态上下文自适应检索（DCAR）步骤为 LLM 构建紧凑证据。它会缓存代码摘要、估计需求复杂度、按需求调整检索预算，并在最终推理前按语义重叠过滤检索结果。

## 结果
- 在覆盖多个领域和两种编程语言的五个公开数据集上，R2Code 报告称，相比最强基线，**F1 平均提升 7.4%**。
- 论文称，在这五个数据集上，R2Code 持续优于强 **IR 基线、稠密检索和基于 RAG 的基线**。
- 通过自适应上下文控制，R2Code 报告称，相比固定或更宽泛的检索设置，**token 消耗最多降低 41.7%**。
- 摘录称，评估包含 **precision、recall、F1、MRR 和 precision/recall@k**，但展示的文本没有给出各数据集的具体数值、基线名称及其精确分数、延迟数值或成本数据。
- 文中的稳健性结论覆盖 **五个数据集**、多个应用领域，以及 **两种语言：Java 和 C#**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22432v1](http://arxiv.org/abs/2604.22432v1)
