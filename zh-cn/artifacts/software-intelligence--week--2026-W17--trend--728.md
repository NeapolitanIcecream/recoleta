---
kind: trend
trend_doc_id: 728
granularity: week
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-27T00:00:00'
topics:
- coding-agents
- evaluation
- repo-level-codegen
- execution
- agent-harness
run_id: materialize-outputs
aliases:
- recoleta-trend-728
tags:
- recoleta/trend
- topic/coding-agents
- topic/evaluation
- topic/repo-level-codegen
- topic/execution
- topic/agent-harness
language_code: zh-CN
---

# Coding-agent 研究正在按可运行证明、代码仓库真实性和 harness 质量来评判

## Overview
本周的 coding-agent 研究里，最有说服力的结论都落在可运行证据上。基准和系统持续追问的是：代码能否构建、执行，并通过工作流检查。同一批材料也反复显示出两个限制：仓库规模任务依然经常失败，而 harness 的选择对结果的影响可以和模型本身一样大。

## Clusters

### 可执行证据正在成为主要标准
评估正在进一步收紧到可执行证据。整周的每日趋势文档反复偏向那些用完整运行、工具轨迹、状态变化和真实工作流存活情况来评分的系统。单篇证据在代码仓库规模上也传达了同样的信息：RealBench 用真实代码仓库、UML 设计输入和人工验证测试来评估代码生成，而最佳平均 Pass@1 仍只有 19.39%。这周的信号很明确：人们要的是可运行的产物，不是打磨过的代码文本。

#### Evidence
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): 单篇基准显示，即使有结构化设计输入和测试支撑的评估，仓库规模任务的通过率仍然很低。

### 仓库规模自动化仍然会卡在环境搭建和复杂度上
代码仓库规模的编码仍然有明显上限。RealBench 报告称，代码仓库小于 500 LOC 时，Pass@1 超过 40%；超过 2000 LOC 时，Pass@1 降到 15% 以下。RAT 说明了为什么在这种场景下环境配置这么重要：它的自动化配置流程提高了 Python、Java、Rust 和 JS/TS 上可执行环境的搭建成功率，但也带来了真实的 token 和时间成本。这周传达出的实际情况很直接：让代码跑起来本身仍然是任务的重要组成部分。

#### Evidence
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): 该基准给出了代码仓库规模扩大后性能下降的具体数据，以及总体较低的 Pass@1。
- [RAT: RunAnyThing via Fully Automated Environment Configuration](../Inbox/2026-04-25--rat-runanything-via-fully-automated-environment-configuration.md): 环境配置研究量化了搭建成功率的提升，同时也给出了 token 和时延成本。

### Harness 设计正在变成模型工作的核心部分
智能体质量很大程度上取决于模型外层的 harness。本文周的趋势覆盖表明，脚手架、文档和控制界面都是决定结果的关键变量。HARBOR 把这一点说得很具体：在它的手动调优研究中，一组较小的标志位配置把 Terminal-Bench 2 的结果从 15/89 提高到 17/89，而后续加入额外自评估和反思功能的配置反而降到了 13/89 和 12/89。这里更好的智能体表现来自严格的配置工作，不只是换一个更强的模型。

#### Evidence
- [HARBOR: Automated Harness Optimization](../Inbox/2026-04-22--harbor-automated-harness-optimization.md): 单篇案例研究显示，手动叠加 harness 功能可能会降低通过率。
