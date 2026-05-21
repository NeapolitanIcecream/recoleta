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
## 摘要
这篇论文测试基础模型能否在没有任务特定训练的情况下标记有问题的 Java 重构。论文报告称，在真实 IDE 缺陷报告上的零样本准确率较高，专有模型领先于开源模型。

## 问题
- IntelliJ IDEA、Eclipse 和 NetBeans 中的自动化重构可能引入编译错误或行为变化，即使它看起来是安全的代码转换。
- 传统检查依赖手写前置条件、静态分析、动态分析或测试；这些检查维护成本高，也可能漏掉 Java 边界情况。
- 这个问题重要，因为开发者经常使用重构工具，而漏检的正确性缺陷会降低他们对自动化软件维护的信任。

## 方法
- 作者构建了一个评估集，包含 2005 年至 2024 年 IDE 报告中的 226 个真实 Java 重构缺陷。
- 数据集包含 185 个编译错误案例和 41 个行为变化案例，覆盖 47 种重构类型。
- 每个实例包含原始 Java 程序和有问题的重构后程序；编译错误标签使用 OpenJDK Temurin 21.0.7+6 检查。
- 行为变化案例各用一个 JUnit 测试验证，其中测试在原始程序上通过，在重构后程序上失败。
- 模型接收零样本提示，判断重构是否保持正确性；研究还使用变形测试检查预测在保持语义的代码变化下是否稳定。

## 结果
- 在 226 个缺陷上，GPT-OSS-20B 的首次运行准确率达到 80.5%。
- GPT-5.4 在同一任务上的首次运行准确率达到 93.8%。
- 该基准覆盖 47 种重构类型；最大的几组包括 Move Method 32 个案例、Inline Method 20 个、Pull Up Method 18 个、Extract Local Variable 15 个，以及 Rename Method 14 个。
- Gemma-4-31B 在开源模型中取得报告的最佳结果，但摘录没有给出其准确率。
- Gemini-3.1-Pro-Preview 取得报告的总体最佳结果，但摘录没有给出其准确率。
- 变形测试发现，在预期保持语义的代码变化下，预测大多保持一致，这支持了模型不只是进行精确输入匹配这一说法。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02096v1](https://arxiv.org/abs/2605.02096v1)
