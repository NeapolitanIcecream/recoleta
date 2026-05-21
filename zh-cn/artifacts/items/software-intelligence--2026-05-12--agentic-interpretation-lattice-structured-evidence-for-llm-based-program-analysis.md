---
source: arxiv
url: https://arxiv.org/abs/2605.12694v1
published_at: '2026-05-12T19:46:24'
authors:
- Jacqueline L. Mitchell
- Chao Wang
topics:
- llm-program-analysis
- static-analysis
- evidence-lattices
- software-security
- agentic-systems
relevance_score: 0.87
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic Interpretation: Lattice-Structured Evidence for LLM-Based Program Analysis

## Summary
## 摘要
Agentic interpretation 将基于 LLM 的程序分析组织为有限格上的证据跟踪，并使用一个工作列表，在相关证据变化时重新访问局部化的声明。它面向仅靠源代码不足以完成的分析，例如不透明库、特定版本的安全通告和非正式 API 契约。

## 问题
- 一次性 LLM 程序分析可能隐藏哪些子声明得到支持、被反驳或仍未解决，这会让审计和后续跟进变得困难。
- 依赖证据的程序分析很重要，因为安全性和正确性可能取决于文档、包元数据、安全通告、第三方行为和非正式 API 契约，而固定的静态分析器未必会检查这些信息。
- 当外部验证器可以验证 LLM 输出时，generate-and-check LLM 方法有效，但许多实际问题没有这样的验证器。

## 方法
- 该方法将高层分析目标和程序图分解为与程序点、组件边界和辅助节点绑定的局部化声明。
- LLM agent 使用受控上下文评估每个声明，包括源代码片段、相关声明、先前证据和外部信息。
- 论文将每个判断记录在有限高度的评估格中，而不是记录为单个自由形式答案。
- 工作示例使用分级证据域 `A_Graded = {⊥, w, s} × {⊥, w, s}`，为支持强度和反驳强度提供 9 个格状态。
- 工作列表算法向前传播上下文边、向后传播反馈边，因此后续发现可以触发针对早期不透明组件的更窄范围搜索。

## 结果
- 论文没有报告实验结果、实现或基准数字；它说明实际实现和评估属于未来工作。
- 它声称有 3 项贡献：agentic interpretation 模型、一个形式化核心模型，以及面向依赖证据的程序分析的设计空间讨论。
- 工作示例为一次不透明组件安全审查定义了 7 个具体声明，覆盖解析器、验证器、处理器、拒绝、组合和退出节点。
- 论文指出 agentic interpretation 有 5 类目标场景，但摘录没有在正文中列出它们的名称。
- 它最强的具体主张是，有限格加工作列表可以让 LLM 证据状态有界、可检查，并能在后续提示中复用，同时仍允许 LLM 查询外部证据。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12694v1](https://arxiv.org/abs/2605.12694v1)
