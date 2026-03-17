---
source: hn
url: https://hantverkskod.se/2026/03/01/saaspocalypse/
published_at: '2026-03-10T23:10:46'
authors:
- mosura
topics:
- agent-memory
- developer-tools
- agentic-coding
- event-sourcing
- multi-agent
- saas-disruption
relevance_score: 0.89
run_id: materialize-outputs
---

# SaaSpocalypse Now

## Summary
这篇文章主张：生成式 AI 显著降低了“自己做一个工具”相对于购买 SaaS 的门槛，并用作者自建的 Shelby 作为例子说明如何为 agentic coding 提供更可控的项目记忆。核心观点不是提出新模型，而是展示一种轻量、可本地嵌入仓库的代理工作流基础设施。

## Problem
- 文章要解决的是 **agentic AI 开发中的上下文与记忆管理问题**：项目状态散落在任意 Markdown 文件中，既不结构化，也难长期维护。
- 这很重要，因为代理需要反复解析大量全局文档才能理解任务背景，造成低效、脆弱，并且随着项目增长更难扩展。
- 作者还隐含指出一个更大的产业问题：当 AI 让定制化开发变便宜时，很多售卖固定工作流的软件产品可能失去价值。

## Approach
- 核心方法很简单：把“做过什么、决定了什么”都记录到一个**追加写入的 JSONL 事件日志**里，而不是依赖零散 Markdown；作者把这些记录称为 *mementos*。
- 每次运行 Shelby 命令时，先**回放 event log 重建当前状态**，从而得到项目的最新结构化记忆。
- 当代理要处理某个任务时，使用 `shelby context <id-or-alias>` **按任务即时生成所需上下文**，避免代理去全局文档里盲目检索。
- 工具被做成**单个自包含可执行文件**，可直接放入任意项目；首次使用时通过 `shelby help agent` 指导在 `AGENTS.md` 中建立开发循环。
- 设计上还考虑了**多并行代理**，虽然作者表示这一点尚未真正投入使用。

## Results
- 文中没有提供标准学术基准、公开数据集或与其他系统的定量对比结果。
- 最具体的工程结果是：作者在 **7 个晚上**内完成 Shelby，实现规模为 **5168 行 Rust 代码**。
- 测试覆盖方面，文中给出 **120 个单元测试** 和 **60 个集成测试**。
- 作者声称 Shelby 已经达到可用状态，并且正在用于“**用 Shelby 开发 Shelby**”，这是最强的实际验证案例。
- 定性结论是：结构化事件日志比随机 Markdown 更适合作为 agent memory；当前代理编程的主要瓶颈不是能力而是**速度**，因此后续方向会转向**多代理编排**。

## Link
- [https://hantverkskod.se/2026/03/01/saaspocalypse/](https://hantverkskod.se/2026/03/01/saaspocalypse/)
