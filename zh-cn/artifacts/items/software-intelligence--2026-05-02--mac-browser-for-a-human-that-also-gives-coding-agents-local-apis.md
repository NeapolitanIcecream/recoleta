---
source: hn
url: https://github.com/wkdomains/macos-app
published_at: '2026-05-02T23:12:14'
authors:
- fcpguru
topics:
- coding-agents
- browser-automation
- mcp
- human-ai-interaction
- code-intelligence
- developer-tools
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Mac browser for a human that also gives coding agents local APIs

## Summary
## 摘要
wkdomains 是一个 macOS 浏览器，让人类在使用实时、已登录页面的同时，让编程代理通过 API 读取结构化的本地浏览器状态。它的主要价值是缩小人类在浏览器中看到的内容与代理可检查内容之间的差距。

## 问题
- 编程代理经常需要页面上下文、登录状态、网络调用、DOM 结构和域名元数据，但单靠截图并不完整，Playwright 流程又要求代理重新创建浏览会话。
- 使用 Codex、Claude Code、Cursor 或类似工具的开发者，需要一种方式共享自己正在查看的确切页面状态，而无需在浏览器、终端和聊天之间复制数据。
- 这对 Web 调试、API 发现、UI 排查和已认证请求重放很有用；缺少浏览器上下文时，代理可能会猜测。

## 方法
- 该应用让浏览保持在人类控制下，并通过本地 API 暴露当前页面状态，默认地址为 `http://localhost:9001`。
- 代理可以请求截图、URL 和视口数据、可见 DOM、链接、控制台消息、资源、XHR/fetch 摘要、cookies、localStorage 和 sessionStorage。
- wkdomains 会在代理终端打开时扫描域名入口点，例如 `/llms.txt`、`/openapi.json`、`/.well-known/agent-card.json`、`/sitemap.xml` 和 `/robots.txt`。
- 右侧浏览器终端会把人类问题作为 MCP human requests 发送，因此单独的 watcher agent 可以检查页面并在应用内回复。
- 视口模式会改变 API 返回的内容，包括桌面模式，以及 700 px 和 390 px 的移动端宽度。

## 结果
- 摘录没有报告基准测试、用户研究、延迟结果、准确率指标，也没有与 Playwright、浏览器 DevTools 或纯代理浏览进行比较。
- 示例显示该系统至少暴露了 8 个具名本地 API 路由：`/screenshot`、`/page`、`/dom`、`/links`、`/console`、`/resources`、`/xhr` 和 `/cookies`。
- 它会检查 9 个可能的代理或开发者入口点：`/llms.txt`、`/llms-full.txt`、`/openapi.json`、`/swagger.json`、`/.well-known/openapi.json`、`/.well-known/ai-plugin.json`、`/.well-known/agent-card.json`、`/sitemap.xml` 和 `/robots.txt`。
- 界面可以把窗口分成 75% 的浏览器区域和 25% 的终端面板，用于提出与页面相关的代理问题。
- 它支持通过更改端口运行多个应用实例，示例使用默认的 `9001`，第二个实例使用 `9003`。
- 最具体的有力主张是对工作流的支持：人类可以保持登录并正常浏览，同时 watcher agent 读取实时页面数据、网络结构、存储和发现的域名文件，而无需重建登录流程。

## Problem

## Approach

## Results

## Link
- [https://github.com/wkdomains/macos-app](https://github.com/wkdomains/macos-app)
