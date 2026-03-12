---
source: arxiv
url: http://arxiv.org/abs/2603.05278v1
published_at: '2026-03-05T15:23:02'
authors:
- David Delgado
- "Lola Burgue\xF1o"
- "Robert Claris\xF3"
topics:
- llm-code-generation
- domain-specific-languages
- constraint-languages
- code-evaluation
- prompt-engineering
relevance_score: 0.91
run_id: materialize-outputs
---

# A framework for assessing the capabilities of code generation of constraint domain-specific languages with large language models

## Summary
本文提出一个用于评估大语言模型从文本规格生成约束型领域专用语言（DSL）代码能力的通用框架，并将其应用到 OCL、Alloy 与 Python 上。核心结论是：LLM 在 Python 上明显更强，而在 OCL/Alloy 这类低资源约束语言上更脆弱，但多次生成与代码修复能带来改进。

## Problem
- 论文解决的问题是：**如何系统评估 LLM 生成低资源约束 DSL 代码的能力**，不仅看能否生成，还要看代码是否**可解析/形式正确**以及**是否真正满足需求**。
- 这很重要，因为 OCL、Alloy 等约束语言用于**精确表达不变量、前置/后置条件和完整性约束**，直接关系到软件的验证、测试与可靠性，但它们比 Python 这类主流语言训练数据更少，LLM 表现通常更差。
- 约束 DSL 还更难：生成时既要理解**约束本身**，又要理解其依赖的**领域模型/模式**；而且这类语言偏声明式、全局性强，不能总靠直接执行来验证。

## Approach
- 提出一个**模块化评估框架**，把代码生成过程拆成四步：**构造提示词**、**调用 LLM 生成并提取代码**、**检查 well-formedness（语法/结构有效性）**、**检查 correctness（功能/语义正确性）**。
- 框架支持多种输入与提示配置：可使用**领域描述**、**领域模型**或两者结合；内置 **9 种 prompt templates（PT1–PT9）**，以及多任务交付方式（批量、串联、隔离）。
- 为提升生成质量，框架系统考察两类策略：**单轮代码修复**（把解析/校验错误信息反馈给 LLM 修正代码）和**multiple attempts**（同一任务生成多个候选，用 pass@k 评估至少一个成功的概率）。
- 在实验实例化中，作者选取 **OCL、Alloy、Python** 三种语言，并比较 **DeepSeek-coder、GPT-4o、GPT-4o-mini、Llama 3.1** 等模型；还整理并扩充了包含领域规格与完整性约束的数据集。
- 论文声称系统评估了**超过 90k 种配置**，用于分析不同 LLM、prompt、修复与多次尝试等决策对结果的影响。

## Results
- 论文明确报告的核心结论是：**LLM 在 Python 上总体优于 OCL 和 Alloy**，说明低资源约束 DSL 的代码生成难度显著更高；但摘要摘录中**未给出具体百分比、准确率或 pass@k 数值**。
- 作者指出，**上下文窗口较小的模型**（尤其一些开源 LLM）可能**无法生成约束相关代码**，因为任务需要同时管理**约束**与其所在的**领域模型**；该摘录同样**未提供具体模型分数**。
- **代码修复**与**多次生成候选**能提升生成质量；而**prompt 模板选择**的影响相对较小。这些是论文最强的实验性主张，但当前提供文本**没有公开具体增益数字或基线差值**。
- 论文的规模性结果之一是：其实验探索了**超过 90,000 个配置**，用于系统比较不同设置下的代码生成效果。
- 从贡献角度看，突破点不在提出新的生成模型，而在于给出一个**可参数化、可复用、跨 GPL/DSL 的评测框架**，专门覆盖约束 DSL 的 well-formedness 与 correctness 两层评估。

## Link
- [http://arxiv.org/abs/2603.05278v1](http://arxiv.org/abs/2603.05278v1)
