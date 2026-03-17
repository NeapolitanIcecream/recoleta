---
source: hn
url: https://hantverkskod.se/2026/03/01/saaspocalypse/
published_at: '2026-03-10T23:10:46'
authors:
- mosura
topics:
- agentic-coding
- developer-tools
- ai-workflow
- context-management
- event-log
relevance_score: 0.04
run_id: materialize-outputs
---

# SaaSpocalypse Now

## Summary
这篇文章不是机器人/AI研究论文，而是一篇关于“AI 代理编程工作流”的工程反思。作者主张，相比购买 SaaS/工作流产品，生成式 AI 让开发者更值得自己构建一个轻量、可定制的“代理记忆”工具。

## Problem
- 作者认为，现有基于一堆 Markdown 文件给代理提供上下文的方式很随意、难维护，而且随着项目增长会让代理反复解析无结构文本，效率低。
- 开发者需要一种更结构化、可持续的方式来记录任务、决策与项目状态，以便在每次执行任务时快速构造所需上下文。
- 这之所以重要，是因为生成式 AI/agentic coding 正在改变“买现成 SaaS 还是自己做”的成本平衡，工作流工具可能成为新的核心生产力瓶颈。

## Approach
- 作者借鉴 Beads 的核心思路：把所有操作和决策记录到数据库式的持久化存储中，而不是散落在 Markdown 里。
- 自己实现了一个极简工具 Shelby：单个可执行文件，可直接放入任意项目中，为代理提供“更好的记忆”。
- Shelby 使用追加式 JSONL 事件日志来记录数据，作者将这些记录称为 mementos；每次命令运行前都通过重放日志来重建当前状态。
- 在任务确定后，通过 `shelby context <id-or-alias>` 为代理生成该任务所需的精确上下文，而不是扫描全局文件。
- 工具设计上还考虑了多并行代理协作，虽然作者表示自己尚未真正使用这一能力。

## Results
- 文中没有提供正式实验、基准数据集或与现有系统的定量对比结果。
- 最具体的工程结果是：作者在 **7 个晚上** 内构建了 Shelby，共 **5168 行 Rust 代码**、**120 个单元测试**、**60 个集成测试**。
- 作者的主要结论性主张是：生成式 AI 已显著推动“自己搭建工具”相对“购买 SaaS/工作流产品”变得更划算，但这是观点性判断，不是严格实验结论。
- 作者还声称，当前 agentic coding 的最大改进空间不是能力而是**速度**；现阶段开发者通过“多代理编排”来弥补“单线程”交互的低效率，但未给出量化收益。

## Link
- [https://hantverkskod.se/2026/03/01/saaspocalypse/](https://hantverkskod.se/2026/03/01/saaspocalypse/)
