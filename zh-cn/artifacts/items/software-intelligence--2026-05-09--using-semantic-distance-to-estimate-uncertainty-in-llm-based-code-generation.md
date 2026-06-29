---
source: arxiv
url: https://arxiv.org/abs/2605.09023v1
published_at: '2026-05-09T16:02:54'
authors:
- Weilin He
- Arindam Sharma
- Cristina David
topics:
- code-generation
- uncertainty-estimation
- semantic-distance
- fuzz-testing
- code-intelligence
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Using Semantic Distance to Estimate Uncertainty in LLM-Based Code Generation

## Summary
## 摘要
本文提出了 SDE 和 DSDE 两个基于执行结果的 LLM 代码生成不确定性分数，用来估计首个生成程序是否可能出错。它们根据在共享的模糊测试输入上的行为距离，对采样程序进行比较，而不是把所有分歧都当成同一类问题。

## 问题
- LLM 代码生成器会输出看起来合理的代码，但没有正确性保证；当生成代码在没有完整外部验证的情况下直接使用时，这个问题很重要。
- 现有的基于采样的不确定性方法通常把行为分歧当成二值事件处理，因此一次输入不匹配和所有输入都失败可能得到相同处理。
- 开发者需要一个不依赖参考答案的信号，在完整验证之前，或在把代码展示给用户之前，给生成代码按可能正确性排序。

## 方法
- 该方法对同一任务采样 K 个候选程序，并在 N 个共享的模糊测试输入上运行它们。
- 具有相同执行签名的程序会被分到语义簇中。每个签名记录正常输出和按错误类型区分的异常终止。
- 方法通过对每个输入上的结果差异取平均，给不同簇之间分配分级距离。正常输出不匹配的代价为 1；异常情况使用固定权重 a、b 和 c。
- SDE 按簇概率，对所有簇对的加权距离取平均。DSDE 则把备选簇与包含最高排名程序的簇进行比较。
- 这条流程只需要生成的代码和可执行输入，不需要模型内部信息、嵌入，也不需要 LLM-as-judge 调用。

## 结果
- 在闭源模型的 LiveCodeBench 上，DSDE 在 pass@1 失败预测中，GPT-3.5-Turbo 的 AUROC 为 0.844，GPT-4o-mini 为 0.844，Gemini-2.5-Flash-Lite 为 0.808，Claude Opus 4.5 为 0.825。
- 在 LiveCodeBench 上，DSDE 在表中列出的每个模型和指标上都优于报告中的基线。例子：对 GPT-4o-mini，DSDE 的 AUROC 为 0.844，而 DiffTrust 为 0.534，HonestCoder 为 0.646，Semantic Entropy 为 0.607。
- DSDE 与 LiveCodeBench 上的部分正确性相关。对 GPT-4o-mini，和 partial_pass@1 对比时，Pearson r 为 -0.624，Spearman rho 为 -0.624。
- 泛化结果包括：在报告的 GPT-4o-mini 设置下，DSDE 在 MBPP 上 AUROC 为 0.752，在 LiveCodeBench 上为 0.844，在 BigCodeBench 上为 0.668，在 HumanEval-X 的 Python 上为 0.757，Java 上为 0.745，C++ 上为 0.804。
- 在运行时间表中，这个方法比基线更便宜：在 K=10、N=10 时，每个 LiveCodeBench 任务大约 5.7 秒，而 HonestCoder 约 11 秒，Semantic Entropy 约 13 秒，DiffTrust 约 27 秒。
- 更小的 K=3、N=3 设置仍然能在 GPT-4o-mini 的 LiveCodeBench 上达到 DSDE AUROC 0.783，约为 K=10、N=10 时 AUROC 的 93%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09023v1](https://arxiv.org/abs/2605.09023v1)
