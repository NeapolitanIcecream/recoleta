---
source: arxiv
url: http://arxiv.org/abs/2604.19315v1
published_at: '2026-04-21T10:24:26'
authors:
- Jamie Lee
- Flynn Teh
- Hengcheng Zhu
- Mengzhen Li
- Mattia Fazzini
- Valerio Terragni
topics:
- llm-test-generation
- unit-testing
- mocking
- java
- mutation-testing
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Improving LLM-Driven Test Generation by Learning from Mocking Information

## Summary
## 摘要
MockMill 通过向模型输入开发者编写的测试中已经存在的 mocking 信息，提升了基于 LLM 的单元测试生成能力。在来自 6 个开源项目的 10 个 Java 类上，它生成了可执行测试，这些测试经常覆盖到现有测试、普通 LLM 基线和 Randoop 漏掉的代码，并杀死它们漏掉的变异体。

## 问题
- LLM 可以生成单元测试，但它们通常只依赖被测类和附近文本，而忽略了测试替身里已经编码的行为，例如 Mockito 的 stubbing 和 verify 调用。
- 这会丢掉具体的使用知识：依赖的方法会被怎么调用，参数是什么，以及应该返回什么值或异常。
- 这很重要，因为符合真实依赖行为的测试可以覆盖更难的路径，并发现通用生成测试漏掉的故障。

## 方法
- MockMill 扫描现有的 Java 测试套件，找出在其他测试中作为 mock 依赖出现的项目类。
- 它用 AST 分析从 JUnit 5 和 Mockito 测试中提取 mocking 事实，主要是 stubbing 和 verify 操作，并把相关的方法调用、参数、返回值和异常存成结构化 JSON。
- 它向 LLM 提供三个输入：目标类的完整源代码、面向变异敏感断言的明确测试生成指令，以及提取出的 mock 信息。
- 它要求 LLM 基于目标类的真实实例构建测试，同时复用 mock 中出现的精确值和交互模式。
- 生成后，它运行一个迭代的编译、执行、修复循环，把编译错误或运行时错误反馈给 LLM，直到测试通过或达到重试上限。

## 结果
- 数据集：来自 6 个开源 Java 项目的 10 个类；评估使用了 4 个 LLM：GPT-4o Mini、GPT-5 Mini、GPT-5 和 Claude Sonnet 4.5。
- 修复后的可执行性很高：最终编译通过率在 GPT-4o Mini 上达到 92%，在 GPT-5、GPT-5 Mini 和 Claude Sonnet 4.5 上达到 100%；测试通过率分别达到 81.6%、98.6%、99.7% 和 99.7%。
- MockMill 下的中位变异分数在 GPT-4o Mini 上为 43%，在 GPT-5 上为 62%，在 GPT-5 Mini 上为 84%，在 Claude Sonnet 4.5 上为 89%；最高变异分数分别达到 85%、100%、100% 和 100%。
- MockMill 下的中位行覆盖率在 GPT-4o Mini 上为 58%，在 GPT-5 上为 91%，在 GPT-5 Mini 上为 93%，在 Claude Sonnet 4.5 上为 94%；最高行覆盖率分别达到 93%、100%、100% 和 100%。
- 测试数量因模型而异：MockMill 用 GPT-4o Mini 平均每个类生成 8.5 个测试，用 GPT-5 Mini 生成 11.4 个，用 GPT-5 生成 13.2 个，用 Claude Sonnet 4.5 生成 45.7 个。
- 论文声称 MockMill 覆盖了现有项目测试、无 mock 的 LLM 基线和 Randoop 漏掉的代码并杀死了它们漏掉的变异体，但这段摘要没有给出这些对比的详细一对一数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.19315v1](http://arxiv.org/abs/2604.19315v1)
