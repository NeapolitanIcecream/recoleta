---
source: hn
url: https://github.com/baristaGeek/open-source-postman-for-mcp
published_at: '2026-03-02T23:40:15'
authors:
- baristaGeek
topics:
- model-context-protocol
- developer-tools
- api-testing
- stdio-transport
- debugging
relevance_score: 0.05
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Open-Source Postman for MCP

## Summary
这是一个面向 Model Context Protocol（MCP）服务器的开源调试与测试工具，定位为“Postman for MCP”。它重点解决现有 API 客户端对 stdio 型 MCP 服务器支持差、可视化与调试体验不足的问题。

## Problem
- MCP 服务器测试流程繁琐：开发者常需手动查看 JSON-RPC 日志、反复输入请求、在多个终端之间切换。
- 现有 API 工具大多偏向 HTTP，而文中明确指出**大多数 MCP 服务器使用 stdio 传输**，导致主流工具难以直接适配。
- 缺少模式检查、请求历史与可视化表单，使得理解工具参数、复现请求和排查失败都很低效，这会拖慢 MCP 生态开发与调试。

## Approach
- 提供一个桌面风格 GUI，统一连接 **stdio、HTTP 和 SSE** 三类 MCP 传输方式，其中尤其强调对 stdio 的原生支持。
- 读取工具 schema，并自动生成输入表单与 schema inspector，让用户无需翻源码就能知道参数要求。
- 内置请求执行、响应查看、错误显示、耗时展示，以及基于 SQLite 的请求历史保存与一键重放。
- 加入 AI 辅助能力：用户可用自然语言描述意图，由 Claude 自动选择工具和参数，并支持总结功能。
- 系统实现上基于 Next.js 15、React 19、Prisma、SQLite、TypeScript 与 Anthropic SDK，后端路由分别处理 stdio 进程管理、HTTP/SSE 转发、历史记录与摘要。

## Results
- 文本**没有提供正式基准测试、用户研究或定量实验结果**，因此没有可报告的准确率、速度提升或与基线工具的数值比较。
- 最强的具体功能性结论是：该工具声称可连接 **3 种传输**（stdio、HTTP、SSE），并将 stdio 作为核心支持对象，而作者认为这是现有 API 客户端普遍缺失的能力。
- 工具提供了 **1-click** 请求执行与 **1-click replay** 历史重放，目标是显著减少手工复制 JSON-RPC 负载与重复输入参数的工作量，但文中未量化节省比例。
- 文中明确指出 **SSE transport 当前仍是 stubbed out（未完整实现）**，因此多传输支持虽被宣称，但完成度并不完全一致。
- 作者的核心主张是它补齐了 MCP 生态缺失的开发者工具链，可作为 MCP 服务器测试、调试、探索 schema 与回放请求的标准化入口，但这仍属于产品宣称而非论文式实证结果。"

## Link
- [https://github.com/baristaGeek/open-source-postman-for-mcp](https://github.com/baristaGeek/open-source-postman-for-mcp)
