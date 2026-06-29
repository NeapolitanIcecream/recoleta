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
这篇论文在同一测试设置下，对 22 个开源 agentic 框架在推理基准上的表现进行了比较。主要发现是，框架选择时，比起宣称的代理架构，更重要的是编排质量、成本控制和故障处理。

## 问题
- 团队把 agentic 框架用于推理密集型工作，但关于哪些框架在实践中更准确、更快、更便宜、更稳定的广泛基准证据很少。
- 以往比较通常只测试少数框架，或者关注架构调研、开发体验、狭窄任务，这让人在真实约束下难以判断该选哪个框架。
- 这对软件工程和其他推理密集型场景很重要，因为糟糕的编排会浪费数天运行时间、烧掉 API 预算，或者在基础模型本来能回答的情况下仍然无法完成任务。

## 方法
- 作者从 2023 年 1 月到 2025 年 7 月收集了 1,200 个 GitHub 仓库，按筛选标准选出 22 个广泛使用的开源 agentic 框架。
- 他们构建了一个包含五种架构类型的分类法：单智能体、基于角色的多智能体、分层、模块化和基于图的架构。
- 他们在统一设置下，用三个推理基准评估这些框架：BBH、GSM8K 和 ARC。
- 他们测量了四个实际结果：推理准确率、执行时间、计算成本，以及跨基准的一致性。
- 他们还分析了失败案例，把推理能力限制与系统故障区分开，例如内存增长、重试循环、配额耗尽和上下文处理问题。

## 结果
- 22 个框架中有 19 个完成了全部三个基准。
- 12 个框架表现一致，平均准确率为 **74.6% 到 75.9%**，每个任务的执行时间为 **4 到 6 秒**，每个任务的成本为 **0.14 到 0.18 美分**。
- 数学推理在所有完成的框架中都较弱：**GSM8K** 的平均准确率是 **44.35%**，而 **BBH** 为 **89.80%**，**ARC** 为 **89.56%**。
- 论文说，这个数学差距在不同架构类型中都存在，说明当前 agent 框架继承了基础模型在多步数值推理上的弱点，而不是把它解决掉。
- 一些较差结果来自系统故障，而不是推理错误：**Camel** 因为上下文不断增长，在 **11 天**后仍未完成 BBH；**Upsonic** 因为抽取失败触发重试和大提示词，在一天内花掉 **$1,434**；**AutoGen** 和 **Mastra** 通过反复的智能体交互耗尽了 API 配额，提示长度不断增加，但答案没有变好。
- 论文的主要实践结论是，推理任务的框架选择应更关注内存控制、重试策略、上下文控制和成本表现，而不只是架构类别。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16646v1](http://arxiv.org/abs/2604.16646v1)
