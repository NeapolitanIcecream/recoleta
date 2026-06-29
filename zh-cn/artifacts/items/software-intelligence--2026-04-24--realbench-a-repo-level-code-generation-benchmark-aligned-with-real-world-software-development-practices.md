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
## 总结
RealBench 是一个仓库级代码生成基准，按软件团队的实际工作方式来设计：代码来自需求和系统设计，而不只是文本提示。它加入了基于 UML 的规格、真实仓库和带测试的评估，并显示当前 LLM 在完整仓库生成上的表现仍然很差。

## 问题
- 现有代码生成基准，如 HumanEval 和 EvoCodeBench，主要评估模型在自然语言到代码任务上的表现，范围通常是函数级或小仓库级。
- 在真实软件开发中，开发者通常根据包图、类图这类结构化设计产物实现代码，因此现有基准分数可能会夸大实际自动化价值。
- 随着仓库规模和依赖密度增加，仓库级生成会更难，这让面向软件工程场景的真实评估变得重要。

## 方法
- 论文构建了 **RealBench**，这是一个 Python 基准，包含来自 **20 个编程领域**的 **61 个真实仓库**。这些仓库选自 **2024.12-2025.05** 创建的 GitHub 项目，以降低污染风险。
- 每个任务都包含 **自然语言需求** 和 **两级 UML 设计**：用于模块和依赖的包图，以及描述类、属性、方法和关系的类图。
- 仓库被分为 **4 个规模等级**：**0-500 LOC**、**500-1000 LOC**、**1000-2000 LOC** 和 **>=2000 LOC**。
- 作者加入了人工验证测试，平均每个仓库有 **50.05 个测试用例**，平均行覆盖率为 **79.76%**。
- 他们评估了 **6 个 LLM**，采用 **3 种生成策略**：整仓库整体生成、逐文件增量生成，以及利用设计中的文件依赖链接进行检索增强生成。

## 结果
- RealBench 比之前的仓库级基准更大，设计信息也更丰富：共有 **2,484 条需求**、**544 张 UML 图**、**538 个文件**，每个仓库平均 **1,201 行代码**；表 1 显示，RealBench 是所列基准里唯一同时包含仓库级任务和图输入的基准。
- 当前模型在这个设置下表现很差：所有研究的 LLM 中，**最佳平均 Pass@1 只有 19.39%**。
- 随着仓库规模增大，性能明显下降：**<500 LOC** 的仓库 **Pass@1 高于 40%**，而 **>2000 LOC** 的仓库 **低于 15%**。
- 基准复杂度很高：平均只有 **44.73%** 的方法/函数是独立的，在 4 级仓库中只有 **26.23%** 是独立的，所以大多数代码都有依赖关系。
- 基准按规模等级给出了较强的测试支持：1 级仓库的行覆盖率是 **91.16%**，2 级是 **81.07%**，3 级是 **74.09%**，4 级是 **72.71%**。
- 论文声称，**整体生成**在较小仓库（<1000 LOC）上效果最好，**增量生成**在较大仓库（>1000 LOC）上更好，而更细的 UML 设计会明显提升仓库级生成效果。摘要中没有给出逐模型分数表，也没有给出消融实验的精确增益。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.22659v1](http://arxiv.org/abs/2604.22659v1)
