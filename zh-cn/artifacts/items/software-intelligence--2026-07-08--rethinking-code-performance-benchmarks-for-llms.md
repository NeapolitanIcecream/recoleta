---
source: arxiv
url: https://arxiv.org/abs/2607.07619v1
published_at: '2026-07-08T16:36:03'
authors:
- Nhat Minh Le
- Yisen Xu
- Zhijie Wang
- Tse-Hsun
- Chen
topics:
- llm-code-generation
- code-performance-benchmarks
- performance-testing
- multi-agent-testing
- statistical-evaluation
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Rethinking Code Performance Benchmarks for LLMs

## Summary
## 摘要
本文发现，现有的函数级 Python 性能基准往往无法显示 LLM 生成的代码是否更快。作者重新测试了四个基准，并提出了一个多智能体测试生成系统，用来暴露更多运行时间差异。

## 问题
- 面向 LLM 代码生成的性能基准通常会将生成代码与标准解进行比较，但测试可能规模太小，或过于关注正确性，难以暴露速度差异。
- 单次或少量运行的计时容易受到调度、缓存状态和后台进程造成的运行时噪声影响。
- 这个问题很重要，因为较弱的基准可能让高效代码看起来没有优势，也会削弱关于 LLM 代码效率的基准结论可信度。

## 方法
- 作者重新评估了 EffiBench、Enamel、EvalPerf 和 Mercury 中的 1,538 个任务。
- 对每个任务，作者在原始基准测试上分别运行标准解和基准提供的高性能实现 30 次。
- 作者使用 Mann-Whitney U 检验并以 p < 0.05 判断单个任务的运行时间差异，使用 Cliff’s delta 衡量效应量，并使用 Wilcoxon 符号秩检验进行基准级比较。
- 作者人工检查了 308 个差异不显著的任务，并使用 DeepSeek-V3.1 和 GPT-4o 作为评判器，将分析扩展到其余差异不显著的任务。
- 作者构建了一个三智能体测试生成系统：一个智能体生成面向性能的测试，一个诊断失败或较弱的测试，一个在保持功能正确性的同时修复测试。

## 结果
- 在原始测试上，1,538 个基准提供的高性能实现中，只有 94 个显著快于标准解，总体占比为 6.11%。
- 四个基准中差异不显著的比例都很高：EffiBench 为 944/1,000 个任务，Enamel 为 153/164，EvalPerf 为 102/118，Mercury 为 245/256。
- 在差异显著的任务中，94 个里有 92 个具有较大的 Cliff’s delta 效应量；1 个效应量较小，1 个效应量中等。
- 在 308 个差异不显著任务的人工样本中，99 个高性能实现没有有意义的性能变化，209 个包含可能的性能改进，但被原始测试掩盖。
- DeepSeek-V3.1 和 GPT-4o 与人工标签的一致性分别达到 Cohen’s Kappa 0.72 和 0.75，随后将剩余差异不显著任务中的 76.06% 和 73.94% 标注为具有潜在性能影响。
- 在 1,345 个此前差异不显著的任务上，生成测试显示：使用 DeepSeek-V3.1 测试时，有 323 个任务出现显著改进，占 24.01%；使用 GPT-4o 测试时，有 342 个任务出现显著改进，占 25.43%；更强的测试还在所评估的 GPT-4o-mini、Claude-Sonnet-4.5 和 Gemini-2.5-Flash 输出中暴露出 22.19% 的显著收益。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.07619v1](https://arxiv.org/abs/2607.07619v1)
