---
source: hn
url: https://github.com/agent-browser-io/browser
published_at: '2026-03-02T23:07:05'
authors:
- dokdev
topics:
- browser-automation
- ai-agents
- token-efficiency
- ascii-ui
- mcp-tools
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: AgentBrowser Token-efficient browser for AI agents via ASCII wireframes

## Summary
AgentBrowser 是一个面向 AI 代理的真实浏览器控制工具，用 ASCII 线框而不是完整网页内容来表示页面，从而降低 token 消耗。它主要服务于 MCP 客户端和 Vercel AI SDK 场景，让代理能以更轻量的方式执行网页导航与交互。

## Problem
- 现有 AI 代理操作浏览器时，通常需要处理完整 DOM、截图或富文本页面表示，导致 **token 开销高**、上下文浪费严重。
- 对需要多步网页操作的代理任务来说，高成本页面表示会限制可扩展性、响应速度和自动化稳定性。
- 这很重要，因为浏览器交互是代码代理、自动化助手和通用软件代理执行真实世界任务的关键接口。

## Approach
- 核心机制是把网页转成带编号的 **ASCII wireframe**：链接、按钮、文本等元素以简化文本形式呈现，代理通过编号理解页面并执行点击、输入、滚动等动作。
- 系统暴露一组统一浏览器工具，如 `launch`、`navigate`、`getWireframe`、`click`、`type`、`scroll`、`screenshot` 等，让模型按工具调用序列完成任务。
- 实际浏览器执行由 **Playwright** 后端驱动，因此代理控制的仍是真实浏览器，而不是模拟页面。
- 提供两种主要集成方式：一是通过 **MCP** 接入 Cursor、Claude Desktop 等客户端；二是通过 **Vercel AI SDK** 以工具形式嵌入应用。

## Results
- 文本没有提供标准学术评测、基准数据或消融实验，因此 **没有量化结果** 可用于比较性能提升幅度。
- 最强的具体主张是：该系统能以 **token-efficient** 的方式让 AI 代理控制真实浏览器，并通过 ASCII 线框完成导航、点击、输入、悬停、选择、勾选、滚动、截图和关闭等操作。
- 提供的工具集合至少包括 **14 个操作**：`launch`、`navigate`、`getWireframe`、`click`、`type`、`fill`、`dblclick`、`hover`、`press`、`select`、`check`、`uncheck`、`scroll`、`screenshot`、`close`。
- 文中给出一个最多 **20 步** 的示例代理工作流（`stopWhen: stepCountIs(20)`），展示模型可访问 Hacker News、打开前 3 条新闻并总结内容，但这只是用法示例，不是正式实验结果。
- 兼容环境方面，项目要求 **Node 18+**，并声明可通过 MCP 在 Cursor/Claude Desktop 中经由 JSON-RPC over stdio 使用。

## Link
- [https://github.com/agent-browser-io/browser](https://github.com/agent-browser-io/browser)
