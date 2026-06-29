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
## 总结
本文提出了 LintQ-LLM+CoT 和 LintQ-LLM+RAG，这两种用于 Qiskit 量子程序的基于 LLM 的 lint 工具。在 55 个 Qiskit 文件上，两者在 F1 分数上都优于基于规则的 LintQ 基线。

## 问题
- 量子程序会出现与测量、量子门、寄存器分配和 Qiskit API 约束相关的 bug；通用 Python lint 工具和传统静态分析会漏掉很多这类问题。
- 像 LintQ 这样的基于规则的量子 lint 工具需要手写 CodeQL 规则，而 Qiskit API 变化时，这些规则的维护成本很高。
- 更好的 lint 有实际意义，因为误报会浪费开发时间，而漏掉量子特有的 bug 可能让电路无效或产生误导。

## 方法
- LintQ-LLM+CoT 让 LLM 一次检查一种量子问题类型，使用系统提示词和两个自动化用户提示词。
- 第一个提示词给出 bug 定义，要求模型规划检测策略、总结代码、执行检查，并返回带有代码片段和行号的 JSON 告警。
- 第二个提示词提供带行号的 Qiskit 源文件供分析。
- LintQ-LLM+RAG 额外加入从 FAISS 向量索引中检索到的一个示例，示例对应特定的问题类型；该索引由 157 个人工验证为真阳性的 Qiskit 文件构建，文件使用 OpenAI text-embedding-3-large 进行嵌入。
- 评估将 LintQ、LintQ-LLM+CoT 和 LintQ-LLM+RAG 与 55 个文件上的人工真值进行比较：43 个真实文件和 12 个注入故障的文件。

## 结果
- 在这 55 个文件的语料上，LintQ-LLM+CoT 的 F1 = 0.70，而 LintQ 的 F1 = 0.41。
- LintQ-LLM+RAG 的 F1 = 0.68，也高于 LintQ 基线。
- LintQ-LLM+CoT 的召回率最高，为 0.96，在语料中漏掉了 3 个真实问题。
- LintQ-LLM+RAG 的精确率最高，为 0.56，作者报告这比只用 CoT 时减少了误报。
- RAG 知识库包含 157 个文件；由于 8 个示例超过 8192 token 限制而被移除。它基于早期 LintQ 数据集中的 165 条经人工验证为真阳性的告警构建。
- 评估语料在人工验证前包含 77 条 LintQ 告警，分布在 10 类量子问题和 5 个干净文件中。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.03943v1](https://arxiv.org/abs/2605.03943v1)
