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
这篇论文衡量代码 LLM 的性能在多大程度上依赖对基准数据的记忆，而不是对代码的普遍理解。论文通过输入扰动来估计模型在多种软件工程任务和基准上的“记忆优势”。

## 问题
- 代码 LLM 的训练数据通常不透明，因此很难直接验证基准泄漏。
- 如果评测样例出现在训练数据中，基准分数就可能高估模型真实的泛化能力。
- 这会影响代码生成、修复、测试和安全任务，因为依赖回忆已知样例的模型，面对新问题中的细小变化时可能会失败。

## 方法
- 论文将**记忆优势**定义为原始输入与该输入轻微扰动版本之间的性能差距。
- 对每个样本，研究会构造逐步增强、但仍保持人类可理解语义的扰动，用每个变体提示模型，并根据参考输出衡量任务表现。
- 研究使用相邻扰动级别之间的最大性能下降作为该样本的敏感度分数：高敏感度说明模型更依赖记忆化模式，或泛化能力较弱。
- 该研究在 19 个基准上评估了 8 个开源代码 LLM，覆盖代码生成、代码理解、漏洞检测、错误识别、测试生成和程序修复。
- 研究比较了不同模型和不同基准上的敏感度分布，使用 Mann-Whitney U 检验和 Bonferroni 校正，设置为 3 次重复、temperature 0.3 和 top_k 0.5。

## 结果
- **StarCoder** 在一些基准上表现出较高敏感度，在 **APPS** 上达到 **0.8**，而 **QwenCoder** 在大多数基准上都低于 **0.4**。
- **代码摘要**任务的敏感度较低，通常 **<0.3**，论文据此认为该任务上的泛化更强。
- **测试生成**的敏感度更高，约为 **0.4-0.7**，且 **p < 0.001**，是最难实现稳定泛化的场景之一。
- **Defects4J** 的敏感度低于其他程序修复基准，约为 **0.2-0.4**，且 **p < 0.01**；其他修复数据集则为 **0.5-0.8**。
- **CVEFixes** 在各模型上的敏感度都低于 **0.1**，这削弱了该基准受到严重污染这一常见说法。
- 论文的核心结论是，像 **CVEFixes** 和 **Defects4J** 这类被怀疑存在泄漏的基准，可能更多反映了真实泛化，而不是简单记忆；同时，敏感度会随模型家族和任务类别显著变化。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13997v1](http://arxiv.org/abs/2604.13997v1)
