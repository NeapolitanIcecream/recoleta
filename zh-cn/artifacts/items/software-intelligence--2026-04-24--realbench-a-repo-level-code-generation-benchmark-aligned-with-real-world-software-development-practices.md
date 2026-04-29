---
source: arxiv
url: http://arxiv.org/abs/2604.22659v1
published_at: '2026-04-24T15:35:54'
authors:
- Jia Li
- Hongyi Deng
- Yiran Zhang
- Kechi Zhang
- Tianqi Shao
- Tiankuo Zhao
- Weinan Wang
- Zhi Jin
- Ge Li
- Yang Liu
- Yingtao Fang
- Yihong Dong
topics:
- repo-level-code-generation
- code-benchmark
- uml-guided-generation
- software-engineering
- llm-evaluation
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices

## Summary
## 摘要
RealBench 是一个仓库级代码生成基准，按软件团队的常见工作方式构建：代码来自需求和系统设计，而不只是文本提示。它加入了基于 UML 的规格、真实仓库和基于测试的评估，并表明当前 LLM 在完整仓库生成上表现仍然很差。

## 问题
- 现有代码生成基准，如 HumanEval 和 EvoCodeBench，主要评估模型把自然语言转成代码的能力，范围通常在函数级或小型仓库级。
- 在真实软件开发中，开发者通常根据包图、类图等结构化设计产物实现代码，因此当前基准分数可能会误判自动化在实际中的价值。
- 随着仓库规模和依赖密度增加，仓库级生成会变得更难，因此面向软件工程场景的真实评估很重要。

## 方法
- 论文构建了 **RealBench**，这是一个 Python 基准，包含来自 **20 个编程领域**的 **61 个真实世界仓库**，从 **2024.12-2025.05** 创建的 GitHub 项目中选取，以降低污染风险。
- 每个任务都包含**自然语言需求**以及**两级 UML 设计**：用于描述模块和依赖关系的包图，以及用于描述类、属性、方法和关系的类图。
- 仓库分为 **4 个规模等级**：**0-500 LOC**、**500-1000 LOC**、**1000-2000 LOC** 和 **>=2000 LOC**。
- 作者加入了人工核验的测试，**每个仓库平均有 50.05 个测试用例**，**平均行覆盖率为 79.76%**。
- 他们在 **3 种生成策略**下评估了 **6 个 LLM**：完整仓库整体生成、按文件逐步生成，以及利用设计中的文件依赖链接进行检索增强生成。

## 结果
- RealBench 的规模和设计信息都多于此前的仓库级基准：**2,484 条需求**、**544 张 UML 图**、**538 个文件**，以及**每个仓库平均 1,201 LOC**；表 1 显示，在列出的基准中，RealBench 是唯一同时包含仓库级任务和图示输入的基准。
- 当前模型在这一设定下表现很差：在所有研究的 LLM 中，**最高平均 Pass@1 为 19.39%**。
- 性能会随着仓库规模增大而明显下降：对于 **<500 LOC** 的仓库，**Pass@1 高于 40%**；对于 **>2000 LOC** 的仓库，**Pass@1 低于 15%**。
- 该基准的复杂度较高：平均只有 **44.73%** 的方法/函数是独立的；在 level-4 仓库中，这一比例只有 **26.23%**，说明大多数代码都有依赖关系。
- 该基准按规模等级报告了较强的测试支持：level-1 的行覆盖率为 **91.16%**，level-2 为 **81.07%**，level-3 为 **74.09%**，level-4 为 **72.71%**。
- 论文称，**整体生成更适合较小的仓库（<1000 LOC）**，而 **增量生成更适合较大的仓库（>1000 LOC）**，并且详细的 UML 设计能明显提升仓库级生成效果。给定摘录没有提供各模型的分数表，也没有提供消融实验中的具体增益。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22659v1](http://arxiv.org/abs/2604.22659v1)
