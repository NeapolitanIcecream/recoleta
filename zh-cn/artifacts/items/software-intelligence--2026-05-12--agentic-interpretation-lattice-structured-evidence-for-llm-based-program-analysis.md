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
代理式解释把基于 LLM 的程序分析组织成对证据的跟踪，建立在一个有限格上，并用工作列表在相关证据变化时重新处理局部主张。它面向源代码本身不足以支持分析的场景，例如不透明库、特定版本的安全公告和非正式 API 合同。

## 问题
- 一次性 LLM 程序分析会隐藏哪些子主张得到支持、被反驳或仍未解决，这会让审计和后续跟进变得困难。
- 依赖证据的程序分析很重要，因为安全性和正确性可能取决于文档、包元数据、公告、第三方行为以及固定静态分析器可能不会检查的非正式 API 合同。
- 生成并检查的 LLM 方法在外部验证器可以验证 LLM 输出时有效，但很多实际问题没有这样的验证器。

## 方法
- 该方法把一个高层分析目标和程序图分解为与程序点、组件边界和辅助节点绑定的局部主张。
- 一个 LLM 代理在受控上下文中评估每个主张，包含源代码片段、相关主张、先前证据和外部信息。
- 论文把每个判断记录在一个有限高度的评估格中，而不是记录成一个自由形式的单一答案。
- 这个工作示例使用一个分级证据域 `A_Graded = {⊥, w, s} × {⊥, w, s}`，为支持和反驳强度提供 9 种格状态。
- 工作列表算法向前传播上下文边、向后传播反馈边，因此后续发现可以触发对更早的不透明组件进行更窄范围的搜索。

## 结果
- 论文没有报告实验结果、实现或基准数据；它说明实际实现和评估是未来工作。
- 它声称有 3 项贡献：代理式解释模型、一个形式核心模型，以及关于依赖证据的程序分析的设计空间讨论。
- 这个工作示例为一个不透明组件的安全审查定义了 7 个具体主张，分别对应解析器、验证器、处理器、拒绝、组合和退出节点。
- 论文识别了 5 类代理式解释的目标，但摘录里没有在正文中列出它们的名称。
- 它最具体的主张是，有限格加工作列表可以让 LLM 的证据状态保持有界、可检查、可在后续提示中复用，同时仍允许 LLM 调用外部证据。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12694v1](https://arxiv.org/abs/2605.12694v1)
