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
## 摘要
R2Code 是一个基于 LLM 的框架，用于把自然语言需求和实现这些需求的代码连接起来。它通过结构化的需求-代码对齐、自检和自适应检索，提高 trace link 的准确率，并降低 LLM 的上下文成本。

## 问题
- 这篇论文关注需求到代码的可追踪性：给定一条需求，找到实现它的文件、类或方法。
- 这对软件维护、变更影响分析和程序理解很重要，因为缺失或过时的 trace link 会增加人工工作量。
- 以往的 IR、embedding 和简单 RAG 方法往往依赖词面重叠，难以捕捉需求与代码之间跨层级的语义匹配，也会因为把过宽的上下文送入 LLM 而浪费 token。

## 方法
- R2Code 将每条需求拆成四部分：意图、动作、条件和输出。它也把每个代码实体概括成四个对应部分：函数意图、控制流、变量影响和返回状态。
- Bidirectional Alignment Network (BAN) 从两个方向给需求-代码对打分：自上而下检查代码是否覆盖需求，自下而上检查代码逻辑是否符合需求。最终的 BAN 分数是两个方向的加权组合。
- Self-Reflective Consistency Verification (SRCV) 先让 LLM 解释为什么某条链接成立，再根据这段解释是否与原始需求一致来打分。这个一致性分数会调整初始链接置信度，减少误报。
- Dynamic Context-Adaptive Retrieval (DCAR) 为 LLM 生成更紧凑的证据。它缓存代码摘要，估计需求复杂度，按每条需求调整检索预算，并在最终推理前按语义重叠过滤检索结果。

## 结果
- 在五个公开数据集、多个领域和两种编程语言上，R2Code 相比最强基线的平均 **F1 提升为 7.4%**。
- 论文称，R2Code 在这五个数据集上持续优于强 **IR 基线、稠密检索和基于 RAG 的基线**。
- 通过自适应上下文控制，R2Code 的 **token 消耗最多降低 41.7%**，相比固定或更宽泛的检索设置更省。
- 摘要提到评估包含 **precision、recall、F1、MRR 和 precision/recall@k**，但展示的文本没有给出逐数据集结果、带精确分数的基线名称、延迟值或成本数据。
- 鲁棒性结论覆盖 **五个数据集**、多个应用领域和 **两种语言：Java 和 C#**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22432v1](http://arxiv.org/abs/2604.22432v1)
