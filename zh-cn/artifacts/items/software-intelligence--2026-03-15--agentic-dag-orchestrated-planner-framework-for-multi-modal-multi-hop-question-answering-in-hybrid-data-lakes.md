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
- dag-planning
- hybrid-data-lake
- agentic-framework
- evidence-tracing
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic DAG-Orchestrated Planner Framework for Multi-Modal, Multi-Hop Question Answering in Hybrid Data Lakes

## Summary
A.DOT 是一个面向企业混合数据湖问答的代理式规划框架，把自然语言问题编译成可执行的 DAG 计划，以支持跨结构化表和非结构化文档的多跳推理。它试图同时提升正确性、完整性、延迟与可审计性，并提供明确的证据链与数据血缘。

## Problem
- 现有企业级 RAG/工具调用方案通常对 SQL 库和向量库分别暴力检索再事后拼接，效率低、容易过检索与数据泄露，也缺少显式多跳推理能力。
- 混合数据湖中的问题常需要在表格与文档之间反复跳转；若没有计划化执行，模型容易幻觉、选错数据源，且难以追踪答案来源。
- 这很重要，因为企业场景不仅要求答案对，还要求低延迟、可验证、可审计、可追踪的数据血缘。

## Approach
- 核心机制是把一个自然语言问题在**单次 LLM 规划**中拆成多个“原子子问题”，生成一个有依赖关系的 DAG；每个节点只面向一种数据源（SQL 或向量库）。
- 系统先做**结构验证 + 语义验证**：检查 schema 合法性、变量依赖、无环性、意图是否保持、聚合/连接是否可执行；有问题时交给 DataOps 诊断、修复或重规划。
- 执行时按 DAG 拓扑顺序运行，**独立节点可并行**，并通过变量绑定只传递最小必要中间结果（如 document_id），减少负载与泄露风险。
- 框架还加入**释义感知计划缓存**，可复用等价查询的 DAG 计划；同时记录每一步的操作、输入输出与证据来源，形成可验证的 lineage/evidence trail。

## Results
- 在 **HybridQA dev 集**（**3,466** 个问答对）上，A.DOT 报告的主结果为：**Answer Correctness 71.0**、**Answer Completeness 73.0**。
- 相比最强基线 **Standard RAG**（Correctness **56.2**，Completeness **62.3**），A.DOT 提升 **14.8 个百分点**正确性、**10.7 个百分点**完整性。
- 其他基线表现：**ReAct 40.2 / 44.3**，**LLM Compiler 27.8 / 30.8**，说明仅靠顺序工具调用或较弱 DAG 编排不足以处理跨模态多跳推理。
- 在 **500** 样本消融实验中，完整 A.DOT 达到 **71.8 / 74.3**；去掉 **DataOps** 降到 **60.0 / 61.8**；去掉 **Plan Validator** 为 **68.0 / 69.6**；两者都去掉为 **67.9 / 69.6**。
- 论文还声称系统正在评估接入 **IBM Watsonx.data Premium**，但部署效果、用户研究和大规模性能测试尚未给出公开量化结果。

## Link
- [http://arxiv.org/abs/2603.14229v1](http://arxiv.org/abs/2603.14229v1)
