---
source: hn
url: https://github.com/agent-browser-io/browser
published_at: '2026-03-02T23:07:05'
authors:
- dokdev
topics:
- browser-agents
- ascii-wireframes
- token-efficiency
- mcp-tools
- playwright
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: AgentBrowser Token-efficient browser for AI agents via ASCII wireframes

## Summary
这是一个面向 AI 智能体的“真实浏览器”控制工具，用 ASCII 线框而非富视觉页面向模型暴露网页，从而降低浏览器交互的 token 成本。它更像工程系统发布而非学术论文，重点在提供统一的 MCP/SDK/CLI 浏览器工具链。

## Problem
- 现有 AI 智能体操作浏览器时，往往依赖截图、HTML 或复杂 DOM/视觉表示，导致上下文很长、token 开销高。
- 高 token 成本会限制多步网页任务的可扩展性与稳定性，尤其是在导航、点击、输入、滚动等反复交互中。
- 需要一种让模型仍能操作真实浏览器、但以更紧凑文本表示页面状态的接口，这对构建实用网页代理很重要。

## Approach
- 核心机制是把网页状态转换成 **ASCII wireframe**：页面上的可交互元素和文本内容被编号并线性化表示，模型通过这些编号理解页面并决定下一步动作。
- 系统仍连接 **真实浏览器**，底层使用 Playwright 执行 `launch`、`navigate`、`click`、`type`、`scroll`、`screenshot` 等操作，因此不是纯模拟环境。
- 它提供统一工具接口，可通过 **MCP** 暴露给 Cursor、Claude Desktop 等客户端，也可通过 **Vercel AI SDK** 直接在代码中调用。
- 交互流程很简单：先启动浏览器，再打开网页，获取 wireframe，随后根据编号元素执行点击、输入、选择等动作。
- 该设计本质上用“紧凑文本 UI”替代“昂贵视觉/页面表示”，以提升代理式浏览的 token 效率。

## Results
- 文本中**没有提供正式论文式定量结果**，没有报告如成功率、token 节省百分比、基准数据集或与其他 browser agent 的数值对比。
- 最强的具体主张是：系统支持一套完整浏览器工具，共 **14 个动作工具**：`launch`、`navigate`、`getWireframe`、`click`、`type`、`fill`、`dblclick`、`hover`、`press`、`select`、`check`、`uncheck`、`scroll`、`screenshot`、`close`（文本列出 15 项名称，覆盖主要浏览操作）。
- 文中给出 Hacker News 的 ASCII 线框示例，其中页面元素被编号到至少 **[137]**，说明该表示可以把较复杂网页压缩成单一文本视图供模型消费。
- 兼容性方面，作者声称可用于 **MCP 客户端**（如 Cursor、Claude Desktop）、**Vercel AI SDK** 与 **CLI**，并要求 **Node 18+**，浏览器自动化基于 **Playwright**。
- 示例代理流程中，模型被限制在 **20 steps** 内（`stepCountIs(20)`）访问 Hacker News、查看前 3 条新闻并总结内容，但这只是使用示例，不构成基准性能证明。

## Link
- [https://github.com/agent-browser-io/browser](https://github.com/agent-browser-io/browser)
