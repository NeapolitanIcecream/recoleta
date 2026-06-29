---
source: hn
url: https://github.com/ahmetvural79/Vitrus
published_at: '2026-06-20T23:22:42'
authors:
- ahvural
topics:
- agent-memory
- code-intelligence
- knowledge-graph
- mcp
- api-verification
- retrieval-augmented-generation
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Vitrus – the company brain that tells you what it doesn't know

## Summary
## 摘要
Vitrus 是一个基于 Markdown 的公司记忆系统，面向人类和 agent。它会用来源、置信度和确定性的缺口列表回答问题。它面向 agent 工作流，因为无依据的说法、过期事实和未授权检索可能导致错误操作。

## 问题
- 团队和 agent 经常在聊天、文档、工单和 API 中搜索，却只得到原始结果，缺少清晰的来源链路。
- 公司知识会随时间变化，所以 agent 在行动前需要发现缺失文档、过期决策、矛盾信息、单人所有权风险和无引用的说法。
- 使用 API 的 agent 可能编造端点或传错参数，除非调用会按真实的 OpenAPI 规范检查。

## 方法
- Markdown 文件和可选的 `.edges.json` sidecar 是标准记录；PGLite 或 Postgres 加 pgvector 会从该记录构建一个可丢弃索引。
- 检索结合向量搜索、BM25 和实体匹配，然后用 reciprocal rank fusion 以及基于图的重新打分来提升有关联或被多个来源佐证的命中结果。
- 缺口检测是确定性的，不使用 LLM：它检查图结构和显式信号，以发现缺失节点、矛盾、过期事实、单点风险和无引用事件。
- `think` 和 `verify` 命令返回带来源的答案、grounded/stale/contradicted/unsupported 等结论、置信度、新鲜度和准确的未记录缺口。
- Agent 通过 MCP 工具和 API 命令连接；OpenAPI import/search/verify/call 会在执行前检查端点名称、缺失参数、错误类型、未知参数、已弃用端点和权限。

## 结果
- 该 repo 报告其 eval gate 上的 `source-hit ≥90%`。
- Gap-Eval 报告在受控合成语料上达到 `100%` 缺口召回率和 `100%` 缺口精确率；作者说明这不能证明在真实环境中的泛化能力。
- ACL 泄漏测试报告 `0` 个未授权结果，并在索引层执行 fail-closed 控制。
- 该项目报告有 `200+` 个测试和四个 CI gate：typecheck、test、eval 和 leak-test。
- MCP 接口从 `13` 个工具增加到 `30` 个工具，包括 search、think、verify、gap reports、API search/verify/call、onboarding paths、quizzes、schema checks 和 briefings。
- 集成覆盖包括 `7` 个一等 live connector、`8` 个 one-token REST preset、`5` 种分页样式，以及对 `13` 个托管来源的 hosted cloud 支持。

## Problem

## Approach

## Results

## Link
- [https://github.com/ahmetvural79/Vitrus](https://github.com/ahmetvural79/Vitrus)
