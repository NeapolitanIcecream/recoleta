---
source: arxiv
url: https://arxiv.org/abs/2607.15762v1
published_at: '2026-07-17T08:53:19'
authors:
- Mingxuan Zhu
- Qingyuan Liang
- Junjie Chen
- Zhihong Xue
- Dan Hao
topics:
- compiler-fuzzing
- code-intelligence
- llm-test-generation
- coverage-guided-testing
- automated-software-production
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# GapForge: Directed Compiler Fuzzing via Coverage-Gap Analysis

## Summary
## 摘要
GapForge 是一种基于 LLM 的编译器模糊测试技术，针对特定的源代码覆盖率缺口，而不是在缺乏全局编译器指导的情况下生成测试。在 GCC 14.3.0 和 LLVM 19.1.0 上，它提升了 72 小时覆盖率，并发现了 12 个实际编译器故障。

## 问题
- GCC 和 LLVM 等大型编译器包含大量覆盖不足的长尾代码区域，通用模糊测试工具经常无法触达这些区域。
- 触达未覆盖区域通常同时需要特定的程序结构和编译器选项，而文件级摘要和程序驱动的生成技术无法可靠地推断这些要求。
- 这一点很重要，因为编译器缺陷可能导致下游软件崩溃或静默错误编译。

## 方法
- GapForge 使用 `L_f × (1-C_f)^2` 为源文件评分，优先选择规模较大且行覆盖率较低的文件，然后在每轮迭代中采样一个目标文件。
- LLM 将每个未覆盖的代码行区间与附近的已覆盖上下文结合起来进行分析，推断触达目标基本块所需的控制流、数据和编译选项条件。
- 它合成一个提示词，将通用的 C/C++ 生成约束、这些目标条件以及同一文件此前失败的提示词结合起来。
- 生成的程序会经过编译，并通过覆盖率反馈进行测量；这些反馈用于指导后续的目标选择和提示词优化。

## 结果
- 在 72 小时内，GapForge 在 GCC 核心模块上达到 68.13% 的行覆盖率，在 LLVM 核心模块上达到 69.11%。
- 与 WhiteFox 相比，它在 GCC 上多覆盖了 24,736 行，在 LLVM 上多覆盖了 19,798 行；WhiteFox 在两者上的覆盖率分别为 64.62% 和 65.02%。
- 与报告结果最佳的基线 LegoFuzz 相比，后者在 GCC 和 LLVM 上的覆盖率分别为 64.99% 和 66.59%，GapForge 在官方测试套件中的覆盖率也分别多增加了 3,452 行 GCC 代码和 531 行 LLVM 代码，而 LegoFuzz 分别增加了 705 行和 143 行。
- GapForge 发现了 12 个实际编译器故障：GCC 中 5 个、LLVM 中 7 个，其中包括 8 个崩溃和 4 个错误编译。
- 九个消融变体的表现均不如完整系统，这表明目标选择、定向摘要、编译选项推断和失败反思机制都作出了贡献。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.15762v1](https://arxiv.org/abs/2607.15762v1)
