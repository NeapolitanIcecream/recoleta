---
source: arxiv
url: http://arxiv.org/abs/2604.06392v1
published_at: '2026-04-07T19:22:20'
authors:
- Varun Pratap Bhardwaj
topics:
- multi-agent-orchestration
- agent-operating-system
- llm-routing
- agent-evaluation
- agent-interoperability
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Qualixar OS: A Universal Operating System for AI Agent Orchestration

## Summary
## 摘要
Qualixar OS 是一个应用层操作系统，用于在多个模型提供商、代理框架和传输方式之间运行异构 AI 代理团队。论文称它覆盖面广，提供内置质量控制，并且在自定义基准上实现了很低的任务执行成本。

## 问题
- 多代理 AI 开发分散在 AutoGen、CrewAI、MetaGPT 和 LangGraph 等框架中，代理在不同系统之间迁移时往往需要重写。
- 文中提到的现有系统要么侧重内核层面的代理调度，要么只支持单一框架，缺少跨提供商路由、质量保证、成本跟踪和运维工具等部分。
- 这很重要，因为论文将薄弱的治理和对 AI 输出的低信任与项目失败风险联系起来，尤其是在生产环境中使用的代理系统里。

## 方法
- 该系统是一个应用层运行时，通过一个确定性的 12 步流水线来编排代理团队：预算检查、记忆注入、自动团队设计、安全检查、基于拓扑的执行、基于裁判的评估、重设计循环、RL 更新以及最终持久化。
- Forge 将自然语言任务转换为代理团队，方式是选择角色、拓扑、工具和模型分配；论文列出了 12 种支持的拓扑，包括 grid、forest、mesh、辩论式和 maker 模式。
- 模型路由使用三层结构：epsilon-greedy contextual bandit 选择一种路由策略，策略再选择模型，其中一种策略使用 Bayesian POMDP 在不确定条件下做选择。模型目录在运行时通过查询 10 家提供商的 API 构建。
- 质量控制结合了 8 个模块，包括共识裁判、通过跨模型熵监控进行 Goodhart 检测、使用 Jensen-Shannon divergence 阈值 Θ = 0.877 的漂移检查、行为契约，以及在重复失败后升级给人工处理的有界重设计循环。
- 互操作性来自 Claw Bridge 和 Universal Command Protocol，它们可跨 8+ 代理框架、MCP 和 A2A 协议，以及 7 种传输方式工作，例如 HTTP、MCP、CLI、WebSocket、Slack、Discord 和 Telegram。

## 结果
- 论文称 Qualixar OS 通过了 2,821 个测试用例验证，覆盖 217 种事件类型和 8 个质量模块。
- 在一个自定义的 20 任务评测套件上，它报告准确率为 100%，平均每个任务成本为 $0.000039。
- 该运行时称可兼容 10 家 LLM 提供商、8+ 代理框架和 7 种通信传输方式。
- 据称，实时发现子系统会在启动时从 10 家提供商构建一个包含 236+ 模型的目录。
- 仪表板包含 24 个标签页、一个具有 9 种节点类型的工作流构建器，以及一个预置了 25 个官方条目的市场。
- 摘录没有给出 Qualixar OS 本身在 GAIA、SWE-Bench 或 HumanEval 等标准基准上相对于具名基线的结果，因此这里最强的定量证据是自定义 20 任务套件和系统测试计数。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.06392v1](http://arxiv.org/abs/2604.06392v1)
