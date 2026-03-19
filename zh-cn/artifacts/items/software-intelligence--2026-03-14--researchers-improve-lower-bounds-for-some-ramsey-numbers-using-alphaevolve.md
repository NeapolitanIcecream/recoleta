---
source: hn
url: https://arxiv.org/abs/2603.09172
published_at: '2026-03-14T23:37:12'
authors:
- 1024core
topics:
- llm-based-search
- combinatorial-optimization
- ramsey-numbers
- code-mutation-agent
- automated-discovery
relevance_score: 0.63
run_id: materialize-outputs
language_code: zh-CN
---

# Researchers improve lower bounds for some Ramsey numbers using AlphaEvolve

## Summary
本文展示了用 AlphaEvolve（一种基于大语言模型的代码变异代理）自动发现组合结构搜索算法，并据此刷新了5个经典 Ramsey 数的下界。其意义在于：过去常需为每个具体问题手工设计专用搜索程序，而该工作声称用单一元算法统一地产生这些结果。

## Problem
- 论文要解决的问题是：如何自动构造用于改进 Ramsey 数下界的组合结构，而不必为每个具体参数手工发明专用搜索算法。
- 这很重要，因为经典 Ramsey 下界大多依赖计算搜索获得，但现有方法通常是“一个问题一种定制算法”，可复用性和可扩展性差。
- 如果能用通用的智能代码生成/变异系统稳定地产生高质量搜索算法，就可能加速数学发现与自动化科学探索。

## Approach
- 核心方法是 AlphaEvolve：一个基于 LLM 的代码变异代理。最简单地说，它会不断修改搜索代码、运行它、看结果好不好，再保留更有效的版本。
- 它不是直接输出某个 Ramsey 构造答案，而是生成/改进“寻找答案的程序”，即把问题转化为自动搜索算法的进化过程。
- 作者将其作为单一的“meta-algorithm”使用，针对不同 Ramsey 数实例产生对应搜索策略，而不是为每个实例单独手写启发式方法。
- 除了寻找新下界外，作者还用它回收已知精确值对应的下界，并在许多其他情形上达到当前最佳已知下界，以验证方法的通用性。

## Results
- 论文声称将 **R(3,13)** 的下界从 **60 提升到 61**。
- 将 **R(3,18)** 的下界从 **99 提升到 100**。
- 将 **R(4,13)** 的下界从 **138 提升到 139**。
- 将 **R(4,14)** 的下界从 **147 提升到 148**，并将 **R(4,15)** 的下界从 **158 提升到 159**。
- 除这 5 个新结果外，作者称其方法**成功恢复了所有已知精确 Ramsey 数对应的下界**。
- 作者还称在**许多其他情形**上**匹配了当前最佳已知下界**；给定摘录未提供更细的实例数量、运行成本或与其他自动方法的系统性对比数字。

## Link
- [https://arxiv.org/abs/2603.09172](https://arxiv.org/abs/2603.09172)
