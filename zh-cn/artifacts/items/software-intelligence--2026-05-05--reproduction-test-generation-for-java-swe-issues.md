---
source: arxiv
url: https://arxiv.org/abs/2605.04320v2
published_at: '2026-05-05T21:49:52'
authors:
- Toufique Ahmed
- Jatin Ganhotra
- Avraham Shinnar
- Martin Hirzel
topics:
- code-intelligence
- software-testing
- java
- llm-agents
- benchmarking
- automated-software-engineering
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Reproduction Test Generation for Java SWE Issues

## Summary
## 摘要
本文提出了 TDD-Bench-Java，一个用于从问题报告生成 Java 复现测试的 250 个样本基准，以及 e-Otter++ for Java，一个编写并改进测试的 LLM 工作流。核心结论是，执行反馈加上问题重写，能提高 Java SWE 问题的 fail-to-pass 成功率。

## 问题
- 复现测试应在有缺陷的代码上失败，并在开发者修复后通过，这样才能用执行结果证明问题真实存在，并在后续验证它已被修复。
- 近年的复现测试工作主要面向 Python，而 Java 还要面对静态类型、包和导入规则、Maven 或 Gradle 构建，以及面向对象代码模式。
- 现有 Java 覆盖有限：之前的数据集规模小、不可用，或者没有评估生成的测试是否能在修复前代码上复现问题。

## 方法
- 作者先从 Multi-SWE-bench 和 SWE-PolyBench 中筛选 Java 样本构建 TDD-Bench-Java，再保留具有 fail-to-pass 行为的开发者测试并去重。
- e-Otter++ 先根据问题文本定位可能相关的 Java 文件和函数，然后为新测试文件选择包、导入和测试目录。
- 生成器会写入一个新的 Java 测试类和方法，而不是修改已有测试，以减少包路径和放置位置错误。
- 一个改进器先在旧代码上运行测试，读取构建或测试日志，询问 LLM 批评者失败是否与问题一致，然后最多迭代 10 次重写测试。
- 系统会用原始问题和 5 个重写后的问题变体生成 6 个候选，再让 LLM 选择器挑出最终测试。

## 结果
- TDD-Bench-Java 包含来自 13 个开源 Java 仓库的 250 个样本；例子包括 trinodb/trino 的 44 个样本、jackson-databind 的 42 个、rocketmq 的 41 个，以及 dubbo 的 36 个。
- 该基准中的问题描述平均长度为 199.4 个词；平均变更代码规模为 86.3 行，平均变更测试规模为 87.2 行。
- e-Otter++ 在 TDD-Bench-Java 上使用 Claude-Sonnet-4.5 时达到 43.6% 的 fail-to-pass 率，使用 GPT-5.2 时达到 46.4%。
- 与初始 Otter 生成器相比，改进模块将 fail-to-pass 率提高了 9.4 个百分点（Claude-Sonnet-4.5）和 13.6 个百分点（GPT-5.2）。
- 论文还报告了在一个 150 样本的专有 Java 数据集上的评估，但摘录中没有给出数值结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04320v2](https://arxiv.org/abs/2605.04320v2)
