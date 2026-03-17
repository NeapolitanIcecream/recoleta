---
source: hn
url: https://github.com/LvcidPsyche/auto-browser
published_at: '2026-03-12T23:56:26'
authors:
- Lvcid
topics:
- mcp
- browser-agent
- human-in-the-loop
- playwright
- auth-session-reuse
- agent-orchestration
relevance_score: 0.95
run_id: materialize-outputs
---

# Auto-Browser – An MCP-native browser agent with human takeover

## Summary
Auto-Browser 是一个面向授权场景的开源浏览器代理系统，把真实浏览器封装成 **MCP 原生服务**，并在自动化失败时支持人工接管。它强调“登录一次、后续复用”、可审计、安全护栏和本地自托管，而不是隐身爬虫或绕过反机器人。

## Problem
- 现有浏览器自动化或 LLM 工具调用在真实网站上常因登录、弹窗、复杂流程、验证码前的人机验证墙或脆弱 UI 流而失效，导致代理无法稳定完成任务。
- 很多系统只是把浏览器“后接”到代理框架里，缺少统一的 MCP 接口、会话持久化、人工接管、审计与审批，难以用于日常授权工作流。
- 对企业/个人实际场景而言，能够安全地复用登录态、在失败时不中断会话并保持可追踪性很重要，因为这直接决定了浏览器代理是否能进入生产辅助流程。

## Approach
- 核心机制是把浏览器代理实现成一个 **MCP server**：控制层用 FastAPI + Playwright 驱动 Chromium，会向模型暴露统一工具接口，也可通过 REST 或 MCP JSON-RPC 调用。
- 系统通过“观察 + 动作”循环工作：返回截图、可交互元素 ID、DOM/可访问性摘要、可选 OCR 文本，让模型基于屏幕和页面结构做点击、输入、悬停、选择、等待、翻页等操作。
- 当网页流程变脆弱或需要人工处理时，使用 noVNC 进行 **human takeover**，让人直接接管同一个浏览器会话，处理完后再继续自动化，不丢失上下文。
- 为了支持“登录一次、后续复用”，系统可保存加密的 auth state 和命名 auth profiles，并在新会话中恢复；同时提供主机白名单、上传审批、操作员身份头、审计日志、指标与持久化作业记录。
- 对更强隔离需求，支持 docker_ephemeral 的每会话浏览器隔离、独立 noVNC 端口、可选 reverse-SSH 远程接入，以及 CLI/API 两种模型提供方接入方式。

## Results
- 文本**没有提供标准基准数据集上的量化指标**，也没有报告成功率、延迟、成本或与其他浏览器代理的公开对比数值。
- 论文/项目给出的最强实证性主张是可运行的端到端能力：支持 **Claude Desktop、Cursor、任意 MCP JSON-RPC 客户端、直接 REST 调用**，并提供真实 MCP 传输端点 `/mcp` 与便捷工具端点 `/mcp/tools`、`/mcp/tools/call`。
- 提供多种可验证的 smoke 测试流程，例如 `make doctor`、`make release-audit`，以及用于 **reverse-SSH、隔离会话、隔离会话隧道** 的脚本化冒烟测试；文中说明这些测试会校验 `/readyz`、创建会话、observe、agent-step、远程 noVNC 连通性、隔离容器清理等具体流程。
- 在接口能力上，系统明确支持 **1-step 和 multi-step agent orchestration**、后台持久化 job、会话级下载捕获、标签页控制、社交页面辅助、上传审批闸门、Prometheus 风格 `/metrics`，这些构成了其相较“纯 Playwright 脚本”更完整的代理基础设施。
- 最突出的应用示例是 Outlook：**登录一次并保存为 `outlook-default` 配置，之后新会话直接从该 auth profile 恢复**，作为“比普通浏览器自动化更有用”的核心演示，但未给出成功率或时间节省数字。

## Link
- [https://github.com/LvcidPsyche/auto-browser](https://github.com/LvcidPsyche/auto-browser)
