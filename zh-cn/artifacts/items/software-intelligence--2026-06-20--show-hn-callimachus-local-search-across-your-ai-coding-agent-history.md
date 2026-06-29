---
source: hn
url: https://github.com/BetaBots-LLC/callimachus
published_at: '2026-06-20T23:00:27'
authors:
- arishaller
topics:
- code-intelligence
- coding-agents
- local-search
- developer-tools
- agent-memory
- human-ai-interaction
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Callimachus – Local search across your AI coding-agent history

## Summary
## 摘要
Callimachus 是一个本地应用，用于索引 AI 编码代理的对话，并支持在桌面端、CLI、VS Code/Cursor 和 MCP 客户端中搜索。它面向同时使用多个编码代理的开发者，帮助他们查找过去的决策、TODO、文件提及和对话记录，同时不把索引发送到云服务。

## 问题
- AI 编码代理的工作记录分散在许多工具中，开发者在后续编码会话中很难找到过去的决策、修复和 TODO。
- 丢失的对话历史可能导致重复工作、项目决策不一致，以及在 Claude Code、Codex、Cursor、Gemini CLI 和其他工具之间切换时上下文不足。
- 这个工具的意义在于，只有当开发者和代理能在实际工作的编辑器、终端或代理会话中检索记忆时，代理记忆才有帮助。

## 方法
- 它把来自 11 个编码代理来源的对话导入到一个本地 SQLite 数据库中。
- 搜索结合 SQLite FTS5/BM25 关键词排序和通过 sqlite-vec 运行的端侧向量搜索，然后用 Reciprocal Rank Fusion 合并排序结果。
- 文件提及索引把路径映射到对话线程，因此像 `file:embed/mod.rs` 这样的查询可以找到曾修改该文件的会话。
- 可选的 LLM 处理会从过往对话线程中提取决策、注意事项、TODO、摘要、冲突和带引用的回答。
- 同一个索引可通过桌面应用、`cal` CLI、VS Code/Cursor 扩展、提供商无关的聊天，以及一个允许代理读写项目记忆的 MCP 服务器访问。

## 结果
- 支持 11 个来源：Claude Code、Codex、Cursor、Gemini CLI、Qwen Code、Goose、OpenCode、Continue、Cline、Roo Code 和 Kilo Code。
- 提供 16 个 MCP 工具，包括线程搜索、当前项目搜索、文件到线程查找、带引用的历史问答、决策回忆、注意事项回忆和记忆写入。
- CLI 提供 21 个命令，包括 search、recent、export、ask、files、memory、done、remember、agents 和 hook。
- 语义索引使用 `bge-small-en-v1.5` 嵌入，维度为 384，并在本地运行 sqlite-vec KNN。
- 作者称，对约 90,000 条消息的 Claude 语料库建立索引用时约 25 秒，后续处理会跳过未更改的文件。
- 所提供文本未报告经过基准测试的检索准确率、基线对比或用户研究结果。

## Problem

## Approach

## Results

## Link
- [https://github.com/BetaBots-LLC/callimachus](https://github.com/BetaBots-LLC/callimachus)
