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
## 总结
本文认为，不能只用 Java 的快照数据集来可靠评估自动化日志生成。它提出了 MultiLogBench，这是一个覆盖六种语言的多语言基准，并在快照任务和修订历史任务上测试了七个大语言模型。

## 问题
- 自动化日志生成要求模型决定**在哪里**插入日志、**调用哪个 API/框架**、**使用什么严重级别**、**写什么消息**，以及**包含哪些变量**。
- 以往证据主要来自**单语言、Java 占主导的代码仓库快照**，因此无法说明这些发现是否能迁移到 Python、Go、C++、JavaScript 和 C# 等语言生态。
- 只看快照还会错过维护场景，也就是开发者在真实代码修改中添加日志的过程；如果模型在修订历史数据上的行为不同，这一点就很重要。

## 方法
- 作者构建了 **MultiLogBench**，一个覆盖 **六种语言** 的基准：Java、Python、Go、C++、JavaScript 和 C#。
- 这个基准有 **三个分支**：**63,965** 个仓库快照实例、从真实加入日志的提交中挖掘出的 **744** 个修订历史案例，以及一个配对的变换后修订历史分支，用于鲁棒性检查。
- 他们用一套统一协议评估了 **七个当代大语言模型**，任务包括日志位置定位、框架锚点匹配、严重级别预测、消息生成、变量恢复和级联端到端质量。
- 他们还按函数内部的结构上下文分析性能，重点看循环和嵌套可调用位置等难点。

## 结果
- MultiLogBench 包含 **63,965** 个快照实例和 **744** 个修订历史案例，覆盖 **6** 个语言生态和 **7** 个大语言模型；这是这项工作的主要基准贡献。
- 论文报告自动化日志生成性能存在**明显的跨语言差异**。它指出，**框架锚点匹配**是**最受语言影响**的组件。
- 结构上下文会影响难度：**循环**位置和**嵌套可调用**位置是最难的案例。
- 模型排名**只在最前列稳定**。排名靠后和中间的模型会随语言变化而重新排序，因此只看一种语言的排行榜可能会误导模型选择。
- 在**修订历史**数据上，论文说**绝对性能下降**，排名稳定性也变弱，但主要的跨语言模式仍然存在。
- 这段摘要**没有给出七个模型的任务指标或精确分数**，因此这里无法做带具体数值的基线比较。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.17529v1](http://arxiv.org/abs/2604.17529v1)
