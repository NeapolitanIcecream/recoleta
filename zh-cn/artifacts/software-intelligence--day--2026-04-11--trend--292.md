---
kind: trend
trend_doc_id: 292
granularity: day
period_start: '2026-04-11T00:00:00'
period_end: '2026-04-12T00:00:00'
topics:
- coding-agents
- verification
- agent-memory
- benchmarks
- systems-optimization
run_id: materialize-outputs
aliases:
- recoleta-trend-292
tags:
- recoleta/trend
- topic/coding-agents
- topic/verification
- topic/agent-memory
- topic/benchmarks
- topic/systems-optimization
language_code: zh-CN
---

# 编码代理研究正在把结构和外部检查变成主要控制面

## Overview
这一天的研究表明，编码代理在控制被写下来并在模型外检查时会更好。最清楚的证据来自形式化规格、架构描述文件、harness 管理的内存和预算化评估。还有一个应用系统结果也很突出：LLM 引导的查询计划编辑在 Apache DataFusion 中带来了可测量的速度和内存收益。

## Clusters

### 明确规格和架构文件正在成为代理的核心输入
这一时期的编码代理论文更强调显式、可检查的控制。一项提议把结对编程分成 driver 和 navigator 两个角色，由 navigator 生成机器可检查的契约和形式化规格，再用确定性验证器和基于 SMT 的反例来验证代码和测试。端到端流程仍然是研究计划，但支撑系统已经给出具体验证结果：AutoReSpec 验证了 72 个程序中的 67 个，AutoJML 验证了 120 个中的 109 个。

另一项仓库研究发现，给代理提供架构描述文件，对减少代码导航步骤的帮助大于对原始任务准确率的提升。在一个 22K 行的 Rust 项目中，架构上下文把平均导航步骤从 5.2 降到 3.4，使用 S-expression 或 JSON 时都是这样，使用 Markdown 时降到 2.9。第二项研究里，一个自动生成的 170 行描述文件在 15 个任务上达到了 100% 准确率，而盲搜只有 80%。共同点很直接：当关键结构被写成工具能复用、能检查的形式时，代理表现更好。

#### Evidence
- [From Helpful to Trustworthy: LLM Agents for Pair Programming](../Inbox/2026-04-11--from-helpful-to-trustworthy-llm-agents-for-pair-programming.md): Pair-programming proposal grounded in formal specs and verification metrics.
- [Formal Architecture Descriptors as Navigation Primitives for AI Coding Agents](../Inbox/2026-04-11--formal-architecture-descriptors-as-navigation-primitives-for-ai-coding-agents.md): Architecture descriptor study with navigation-step and accuracy results.

### 状态处理正在转入 harness
这一组里最强的基础设施结果来自代理 harness 内部的内存管理。ClawVM 把代理状态当作带类型的页面，并设置最低保真规则，然后分两阶段组装提示词：先保留必需状态，再把剩余 token 花在更有价值的细节上。这直接对应长会话里的常见失效模式，也就是计划、约束或先前证据在压缩或重置后消失。

报告的提升很大。跨四类工作负载和六个 token 预算，ClawVM 把平均可由策略控制的故障数从检索基线的 67.8、以及压缩加检索基线的 1.5，降到在最低必需状态能装入预算时的 0。在 12 条真实轨迹和 30 次任务重放上，它也报告了同样的零故障结果，以及在最紧预算下 100% 成功，单轮策略开销的中位数低于 50 微秒。这样，内存处理留在 harness 里，而不是依赖脆弱的提示词文本。

#### Evidence
- [ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents](../Inbox/2026-04-11--clawvm-harness-managed-virtual-memory-for-stateful-tool-using-llm-agents.md): Harness-managed memory design and zero-fault evaluation results.

### 编码基准开始为 token、测试和时间定价
基准测试正在更接近真实运行限制。USACOArena 会向代理收取 token、测试和经过时间的成本，然后用 ICPC 风格的评分来排名。这一设置暴露了一个直接事实：当成本变重要时，前沿编码代理还有很大改进空间。在四场比赛里，理论最高分是 54 分，而顶尖代理平均只有大约 15 分。

Gemini-2.5-pro 和 GPT-5-Codex 在只看算力的设置中领先，但这个基准远没有被解决。Gemini 的平均排名是 1.3，胜率 70%，在 USACO 2025 US Open 上得分 14.6，对比 GPT-5-Codex 的 3.0。预算扩展也不均匀。把 Gemini 的信用上限降到 10M，会把分数从 13.2 拉到 8.3；把预算提高到 40M，分数仍然接近 13.0。多花钱并不能稳定换来更好的表现。

#### Evidence
- [Credit-Budgeted ICPC-Style Coding: When Agents Must Pay for Every Decision](../Inbox/2026-04-11--credit-budgeted-icpc-style-coding-when-agents-must-pay-for-every-decision.md): Credit-budgeted coding benchmark and frontier-agent results.

### 已发布代码和查询引擎里开始出现应用结果
一篇论文把编码代理推进到已发布研究代码上的直接实验工作，另一篇系统论文把 LLM 用到数据库执行计划上。算法改进研究报告说，在一个工作日内，所选的 11 个实现全部都有提升，其中组合优化的运行时间快了 193 倍，高 K 条件下的图像分割快了 1000 倍以上。论文也说明，这些结果没有在代理环境之外独立重跑，所以这些头条数字需要谨慎看待。

数据库论文的范围更窄，但机制更具体。它让模型通过 JSON Patch 操作修改现有的 Apache DataFusion 物理计划，然后只保留能改善执行的重写。在一个 TPC-DS 风格案例里，把年份过滤提前，让销售表在后续连接前从 1510 万行降到 290 万行，带来 4.78 倍加速，并把哈希表构建内存从 3.3 GB 降到 411 MB。这一时期有几篇代理论文，但这个应用系统结果是最清楚的用户可见收益之一。

#### Evidence
- [Applying an Agentic Coding Tool for Improving Published Algorithm Implementations](../Inbox/2026-04-11--applying-an-agentic-coding-tool-for-improving-published-algorithm-implementations.md): Agent-driven improvement of released research implementations, with caveats.
- [AI for Systems: Using LLMs to Optimize Database Query Execution](../Inbox/2026-04-11--ai-for-systems-using-llms-to-optimize-database-query-execution.md): LLM-guided database plan rewrites with concrete speed and memory gains.
