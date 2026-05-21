---
source: arxiv
url: https://arxiv.org/abs/2604.26923v1
published_at: '2026-04-29T17:38:37'
authors:
- Yeheng Chen
- Chaoxiang Xie
- Yuling Shi
- Wenhao Zeng
- Yongpan Wang
- Hongyu Zhang
- Xiaodong Gu
topics:
- code-generation
- code-benchmark
- class-level-synthesis
- llm-evaluation
- software-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# ClassEval-Pro: A Cross-Domain Benchmark for Class-Level Code Generation

## Summary
## 摘要
ClassEval-Pro 是一个包含 300 个任务的基准，用于根据规格生成完整的 Python 类。它评测类级代码生成，要求模型协调方法、共享状态和领域逻辑。

## 问题
- 当前代码基准主要关注孤立函数或仓库问题修复，因此遗漏了从零构建类的能力。
- 类级生成很重要，因为面向对象软件通常需要多个方法共享状态，并正确地相互调用。
- 现有类级基准规模小、依赖人工整理且年代较早，这会带来成本和训练数据污染方面的担忧。

## 方法
- 该基准构建了 300 个类级任务，覆盖 11 个领域，其中 233 个是跨领域任务，67 个是同领域任务。
- 流程从 2025 年 1 月 1 日或之后创建的 GitHub 仓库中收集 Python 类，然后筛选只依赖标准库、可自包含、至少有 5 个方法且长度为 40 到 800 行的类。
- 它使用 AST 引导的提示合并类结构，创建更难的类骨架，用来组合领域逻辑。
- 它用 LLM 生成测试，使用三个 LLM 评审检查骨架与测试是否一致，并且只保留至少两个评审给出满分的样例。
- 它只保留参考解法可编译、通过所有测试且行覆盖率超过 90% 的任务。

## 结果
- ClassEval-Pro 包含 300 个任务，覆盖 11 个领域。源池包含 206 个仓库、1,114 个抽取出的类，筛选后剩下 383 个类。
- 新任务比 ClassEval 更大：跨领域任务的平均 LOC 为 117.0，同领域任务为 122.0，而 ClassEval 为 45.7。
- 新任务的结构指标更高：跨领域任务的平均依赖深度为 3.01，同领域任务为 2.85，而 ClassEval 为 1.77；平均方法数分别为 9.53 和 8.60，而 ClassEval 为 4.97。
- 在整体生成策略下，五个 LLM 的类级 Pass@1 介于 27.9% 到 45.6% 之间，差距为 17.7 个百分点。
- 策略选择影响很大：自底向上生成可将较弱模型的表现最多提高 9.4 个百分点，而组合式生成的类级 Pass@1 最低降至 1.3%。
- 在 500 个经过人工标注的失败样例中，逻辑错误占 56.2%，依赖错误占 38.0%，说明跨方法协调是主要失败来源。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26923v1](https://arxiv.org/abs/2604.26923v1)
