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
- performance-testing
- compiler-bugs
- differential-testing
- empirical-study
relevance_score: 0.01
run_id: materialize-outputs
---

# Understanding and Finding JIT Compiler Performance Bugs

## Summary
本文研究JIT编译器中的性能缺陷：这类缺陷不会让程序算错，但会让编译或运行明显变慢。作者先分析4个主流JIT中的191个真实缺陷，再提出自动检测工具Jittery。

## Problem
- 论文要解决的是**JIT编译器性能bug**的理解与自动发现问题，包括两类：**编译过慢**和**生成代码运行过慢**。
- 这很重要，因为JIT在程序运行时做优化；一旦出错，应用会在真实执行过程中直接遭遇延迟、吞吐下降或回退，而应用开发者往往无法在源码层面彻底修复。
- 以往工作主要关注JIT**功能正确性bug**或AOT/应用层性能bug，几乎没有系统方法专门面向JIT性能bug，而JIT又有 profiling、speculation、deoptimization、tiered compilation 等独特复杂性。

## Approach
- 作者先做了首个较系统的经验研究：从 **HotSpot、Graal、V8、SpiderMonkey** 收集并人工筛选真实缺陷，最终分析 **191** 个报告，归纳触发输入、表现模式和根因。
- 研究发现很多性能bug可由**小型微基准**触发，而不是必须依赖完整基准套件；很多bug通过**差分信号**暴露，例如不同JIT配置、不同版本或等价执行之间的性能差异。
- 基于这些洞察，作者提出 **layered differential performance testing**：为大量随机小程序，在两种JIT配置下执行并比较时间差异，把明显异常的程序标记为候选缺陷。
- 为了兼顾速度与准确性，方法采用**分层测试**：前几层用少量迭代快速淘汰无异常样例，后几层才对剩余候选做更严格、更高迭代次数的测量。
- 工具 **Jittery** 还加入实用优化：**test prioritization** 利用前层运行信息优先安排更可疑样例；并通过启发式方法自动过滤**误报和重复项**，减少人工审查负担。

## Results
- 经验研究覆盖 **4** 个主流JIT编译器、初始收集 **272** 个问题，人工过滤后保留并分析 **191** 个真实性能bug。
- 作者声称约**近一半**的性能bug可以由**小而集中的微基准**暴露，而不需要完整benchmark suite；这是其测试设计的重要依据。
- Jittery 的 **test prioritization** 将测试时间降低 **92.40%**，同时声称**不损害**缺陷发现能力。
- 使用 Jittery，作者在 **Oracle HotSpot** 和 **Graal** 中发现 **12** 个此前未知的性能bug。
- 这 **12** 个新bug中，**11** 个已被开发者确认，**6** 个已经修复。
- 摘要未提供更细的标准化性能指标数值（如具体 slowdown 倍数、precision/recall、每编译器发现率或与现有工具的直接对比），最强的量化结论主要是上述 bug 发现数和 **92.40%** 的时间缩减。

## Link
- [http://arxiv.org/abs/2603.06551v1](http://arxiv.org/abs/2603.06551v1)
