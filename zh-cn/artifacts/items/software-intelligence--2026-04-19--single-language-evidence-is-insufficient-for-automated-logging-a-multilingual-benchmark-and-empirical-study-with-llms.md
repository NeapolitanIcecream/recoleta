---
source: arxiv
url: http://arxiv.org/abs/2604.17529v1
published_at: '2026-04-19T16:43:17'
authors:
- Renyi Zhong
- Yichen Li
- Yulun Wu
- Jinxi Kuang
- Yintong Huo
- Michael R. Lyu
topics:
- automated-logging
- multilingual-benchmark
- code-generation
- llm-evaluation
- software-maintenance
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Single-Language Evidence Is Insufficient for Automated Logging: A Multilingual Benchmark and Empirical Study with LLMs

## Summary
## 概要
这篇论文认为，只用 Java 快照数据集无法可靠地评估自动化日志生成。论文提出了 MultiLogBench，这是一套覆盖六种语言的多语言基准，并在快照任务和修订历史日志任务上测试了七个 LLM。

## 问题
- 自动化日志生成要求模型判断**在哪里**插入日志、调用**哪个 API/框架**、使用**什么严重级别**、写**什么消息**，以及包含**哪些变量**。
- 以往证据大多来自**单一语言、以 Java 为主的代码仓库快照**，因此无法说明这些结论是否适用于 Python、Go、C++、JavaScript 和 C# 等不同语言生态。
- 只评估快照数据也会漏掉维护场景：开发者会在真实代码变更过程中加入日志。如果模型在修订历史数据上的行为发生变化，这一点就很关键。

## 方法
- 作者构建了 **MultiLogBench**，这是一个覆盖**六种语言**的基准：Java、Python、Go、C++、JavaScript 和 C#。
- 该基准包含**三个分支**：**63,965** 个代码仓库快照实例、**744** 个从真实日志引入提交中挖掘出的修订历史案例，以及一个成对的修订历史变换分支，用于稳健性检查。
- 他们用统一协议评估了**七个当代 LLM**，覆盖多个子任务：日志位置定位、框架锚点匹配、严重级别预测、消息生成、变量恢复，以及级联的端到端整体质量。
- 他们还按函数内部的结构上下文分析性能，重点关注循环和嵌套可调用对象等困难位置。

## 结果
- MultiLogBench 包含 **63,965** 个快照实例和 **744** 个修订历史案例，覆盖 **6** 个语言生态和 **7** 个 LLM；这是论文的主要基准贡献。
- 论文报告了自动化日志生成性能中**明显的跨语言差异**。其中 **framework-anchor matching** 是**最受语言影响**的组件。
- 结构上下文会影响难度：论文指出，**loop** 位置和 **nested-callable** 位置最难处理。
- 模型排名**只在头部梯队较稳定**。中游和较低排名模型会随语言变化而重新排序，因此基于单一语言的排行榜可能会误导模型选择。
- 在**修订历史**数据上，论文称**绝对性能下降**，排名稳定性也变弱，但主要的跨语言模式仍然存在。
- 这段摘录**没有给出七个模型的任务指标或具体分数**，因此这里无法提供与特定基线的数值比较。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17529v1](http://arxiv.org/abs/2604.17529v1)
