---
source: arxiv
url: https://arxiv.org/abs/2607.13303v1
published_at: '2026-07-14T22:12:14'
authors:
- Hongyi Liu
- Madhusudan Parthasarathy
- Adithya Murali
topics:
- code-intelligence
- automated-software-production
- software-foundation-model
- generative-engineering
- human-ai-interaction
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Faithful Autoformalization of Natural Language Assertions

## Summary
## 摘要
Monty 结合 LLM 生成、测试、分句一致性评分和用户引导的消歧，提高了将自然语言方法断言转换为可执行 JML 规范的可靠性。在涵盖 22 个 Java 类、共 541 个任务的评估中，与直接使用 LLM 翻译相比，它将精确率最高提高了 20 个百分点，同时保持了较高的召回率。

## 问题
- 为软件测试和验证编写形式化契约需要大量人工工作，而错误的翻译可能误报正确代码，也可能使有缺陷的代码通过测试。
- 自然语言断言存在歧义，现有自动形式化方法通常假设断言对实现应当有效；但这一假设不适用于测试代码或验证 AI 生成的代码。

## 方法
- Monty 提示 LLM 根据自然语言断言以及 Java 类或方法的上下文，生成多个候选 JML 断言。
- 它通过语法检查、模糊测试安全性检查，以及使用 Randoop 生成的模糊语义测试来筛选候选项，同时保留可能对测试有效和无效的两类解释。
- 在分句覆盖率指标中，LLM 先用自然语言描述每个形式化断言，再针对原始断言对双向分句匹配进行评分；在实验中，一致性低于 0.6 阈值的候选项会被移除。
- 当有效和无效候选项同时存在时，主动学习会为程序员或预言机生成一个能够区分它们的程序取值，以解决歧义。

## 结果
- 评估涵盖来自 22 个 Java 类的 541 对自然语言断言和形式化规范。这些类代表类似集合的数据结构，并包含有效和无效断言。
- 在使用 320 亿参数模型 Qwen2.5-Coder 时，Monty 将一个数据集上的精确率从 75% 提高到 91.6%，并将另一个数据集上的精确率从 64% 提高到 85%。
- 这些结果分别提高了 16.6 个百分点和 21 个百分点；论文报告称，召回率仍保持较高水平。
- 消融实验发现，在一致性检查方面，分句覆盖率比所评估的基线方法更有效；实验还显示，使用更小模型时，精确率提升更加明显。
- 摘录未提供确切的召回率数值、完整的基线配置或置信区间，因此上述提升仅适用于所提供的基准和实验设置。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.13303v1](https://arxiv.org/abs/2607.13303v1)
