---
source: arxiv
url: http://arxiv.org/abs/2603.09004v1
published_at: '2026-03-09T22:48:41'
authors:
- Bassam Adnan
- Matteo Esposito
- Davide Taibi
- Karthik Vaidhyanathan
topics:
- ai-agents
- microservice-generation
- code-generation
- software-engineering
- empirical-study
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Can AI Agents Generate Microservices? How Far are We?

## Summary
本文系统评估了AI代码代理在微服务生成上的真实能力：它们已经能生成不少可运行、较易维护的微服务，但离“无需人类监督的全自动开发”仍有明显差距。

## Problem
- 论文要解决的问题是：AI agents 能否生成**功能正确且可集成**的微服务，而不仅是单个函数或零散代码片段。
- 这很重要，因为微服务开发不仅要求本地业务逻辑正确，还要求遵守跨服务 API 合同、依赖关系和项目结构；小错误就会导致系统集成失败。
- 现有关于 agent 的评测多集中在 bug 修复或仓库级任务，针对“从需求到微服务实现”的系统性实证研究很少。

## Approach
- 作者设计了一个实证研究，评估 **144 个生成出的微服务**，覆盖 **3 个 agents、4 个项目、2 种提示策略、2 种生成场景**。
- 两种场景分别是：**incremental generation**（在已有系统中删掉目标服务后重建，保留上下文与测试）和 **clean state generation**（仅从需求出发，移除服务实现及相关调用痕迹）。
- 两种提示策略分别是：**P1 最小提示**（服务名 + 需求路径）与 **P2 详细提示**（再额外提供目标服务实现摘要），用来测上下文信息形式对结果的影响。
- 功能正确性用自动化测试衡量：incremental 场景看**单元测试通过率**，clean state 场景看**依赖该服务的集成测试通过率**；代码质量用 **SLOC、圈复杂度、认知复杂度** 与人工基线比较。
- 还比较了效率指标，包括 **token 消耗、成本、生成时间**，并使用 Anderson-Darling 与 Wilcoxon/Dunn 等统计分析方法检验差异。

## Results
- 在 **incremental generation** 中，**最小提示 P1 反而优于更详细的 P2**，单元测试通过率约为 **50%–76%**；说明给更多摘要上下文不一定提升微服务重建效果。
- 在 **clean state generation** 中，集成测试通过率更高，达到 **81%–98%**；这表明 agents 在仅凭需求生成时，往往能较好遵守 **API contract** 并满足跨服务交互要求。
- 代码质量方面，生成代码的复杂度**低于人工基线**；论文据此声称生成结果整体更易维护，但也提示低复杂度可能部分来自缺少防御式编程。
- 效率方面，不同 agents 的生成时间差异很大，平均每个微服务约 **6–16 分钟**；论文同时比较了 token 与成本，但摘录中未给出更细的数值。
- 论文的核心结论是：AI agents **已经可以生成可工作的微服务**，但功能正确性仍不稳定，且仍依赖人工监督，因此**尚不能实现完全自治的微服务生成**。
- 摘录未提供各 agent 间更细粒度的完整定量对比、具体 baseline 数值或显著性检验结果表，因此最强的量化结论主要来自上述通过率区间与时间范围。

## Link
- [http://arxiv.org/abs/2603.09004v1](http://arxiv.org/abs/2603.09004v1)
