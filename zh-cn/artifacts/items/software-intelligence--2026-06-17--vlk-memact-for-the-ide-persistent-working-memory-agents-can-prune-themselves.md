---
source: hn
url: https://github.com/aranajhonny/vlk
published_at: '2026-06-17T23:23:12'
authors:
- akatsutki
topics:
- code-intelligence
- ide-agents
- persistent-memory
- mcp-server
- agent-context-management
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Vlk: MemAct for the IDE – persistent working memory agents can prune themselves

## Summary
## 摘要
Vlk 是一个 Rust MCP 服务器，为 IDE 编码代理提供持久化 SQLite 记忆，并提供一个工具，用于删除过期记忆条目，同时保存新的经验。它面向长时间运行的编码代理会话中的失败循环和上下文膨胀问题。

## 问题
- 长时间运行的 IDE 代理可能会保留重试错误、死胡同和过期上下文，浪费 token，并可能让代理陷入循环。
- 普通聊天上下文通常会在重启后消失，所以编码代理会在会话之间丢失有用经验。
- 这个问题影响 Zed、Cursor 和 Claude Desktop 中的编码代理，因为它们需要持久的任务记忆，同时不能把每一次失败尝试都带到后续上下文中。

## 方法
- Vlk 通过 stdio JSON-RPC 暴露一个 MCP 工具：`vlk_time_travel`。
- 代理调用该工具时传入要移除的 `target_mem_ids` 和要保留的 `learning` 字符串。
- `vlk-core` 执行一个原子 SQLite 操作：先从 `agent_history` 删除选中的行，再插入经验。
- SQLite WAL 将记忆存储在 `vlk.db` 中，因此 IDE 代理可以在重启后复用这些记忆。
- 该设计遵循 Zhang et al. 2025 的 MemAct，其中记忆编辑是代理可在运行时选择的动作。

## 结果
- 摘录没有提供基准测试、用户研究、任务成功率、延迟结果或 token 节省测量。
- 它声称暴露了一个工具：`vlk_time_travel`。
- 在展示的示例中，记忆槽 `5`、`6` 和 `7` 被删除，并替换为经验 `London API down, use cached 12°C`。
- 测试命令报告 `1 slots pruned, N tokens saved`，但摘录没有给出 `N` 的具体值。
- 摘录中点名支持的客户端是通过 MCP 配置接入的 Zed、Cursor 和 Claude Desktop。

## Problem

## Approach

## Results

## Link
- [https://github.com/aranajhonny/vlk](https://github.com/aranajhonny/vlk)
