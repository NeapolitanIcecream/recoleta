---
source: hn
url: https://github.com/baristaGeek/open-source-postman-for-mcp
published_at: '2026-03-02T23:40:15'
authors:
- baristaGeek
topics:
- mcp
- developer-tools
- code-intelligence
- debugging
- agent-tooling
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Open-Source Postman for MCP

## Summary
这是一个面向 Model Context Protocol（MCP）服务器的开源调试与测试工具，定位类似“Postman for MCP”。它重点解决多数 MCP 服务器依赖 stdio 传输、现有 API 客户端难以可视化调试的问题。

## Problem
- MCP 服务器测试体验差：开发者往往只能在终端里查看 JSON-RPC 日志、手工拼请求，调试成本高。
- 现有工具主要支持 HTTP，但文中声称**90% 的 MCP 服务器使用 stdio**，导致主流 API 客户端无法直接适配最常见场景。
- 缺少 schema 检查、请求历史与重放能力，使开发者难以理解工具参数、复现问题和提高迭代效率。

## Approach
- 提供一个桌面/GUI 风格的 MCP 客户端，统一连接 **stdio、HTTP 和 SSE** 三种传输方式，其中重点支持 stdio 进程管理。
- 通过 **schema inspector + 自动生成表单**，把 MCP 工具的 JSON schema 转成可填写界面，减少手写 JSON-RPC 请求。
- 提供 **请求历史持久化**，将请求保存到 SQLite，并支持一键重放，便于调试和复现。
- 集成基于 Anthropic 的 **AI auto-select**：用户用自然语言描述需求，让模型自动选择工具和参数。
- 系统实现上采用 Next.js 15/React 19、Prisma + SQLite、TypeScript 与 API routes 组织 stdio、HTTP/SSE、历史与总结功能。

## Results
- 该项目的核心成果是交付了一个可运行的开源工具，而不是论文式基准评测；**文中未提供标准数据集、准确率、成功率或速度等定量实验结果**。
- 文中给出的最强定量/具体主张包括：**90% 的 MCP 服务器使用 stdio**，而该工具支持 **3 种传输方式**（stdio、HTTP、SSE）。
- GUI 支持的关键能力包括：自动生成输入表单、完整 JSON schema 查看、请求历史保存到 SQLite、单击重放、错误与 timing 展示。
- 作者声称该工具显著改善了 MCP 开发体验，避免“一个终端跑服务器、另一个终端跑客户端、手工复制 JSON-RPC”的低效流程。
- 当前仍有限制：**SSE transport 目前是 stubbed out**，说明多传输支持尚未完全成熟；后续计划包括导出 collection、环境变量、批处理/脚本请求和桌面应用封装。

## Link
- [https://github.com/baristaGeek/open-source-postman-for-mcp](https://github.com/baristaGeek/open-source-postman-for-mcp)
