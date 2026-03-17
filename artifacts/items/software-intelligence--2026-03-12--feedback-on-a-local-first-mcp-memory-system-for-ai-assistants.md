---
source: hn
url: https://github.com/ptobey/local-memory-mcp
published_at: '2026-03-12T23:32:30'
authors:
- ptobey
topics:
- local-rag
- mcp
- ai-memory
- vector-database
- self-hosting
relevance_score: 0.91
run_id: materialize-outputs
---

# Feedback on a local-first MCP memory system for AI assistants?

## Summary
这是一个面向 AI 助手的本地优先个人记忆系统，通过 MCP 工具把本地向量库中的用户上下文快速提供给新的 LLM 会话。它强调自托管、可追溯版本历史和对模型友好的上下文组织，而不是复杂的人类知识分类。

## Problem
- 解决新开启的 LLM 会话无法稳定继承用户长期上下文的问题，导致助手忘记偏好、约束、计划和历史决策。
- 现有记忆方案常依赖云端/SaaS 或复杂文档结构，不适合重视隐私、自托管和可控数据流的技术用户。
- 记忆写入还容易出现冲突、覆盖和过时信息污染，影响检索质量和后续代理行为可靠性。

## Approach
- 采用本地优先 RAG：把文本块和少量元数据存入本地 ChromaDB，再通过 MCP 暴露 `store/search/update/delete/get_chunk/get_evolution_chain` 等工具给 AI 助手调用。
- 核心机制很简单：把用户上下文切成清晰文本片段保存；新会话需要记忆时做语义检索，并结合少量词法和时间新鲜度信号重新排序。
- 用轻量元数据而不是重 schema：包含时间戳、置信度、`supersedes` 版本链和弃用标记，以保留历史并隐藏默认已弃用内容。
- 写入时做启发式 reconciliation，发现重叠或冲突就返回结构化 `warnings[]` 和自修复提示，让模型调整写入行为，而不是静默覆盖。
- 默认软删除和版本化更新（`strategy="version"`），辅以健康检查、冲突日志、备份恢复，以及 stdio/SSE 两种 MCP 传输方式。

## Results
- 文本未提供标准论文式定量评测结果，因此**没有可报告的准确率、召回率或基准对比数字**。
- 明确声称的可用成果是：发布了“early but usable v1”，可用于“personal self-hosted workflows”，并已支持 6 个核心 MCP 工具：`store`、`search`、`update`、`delete`、`get_chunk`、`get_evolution_chain`。
- 检索侧声称支持语义搜索，并在排序中融合相似度、轻量词法信号和时间新鲜度；默认隐藏 deprecated chunks，以提高当前上下文质量。
- 写入侧声称支持启发式冲突检测、冲突日志、warning-first 返回和 self-heal 字段，以提升模型写记忆时的可靠性。
- 工程交付上提供了 2 种运行路径（Docker 或本地 Python）、2 种 MCP 传输（stdio、SSE）以及 3 种 SSE 鉴权模式（`none`、`bearer`、`oauth`）。

## Link
- [https://github.com/ptobey/local-memory-mcp](https://github.com/ptobey/local-memory-mcp)
