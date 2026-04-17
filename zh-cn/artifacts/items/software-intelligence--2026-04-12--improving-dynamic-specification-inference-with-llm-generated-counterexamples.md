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
这篇论文在动态规格推断流程中加入了一个基于 LLM 的反例步骤，用可执行测试删除无效的推断断言。在 43 个 Java 方法上，这种方法相比 SpecFuzzer 提高了精确率，同时保持召回率不变。

## 问题
- Daikon 和 SpecFuzzer 这类动态规格推断工具会根据执行轨迹推断可能的前置条件、后置条件和不变式，但输出结果依赖测试套件的覆盖率。
- 测试套件较弱或不完整时，很多假阳性会保留下来：这些断言与已观察到的运行一致，但整体上并不成立。
- 这些无效断言会增加人工审查工作，也会影响验证、测试生成、调试和修复等下游用途。

## 方法
- 这条流程从 SpecFuzzer 开始，它先生成候选后置条件，再用现有测试套件进行过滤。
- 对每个推断出的后置条件，LLM 会接收完整的类代码、目标方法和候选断言，然后判断该断言是否有效。
- 如果 LLM 判断断言无效，就必须生成一个可执行的 JUnit 测试，作为反例。测试会被编译；如果失败，最多可进行三次修复尝试。
- 所有能够成功编译的反例测试都会加入原始测试套件，然后在扩充后的测试套件上再次运行 SpecFuzzer，以删除被新测试证伪的断言。
- 评估使用了来自 GAssert 和 EvoSpex 相关基准的 43 个 Java 方法，以及基于 SAT/SMT 的自动真值检查器。测试的模型包括 GPT-5.1、Llama 3.3 70B 和 DeepSeek-R1。

## 结果
- GPT-5.1 生成的反例删除了 SpecFuzzer 推断出的 1,877 条无效规格，使噪声降低了 10.09%。
- Llama 3.3 70B 删除了 1,048 条无效断言，使噪声降低了 5.63%。
- DeepSeek-R1 删除了 2,173 条无效断言，使噪声降低了 11.68%，这是摘录中报告的最佳无效断言削减效果。
- SpecFuzzer+GPT-5.1 相对于基准真值得到 74.17% 的精确率、54.57% 的召回率和 53.94% 的 F1，精确率比 SpecFuzzer 提高约 7%，且没有召回损失。
- Llama 3.3 70B 将 SpecFuzzer 的精确率提高了约 3.5%。
- 根据摘要，DeepSeek-R1 将 SpecFuzzer 的精确率提高了约 8%，同时也没有影响召回率。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.10761v1](http://arxiv.org/abs/2604.10761v1)
