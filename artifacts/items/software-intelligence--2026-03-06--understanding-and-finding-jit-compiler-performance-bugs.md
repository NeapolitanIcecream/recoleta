---
source: arxiv
url: http://arxiv.org/abs/2603.06551v1
published_at: '2026-03-06T18:39:33'
authors:
- Zijian Yi
- Cheng Ding
- August Shi
- Milos Gligoric
topics:
- jit-compilers
- performance-bugs
- differential-testing
- compiler-testing
- java-javascript
relevance_score: 0.58
run_id: materialize-outputs
---

# Understanding and Finding JIT Compiler Performance Bugs

## Summary
本文研究 JIT 编译器中的性能缺陷，这是此前几乎未被系统研究的一类问题。论文先分析 4 个主流 JIT 的真实缺陷，再提出自动化检测工具 Jittery 来发现这类 bug。

## Problem
- 论文要解决的是 **JIT 编译器性能 bug** 的理解与检测问题：编译器可能生成过慢的代码，或自身编译过程过慢，但现有工作主要关注语义错误而非性能退化。
- 这很重要，因为 JIT 在运行时做优化，性能 bug 会直接拖慢真实应用，而且应用开发者往往无法仅通过改业务代码彻底规避。
- JIT 的动态特性使问题更难发现：运行时 profiling、推测优化、去优化、分层编译及与运行时系统的交互都会引入复杂且不稳定的性能异常。

## Approach
- 作者先做了首个系统性实证研究：从 HotSpot、Graal、V8、SpiderMonkey 四个主流 JIT 的 issue tracker 中收集并人工分析 **191** 个已修复性能 bug，总结触发输入、外在症状和根因模式。
- 基于这些发现，提出 **layered differential performance testing**：对大量小型随机程序，在两种 JIT 配置下运行并比较性能差异，把异常大的差异视为候选性能 bug。
- “分层”机制的核心很简单：先用低成本、少迭代的快速测试筛掉大多数正常样本，再对少量可疑程序逐层增加迭代和测量强度，以兼顾吞吐量与测量可靠性。
- 工具 **Jittery** 还加入工程化优化：利用早期层的运行时信息进行测试优先级排序，并自动过滤误报与重复样例，减少人工排查负担。
- 方法设计直接对应实证结论：很多性能 bug 可由小型 micro-benchmark 触发，且常通过“同一程序在不同配置/版本下的性能差异”暴露，因此差分测试是合适的检测机制。

## Results
- 实证研究共分析 **191** 个真实 JIT 性能 bug，覆盖 **4** 个广泛使用的 JIT 编译器（HotSpot、Graal、V8、SpiderMonkey）；原始收集 **272** 个 issue，人工过滤后保留 191 个。
- 论文声称发现：**接近一半** 的性能 bug 可以由小型、聚焦的 **micro-benchmarks** 暴露，而不需要完整 benchmark suite。
- Jittery 的测试优先级优化将测试时间降低 **92.40%**，同时 **不损失 bug 检测能力**。
- 使用 Jittery，作者在 **Oracle HotSpot 和 Graal** 中发现 **12 个此前未知** 的性能 bug，其中 **11 个已被开发者确认**，**6 个已修复**。
- 论文还声称这些新 bug 不仅涉及传统优化/代码生成问题，也覆盖 JIT 特有机制，如 **speculation** 与运行时交互。
- 摘要未提供更细粒度的标准数据集指标（如统一 benchmark 上的 precision/recall、吞吐量或与现有工具的直接数值对比），最强的量化证据主要是上述缺陷发现数量和 **92.40%** 的时间缩减。

## Link
- [http://arxiv.org/abs/2603.06551v1](http://arxiv.org/abs/2603.06551v1)
