---
source: arxiv
url: http://arxiv.org/abs/2604.13997v1
published_at: '2026-04-15T15:43:10'
authors:
- "Djir\xE9 Alb\xE9rick Euraste"
- "Kabor\xE9 Abdoul Kader"
- Jordan Samhi
- Earl T. Barr
- Jacques Klein
- "Tegawend\xE9 F. Bissyand\xE9"
topics:
- code-llm-evaluation
- memorization-detection
- benchmark-contamination
- perturbation-analysis
- software-engineering-benchmarks
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Learned or Memorized ? Quantifying Memorization Advantage in Code LLMs

## Summary
## 摘要
本文衡量代码 LLM 的性能有多大程度依赖于记忆过的基准数据，而不是一般性的代码理解。它用输入扰动来估计模型在多个软件工程任务和基准上的“记忆优势”。

## 问题
- 代码 LLM 的训练数据通常不透明，因此很难直接验证基准泄漏。
- 如果评测样例出现在训练中，公开的基准分数可能会高估真实泛化能力。
- 这会影响代码生成、修复、测试和安全任务，因为记住已知样例的模型在新问题的细微变化上可能会失效。

## 方法
- 论文把 **记忆优势** 定义为原始输入与其轻微扰动版本之间的性能差距。
- 对每个样本，论文生成逐步增强但仍保持人工可读的扰动版本，分别向模型提问，并用参考输出衡量任务表现。
- 它把相邻扰动层级之间的最大性能下降作为样本的敏感度分数：高敏感度说明更依赖记忆模式或泛化较弱。
- 研究评估了 8 个开源代码 LLM 在 19 个基准上的表现，覆盖代码生成、代码理解、漏洞检测、缺陷识别、测试生成和程序修复。
- 论文使用 Mann-Whitney U 检验并做 Bonferroni 校正，对不同模型和不同基准的敏感度分布进行比较，设置为 3 次重复、temperature 0.3、top_k 0.5。

## 结果
- **StarCoder** 在部分基准上敏感度很高，在 **APPS** 上达到 **0.8**；**QwenCoder** 在大多数基准上都低于 **0.4**。
- **代码摘要** 的敏感度较低，通常 **<0.3**，论文把这解读为该任务上的泛化更强。
- **测试生成** 的敏感度更高，约 **0.4-0.7**，且 **p < 0.001**，是稳定泛化最困难的场景之一。
- **Defects4J** 的敏感度低于其他程序修复基准，约 **0.2-0.4**，且 **p < 0.01**；其他修复数据集则在 **0.5-0.8** 之间。
- **CVEFixes** 在各模型上都低于 **0.1**，这削弱了它被严重污染的常见说法。
- 论文的主要结论是，像 **CVEFixes** 和 **Defects4J** 这类被怀疑泄漏的基准，可能更多反映真实泛化，而不是单纯记忆；同时，敏感度会随模型家族和任务类别明显变化。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13997v1](http://arxiv.org/abs/2604.13997v1)
