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
- ltl-formalization
- compact-language-models
- syntax-constrained-decoding
- symbolic-reasoning
- requirements-engineering
relevance_score: 0.83
run_id: materialize-outputs
language_code: zh-CN
---

# LTLGuard: Formalizing LTL Specifications with Compact Language Models and Lightweight Symbolic Reasoning

## Summary
LTLGuard旨在把自然语言需求更可靠地翻译成LTL形式化规格，重点是在**4B–14B的紧凑开源模型**上实现高质量、可本地部署、保护隐私的形式化。核心思想是让小模型先按语法受限生成，再用轻量符号推理检查并迭代修复语法与跨公式冲突。

## Problem
- 解决的问题是：把**含糊、易多义**的自然语言需求，转换成**语法正确、语义尽量忠实、且彼此一致**的LTL公式。
- 这很重要，因为形式化需求是验证、监控与正确性保证的基础，但工业界普及受阻于**人工形式化门槛高**、需求文本天然歧义，以及大模型的**隐私、成本、可控性**问题。
- 小/中型模型更适合本地部署，但在时序逻辑这类小众逻辑任务上常出现**语法错误、幻觉和互相矛盾的规格**。

## Approach
- 用一个**模块化流水线**替代“直接让LLM一次性翻译”：系统提示词 + **检索增强少样本**(RAFSL) + **语法约束解码** + **解析器反馈修复** + **LTL一致性检查**。
- RAFSL会从NL-LTL示例库中，按语义相似度动态检索最相关例子加入提示，帮助小模型“临时补课”时序逻辑模式，而无需微调。
- 生成时使用**LTL语法约束**（SynCode/DFA掩码）限制下一个token只能落在合法语法路径上，尽量直接产出可解析公式。
- 若解析失败，就把调试信息回灌给模型进行迭代修正；若多条公式联合后不一致，则用BLACK检查**SAT/UNSAT**并返回**unsat core**解释冲突来源。
- 本质上，核心机制可以简单理解为：**让小模型负责“猜公式”，让语法器和求解器负责“兜底纠错与找冲突”**。

## Results
- 在70条NL-LTL对的消融实验中，**Mistral-7B**从Vanilla的**10.0%语法正确 / 7.1%语义正确**，提升到完整系统V7的**92.8%语法正确 / 38.5%语义正确**；最佳语义配置V6达到**40.0%**。
- **Phi-3-mini-4B**从**47.1% / 24.2%**提升到V6的**91.4%语法正确 / 64.2%语义正确**；V7语法为**92.8%**，语义为**35.7%**，显示不同组件组合对小模型语义效果有明显影响。
- **Mistral-Nemo-12B**从**51.4% / 31.4%**提升到V4的**92.8%语法正确 / 67.1%语义正确**。**Qwen2.5-14B**在Vanilla已较强（**95.7% / 68.5%**），V6进一步把语义正确率提升到**78.6%**，并保持**97.1%**语法正确。
- 在**nl2spec hard 36例**基准上，最佳设置（V6 + Qwen2.5-14B）在有RAFSL重叠时达到**100.0%语法正确，75.0%语义准确(S1)，77.8%语义准确(S2)**；去除重叠后仍有**97.2%语法正确，50.0%(S1)，63.9%(S2)**。
- 与文中复现的先前方法相比，LTLGuard在该hard基准上显著优于**NL2LTL 2.7%**、**T5 5.5%**、**nl2spec初始Bloom 13.8%**、**nl2spec初始Codex 44.4%**、**nl2spec初始+示例Codex 58.3%**，并接近**nl2spec交互式Codex 86.1%**的水平，但使用的是**更小的开源模型且无需微调**。
- 论文还强调：由于自然语言需求本身存在歧义，部分“错误”其实是**与标注不同但合理的替代形式化**；不过本文已通过“等价判定”和S1/S2两种评估尽量反映这一点。

## Link
- [http://arxiv.org/abs/2603.05728v1](http://arxiv.org/abs/2603.05728v1)
