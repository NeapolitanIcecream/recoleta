---
source: hn
url: https://root-ai.beehiiv.com/p/build-a-deep-data-mcp-server-to-connect-llms-to-your-local-database-in-10min
published_at: '2026-03-10T23:15:02'
authors:
- mehdikbj
topics:
- model-context-protocol
- llm-tools
- local-database
- sqlite
- rag
- typescript
relevance_score: 0.05
run_id: materialize-outputs
---

# Build a "Deep Data" MCP Server to Connect LLMs to Your Local Database

## Summary
这篇文章不是学术论文，而是一篇实操教程，演示如何用 MCP（Model Context Protocol）把本地 SQLite 数据库安全地接到 Claude 或 Cursor 这类 LLM 客户端上。核心价值是让模型通过标准化工具调用访问私有本地数据，而不必手写定制 REST API 或把数据上传到云端。

## Problem
- LLM 本身不知道公司内网、本地文件系统或内部数据库里的实时/私有信息，因此无法直接回答依赖这些数据的问题。
- 传统做法往往需要手写脆弱的 REST API，并依赖模型正确构造 JSON 请求，工程复杂且容易出错。
- 对很多企业和个人场景来说，**在不上传私有数据到云端的前提下**让 LLM 访问本地数据很重要，因为这关系到安全、隐私和可落地性。

## Approach
- 用 MCP 作为 LLM 与本地资源之间的标准协议，文中将其类比为 AI 与本地数据之间的“USB-C”。
- 搭建一个本地 TypeScript MCP server，并通过 `stdio` 与 Claude Desktop / Cursor 内置的 MCP client 通信。
- 在服务器中定义一个工具 `query_users_by_role`，并用严格的 `inputSchema` 限定模型只能传入合法参数（这里是 `role` 字符串）。
- 工具执行时，把模型传来的参数映射为参数化 SQLite 查询 `SELECT * FROM users WHERE role = ?`，再把结果转成文本/JSON 返回给模型。
- 通过客户端配置文件注册该本地服务后，LLM 就能在对话中自动发现工具、提取参数、调用本地脚本并整合数据库结果生成自然语言回答。

## Results
- 文中给出的是**工程演示结果**，不是标准研究实验；**没有提供系统化基准、数据集评测或量化指标**。
- 具体示例中，数据库包含 **3 条用户记录**，字段为 `id/name/role/active`，角色示例包括 `Admin`、`Developer`、`DevOps`。
- 演示工具支持按角色查询：当用户询问“active Admin”时，模型会抽取参数并调用工具，传入 `{"role":"Admin"}`。
- 示例返回显示系统能从本地库中找到 **1 名 Admin：Alice Cyber**，并由 Claude 生成为自然语言回答。
- 文章声称该方案可在 **约 10 分钟**内搭建完成，并实现“**不上传一字节私有数据库到云端**”的本地 RAG/工具调用流程。
- 代码中 MCP server 版本标记为 **2.0.0**，技术栈包括 Node.js、TypeScript、官方 MCP SDK 与 SQLite3。

## Link
- [https://root-ai.beehiiv.com/p/build-a-deep-data-mcp-server-to-connect-llms-to-your-local-database-in-10min](https://root-ai.beehiiv.com/p/build-a-deep-data-mcp-server-to-connect-llms-to-your-local-database-in-10min)
