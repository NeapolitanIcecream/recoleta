---
source: hn
url: https://arxiv.org/abs/2603.09172
published_at: '2026-03-14T23:37:12'
authors:
- 1024core
topics:
- ramsey-numbers
- combinatorics
- llm-search
- code-mutation
- automated-discovery
relevance_score: 0.01
run_id: materialize-outputs
language_code: zh-CN
---

# Researchers improve lower bounds for some Ramsey numbers using AlphaEvolve

## Summary
这篇论文用 AlphaEvolve（一种基于大语言模型的代码变异代理）自动生成搜索算法，改进了五个经典 Ramsey 数的下界。其意义在于，它把以往高度定制、问题特定的组合搜索流程，统一成了一个可复用的元算法。

## Problem
- 论文要解决的问题是：如何为经典 Ramsey 数构造更大的反例，从而提升其**下界**；这在组合数学中是长期困难问题。
- 这很重要，因为 Ramsey 数是极其基础但又 notoriously hard 的离散数学对象，很多最好结果都依赖复杂的计算搜索。
- 以往方法通常是为单个或少数实例手工设计专用搜索算法，泛化性弱、复现细节也常不完整。

## Approach
- 核心方法是使用 **AlphaEvolve**，即一个基于 LLM 的**代码变异代理**，自动提出、修改并改进用于搜索组合结构的程序。
- 用最简单的话说：系统不是直接猜答案，而是不断“写和改搜索代码”，让代码去寻找能证明更高下界的图构造。
- 作者将其定位为一个**单一元算法**：同一套自动化机制可用于多个 Ramsey 数实例，而不是每个目标都手工做一个专用算法。
- 除了追求新结果，作者还用该方法回收已知精确值对应的下界，并在许多其他情形上复现当前最佳已知下界，以验证方法的广泛性。

## Results
- 改进了 **5 个**经典 Ramsey 数下界：**R(3,13)** 从 **60 提升到 61**。
- **R(3,18)** 从 **99 提升到 100**。
- **R(4,13)** 从 **138 提升到 139**。
- **R(4,14)** 从 **147 提升到 148**。
- **R(4,15)** 从 **158 提升到 159**。
- 此外，作者声称该方法**成功回收了所有已知精确 Ramsey 数对应的下界**，并在**许多其他案例**上**匹配当前最佳已知下界**；摘要未提供更细的数量化覆盖范围或与特定先前算法的系统对比数据。

## Link
- [https://arxiv.org/abs/2603.09172](https://arxiv.org/abs/2603.09172)
