---
source: arxiv
url: http://arxiv.org/abs/2603.05728v1
published_at: '2026-03-05T22:34:45'
authors:
- Medina Andresel
- Cristinel Mateis
- Dejan Nickovic
- Spyridon Kounoupidis
- Panagiotis Katsaros
- Stavros Tripakis
topics:
- nl-to-ltl
- formal-specification
- compact-llm
- symbolic-reasoning
- constrained-decoding
relevance_score: 0.06
run_id: materialize-outputs
---

# LTLGuard: Formalizing LTL Specifications with Compact Language Models and Lightweight Symbolic Reasoning

## Summary
LTLGuard 旨在把自然语言需求更可靠地翻译成 LTL 公式，尤其面向可本地部署的紧凑开源模型。它把受约束生成、检索增强示例和轻量符号推理结合起来，以提升语法正确性、语义准确性和跨公式一致性。

## Problem
- 论文解决的是：如何将**含糊的自然语言需求**自动形式化为**语法正确、语义尽量忠实且彼此一致**的 LTL 规格。
- 这很重要，因为需求形式化是形式化验证落地的主要瓶颈；大模型虽强，但常有隐私、成本、能耗和可控性问题，而小/中模型在时序逻辑上往往不可靠。
- 难点在于自然语言本身存在歧义，同一句需求可能对应多个合理但不等价的 LTL 解释，而且多个需求之间还可能互相冲突。

## Approach
- 核心方法是一个**模块化工具链**：先用紧凑语言模型生成候选 LTL，再用**语法约束解码**强制输出尽量符合 LTL 文法。
- 它用 **RAFSL**（retrieval-augmented few-shot learning）从 NL-LTL 示例库中按语义相似度检索 top-k 示例，把相关例子拼进提示词，帮助小模型“看着例子翻译”。
- 生成后先做**语法解析/纠错**；若解析失败，就把错误信息反馈给模型迭代修复，直到得到可解析公式。
- 然后用 **BLACK** 做 LTL 可满足性/一致性检查；若多条规格冲突，则给出**unsat core** 等解释，并把冲突信息反馈给模型辅助修复。
- 用最简单的话说：它不是只相信模型一次性写对，而是让模型在“**示例提示 + 文法护栏 + 解析反馈 + 逻辑检查**”的闭环里反复修正。

## Results
- 在 70 条 NL-LTL 对上的消融实验中，**Mistral-7B** 从 vanilla 的 **10.0%** 语法正确率 / **7.1%** 语义正确率，提升到完整系统 **V7 的 92.8% / 38.5%**；其最佳语义分数出现在 **V6：40.0%**。
- **Phi-3-mini-4B** 从 **47.1% / 24.2%** 提升到 **V7 的 92.8% / 35.7%**，而最佳语义分数在 **V6 达到 64.2%**。
- **Mistral-Nemo-12B** 从 **51.4% / 31.4%** 提升到 **V4 的 92.8% / 67.1%**（该模型最佳）。**Qwen2.5-14B** 从 **95.7% / 68.5%** 提升到 **V6 的 97.1% / 78.6%**（最佳语义）。
- 在 **nl2spec hard** 36 条基准上，LTLGuard（Qwen2.5-14B, V6）达到：**Exp.1 有重叠检索集时 100.0% 语法、75.0% S1 语义、77.8% S2 语义**；**Exp.2 去重叠后 97.2% 语法、50.0% S1、63.9% S2**。
- 与已有方法对比：同一 hard 基准上，**NL2LTL 为 2.7%**，**fine-tuned T5 为 5.5%**，**nl2spec initial + Codex 为 58.3%**，**nl2spec interactive + Codex 为 86.1%**。LTLGuard 在**非交互、紧凑开源模型**设定下优于所有已报告的非交互基线，并接近最佳交互式 Codex 结果。
- 论文还明确指出：由于自然语言歧义，某些生成公式虽与标注不等价，但仍可能是**合理解释**；因此他们同时报告了**ambiguity-intolerant (S1)** 与 **ambiguity-friendly (S2)** 两种语义评估。

## Link
- [http://arxiv.org/abs/2603.05728v1](http://arxiv.org/abs/2603.05728v1)
