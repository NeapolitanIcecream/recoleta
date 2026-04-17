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

# 编码智能体研究正把结构化信息和外部检查变成主要控制面

## Overview
这一天的研究表明，当控制被写下来并在模型外部接受检查时，编码智能体会表现更好。最清楚的证据来自形式化规范、架构描述符、由 harness 管理的内存，以及带预算的评测。还有一个应用系统结果也很突出：LLM 引导的查询计划编辑在 Apache DataFusion 中带来了可测量的速度和内存收益。

## Clusters

### 显式规范和架构文件正成为智能体的核心输入
这一时期的编码智能体论文更强调显式、可检查的控制。一项提案把结对编程设定为 driver 和 navigator 协作，其中 navigator 生成机器可检查的契约和形式化规范，再用确定性验证器和由 SMT 支持的反例来验证代码与测试。端到端工作流本身仍是研究计划，但其配套系统已经报告了具体的验证结果：AutoReSpec 在 72 个程序中验证通过了 67 个，AutoJML 在 120 个程序中验证通过了 109 个。

另一项代码仓库研究发现，给智能体提供架构描述符，对减少代码导航步骤的帮助大于对原始任务准确率的提升。在一个 2.2 万行的 Rust 项目中，加入架构上下文后，平均导航步骤从 5.2 降到 3.4（使用 S-expression 或 JSON），使用 Markdown 时降到 2.9。在第二项研究中，自动生成的 170 行描述符在 15 个任务上达到 100% 准确率，而盲搜为 80%。共同点很实际：当关键结构以工具可复用、可检查的形式写下来时，智能体表现更好。

#### Evidence
- [From Helpful to Trustworthy: LLM Agents for Pair Programming](../Inbox/2026-04-11--from-helpful-to-trustworthy-llm-agents-for-pair-programming.md): 基于形式化规范和验证指标的结对编程提案。
- [Formal Architecture Descriptors as Navigation Primitives for AI Coding Agents](../Inbox/2026-04-11--formal-architecture-descriptors-as-navigation-primitives-for-ai-coding-agents.md): 包含导航步数和准确率结果的架构描述符研究。

### 状态处理正在转移到 harness 中
这组研究里最强的基础设施结果来自智能体 harness 内部的内存管理。ClawVM 把智能体状态视为带最小保真规则的类型化页面，然后分两阶段组装提示：先保留必需状态，再把剩余 token 用在价值更高的细节上。这直接对应了长会话中的一个常见失败模式：计划、约束或先前证据在压缩或重置后消失。

报告中的提升幅度很大。在四类工作负载和六种 token 预算下，只要最小必需状态能够装下，ClawVM 就把平均策略可控故障从检索基线的 67.8、压缩加检索基线的 1.5 降到零。在 12 条真实轨迹和 30 次任务重放中，它也报告了同样的零故障结果，并且在最紧的预算下成功率达到 100%，每轮的策略开销中位数低于 50 微秒。这样，内存处理留在 harness 里，而不是放在脆弱的提示文本中。

#### Evidence
- [ClawVM: Harness-Managed Virtual Memory for Stateful Tool-Using LLM Agents](../Inbox/2026-04-11--clawvm-harness-managed-virtual-memory-for-stateful-tool-using-llm-agents.md): harness 管理的内存设计和零故障评估结果。

### 编码基准开始为 token、测试和时间计价
基准测试工作正更接近真实运行限制。USACOArena 会对智能体的 token、测试和耗时收费，再用 ICPC 风格的评分规则进行排名。这个设置直接说明了一点：当前前沿编码智能体在成本重要时仍有很大改进空间。在四场竞赛中，理论最高分是 54 分，而顶尖智能体平均只有约 15 分。

Gemini-2.5-pro 和 GPT-5-Codex 在纯算力设置下领先，但这个基准远未被攻克。Gemini 的平均名次是 1.3，胜率为 70%；在 USACO 2025 US Open 上，它得分 14.6，而 GPT-5-Codex 为 3.0。预算扩展的效果也不均匀。把 Gemini 的 credit 上限降到 10M 后，分数从 13.2 降到 8.3；把预算提高到 40M，分数仍在 13.0 附近。花更多成本并不稳定地带来更好的表现。

#### Evidence
- [Credit-Budgeted ICPC-Style Coding: When Agents Must Pay for Every Decision](../Inbox/2026-04-11--credit-budgeted-icpc-style-coding-when-agents-must-pay-for-every-decision.md): 带 credit 预算的编码基准以及前沿智能体结果。

### 应用结果开始出现在已发布代码和查询引擎中
一篇论文把编码智能体推进到对已发布研究代码的直接实验工作中，另一篇系统论文则把 LLM 用于数据库执行计划。算法改进研究报告称，在一个工作日内，11 个入选实现全部获得提升，其中组合优化的运行时间提升达到 193 倍，高 K 条件下的图像分割速度提升超过 1000 倍。论文也说明，这些结果没有在智能体环境外独立复现过，因此标题数字需要谨慎看待。

数据库论文的范围更窄，但对机制的描述更具体。它让模型通过 JSON Patch 操作修改现有的 Apache DataFusion 物理计划，然后只保留能改善执行效果的重写。在一个 TPC-DS 风格案例中，把年份过滤提前后，后续连接前的 sales 表行数从 1510 万降到 290 万，带来 4.78 倍加速，并把哈希表构建内存从 3.3 GB 降到 411 MB。这个时期有几篇智能体论文，但这个应用系统结果是用户可见收益最清楚的之一。

#### Evidence
- [Applying an Agentic Coding Tool for Improving Published Algorithm Implementations](../Inbox/2026-04-11--applying-an-agentic-coding-tool-for-improving-published-algorithm-implementations.md): 智能体驱动的已发布研究实现改进，附带注意事项。
- [AI for Systems: Using LLMs to Optimize Database Query Execution](../Inbox/2026-04-11--ai-for-systems-using-llms-to-optimize-database-query-execution.md): LLM 引导的数据库计划重写，带来具体的速度和内存收益。
