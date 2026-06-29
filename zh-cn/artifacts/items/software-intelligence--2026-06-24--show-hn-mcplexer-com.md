---
source: hn
url: https://mcplexer.com
published_at: '2026-06-24T23:08:50'
authors:
- maxrev17
topics:
- mcp-runtime
- agent-orchestration
- code-intelligence
- multi-agent-systems
- human-ai-interaction
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Mcplexer.com

## Summary
## 摘要
MCPlexer 是一个开源的跨运行外壳 MCP 运行时，为编码代理提供一个小型工具入口，并通过路由访问 workers、memory、browser control、approvals、audit、workspaces 和 servers。它面向使用多个 AI 编码客户端的团队，以及需要在真实软件项目中共享控制能力的场景。

## 问题
- AI 编码客户端常把大型静态工具列表加载进上下文，浪费上下文空间，也让工具访问更难控制。
- 分散在 Claude Code、Codex、Cursor、Gemini 和类似客户端中的工作，可能丢失任务状态、记忆、审批和审计历史。
- 面向 GitHub、数据库、电子邮件、日历、浏览器和部署工具的强大 MCP 服务器，在真实代码仓库中安全使用前，需要路由、密钥、沙箱和审查。

## 方法
- MCPlexer 暴露一个小型通用入口，以 `mcpx__search_tools`、`mcpx__execute_code` 和 secret refs 为中心，而不是直接暴露每个下游工具。
- 它通过 workspace policy、auth scopes、approvals、audit logging、restrictions 和 sandbox controls 来路由工具调用。
- 它增加了代理协作原语：delegations、workers、task ledgers、leases、offers、assignments、context packets、attachments 和 persistent memory。
- 它通过可见的 Chrome/Playwright 层提供浏览器控制，可供不同运行外壳和 workers 使用。
- 它允许代理在 `~/.mcplexer` 中配置 servers、routes、auth scopes、audit 和 approvals，而普通项目代码仓库只看到这个小型入口。

## 结果
- 摘录没有报告基准测试结果、用户研究、延迟数据、安全评估或成本对比。
- 它声称支持 7 个具名 MCP 客户端：Claude Code、Codex、OpenCode、Cursor、Grok、Pi 和 Gemini，另有其他 MCP 客户端。
- 它列出 15 个功能领域：delegations、workers、tasks、memory、browser、workspaces、restrictions、approvals、audit、servers、secrets、mesh、skills、models 和 dashboard。
- 它点名至少 11 个下游服务目标：GitHub、Linear、Slack、Gmail、Calendar、Postgres、Vercel、WordPress、WooCommerce、Reddit 和 Telegram，另有浏览器和自定义服务器。
- 它最强的具体主张属于运行层面，缺少实验结果支撑：一个带路由的 MCP 层可以让多个编码运行外壳获得相同的 delegation、memory、browser、approval、audit、workspace、sandbox 和 secret-handling 行为。

## Problem

## Approach

## Results

## Link
- [https://mcplexer.com](https://mcplexer.com)
