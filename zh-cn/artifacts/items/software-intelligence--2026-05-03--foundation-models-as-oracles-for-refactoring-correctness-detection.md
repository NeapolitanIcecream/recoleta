---
source: arxiv
url: https://arxiv.org/abs/2605.02096v1
published_at: '2026-05-03T23:31:18'
authors:
- Rohit Gheyi
- Rian Melo
- Jonhnanthan Oliveira
- Marcio Ribeiro
- Baldoino Fonseca
topics:
- code-intelligence
- software-foundation-models
- refactoring
- program-analysis
- llm-evaluation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Foundation Models as Oracles for Refactoring Correctness Detection

## Summary
## 概述
本文测试基础模型是否能在没有任务特定训练的情况下，识别有缺陷的 Java 重构。结果显示，在真实的 IDE 缺陷报告上，零样本准确率很高，且专有模型优于开源模型。

## 问题
- IntelliJ IDEA、Eclipse 和 NetBeans 中的自动重构可能会引入编译错误或行为变化，同时表面上仍像一次安全的代码转换。
- 传统检查依赖手工编写的前置条件、静态分析、动态分析或测试；这些检查维护成本高，也可能漏掉 Java 的边界情况。
- 这个问题很重要，因为开发者经常使用重构工具，漏检正确性缺陷会削弱他们对自动化软件维护的信任。

## 方法
- 作者构建了一个评测集，包含 226 个来自 IDE 报告的真实 Java 重构缺陷，时间跨度从 2005 年到 2024 年。
- 数据集包含 185 个编译错误案例和 41 个行为变化案例，覆盖 47 种重构类型。
- 每个实例都包含原始 Java 程序和有缺陷的重构后程序；编译错误标签使用 OpenJDK Temurin 21.0.7+6 进行检查。
- 行为变化案例各配有一个 JUnit 测试，测试在原始程序上通过，在重构后程序上失败。
- 模型接收零样本提示，判断重构是否保持正确性；研究还使用变形测试检查在保持语义不变的代码变体下，预测是否稳定。

## 结果
- 在 226 个缺陷上，GPT-OSS-20B 的首轮准确率达到 80.5%。
- GPT-5.4 在同一任务上的首轮准确率达到 93.8%。
- 基准覆盖 47 种重构类型；数量最多的几类包括 Move Method 32 个案例、Inline Method 20 个、Pull Up Method 18 个、Extract Local Variable 15 个，以及 Rename Method 14 个。
- Gemma-4-31B 在开源模型中给出了最强结果，但摘要未提供其精确准确率。
- Gemini-3.1-Pro-Preview 在所有评测模型中给出了最佳结果，但摘要未提供其精确准确率。
- 变形测试发现，模型预测在保持语义不变的代码变体下大多一致，这支持模型并不只是做精确输入匹配。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02096v1](https://arxiv.org/abs/2605.02096v1)
