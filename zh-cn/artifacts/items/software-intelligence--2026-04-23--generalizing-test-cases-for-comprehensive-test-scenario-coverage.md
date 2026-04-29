---
source: arxiv
url: http://arxiv.org/abs/2604.21771v2
published_at: '2026-04-23T15:29:09'
authors:
- Binhang Qi
- Yun Lin
- Xinyi Weng
- Chenyan Liu
- Hailong Sun
- Gordon Fraser
- Jin Song Dong
topics:
- test-generation
- software-testing
- llm-for-code
- scenario-coverage
- java
- program-analysis
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# Generalizing Test Cases for Comprehensive Test Scenario Coverage

## Summary
## 摘要
TestGeneralizer 把开发者写的一个测试扩展成更多测试，用来覆盖方法预期的行为场景。它针对的是场景覆盖率，而不是分支覆盖率；在一个 Java 基准上，它报告的覆盖效果优于 EvoSuite、gpt-o4-mini 和 ChatTester。

## 问题
- 现有自动化测试生成工具大多优化代码覆盖率，但开发者编写测试是为了检查由需求驱动的场景，这些场景可能并不对应控制流分支。
- 首个测试写出时，重要场景往往还缺失，之后常常要等到出现 bug 或收到问题报告才补上，这会让测试更慢，也不够完整。
- 需求常常隐含在代码和测试中，因此任务是从单个初始测试中推断出隐藏的测试模式，并生成有效的场景变体。

## 方法
- 系统接收一个目标方法、一个已有测试和项目代码库，然后运行一个名为 TestGeneralizer 的三阶段流程。
- 第 1 阶段使用 **Masked Oracle Modeling (MOM)**：它把原始测试中的断言改写成可执行但错误的备选项，再让 LLM 选出正确答案。如果模型不确定或选错，系统会通过程序分析提取项目事实，以改进理解。
- 第 2 阶段让 LLM 编写一个**测试场景模板**：这是一个紧凑的计划，包含输入风格、对象类型或 API 选择等变化点。然后系统把这些变化点实例化为具体的场景实例，并为每个实例生成主要和备选预言结果。
- 为了更准确地识别变化点，提示词会自动调优。为了让实例化后的场景符合项目实际，系统会用 CodeQL 和 JDTLS 等工具提取代码事实。
- 第 3 阶段为每个场景实例生成可执行测试，并迭代修复编译错误、运行时错误和断言失败，直到测试通过或达到迭代上限。

## 结果
- 评估覆盖 **12 个开源 Java 项目**、**506 个带多个测试的目标方法**，以及 **1,637 个测试场景**。
- 相比 **EvoSuite**，TestGeneralizer 的**基于变异的场景覆盖率提升了 57.67%**，**由 LLM 评估的场景覆盖率提升了 59.62%**。
- 相比 **gpt-o4-mini**，它的**基于变异的场景覆盖率提升了 37.44%**，**由 LLM 评估的场景覆盖率提升了 32.82%**。
- 相比 **ChatTester**，它的**基于变异的场景覆盖率提升了 31.66%**，**由 LLM 评估的场景覆盖率提升了 23.08%**。
- 在一项现场研究中，作者提交了 **27** 个开发者遗漏的生成测试；其中 **16** 个被接受并合并进官方仓库。
- 论文还称，该方法在商业和开源 LLM 上都表现稳定，包括 **ChatGPT** 和 **DeepSeek-V3.1**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21771v2](http://arxiv.org/abs/2604.21771v2)
