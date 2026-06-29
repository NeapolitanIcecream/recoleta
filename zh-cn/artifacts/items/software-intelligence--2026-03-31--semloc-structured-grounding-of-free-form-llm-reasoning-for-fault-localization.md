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
SemLoc 是一种面向这类缺陷的故障定位方法：通过和不同的控制流无关的 passing 和 failing 运行，覆盖率信号无法区分出有问题的代码行。它把 LLM 写出的语义约束转成可执行检查，测量这些检查在各个测试上的失败情况，并用这些证据给可疑代码排序。

## 问题
- 它针对的是语义型缺陷，例如数值关系错误、缺少归一化、边界逻辑错误；这类缺陷里，passing 和 failing 执行可能按相同顺序经过相同语句。
- 基于覆盖率、切片或轨迹结构的传统故障定位方法在这种场景下会丢失信号，导致调试变慢、成本变高。
- 之前基于 LLM 的定位方法常常输出自由形式的猜测或解释，难以和运行时行为对照，也难以在不同测试之间比较。

## 方法
- SemLoc 让 LLM 根据有缺陷的函数、SSA 转换后的代码以及 passing/failing 测试，推断程序预期行为的语义约束。
- 每个推断出的约束都会被强制写入一个封闭的中间表示，包含类别、程序锚点和可执行的布尔表达式，因此可以在精确的代码位置检查。
- 系统对程序加埋点，运行测试集，构建语义违反谱：这是一个按约束和测试组织的矩阵，记录哪些语义检查在了哪些测试上失败。
- 它用类似 SBFL 的 Ochiai 公式给约束打分，再把这些分数映射回语句，用语义证据而不是单纯覆盖率生成排序后的故障列表。
- 反事实验证步骤会为优先级最高的约束提出最小修复，重新运行测试，并区分主要因果违反、下游效应和过宽的约束。

## 结果
- 评测使用 **SemFault-250**，这是一个包含 **250 个 Python 程序** 的语料库，程序里各有一个语义缺陷，来源于真实仓库和已有基准。
- 使用 **Claude Sonnet 4.6** 时，SemLoc 的故障定位准确率为 **Top-1 42.8%**、**Top-3 68.0%**。
- 与命名基线相比，它在这个基准上优于 **SBFL-Ochiai：Top-1 6.4% / Top-3 13.2%** 和 **delta debugging：0.0% / 0.0%**。
- 它把需要检查的范围缩小到 **7.6% 的可执行行**，论文把这描述为相对 SBFL 的 **5.7 倍减少**。
- 反事实验证把 **Top-1 准确率从 30.8% 提高到 42.8%**，提升了 **12.0 个百分点**。
- 论文还声称，反事实验证为 **60.8%** 的程序识别出了一个 **主要因果约束**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29109v1](http://arxiv.org/abs/2603.29109v1)
