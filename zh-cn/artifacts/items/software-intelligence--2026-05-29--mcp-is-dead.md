---
source: hn
url: https://www.quandri.io/engineering-blog/mcp-is-dead
published_at: '2026-05-29T22:56:49'
authors:
- nadis
topics:
- mcp
- claude-code
- developer-tools
- code-agents
- cli-automation
- tool-use
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# MCP is dead?

## Summary
## 总结
文章认为，对于许多开发工具来说，MCP 会带来过高的上下文成本、延迟和工作流脆弱性。若已经有 CLI，文章建议优先使用 CLI/API，再按需加载 Skills。

## 问题
- MCP 会把工具 schema 加载进 LLM 的上下文，所以常用工具在用户真正发起请求前就会占用空间。
- 额外的 MCP 服务进程会增加延迟，也可能在初始化时或会话中途失败。
- 这对软件代理很重要，因为浪费的上下文、更慢的调用和脆弱的工具配置，会减少模型能处理的代码、日志和任务状态。

## 方法
- 作者测量了他们在 Claude Code 配置中加载的 MCP 服务的 JSON 工具 schema，使用了工具名、描述和参数。
- 他们把通过 MCP 查找 Linear issue 的方式和直接用 `curl` 调用 Linear GraphQL API 做了对比。
- 他们提出的机制很简单：先用现有的 CLI 或 API，再把简短的使用说明放进 Claude Skills，这样模型只在需要时才加载它们。
- 在确实有实际需求的场景里，他们仍然保留 MCP，比如没有合适 CLI 的服务、共享认证，或更安全的数据库访问。

## 结果
- 在他们的 4 服务 Claude Code 配置中，MCP 工具定义在任何工具调用前就占用了 10.5% 的上下文窗口。
- 仅 Linear 就加载了 42 个工具定义和约 12,807 个 token，即使任务只需要查一个 issue 也是如此。
- 同样的 Linear issue 查询，用 CLI/API 调用大约消耗 200 个 token，而用 MCP 大约消耗 12,957 个 token，token 开销约增加 65 倍。
- 引用的 Jira 基准测试发现，MCP 每次调用比 REST API 慢 3 倍，算上初始化后，首次调用慢 9.4 倍。
- 在 Quandri 的工作流中，用包装 CLI 的 Skills 替换 MCP 服务后，释放了约 21K 的上下文 token，并消除了他们每天遇到的 MCP 初始化失败。
- 更新说明提到，Claude Code 的 Tool Search with Deferred Loading 现在能把 MCP 上下文使用量降低 85%+，所以上下文膨胀这一结果对当前 Claude Code 用户的适用性弱了很多。

## Problem

## Approach

## Results

## Link
- [https://www.quandri.io/engineering-blog/mcp-is-dead](https://www.quandri.io/engineering-blog/mcp-is-dead)
