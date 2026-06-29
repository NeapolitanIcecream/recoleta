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
TestGeneralizer 把一个开发者编写的测试扩展成更多测试，用来覆盖方法预期的行为场景。它关注的是场景覆盖，而不是分支覆盖，并且在一个 Java 基准上报告的覆盖率优于 EvoSuite、gpt-o4-mini 和 ChatTester。

## 问题
- 现有自动化测试生成工具主要优化代码覆盖率，但开发者写测试是为了检查由需求驱动的场景，而这些场景不一定对应控制流分支。
- 在写出第一个测试时，重要场景经常缺失，之后才因为 bug 或问题报告补上，这会让测试变慢，也不够完整。
- 需求常常隐含在代码和测试里，因此任务是从一个初始测试中推断隐藏的测试模式，并生成有效的场景变体。

## 方法
- 系统接收一个目标方法、一个已有测试和项目代码库，然后运行名为 TestGeneralizer 的三阶段流程。
- 第 1 阶段使用 **Masked Oracle Modeling (MOM)**：它把原始测试的断言改写成可执行的错误备选项，再让 LLM 选出正确项。如果模型不确定或选错，就通过程序分析检索项目事实，以改善理解。
- 第 2 阶段让 LLM 编写一个 **test scenario template**：一个简洁的计划，包含输入风格、对象类型或 API 选择等变化点。随后它把这些变化点实例化成具体的场景实例，并为每个实例生成主断言和备选断言。
- 为了让变化点检测更准确，提示词会自动调优。为了让实例化后的场景符合项目约束，系统会用 CodeQL 和 JDTLS 等工具检索代码事实。
- 第 3 阶段为每个场景实例生成可执行测试，并迭代修复编译错误、运行时错误和断言失败，直到测试通过或达到迭代上限。

## 结果
- 评估覆盖 **12 个开源 Java 项目**、**506 个多测试目标方法** 和 **1,637 个测试场景**。
- 与 **EvoSuite** 相比，TestGeneralizer 的 **基于突变的场景覆盖率** 提升 **57.67%**，**LLM 评估的场景覆盖率** 提升 **59.62%**。
- 与 **gpt-o4-mini** 相比，它的 **基于突变的场景覆盖率** 提升 **37.44%**，**LLM 评估的场景覆盖率** 提升 **32.82%**。
- 与 **ChatTester** 相比，它的 **基于突变的场景覆盖率** 提升 **31.66%**，**LLM 评估的场景覆盖率** 提升 **23.08%**。
- 在一项实地研究中，作者提交了 **27** 个开发者漏掉的生成测试；其中 **16** 个被接受并合并到官方仓库。
- 论文还声称，该方法在商业和开源 LLM 上都表现一致，包括 **ChatGPT** 和 **DeepSeek-V3.1**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.21771v2](http://arxiv.org/abs/2604.21771v2)
