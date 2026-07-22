---
source: hn
url: https://blog.jetbrains.com/ai/2026/07/introducing-jetbrains-context-repository-intelligence-for-coding-agents/
published_at: '2026-07-21T23:18:13'
authors:
- monkey_monkey
topics:
- code-intelligence
- coding-agents
- repository-search
- semantic-retrieval
- multi-repository
- software-production
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# JetBrains Context: Repository Intelligence for Coding Agents

## Summary
## 摘要
JetBrains Context 通过增量索引代码并检索相关实现知识，为编码代理提供代码仓库智能。JetBrains 表示，在开源项目、生产级单体仓库和代码定位评测中，该系统降低了代理操作次数、延迟和执行成本，但摘录未提供基线详情或独立验证结果。

## 问题
- 编码代理通常需要花费大量时间搜索代码仓库、阅读文件，并启动探索性代理，之后才能实现或审查变更。
- 对 API、依赖关系、实现模式和组织范围内代码的了解有限，会降低代理在大型代码库中的效果，并可能增加审查、返工和令牌成本。

## 方法
- JetBrains Context 以增量方式构建每个代码仓库的语义索引，并提供语义检索工具，使代理能够查询概念和相关代码，而不必仅依赖关键词搜索和反复探索文件。
- 其多代码仓库搜索功能允许代理在本地未检出的代码仓库中查找相关代码、API、依赖关系和实现示例。
- 该层集成 Claude Code、Codex CLI 和 Junie CLI，并可通过 JetBrains IDE、Air、VS Code 及其他受支持的编辑器访问。
- 代理钩子可以自动预先索引源代码；JetBrains 表示，源代码不会存储在其服务器上。

## 结果
- JetBrains 在 205 个开源 SWE-bench 任务、175 个生产级单体仓库任务和 1,953 个代码定位任务上评估了该系统。
- 在这些评测中，JetBrains 报告代理操作次数最多减少 68%、延迟最多减少 59%、执行成本最多减少 48%。
- 报告的数值是最大降幅而非平均值，摘录未说明对比基线、任务层面的成功率变化或独立评测结果。
- JetBrains 面向 JetBrains AI for Teams and Organizations 计划的订阅者提供这项能力，目前处于早期访问阶段且不额外收费。

## Problem

## Approach

## Results

## Link
- [https://blog.jetbrains.com/ai/2026/07/introducing-jetbrains-context-repository-intelligence-for-coding-agents/](https://blog.jetbrains.com/ai/2026/07/introducing-jetbrains-context-repository-intelligence-for-coding-agents/)
