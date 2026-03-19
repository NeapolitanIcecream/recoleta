---
source: hn
url: https://github.com/LvcidPsyche/auto-browser
published_at: '2026-03-12T23:56:26'
authors:
- Lvcid
topics:
- browser-agent
- mcp
- playwright
- human-in-the-loop
- auth-state
- workflow-automation
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Auto-Browser – An MCP-native browser agent with human takeover

## Summary
Auto-Browser 是一个面向授权网页工作流的开源浏览器代理，把真实浏览器能力直接封装成 MCP 服务器，并支持人在回路中的接管。它的核心价值是让 LLM/代理在脆弱网页流程中不中断地继续工作，同时保留登录态复用、安全审计与受控执行能力。

## Problem
- 现有浏览器自动化或代理工具往往在登录、弹窗、验证码前置验证、复杂多标签页流程中容易失效，而纯自动执行一旦卡住就会丢失上下文或会话。
- 对于内部后台、QA、导出下载、账号复用等授权场景，开发者需要的不只是“自动化”，而是**可恢复、可监督、可审计**的浏览器代理基础设施。
- 很多工具并非原生 MCP，接入 Claude Desktop、Cursor 等 MCP 客户端时需要额外兼容层，增加部署与维护复杂度。

## Approach
- 将“浏览器代理”实现为一个**MCP-native server**：通过 `/mcp` 提供真实 JSON-RPC MCP 传输，也提供 `/mcp/tools` 与 REST 接口，供 MCP 客户端、代理框架或直接脚本调用。
- 底层使用 **Chromium + Playwright + FastAPI**，并返回面向代理的“屏幕感知观察”：截图、可交互元素 ID、DOM/可访问性摘要、可选 OCR 文本，从而让模型基于页面状态行动。
- 当网页流程变脆弱时，使用 **noVNC 人工接管**，让人类在同一会话中手动恢复，再把控制权交回代理，避免“失败后重开”的模式。
- 通过**命名认证配置文件**与加密 auth-state 存储实现“登录一次，后续复用”；并加入 allowlist、上传审批、审计日志、操作员身份、速率限制等安全护栏。
- 支持共享浏览器节点与 `docker_ephemeral` 会话隔离、反向 SSH/远程接管、持久化作业与会话元数据，强调在真实运维环境中的可部署性。

## Results
- 文本**没有提供标准论文式基准数据**，没有报告成功率、任务完成率、延迟或与其他浏览器代理的量化对比。
- 明确给出的工程能力包括：支持 **4 类接入方式/客户端类型**（Claude Desktop、Cursor、任意 MCP JSON-RPC 客户端、直接 REST 调用）。
- MCP 侧明确支持 **6 个 JSON-RPC 能力/方法族**：`initialize`、`notifications/initialized`、`ping`、`tools/list`、`tools/call`、`DELETE /mcp` 会话销毁；并且**拒绝 JSON-RPC batching**。
- 动作层新增并统一到共享 schema 的浏览器能力至少包括 **7 类操作**：`hover`、`select_option`、`wait`、`reload`、`go_back`、`go_forward`，加上已有 click/type 等基础操作。
- 安全与运维方面给出若干具体约束/阈值：生产模式缺少必要安全配置时**启动失败闭锁**；Codex host bridge 请求默认 **55 秒**超时终止；恢复认证状态时执行 `AUTH_STATE_MAX_AGE_HOURS` 过期检查；指标端点可通过 `METRICS_ENABLED=false` 关闭并返回 **404**。
- 最强的实际主张是：通过“**人工登录一次 + 保存 auth profile + 新会话复用已登录状态**”这一流程，系统比普通浏览器自动化更适合日常授权网页工作流，但这是产品性主张而非量化实验结论。

## Link
- [https://github.com/LvcidPsyche/auto-browser](https://github.com/LvcidPsyche/auto-browser)
