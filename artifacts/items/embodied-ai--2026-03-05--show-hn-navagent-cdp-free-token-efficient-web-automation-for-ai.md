---
source: hn
url: https://github.com/DimitriBouriez/navagent-mcp
published_at: '2026-03-05T23:36:46'
authors:
- DimitriBouriez
topics:
- web-automation
- browser-agent
- token-efficiency
- anti-bot
- mcp
- chrome-extension
relevance_score: 0.08
run_id: materialize-outputs
---

# Show HN: NavAgent – CDP-free, token-efficient web automation for AI

## Summary
NavAgent 是一个面向 AI 的轻量级网页自动化工具，用紧凑的编号元素列表替代截图或冗长可访问性树，从而显著降低上下文 token 成本。它通过 Chrome 扩展原生消息机制而非 CDP 实现浏览器控制，主打更强的反检测能力与更广的网站兼容性。

## Problem
- 现有 AI 网页自动化常依赖截图或 ARIA/accessibility tree，导致上下文非常臃肿，增加 token 成本并拖慢代理决策。
- 很多方案基于 CDP，容易暴露自动化特征，被 Cloudflare、Akamai 等反爬/反机器人系统识别。
- 现代网站包含 SPA、shadow DOM、iframe 和富文本编辑器，常让通用网页代理失效或不稳定；这很重要，因为真实世界网页操作正需要在这些复杂前端环境中稳定执行。

## Approach
- 核心机制是：不把网页作为图像或整棵可访问性树交给模型，而是扫描 DOM，提取可交互元素，压缩成带编号的简短列表，让模型只需输出类似 `browse_click(6)` 的动作。
- 系统由两个必需组件组成：本地运行的 `navagent-mcp` 服务器与 Chrome 扩展；MCP 客户端通过 stdio 连接本地服务器，再经 localhost WebSocket 与扩展通信，扩展用 `chrome.tabs.sendMessage` 驱动内容脚本扫描和操作页面。
- 为覆盖复杂网页，它支持 SPA hash 路由、强制打开并遍历 shadow DOM、跨 same-origin iframe 访问、以及对 DraftJS/ProseMirror 等 `contenteditable` 编辑器使用 `execCommand('insertText')` 输入文本。
- 为提高元素发现率，它结合强可点击规则（如 `<a>`、`<button>`、ARIA interactive roles、`tabindex>=0`）与弱可点击启发式（如 `cursor:pointer`、`data-*`、框架点击指令），并加入 landmarks/zone detection 与扫描后的 `querySelectorAll` 安全回退。
- 为降低被检测风险，它避免 CDP，不触发 `navigator.webdriver` 标志，强调使用原生扩展消息、真实本地浏览器会话、用户自己的 cookies/logins，以及零遥测。

## Results
- 文中给出的最明确量化收益是 token 效率：编号列表方式相对截图可避免约 **2000+ tokens** 的输入，相对 ARIA/accessibility trees 可避免约 **15k-20k tokens** 的输入，但未提供标准化基准测试或端到端任务成功率。
- 工程验证方面，项目声称有 **111 tests**（`vitest + jsdom`），说明作者对实现做了基础测试覆盖，但这不是学术基准结果。
- 兼容性声明包括：可用于 **任意网站**，支持 **SPAs、shadow DOM、same-origin iframes、contenteditable editors**，并兼容多种 MCP 客户端（如 Claude Code、Claude Desktop、Cursor、Windsurf、Zed、OpenClaw）。
- 反检测声明包括：因使用 Chrome 原生扩展消息而非 CDP，系统声称对 **Cloudflare、Akamai** 等“undetectable/anti-bot-proof”，但文摘未提供实验设置、检测通过率或对照基线数据。
- 安全与部署方面的具体可核实信息包括：WebSocket 默认端口 **61822**、仅监听 **127.0.0.1**，扩展最小权限为 `activeTab`、`storage`、`alarms`，且声称 **zero telemetry**。

## Link
- [https://github.com/DimitriBouriez/navagent-mcp](https://github.com/DimitriBouriez/navagent-mcp)
