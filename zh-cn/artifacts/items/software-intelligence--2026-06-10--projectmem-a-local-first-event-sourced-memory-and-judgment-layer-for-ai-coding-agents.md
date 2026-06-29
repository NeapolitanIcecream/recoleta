---
source: arxiv
url: https://arxiv.org/abs/2606.12329v1
published_at: '2026-06-10T17:02:56'
authors:
- Ripon Chandra Malo
- Tong Qiu
topics:
- code-intelligence
- ai-coding-agents
- project-memory
- mcp
- event-sourcing
- agent-guardrails
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# PROJECTMEM: A Local-First, Event-Sourced Memory and Judgment Layer for AI Coding Agents

## Summary
## 概要
PROJECTMEM 为 AI 编码代理加入了持久化项目记忆和一个确定性的行动前警告层。它针对的是在编码会话中反复出现的失败修复和重复的上下文重建。

## 问题
- AI 编码代理在会话之间会丢失项目特定状态，因此它们会重新读取文件、重新推导决策，并且可能再次尝试已经失败过的修复。
- 论文估计，重建项目上下文每个会话可能需要 5,000-20,000 个 token，这会增加成本并浪费时间。
- 反复失败的修复很重要，因为它们会让代理沿着同一条调试路径前进，却没有新的证据或测试。

## 方法
- PROJECTMEM 将开发历史记录为一个只追加、纯文本的事件日志，使用类型化事件：问题、尝试、修复、决策和笔记。
- 它从日志中确定性地重建适合 AI 阅读的摘要，因此代理读取的是紧凑的项目记忆，而不是依赖向量检索、嵌入或 LLM 事实抽取。
- 它通过 MCP 提供记忆访问，包含读写工具，以及 CLI 命令和一个 Markdown 桥接，供不支持 MCP 的工具使用。
- 其 precheck_file(path) 门控会在编辑前检查日志，并对此前失败的尝试、未解决问题或与该路径相关的高变动文件发出警告。
- 它在本地运行，没有遥测或云端依赖；写入事件前会脱敏秘密信息，并且可以把库级别的坑点提升到机器级的本地存储中。

## 结果
- 发布的实现是一个 Python 包，运行时依赖 3 个，体积小于 5 MB，包含 14 个 MCP 工具、19 条 CLI 命令和 37 个自动化测试。
- 论文通过一项为期 2 个月的自我研究评估使用情况，覆盖 10 个项目，共记录 207 个事件。
- 系统通过 pjm score 报告估算节省，包括小时、token 和美元，但摘要没有给出实测节省值。
- 论文声称，重建上下文每个会话可能需要 5,000-20,000 个 token，而在事件写入后，读取记忆的成本更固定。
- 能力表将 PROJECTMEM 与 13 个命名系统进行比较，并声称它是所列系统中唯一同时具备六项目标属性的系统：local-first、无需向量数据库的纯文本、事件驱动的不变存储、行动前判断、MCP 原生访问，以及跨项目记忆。
- 论文没有报告用于编码任务成功率、修复准确率或代理正面对比性能的受控基准。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.12329v1](https://arxiv.org/abs/2606.12329v1)
