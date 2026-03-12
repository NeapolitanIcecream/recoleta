---
source: hn
url: https://github.com/DimitriBouriez/navagent-mcp
published_at: '2026-03-05T23:36:46'
authors:
- DimitriBouriez
topics:
- web-automation
- mcp
- browser-agent
- token-efficiency
- anti-bot
relevance_score: 0.91
run_id: materialize-outputs
---

# Show HN: NavAgent – CDP-free, token-efficient web automation for AI

## Summary
NavAgent 是一个面向 AI 的超轻量网页自动化方案，用紧凑的编号元素列表替代截图、CDP 或冗长可访问性树，从而降低 token 成本并提升跨站点可用性。它主打本地浏览器、低检测风险和对现代网页结构的广泛兼容，适合作为 MCP 生态中的网页操作基础设施。

## Problem
- 现有 AI 网页自动化常依赖截图或 ARIA/accessibility tree，输入冗长，单页可能消耗约 **2000+ tokens**（截图）或 **15k–20k tokens**（ARIA 树），导致成本高、上下文浪费严重。
- 很多自动化方案依赖 **CDP**，容易暴露自动化痕迹，被 Cloudflare、Akamai 等反爬/反机器人系统识别，影响真实网站可用性。
- 现代网站包含 **SPA、shadow DOM、iframe、contenteditable 富文本编辑器** 等复杂结构，传统网页代理常不稳定或覆盖不全，这对代码智能体和自动化软件生产很重要，因为它们需要可靠地在真实浏览器中执行任务。

## Approach
- 核心机制是：**把网页扫描成“可操作元素的编号列表”给 AI 看**，而不是给整张截图或整棵可访问性树；AI 再通过诸如 `browse_click(6)` 这样的简单动作选择目标元素。
- 系统架构分两部分：**MCP server + Chrome 扩展**。MCP 服务器通过 `stdio` 接入 Claude Code、Cursor、Zed 等客户端，再通过本地 WebSocket 与扩展通信。
- 扩展侧通过 **Chrome 原生扩展消息** `chrome.tabs.sendMessage` 驱动内容脚本扫描 DOM，而**不使用 CDP**；因此不会触发 `navigator.webdriver` 这类典型自动化标记。
- DOM 扫描器会识别强/弱可点击元素，并额外处理 **SPA hash 路由、shadow DOM（强制 open）、同源 iframe 穿透、contenteditable 编辑器、页面区域/landmark 检测**，提高复杂页面上的导航与输入成功率。
- 方案完全在**本地真实浏览器会话**中运行，复用用户 cookies 和登录状态，并声明 **zero telemetry**、仅监听本机 `127.0.0.1`。

## Results
- 论文/项目摘录给出的最明确量化收益是 **token 效率**：相较截图约 **2000+ tokens**、ARIA 树约 **15,000–20,000 tokens**，其编号列表表示更紧凑，但**未提供统一基准上的平均 token 数、压缩比或任务成功率统计**。
- 工程覆盖能力声明包括：支持 **SPAs、shadow DOM、same-origin iframes、contenteditable editors**，并适用于 Amazon 等真实站点展示的导航示例；但**未给出数据集、成功率或对比基线**。
- 反检测能力声明为：因采用 **原生扩展消息而非 CDP**，因此对 Cloudflare、Akamai 等“undetectable/anti-bot-proof”；不过**没有实验设计、误检率或通过率数字**。
- 兼容性声明为：可接入 **Claude Code、Claude Desktop、Cursor、Windsurf、Zed、OpenClaw** 及“any MCP client”，强调其作为通用 MCP 浏览器导航层的可移植性。
- 软件质量方面给出一个具体数字：项目测试为 **111 tests**（`vitest + jsdom`），说明其至少具备一定工程验证，但这**不等同于学术性能指标**。

## Link
- [https://github.com/DimitriBouriez/navagent-mcp](https://github.com/DimitriBouriez/navagent-mcp)
