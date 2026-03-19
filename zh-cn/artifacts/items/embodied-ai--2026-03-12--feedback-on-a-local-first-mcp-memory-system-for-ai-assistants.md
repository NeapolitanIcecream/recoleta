---
source: hn
url: https://github.com/ptobey/local-memory-mcp
published_at: '2026-03-12T23:32:30'
authors:
- ptobey
topics:
- local-rag
- mcp-tools
- assistant-memory
- chromadb
- local-first
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Feedback on a local-first MCP memory system for AI assistants?

## Summary
这是一个面向 AI 助手的本地优先个人记忆系统，通过 MCP 工具把本地向量数据库中的用户上下文快速提供给新的 LLM 会话。它强调自托管、版本化记忆、轻量元数据和对模型更友好的告警式写入反馈，而不是复杂的人类知识管理结构。

## Problem
- 解决新开启的 LLM 会话无法稳定恢复用户长期上下文的问题，否则助手很难持续记住偏好、约束、日程和历史决策。
- 现有记忆方案常依赖云端/SaaS或重 schema 设计，不利于技术用户自托管、控制隐私数据，也未必适合 LLM 的上下文消费方式。
- 记忆写入还容易出现覆盖、冲突、过时信息污染等问题，导致检索质量和助手行为不可靠。

## Approach
- 用本地 ChromaDB 存储文本块和少量元数据，把记忆表示为“清晰文本片段 + 少量状态字段”，而不是复杂文档结构。
- 通过 MCP 暴露 `store`、`search`、`update`、`delete`、`get_chunk`、`get_evolution_chain` 等工具，让新会话能直接检索并恢复上下文。
- 检索时将语义相似度与轻量词法信号、时间新鲜度结合排序，并默认隐藏 deprecated 片段，以减少过时信息干扰。
- 更新采用版本链和 `supersedes` 关系，默认软删除保留历史，不做破坏性覆盖，便于追踪记忆演化。
- 写入路径加入启发式冲突检测、结构化 `warnings[]` 与自愈提示，以及健康检查，帮助模型在写入风险较高时自我纠错。

## Results
- 文本没有提供标准基准测试、公开数据集实验或量化指标，因此**没有可报告的定量结果**。
- 明确声称当前是“early but usable v1 release”，已足够支持“personal self-hosted workflows”，但 API 和内部启发式规则在后续小版本中仍可能变化。
- 已实现 6 类核心 MCP 工具：`store`、`search`、`update`、`delete`、`get_chunk`、`get_evolution_chain`。
- 支持 2 种传输方式：stdio 与 SSE；SSE 提供 3 种认证模式：`none`、`bearer`、`oauth`。
- 使用本地嵌入模型 `all-MiniLM-L6-v2` 与本地 ChromaDB 持久化目录 `./chroma_db`，强调 0 云后端必需、数据默认本地保存。
- 最强的具体主张是：通过版本链、冲突日志、warning-first 写入响应和默认隐藏废弃片段，提升“practical retrieval quality and reliable AI behavior”，但文中未给出相对基线提升百分比。

## Link
- [https://github.com/ptobey/local-memory-mcp](https://github.com/ptobey/local-memory-mcp)
