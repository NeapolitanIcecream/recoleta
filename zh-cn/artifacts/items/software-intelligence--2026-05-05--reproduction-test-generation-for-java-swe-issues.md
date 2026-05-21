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
论文提出了 TDD-Bench-Java，这是一个包含 250 个实例的基准，用于从 issue 报告生成 Java 复现测试；论文还提出了 e-Otter++ for Java，这是一个用于编写和改进测试的 LLM 工作流。主要结论是，执行反馈加上 issue 改写可以提高 Java SWE issue 的 fail-to-pass 率。

## 问题
- 复现测试应在有缺陷的代码上失败，并在开发者修复后通过，从而用执行结果证明 issue 确实存在且之后已被修复。
- 近期大多数复现测试研究面向 Python，而 Java 增加了静态类型、包和 import 规则、Maven 或 Gradle 构建，以及面向对象代码模式。
- 现有 Java 覆盖有限：以往数据集规模小、不可用，或者不评估生成的测试是否能在修复前代码上复现 issue。

## 方法
- 作者从 Multi-SWE-bench 和 SWE-PolyBench 的 Java 样本构建 TDD-Bench-Java，然后筛选出具有 fail-to-pass 行为的开发者测试，并删除重复项。
- e-Otter++ 先根据 issue 文本定位可能相关的 Java 文件和函数，然后为新测试文件选择包、import 和测试目录。
- 生成器编写一个新的 Java 测试类和方法，而不是编辑现有测试，以减少包和放置位置错误。
- 改进器在旧代码上运行测试，读取构建或测试日志，要求 LLM 批评器判断失败是否匹配该 issue，并最多进行 10 轮测试改写。
- 系统使用原始 issue 加上 5 个改写后的 issue 变体创建 6 个候选测试，然后要求 LLM 选择器选出一个最终测试。

## 结果
- TDD-Bench-Java 包含来自 13 个开源 Java 仓库的 250 个实例；示例包括 trinodb/trino 的 44 个实例、jackson-databind 的 42 个实例、rocketmq 的 41 个实例，以及 dubbo 的 36 个实例。
- 该基准的 issue 描述平均长度为 199.4 个词；平均修改代码规模为 86.3 行，平均修改测试规模为 87.2 行。
- 在 TDD-Bench-Java 上，e-Otter++ 使用 Claude-Sonnet-4.5 达到 43.6% 的 fail-to-pass 率，使用 GPT-5.2 达到 46.4%。
- 与初始 Otter 生成器相比，改进步骤将 fail-to-pass 率提高了 9.4 个百分点（Claude-Sonnet-4.5）和 13.6 个百分点（GPT-5.2）。
- 对两个模型而言，Otter 到 e-Otter 的提升在 McNemar 检验中均具有统计显著性，p < 0.01。
- 论文还报告了一个包含 150 个实例的专有 Java 数据集上的评估，但摘录未包含其数值结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.04320v2](https://arxiv.org/abs/2605.04320v2)
