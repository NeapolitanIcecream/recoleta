---
source: hn
url: https://pypi.org/project/toolnexus/
published_at: '2026-07-01T22:59:33'
authors:
- muthuishere
topics:
- llm-agents
- mcp
- agent-tools
- a2a
- multi-agent-systems
- developer-tools
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Toolnexus for Python – MCP, agent skills,a2a for any LLM

## Summary
## 摘要
Toolnexus 是一个 Python 工具包，通过一个统一的工具接口，把 LLM Agent 连接到 MCP 服务器、本地 skills、自定义函数、HTTP 端点、内置工具和 A2A Agent。它面向需要小型 Agent 运行时的开发者，支持流式输出、重试、记忆、指标，以及跨模型提供商的工具执行。

## 问题
- LLM Agent 经常需要同时使用多种工具来源：MCP 服务器、本地 skills、自定义代码、REST API、Shell 和文件工具，以及同级 Agent。
- 团队需要同一套 Agent 代码能在 OpenAI 风格、Anthropic 风格、OpenRouter、Gemini schema adapter 和本地执行循环中工作。
- 生产使用需要围绕远程 Agent 提供记忆、流式输出、重试、指标和故障隔离。

## 方法
- `create_toolkit(...)` 从 `mcp.json`、`skills/` 文件夹、Python 函数、HTTP 端点、10 个内置工具和远程 A2A Agent Card 加载工具。
- `create_client(...)` 指向 OpenAI 或 Anthropic 风格的端点，并运行一个循环：发送工具 schema、执行工具调用，然后返回 `RunResult`。
- `ask(prompt, tk, id=...)` 通过 `ConversationStore` 存储和重新加载转录；`stream(...)` 发出文本和工具事件，并在完成时保存线程。
- A2A 支持通过 JSON-RPC 2.0 子集暴露 `SKILL.md` skills，包含 Agent Card discovery、`SendMessage` 和 `GetTask`；出站 A2A skills 会显示为工具。
- 指标通过 `on_metric` 回调和 Prometheus 文本暴露，不依赖第三方依赖。

## 结果
- 摘录没有报告基准、准确率、延迟、可靠性或用户研究结果。
- 它声称使用默认内置工具时，可以用 5 行代码构建一个可工作的 Agent。
- 它包含 10 个内置工具：`bash`、`read`、`write`、`edit`、`grep`、`glob`、`webfetch`、`question`、`apply_patch` 和 `todowrite`。
- Python 包版本为 0.4.0，支持 Python 3.11 或更新版本，并发布 117.4 kB 源码归档和 53.2 kB wheel。
- 它声称 5 种语言移植版具有相同的库行为：Python、JavaScript、Go、Java 和 C#。
- v1 中的 A2A 支持有限：包含 JSON-RPC 2.0、Agent Card discovery、`SendMessage` 和轮询 `GetTask`；不包含流式输出、推送和认证。

## Problem

## Approach

## Results

## Link
- [https://pypi.org/project/toolnexus/](https://pypi.org/project/toolnexus/)
