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
wkdomains 是一款 macOS 浏览器，让人类在已登录的实时页面上操作，同时让编码代理通过 API 读取结构化的本地浏览器状态。它的主要价值在于缩小人类在浏览器里看到的内容和代理能检查到的内容之间的差距。

## 问题
- 编码代理经常需要页面上下文、登录状态、网络请求、DOM 结构和域名元数据，但截图不完整，Playwright 流程又要求代理重建整个浏览会话。
- 使用 Codex、Claude Code、Cursor 或类似工具的开发者，需要一种方式把自己正在看的准确页面状态共享出去，而不用在浏览器、终端和聊天之间来回复制数据。
- 这对 Web 调试、API 发现、UI 排查和已认证请求回放很重要，因为缺少浏览器上下文时，代理很容易靠猜。

## 方法
- 这个应用把浏览控制权留在人类手里，并通过本地 API 暴露当前页面状态，默认地址是 `http://localhost:9001`。
- 代理可以请求截图、URL 和 viewport 数据、可见 DOM、链接、控制台消息、资源、XHR/fetch 摘要，以及 cookies、localStorage 和 sessionStorage。
- 当代理终端打开时，wkdomains 会扫描 `/llms.txt`、`/openapi.json`、`/.well-known/agent-card.json`、`/sitemap.xml` 和 `/robots.txt` 这类域名入口点。
- 右侧的浏览器终端会把人类问题作为 MCP human requests 发送出去，这样另一个监听代理就可以检查页面并在应用内回复。
- viewport 模式会改变 API 报告的内容，包含桌面模式，以及 700 px 和 390 px 的移动宽度。

## 结果
- 摘要里没有基准测试、用户研究、延迟结果、准确率指标，也没有和 Playwright、浏览器 DevTools 或仅代理浏览方式的对比。
- 通过示例可以看到，这个系统至少暴露了 8 个命名的本地 API 路由：`/screenshot`、`/page`、`/dom`、`/links`、`/console`、`/resources`、`/xhr` 和 `/cookies`。
- 它会检查 9 个可能给代理或开发者使用的入口点：`/llms.txt`、`/llms-full.txt`、`/openapi.json`、`/swagger.json`、`/.well-known/openapi.json`、`/.well-known/ai-plugin.json`、`/.well-known/agent-card.json`、`/sitemap.xml` 和 `/robots.txt`。
- 界面可以把窗口分成 75% 的浏览器区域和 25% 的终端面板，用来处理页面感知的代理问题。
- 它支持通过更改端口运行多个应用实例，示例里用了默认的 `9001` 和第二个实例的 `9003`。
- 最明确的具体结论是工作流支持：人类可以保持登录并正常浏览，而监听代理可以读取实时页面数据、网络结构、存储内容和发现的域文件，不用重建登录流程。

## Problem

## Approach

## Results

## Link
- [https://github.com/wkdomains/macos-app](https://github.com/wkdomains/macos-app)
