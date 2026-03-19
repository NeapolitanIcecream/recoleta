---
source: arxiv
url: http://arxiv.org/abs/2603.14501v1
published_at: '2026-03-15T17:35:03'
authors:
- Junhang Cheng
- Fang Liu
- Jia Li
- Chengru Wu
- Nanxiang Jiang
- Li Zhang
topics:
- code-benchmark
- low-resource-pl
- code-generation
- code-translation
- llm-evaluation
- syntax-constrained-prompting
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# CangjieBench: Benchmarking LLMs on a Low-Resource General-Purpose Programming Language

## Summary
本文提出 **CangjieBench**，用于系统评测大模型在低资源通用编程语言仓颉上的代码生成与翻译能力。作者发现主流模型直接生成效果很差，而加入简明语法约束通常最划算，Agent 虽然最强但成本最高。

## Problem
- 现有代码LLM主要在 Python、C++ 等高资源语言上表现好，但对 **低资源通用语言** 的泛化能力缺少严格评测。
- 以往低资源代码研究多聚焦 DSL，容易把“不会语法”与“缺少领域知识”混在一起，难以纯粹衡量语言泛化。
- 现实中存在把高资源语言项目迁移到新语言/新生态（如 HarmonyOS/Cangjie）的需求，因此评测 **Text-to-Code** 和 **Code-to-Code** 都很重要。

## Approach
- 构建了首个面向仓颉的基准 **CangjieBench**：从 **HumanEval** 和 **ClassEval** 人工翻译得到 **248** 个高质量样本，其中 **164** 个来自 HumanEval、**84** 个来自 ClassEval。
- 数据集覆盖两类任务：**Text-to-Code**（自然语言到仓颉代码）和 **Code-to-Code**（Python 到仓颉翻译），并强调人工构造带来的 **zero contamination**。
- 设计 Docker 沙箱执行评测，按原始测试逻辑验证：函数题看测试是否通过，类题要求类中全部方法及主测试通过。
- 在 **4** 种无参数更新范式下系统评估多种 LLM：**Direct Generation**、**Syntax-Constrained Generation**、**RAG**（Docs/Code）、**Agent**。
- 其中语法约束方法的核心非常简单：把精简但关键的仓颉语法规则直接放进提示词里，帮助模型少犯“套用其他语言语法”的错误。

## Results
- 基准规模方面：作者报告数据集共 **248** 题，含 **164** 个函数级问题和 **84** 个类级问题；这是文中最明确的定量结果之一。
- 在 **Direct Generation** 下，模型总体表现较差。表中可见平均 **Pass@1** 大致只有 **12%–24%** 左右、平均 **Compile** 大致约 **51%–56%**（不同模型/子任务有波动），说明模型常常连可编译代码都难稳定生成。
- **Syntax-Constrained Generation** 明显提升效果并给出最佳性价比。例如 **GPT-5** 在该设置下的平均 **Pass@1 = 53.8%**、平均 **Compile = 38.1%**（按表中给出的 Avg. 数值）；在 HumanEval 上 **Pass@1 = 67.1%**，在 ClassEval 上 **Pass@1 = 40.5%**。文中主张它在准确率与计算成本之间最均衡。
- 其他语法约束结果也较强：如 **Kimi-K2** 平均 **Pass@1 = 42.4%**，**Qwen3 = 40.0%**，**DeepSeek-V3 = 32.2%**；相较直接生成均有明显改善。
- 文中还声称 **Agent** 达到最先进准确率，但会消耗大量 token；不过在给定摘录中，**Agent 的完整量化表格未提供**，因此无法准确复述其具体数值提升。
- 作者还观察到 **Code-to-Code 往往不如 Text-to-Code**，并将其解释为一种 **negative transfer**：模型过度贴合源语言（如 Python）模式，反而更难生成正确的仓颉语法。摘录中未给出该现象的完整对比数字。

## Link
- [http://arxiv.org/abs/2603.14501v1](http://arxiv.org/abs/2603.14501v1)
