---
source: arxiv
url: http://arxiv.org/abs/2603.14229v1
published_at: '2026-03-15T05:34:16'
authors:
- Kirushikesh D B
- Manish Kesarwani
- Nishtha Madaan
- Sameep Mehta
- Aldrin Dennis
- Siddarth Ajay
- Rakesh B R
- Renu Rajagopal
- Sudheesh Kairali
topics:
- multi-hop-qa
- hybrid-data-lake
- dag-planning
- agentic-systems
- rag
- enterprise-search
relevance_score: 0.04
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic DAG-Orchestrated Planner Framework for Multi-Modal, Multi-Hop Question Answering in Hybrid Data Lakes

## Summary
A.DOT 是一个面向企业混合数据湖问答的代理式规划框架，把自然语言问题编译成可执行的 DAG 计划，在结构化表和非结构化文档之间做多跳推理。它强调并行执行、计划校验、错误修复、缓存与证据链追踪，以提升正确性、完整性和可验证性。

## Problem
- 论文解决的是**混合数据湖上的多模态、多跳问答**：用户问题往往要在 SQL 表与文档/向量库之间来回检索与推理，而现有 RAG 或简单工具调用通常只是分别检索再事后拼接。
- 这件事重要，因为企业场景既要求**答案正确**，也要求**高效、少泄露数据、可追溯来源**；暴力检索会带来冗余计算、幻觉风险和合规问题。
- 现有方法普遍缺少对**显式多跳规划、跨模态中间变量传递、并行执行、计划复用与审计证据链**的统一支持。

## Approach
- 核心方法是把一个自然语言问题**一次性生成成 DAG 执行计划**：每个节点是一个原子子问题，只访问一种数据源（SQL 或向量库），边表示依赖关系。
- 系统先做**结构校验 + 语义校验**，检查 schema 合法性、变量引用、无环性、连接键类型和是否偏离用户意图；若失败，则交给 DataOps 模块诊断、修复或重规划。
- 执行时按 DAG **拓扑顺序并行运行独立节点**，并只把下游真正需要的最小字段（如 document_id）作为变量传递，减少上下文负担、内存占用和数据泄露。
- 系统还加入**释义感知的计划缓存**，可复用语义等价问题的 DAG 计划；同时记录每一步输入、输出和证据来源，形成可验证的数据 lineage。

## Results
- 在 **HybridQA dev** 数据集（**3,466** 个问答样本）上，A.DOT 相比最强基线 **Standard RAG**，**Answer Correctness 从 56.2 提升到 71.0（+14.8 绝对点）**。
- 同一设置下，**Answer Completeness 从 62.3 提升到 73.0（+10.7 绝对点）**，评测使用 Unitxt 指标，LLM-as-a-judge 为 **Mistral Large 2**；推理模型为 **LLaMA-3 70B**。
- 其他基线分数：**ReAct 40.2 / 44.3**，**LLM Compiler 27.8 / 30.8**，A.DOT 明显领先，说明其在跨结构化与非结构化源的多跳推理上更强。
- 在 **500** 条样本的消融实验中，完整 A.DOT 达到 **71.8 correctness / 74.3 completeness**；去掉 **DataOps** 后降到 **60.0 / 61.8**，去掉 **Plan Validator** 后为 **68.0 / 69.6**，去掉二者后为 **67.9 / 69.6**。
- 论文还声称其具备**更低延迟、并行执行、计划复用、可审计证据链**等优势，但正文摘录未提供延迟、缓存命中率或真实部署吞吐等量化数据。

## Link
- [http://arxiv.org/abs/2603.14229v1](http://arxiv.org/abs/2603.14229v1)
