---
source: arxiv
url: https://arxiv.org/abs/2607.19653v1
published_at: '2026-07-22T01:19:42'
authors:
- Ryan Deng
- Yuanzhe Liu
- Bastian Lipka
- Yao Ma
- Xuhao Chen
- Tim Kaler
- Jatin Ganhotra
topics:
- code-intelligence
- automated-software-production
- repository-optimization
- software-agents
- profiler-guided-optimization
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# PerfAgent: Profiler-Guided Iterative Refinement for Repository-Level Code Optimization

## Summary
## 摘要
PerfAgent 通过向编码代理提供性能分析器摘要、迭代式加速反馈和针对性的正确性检查，提升了仓库级代码优化效果。在 GSO 和 SWE-fficiency-Lite 上，与使用 GPT-5.1 的 OpenHands 相比，其达到专家性能的补丁比例提高了一倍以上。

## 问题
- 通用编码代理通常会优化显眼的 Python 代码，却忽略抽象层之间或原生扩展内部的性能瓶颈。
- 它们可能在第一个通过测试的补丁后就停止，并且测试范围过窄，从而只能取得有限的加速，或引入正确性回归。
- 该问题之所以重要，是因为仓库级优化要求在保持行为不变的同时接近专家级性能，而不只是通过测试。

## 方法
- PerfAgent 使用低开销的 `py-spy` 采样性能分析器识别 Python 和原生代码中的热点，然后将原始采样转换为简洁摘要，其中包含位置、调用上下文、自身耗时、总耗时和运行时占比。
- 一个目标驱动的控制器会拦截代理的停止信号，重新构建并验证每个补丁，再次分析工作负载，并要求代理最多继续迭代 5 次。
- 最佳补丁选择器会保留速度最快且正确的补丁，而不是最后提交的补丁。
- 使用 `pytest-testmon` 进行选择性验证，只运行受代码变更影响的测试，并将构建或测试失败作为反馈返回，无需运行整个仓库的测试套件。

## 结果
- 在 GPT-5.1 下，达到专家性能的补丁比例相对于 OpenHands 在 GSO 上从 19.6% 提高到 39.2%，在 SWE-fficiency-Lite 上从 26% 提高到 74%。
- 在 GSO 上，该基准包含来自 10 个仓库的 102 个任务；平均调和均值加速比从第 1 轮的 2.5x 提高到第 5 轮的 6.4x，同时验证失败实例从 53 个降至 5 个。
- 在 48 个 GSO 实例中，PerfAgent 触及了底层 C、C++、Cython 或 Rust 代码，而 OpenHands 仅在 31 个实例中触及这些代码；其中有 21 个实例里，OpenHands 只修改了 Python 代码。
- 与运行完整测试套件相比，选择性测试在 GSO 上减少了 66%–99% 的测试数量，在 SWE-fficiency-Lite 上减少了 47%–98%。
- 在一个经过跟踪的 NumPy 字符串替换示例中，加速比达到 5.87x；控制器保留了第 4 轮的这一补丁，而不是第 5 轮略慢的 5.85x 补丁。
- 论文报告称，PerfAgent 以显著更低的成本超过了 oracle best-of-five 基线，但摘录没有提供确切的成本或得分数值；在 SWE-fficiency-Lite 上，后续轮次的结果受到每个任务 5 美元预算的限制。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.19653v1](https://arxiv.org/abs/2607.19653v1)
