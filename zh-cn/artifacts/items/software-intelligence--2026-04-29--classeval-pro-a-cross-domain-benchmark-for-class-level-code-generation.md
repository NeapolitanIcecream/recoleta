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
## 总结
ClassEval-Pro 是一个包含 300 个任务的基准，用于从规格说明生成完整的 Python 类。它面向类级代码生成，要求模型协调方法、共享状态和领域逻辑。

## 问题
- 现有代码基准主要关注孤立函数或仓库级问题修复，因此没有覆盖从零构建类。
- 类级生成很重要，因为面向对象软件通常需要多个方法共享状态并正确相互调用。
- 现有类级基准规模小、依赖人工整理，而且发布时间较早，这会带来成本和训练数据污染问题。

## 方法
- 该基准包含 300 个跨 11 个领域的类级任务，其中 233 个是跨领域任务，67 个是同领域任务。
- 该流程收集了 2025 年 1 月 1 日之后创建的 GitHub 仓库中的 Python 类，然后筛选出仅使用标准库、自包含、至少有 5 个方法且长度在 40 到 800 行之间的类。
- 它将类结构与 AST 引导的提示相结合，生成更难的类骨架，把不同领域的逻辑合并到一起。
- 它用 LLM 生成测试，再用 3 个 LLM 评审检查骨架与测试的匹配情况，只保留至少有 2 个评审给满分的案例。
- 它只保留参考解能通过编译、通过全部测试并且达到 90% 以上行覆盖率的任务。

## 结果
- ClassEval-Pro 包含 300 个任务，覆盖 11 个领域。源库共有 206 个仓库、1,114 个提取出的类，过滤后剩下 383 个类。
- 新任务比 ClassEval 更大：跨领域任务的平均代码行数为 117.0，同领域任务为 122.0，而 ClassEval 为 45.7。
- 新任务的结构指标更高：跨领域任务的平均依赖深度为 3.01，同领域任务为 2.85，而 ClassEval 为 1.77；平均方法数分别为 9.53 和 8.60，而 ClassEval 为 4.97。
- 在整体生成设置下，5 个 LLM 的类级 Pass@1 介于 27.9% 到 45.6% 之间，相差 17.7 个百分点。
- 策略选择影响很大：自底向上的生成方式让较弱模型最高提升 9.4 个百分点，而组合式生成的类级 Pass@1 低至 1.3%。
- 在 500 个人工标注的失败案例中，逻辑错误占 56.2%，依赖错误占 38.0%，说明跨方法协调是主要失败来源。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26923v1](https://arxiv.org/abs/2604.26923v1)
