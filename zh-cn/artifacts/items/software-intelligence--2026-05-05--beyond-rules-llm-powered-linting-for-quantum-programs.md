---
source: arxiv
url: https://arxiv.org/abs/2605.03943v1
published_at: '2026-05-05T16:31:14'
authors:
- Pietro Cassieri
- Giuseppe Scanniello
- Seung Yeob Shin
- Fabrizio Pastore
- Domenico Bianculli
topics:
- code-intelligence
- llm-linting
- quantum-software
- static-analysis
- rag
- chain-of-thought
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Rules: LLM-Powered Linting for Quantum Programs

## Summary
## 摘要
论文提出了 LintQ-LLM+CoT 和 LintQ-LLM+RAG，这是面向用 Qiskit 编写的量子程序的 LLM 代码检查器。在 55 个 Qiskit 文件上，两者的 F1 分数都高于基于规则的基线 LintQ。

## 问题
- 量子程序的缺陷与测量、量子门、寄存器分配和 Qiskit API 约束有关；通用 Python 代码检查器和经典静态分析会漏掉其中许多问题。
- LintQ 等基于规则的量子代码检查器需要手写 CodeQL 规则，而 Qiskit API 变化会增加维护成本。
- 更好的代码检查很重要，因为误报会浪费开发者时间，漏掉的量子特定缺陷可能使电路无效或造成误导。

## 方法
- LintQ-LLM+CoT 要求 LLM 每次检查一种量子问题类型，使用一个系统提示和两个自动化用户提示。
- 第一个提示给出缺陷定义，并要求模型规划检测策略、总结代码、执行检查，然后返回带有代码片段和行号的 JSON 警告。
- 第二个提示提供带行号的 Qiskit 源文件供分析。
- LintQ-LLM+RAG 为特定问题类型加入一个从 FAISS 向量索引检索出的示例；该索引由 157 个经人工验证的真阳性 Qiskit 文件构建，并使用 OpenAI text-embedding-3-large 生成嵌入。
- 评估在 55 个文件上将 LintQ、LintQ-LLM+CoT 和 LintQ-LLM+RAG 与人工标注的真值进行比较：其中 43 个是真实文件，12 个是注入故障的文件。

## 结果
- 在 55 文件语料上，LintQ-LLM+CoT 达到 F1 = 0.70，而 LintQ 的 F1 = 0.41。
- LintQ-LLM+RAG 达到 F1 = 0.68，也高于 LintQ 基线。
- LintQ-LLM+CoT 的召回率最高，为 0.96，在语料中漏掉了 3 个真实问题。
- LintQ-LLM+RAG 的精确率最高，为 0.56；作者报告称，与仅使用 CoT 相比，它减少了误报。
- RAG 知识库在移除 8 个超过 8192-token 限制的示例后包含 157 个文件；它基于早期 LintQ 数据集中的 165 条经人工验证的真阳性警告构建。
- 评估语料在人工验证前包含 77 条 LintQ 警告，覆盖 10 个量子问题类别，另有 5 个无问题文件。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.03943v1](https://arxiv.org/abs/2605.03943v1)
