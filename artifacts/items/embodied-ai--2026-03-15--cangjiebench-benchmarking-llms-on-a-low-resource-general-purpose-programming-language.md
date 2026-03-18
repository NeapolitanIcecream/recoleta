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
- llm-benchmark
- code-generation
- code-translation
- low-resource-language
- program-synthesis
relevance_score: 0.01
run_id: materialize-outputs
---

# CangjieBench: Benchmarking LLMs on a Low-Resource General-Purpose Programming Language

## Summary
本文提出 **CangjieBench**，用于系统评测大语言模型在低资源通用编程语言 Cangjie 上的代码生成与代码翻译能力。核心发现是：直接生成效果很差，加入简明语法约束最划算，而 Agent 准确率最高但代价很大。

## Problem
- 现有 LLM 在 Python、C++ 等高资源语言上很强，但对 **低资源通用语言** 的泛化能力缺少严格评测。
- 以往低资源代码研究多聚焦 DSL，容易把“不会新语法”和“缺少领域知识”混在一起，无法纯粹测语法迁移能力。
- 工业上需要把高资源语言代码迁移到新语言（如 Python 到 Cangjie），但针对 **高资源→低资源** 通用语言翻译的基准很少，这很重要，因为 HarmonyOS 生态扩张会带来真实迁移需求。

## Approach
- 构建 **CangjieBench**：将 HumanEval 和 ClassEval **人工翻译**到 Cangjie，得到 **248** 个高质量、无污染样本，其中 **164** 个来自 HumanEval、**84** 个来自 ClassEval。
- 基准同时覆盖两类任务：**Text-to-Code**（自然语言到 Cangjie 代码）与 **Code-to-Code**（Python 到 Cangjie 翻译），覆盖函数级和类级难度。
- 为保证公平性，作者使用人工翻译而非网络抓取，从而强调 **zero contamination**；并构建 Docker 沙箱执行编译和测试。
- 系统比较四种无需微调的范式：**Direct Generation**、**Syntax-Constrained Generation**（在提示中加入简明语法规则）、**RAG**（文档检索或代码检索）、**Agent**（CLI 自主查文档与自纠错）。
- 最核心机制可以简单理解为：不给模型改参数，而是用“**语法提示 / 外部知识 / 代理式试错**”帮助它临时学会一门几乎没见过的新语言。

## Results
- 在 **Direct Generation** 下，模型整体表现较差：表中平均 **Pass@1** 约在 **22.1%–24.3%**，平均 **Compile** 约在 **52.1%–56.1%**，说明仅靠预训练知识难以稳定掌握 Cangjie 语法。
- **Syntax-Constrained Generation** 明显更强且更稳定：例如 **GPT-5** 的平均 **Pass@1=53.8%**、**Compile=38.1%**（按文中表格原始展示记录）；相较 Direct 的 **24.3% / 56.1%**，作者据此认为语法约束在准确率与成本之间提供了最佳折中。
- 在 HumanEval 上，**GPT-5 + Syntax-Constrained** 达到 **67.1% Pass@1**；在 ClassEval 上达到 **40.5% Pass@1**，是表中最强的已完整可见结果之一。
- 其他强基线也从语法约束中获益：如 **Kimi-K2** 平均 **Pass@1=42.4%**，**Qwen3** 平均 **40.0%**，均显著高于各自 Direct 结果。
- **RAG** 并非总是最优：可见表格中 **RAG(Code)** 的平均 Pass@1 多落在 **8.5%–31.3%** 或 **10.1%–23.7%** 区间（不同模型），整体通常不如语法约束；作者据此认为外部示例或文档并不能稳定替代显式语法指导。
- 摘要还明确声称 **Agent 达到 state-of-the-art accuracy**，但会带来 **高 token 消耗**；同时 **Code-to-Code 往往劣于 Text-to-Code**，作者将其解释为对源语言模式的 **negative transfer**。给定摘录未完整展示 Agent 与翻译任务的具体数值，因此这里无法精确列出对应定量结果。

## Link
- [http://arxiv.org/abs/2603.14501v1](http://arxiv.org/abs/2603.14501v1)
