---
source: arxiv
url: http://arxiv.org/abs/2604.16646v1
published_at: '2026-04-17T19:02:54'
authors:
- Zeeshan Rasheed
- Abdul Malik Sami
- Muhammad Waseem
- Kai-Kristian Kemell
- Mika Saari
- Pekka Abrahamsson
topics:
- agentic-frameworks
- reasoning-benchmarks
- multi-agent-systems
- software-engineering
- llm-evaluation
relevance_score: 0.85
run_id: materialize-outputs
language_code: zh-CN
---

# Agentic Frameworks for Reasoning Tasks: An Empirical Study

## Summary
## 摘要
这篇论文在同一套测试设置下，对 22 个开源 agentic 框架进行了推理基准对比。主要发现是：与其宣称的智能体架构相比，框架选择对编排质量、成本控制和故障处理的影响更大。

## 问题
- 团队会把 agentic 框架用于需要大量推理的工作，但目前缺少基于基准测试、覆盖面较广的证据来说明哪些框架在实际中准确、快速、成本可控且稳定。
- 以往的对比通常只测试少数几个框架，或侧重于架构综述、开发者体验或范围较窄的任务，因此在真实约束下如何选型仍不清楚。
- 这对软件工程和其他推理密集型场景很重要，因为糟糕的编排会浪费数天运行时间、消耗 API 预算，或者即使底层模型本来能答对，也无法完成任务。

## 方法
- 作者收集了 2023 年 1 月到 2025 年 7 月之间的 1,200 个 GitHub 仓库，按筛选标准选出 22 个被广泛使用的开源 agentic 框架。
- 他们建立了一个包含五类架构的分类体系：单智能体、基于角色的多智能体、分层式、模块化和图结构。
- 他们在统一设置下，使用三个推理基准评估这些框架：BBH、GSM8K 和 ARC。
- 他们衡量了四项实际结果：推理准确率、执行时间、计算成本，以及跨基准的一致性。
- 他们还分析了失败案例，以区分推理能力的限制和系统故障，例如内存增长、重试循环、配额耗尽和上下文处理问题。

## 结果
- 22 个框架中有 19 个完成了全部三个基准测试。
- 其中 12 个框架表现稳定，平均准确率为 **74.6% 到 75.9%**，执行时间为**每个任务 4 到 6 秒**，成本为**每个任务 0.14 到 0.18 美分**。
- 所有完成测试的框架在数学推理上都较弱：**GSM8K 的平均准确率为 44.35%**，而 **BBH 为 89.80%**，**ARC 为 89.56%**。
- 论文指出，这一数学差距在不同架构类型中都存在，这说明当前智能体框架更多是继承了底层模型在多步数值推理上的弱点，而没有解决它。
- 一些较差结果来自系统故障，而不是推理错误：**Camel** 因为上下文持续增长，在运行 **11 天**后仍未完成 BBH；**Upsonic** 因提取失败触发重试和大提示词，在 **一天内花费了 1,434 美元**；**AutoGen** 和 **Mastra** 因重复的智能体交互不断增加提示长度、却没有改善答案，最终耗尽了 API 配额。
- 论文最主要的实践结论是：为推理任务选择框架时，应更看重内存管理、重试策略、上下文控制和成本表现，而不只是架构类别。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16646v1](http://arxiv.org/abs/2604.16646v1)
