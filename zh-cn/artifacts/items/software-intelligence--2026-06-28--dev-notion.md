---
source: hn
url: https://www.notion.com/product/dev
published_at: '2026-06-28T23:00:48'
authors:
- handfuloflight
topics:
- agent-workflows
- human-ai-interaction
- developer-tools
- workflow-automation
- external-agent-api
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# /Dev/Notion

## Summary
## 摘要
/Dev/Notion 将 Notion 描述为一个共享工作区，人类团队可以在其中调用、监督并扩展 AI 代理。它的主要说法是，代理、Notion 页面、数据库、工作流和外部 API 可以通过 Notion 托管的 Workers 和代理界面协同工作。

## 问题
- 团队通常把 AI 代理、文档、项目任务、SaaS 数据和审批流程放在不同工具中，这让代理工作难以跟踪和治理。
- 工程团队需要把代理连接到实时公司数据和 API 的方式，同时不必在自有基础设施上运行每一个同步、工具或工作流。
- 该产品的意义在于，代理输出如果能在团队分配任务、审查工作和存储上下文的同一工作区内执行操作，就会更有用。

## 方法
- Notion 允许用户在页面、评论或直接聊天中 @mention 代理，因此代理可以在与队友相同的位置接收工作任务。
- Notion Workers 在 Notion 基础设施上运行隔离的代码沙箱，用于数据同步、自定义工具和工作流。
- Workers 可以使用声明式 schema 和持久游标，持续将外部记录 upsert 到 Notion 数据库中。
- 开发者可以编写工具，让 Notion Agents 生成资产、查询实时数据、调用外部 API，并响应传入的 webhook。
- Claude、Cursor、Decagon 等外部代理或内部自建代理，可以通过 API 接入，并使用触发器、工具、权限、多轮线程和实时流式响应。

## 结果
- 摘录未提供量化结果、基准测试、延迟数字、可靠性数据或用户研究结果。
- 它声称代理可以作为一等协作者，在 Notion 页面、评论、聊天、任务、数据库和工作流中使用。
- 它声称 Notion Workers 让团队无需在自有服务器上托管同步、工具和工作流背后的代码。
- 它声称外部代理可以通过共享触发器、工具、权限、审查流程和审批点接入 Notion。
- 它声称编码代理可以使用节省 token 的命令，向 Workers 运行时构建和部署同步与工具。

## Problem

## Approach

## Results

## Link
- [https://www.notion.com/product/dev](https://www.notion.com/product/dev)
