---
source: arxiv
url: http://arxiv.org/abs/2604.10761v1
published_at: '2026-04-12T18:09:53'
authors:
- "Agust\xEDn Balestra"
- "Agust\xEDn Nolasco"
- Facundo Molina
- Diego Garbervetsky
- Renzo Degiovanni
- Nazareno Aguirre
topics:
- dynamic-specification-inference
- llm-based-testing
- counterexample-generation
- code-intelligence
- program-analysis
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Improving Dynamic Specification Inference with LLM-Generated Counterexamples

## Summary
## 摘要
本文在动态规格推断中加入了一个基于 LLM 的反例步骤，从而可以用可执行测试删去无效的推断断言。在 43 个 Java 方法上，这种方法在保持召回率不变的同时，提高了相较于 SpecFuzzer 的精确率。

## 问题
- Daikon 和 SpecFuzzer 这类动态规格推断工具会从执行轨迹中推断可能的前置条件、后置条件和不变式，但它们的输出取决于测试集覆盖率。
- 测试集如果薄弱或不完整，就会留下很多假阳性：这些断言能匹配已观察到的运行，但一般情况下并不成立。
- 这些无效断言会增加人工审查工作，也会影响验证、测试生成、调试和修复等下游用途。

## 方法
- 流水线从 SpecFuzzer 开始，先生成候选后置条件，再用现有测试集筛选。
- 对每个推断出的后置条件，LLM 会读取完整的类代码、目标方法和候选断言，然后判断该断言是否有效。
- 如果 LLM 判断断言无效，它必须生成一个可执行的 JUnit 测试，作为反例。该测试会被编译，必要时最多修复三次。
- 所有能够编译通过的反例测试都会加入原始测试集，然后再次运行 SpecFuzzer，用这些新测试删去被否定的断言。
- 评估使用了来自 GAssert 和 EvoSpex 相关基准的 43 个 Java 方法，并结合自动化的 SAT/SMT 事实核查器。测试的模型包括 GPT-5.1、Llama 3.3 70B 和 DeepSeek-R1。

## 结果
- GPT-5.1 生成的反例删去了 SpecFuzzer 推断出的 1,877 个无效规格，噪声减少 10.09%。
- Llama 3.3 70B 删去了 1,048 个无效断言，噪声减少 5.63%。
- DeepSeek-R1 删去了 2,173 个无效断言，噪声减少 11.68%，这是摘录中报告的最佳无效断言减少幅度。
- SpecFuzzer+GPT-5.1 在基准事实真值上达到 74.17% 的精确率、54.57% 的召回率和 53.94% 的 F1，精确率比 SpecFuzzer 高约 7%，召回率没有下降。
- Llama 3.3 70B 让 SpecFuzzer 的精确率提高了约 3.5%。
- DeepSeek-R1 让 SpecFuzzer 的精确率提高了约 8%，摘要还说召回率没有受到影响。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.10761v1](http://arxiv.org/abs/2604.10761v1)
