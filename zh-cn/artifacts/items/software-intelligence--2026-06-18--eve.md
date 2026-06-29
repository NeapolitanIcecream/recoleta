---
source: hn
url: https://vercel.com/blog/introducing-eve
published_at: '2026-06-18T23:23:48'
authors:
- gmays
topics:
- agent-runtime
- software-agents
- human-in-the-loop
- multi-agent-systems
- developer-tools
- evals
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Eve

## Summary
## 摘要
Eve 是一个开源 TypeScript 智能体运行时，把一个智能体组织成一个文件目录，并提供持久会话、沙箱、审批、渠道、追踪和评测。它的主要价值是让构建大量智能体的团队少写自定义生产代码。

## 问题
- 团队会为状态、工具、凭据、日志、部署、审批和渠道集成反复重建同一类智能体基础设施。
- 智能体经常要处理长任务、慢系统和人工审批，因此崩溃、部署和不安全操作都可能破坏生产使用。
- 这一点很重要，因为 Vercel 称，智能体现在触发了其平台约 29% 的部署，一年前这一比例低于 3%。

## 方法
- 一个智能体就是一个目录：`agent.ts` 设置模型，`instructions.md` 设置行为，`tools/` 存放带类型的 TypeScript 工具，`skills/` 存放 Markdown 知识，`subagents/` 存放被委派的智能体，`channels/` 存放集成，`schedules/` 存放 cron 任务。
- 每段对话都作为带步骤检查点的持久工作流运行，因此它可以暂停，在崩溃或部署后继续，并从同一点恢复。
- 智能体编写的代码在隔离沙箱中运行，部署时使用 Vercel Sandbox，本地使用 Docker、microsandbox 或 shell 适配器。
- 工具操作可以要求人工审批；Eve 会暂停且不占用计算资源，直到有人批准后再恢复。
- 连接使用 MCP 或 OpenAPI 文件并配合代理式认证，运行过程会输出 OpenTelemetry 追踪，并使用基于文件的评测支持本地和 CI 测试。

## 结果
- Vercel 称其在 Eve 上运行了 100 多个生产智能体，这些智能体现在共用一个 monorepo、约定、可观测性和升级路径。
- 其内部数据分析智能体每月在 Slack 中处理 30,000 多个问题，数据仓库访问权限按提问者的权限限定。
- Lead Agent 每年运行成本约为 5,000 美元，带来 32 倍于该金额的回报，并由一名兼职工程师维护。
- Athena 由 RevOps 在没有工程师参与的情况下用 6 周构建完成，发布后 pipeline 覆盖率接近翻倍。
- Vertex 自行解决 92% 的支持工单，并升级处理其余工单。
- Vercel 称，CLI 可以生成第一个智能体脚手架，并在不到 1 分钟内启动可运行的开发服务器。

## Problem

## Approach

## Results

## Link
- [https://vercel.com/blog/introducing-eve](https://vercel.com/blog/introducing-eve)
