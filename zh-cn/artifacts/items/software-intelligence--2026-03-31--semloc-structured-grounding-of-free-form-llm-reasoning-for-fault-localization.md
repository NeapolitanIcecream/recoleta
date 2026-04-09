---
source: arxiv
url: http://arxiv.org/abs/2603.29109v1
published_at: '2026-03-31T00:56:43'
authors:
- Zhaorui Yang
- Haichao Zhu
- Qian Zhang
- Rajiv Gupta
- Ashish Kundu
topics:
- fault-localization
- llm-grounding
- semantic-analysis
- code-intelligence
- software-debugging
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# SemLoc: Structured Grounding of Free-Form LLM Reasoning for Fault Localization

## Summary
## 摘要
SemLoc 是一种用于故障定位的方法，面向通过运行和失败运行遵循相同控制流、因此覆盖率信号无法区分故障代码行的缺陷。它把 LLM 写出的语义约束转换为可执行检查，衡量这些检查在各个测试中的失败情况，并用这些证据对可疑代码进行排序。

## 问题
- 它针对语义类缺陷，例如错误的数值关系、缺失的归一化处理或错误的边界逻辑。在这类问题中，通过和失败的执行可能以相同顺序命中相同语句。
- 基于覆盖率、切片或执行轨迹结构的标准故障定位方法在这种情况下会丢失有效信号，这会让调试变慢且成本更高。
- 以往基于 LLM 的定位方法常常输出自由形式的猜测或解释，这些内容很难根据运行时行为验证，也很难在不同测试之间做比较。

## 方法
- SemLoc 让 LLM 根据有缺陷的函数、经过 SSA 转换的代码以及通过/失败测试，推断程序预期行为的语义约束。
- 每个推断出的约束都会被限制到一种封闭的中间表示中，其中包含类别、程序锚点和可执行的布尔表达式，因此可以在精确的代码位置进行检查。
- 系统会对程序插桩，运行测试套件，并构建语义违规谱：一个按约束与测试组织的矩阵，记录哪些语义检查在哪些测试上失败。
- 它使用类似 SBFL 的 Ochiai 公式为约束打分，再把这些分数映射回语句，从语义证据而不是仅靠覆盖率生成故障排序列表。
- 一个反事实验证步骤会为排名靠前的约束提出最小修复方案，重新运行测试，并区分主要因果违规与下游影响或范围过宽的约束。

## 结果
- 评估使用 **SemFault-250**，这是一个包含 **250 个 Python 程序** 的语料库，包含来自真实代码仓库和以往基准的单个语义缺陷。
- 在 **Claude Sonnet 4.6** 上，SemLoc 报告的故障定位准确率为 **42.8% Top-1** 和 **68.0% Top-3**。
- 与具名基线相比，它优于 **SBFL-Ochiai：6.4% Top-1 / 13.2% Top-3** 和 **delta debugging：0.0% / 0.0%**（基于该基准）。
- 它把检查范围缩小到 **7.6% 的可执行代码行**，文中称相对 SBFL 实现了 **5.7x reduction**。
- 反事实验证将 **Top-1 准确率从 30.8% 提高到 42.8%**，增幅为 **12.0 个百分点**。
- 论文还声称，反事实验证为 **60.8%** 的程序识别出了**主要因果约束**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29109v1](http://arxiv.org/abs/2603.29109v1)
