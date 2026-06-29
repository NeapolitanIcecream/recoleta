---
source: arxiv
url: https://arxiv.org/abs/2606.01522v1
published_at: '2026-06-01T01:09:13'
authors:
- Shriram Krishnamurthi
- Matthew Flatt
topics:
- ai-coding-agents
- type-errors
- program-repair
- compiler-diagnostics
- hindley-milner
- code-intelligence
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Type-Error Ablation and AI Coding Agents

## Summary
## 摘要
本文测试更详细的类型错误信息是否能帮助 AI 编程代理修复带类型的程序。在 Shplait 实验中，更丰富的编译器诊断改善了代理的修复表现，而且 97.9% 的去除类型错误的修复也通过了语义测试。

## 问题
- 编程语言的错误信息一直按人类读者来调，通常很短，只保留部分信息。
- AI 编程代理可以处理更长的诊断信息，所以过于简短的编译器输出可能会漏掉有用的修复线索。
- 这个问题很重要，因为编译器诊断现在进入了自动修复流程，而不只是在人工调试时使用。

## 方法
- 作者修改了 Shplait，这是一门带 Hindley-Milner 类型推断的 ML 风格语言，用来暴露多种诊断模式。
- 他们构建了 10 个正确的 Shplait 程序，并派生出 60 个损坏变体，每个变体都含有一个有意加入的类型错误，并且在不经过类型检查时至少会有 5 个测试失败。
- 他们比较了四种反馈模式：完整的统一栈、靠近错误位置、最小类型错误，以及不带类型信息的测试套件反馈。
- Aider 驱动修复循环，主要通过 ollama 使用 qwen2.5-coder:14b；作者还用 claude-haiku-4.5 跑了两轮完整实验。
- 一个确定性 oracle 通过运行类型检查器和测试，把每次最终尝试分成仍然是类型错误、语义错误，或语义正确。

## 结果
- 主要的 qwen2.5-coder:14b 实验用了 2,400 次试验：60 个干扰程序 × 4 种反馈模式 × 10 次完整运行。
- 论文报告说，更详细的类型错误信息提高了代理的修复率，其中完整统一栈模式优于更少细节的诊断；摘录里没有给出各模式的精确比例。
- 带类型的反馈优于只有测试套件、没有类型信息的反馈，所以类型检查器给代理提供了超出失败测试之外的修复信号。
- 在代理修复了类型错误的案例中，97.9% 也通过了全部语义测试。
- 在靠近位置模式中，报告的行号与注入错误的行号在 60 个干扰样本里有 39 个一致；另外 21 个案例说明了为什么 Hindley-Milner 诊断有时会指向真正来源之外的位置。
- 研究还报告说，即使把所有名字都做了混淆，领先的代理通常还是能修复程序，但摘录没有给出这一结果的精确成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.01522v1](https://arxiv.org/abs/2606.01522v1)
