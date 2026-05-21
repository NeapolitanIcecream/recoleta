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
论文提出了 SDE 和 DSDE，这是两种用于 LLM 代码生成的基于执行的不确定性评分，用来估计第一个生成程序是否可能出错。它们在共享的模糊测试输入上，用分级的行为距离比较采样程序，而不是把每次分歧都当成同等严重。

## 问题
- LLM 代码生成器会生成看起来合理但没有正确性保证的代码。如果生成代码在缺少完整外部验证的情况下被使用，这一点会带来风险。
- 现有基于采样的不确定性方法通常把行为分歧按二元方式计数，所以一个测试用例不匹配可能会和所有输入都失败得到相同处理。
- 开发者需要一种不依赖参考答案的信号，在运行完整验证或向用户展示代码之前，按可能正确性对生成代码排序。

## 方法
- 该方法为同一任务采样 K 个候选程序，并在 N 个共享的模糊测试输入上运行它们。
- 执行签名相同的程序会被分到语义簇中。每个签名记录正常输出，以及按错误类型划分的异常终止。
- 该方法通过对每个输入的结果差异取平均，为簇之间分配分级距离。正常输出不匹配的代价为 1；异常情况使用固定权重 a、b 和 c。
- SDE 使用簇概率，对所有簇对的加权距离取平均。DSDE 将其他簇与包含最高排名程序的簇进行比较。
- 该流程只需要生成代码和可执行输入。它不使用模型内部信息、嵌入或 LLM-as-judge 调用。

## 结果
- 在使用闭源模型的 LiveCodeBench 上，DSDE 在 pass@1 失败预测中，对 GPT-3.5-Turbo 的 AUROC 达到 0.844，对 GPT-4o-mini 为 0.844，对 Gemini-2.5-Flash-Lite 为 0.808，对 Claude Opus 4.5 为 0.825。
- 在 LiveCodeBench 上，DSDE 在列出的每个模型和指标上都超过了报告的基线。示例：对于 GPT-4o-mini，DSDE 的 AUROC 为 0.844，而 DiffTrust 为 0.534，HonestCoder 为 0.646，Semantic Entropy 为 0.607。
- DSDE 与 LiveCodeBench 上的部分正确性相关。对于 GPT-4o-mini，相对于 partial_pass@1，Pearson r 为 -0.624，Spearman rho 为 -0.624。
- 在报告的 GPT-4o-mini 设置下，DSDE 的泛化结果包括 MBPP AUROC 0.752、LiveCodeBench AUROC 0.844、BigCodeBench AUROC 0.668、HumanEval-X Python AUROC 0.757、Java AUROC 0.745，以及 C++ AUROC 0.804。
- 在运行时间表中，该方法比基线更省成本：K=10、N=10 时，每个 LiveCodeBench 任务约 5.7 秒，而 HonestCoder 约 11 秒，Semantic Entropy 约 13 秒，DiffTrust 约 27 秒。
- 较小的 K=3、N=3 设置在使用 GPT-4o-mini 的 LiveCodeBench 上仍达到 DSDE AUROC 0.783，约为 K=10、N=10 时 AUROC 的 93%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.09023v1](https://arxiv.org/abs/2605.09023v1)
