---
source: arxiv
url: http://arxiv.org/abs/2603.02504v2
published_at: '2026-03-03T01:26:42'
authors:
- Pratibha Zunjare
- Michael Hsiao
topics:
- neurosymbolic-reasoning
- mathematical-reasoning
- multi-task-fine-tuning
- prolog-program-synthesis
- execution-guided-decoding
relevance_score: 0.72
run_id: materialize-outputs
---

# NeuroProlog: Multi-Task Fine-Tuning for Neurosymbolic Mathematical Reasoning via the Cocktail Effect

## Summary
NeuroProlog提出一种将数学题转成可执行Prolog程序的神经符号框架，并用多任务“Cocktail”微调让模型同时学习数学知识表达与解题程序生成。它的目标是让LLM不仅会“说得像在推理”，还能够生成可验证、可执行、可修复的正式推理过程。

## Problem
- 现有LLM在数学推理上常依赖模式匹配，容易生成看似流畅但逻辑错误的答案，且中间步骤难以验证。
- 许多神经符号方法只在推理时做事后校验，模型本身没有在训练中真正学会符号结构与可执行推理。
- 这很重要，因为数学与程序化推理需要**可靠性、可解释性和可验证性**，尤其是在组合泛化与错误恢复场景中。

## Approach
- 将数学推理统一为**生成Prolog程序**：把数学公式/概念翻译成规则，把文字题翻译成可执行程序，再通过执行得到答案。
- 使用多任务Cocktail训练，联合优化三类监督信号：**KB**（公式到Prolog规则）、**SOLVE**（自然语言题目到程序）、以及程序与答案的语义对齐/执行验证。
- 训练数据包含约**200条数学知识库条目**、**310条人工构造解题样例**和**7476条GSM8K-Prolog题目**，都使用统一的Prolog表示。
- 推理时采用**执行引导解码**：先生成程序并执行；若失败，则根据错误类型（语法、类型、领域、实例化、逻辑错误）给模型反馈，最多迭代修复**3次**。
- 核心直觉很简单：先让模型学会“数学概念如何写成规则”，再让它学会“如何把题目拼装成这些规则”，这样能把抽象知识迁移到具体解题中。

## Results
- 在**GSM8K**上跨**4个模型规模（3B–32B）**评测，Cocktail训练相对单任务基线带来稳定提升：**Qwen-32B +5.23%（p<0.01）**、**GPT-OSS-20B +3.43%（p<0.01）**、**Llama-3B +5.54%（p<0.05）**。
- 最佳配置为**GPT-OSS-20B，88.3%/88.34%准确率**，优于更大的程序合成系统**ToRA-Code-34B（80.7%）**，并接近/超过文中对比的**OpenMath-70B（84.6%）**，同时参数量约少**3.5×**。
- 文中还报告与单任务Prolog微调相比的增益：**GPT-OSS-20B +2.22%**、**Qwen-32B +0.38%**、**Llama-3B +5.24%**；但**Qwen3-8B -2.28%**，说明中等规模模型可能还不足以稳定学习类型安全的符号推理。
- 执行引导修复在大模型上表现突出：**32B**规模下总体**纠错率92.7%（k=3）**；Cocktail训练把原本难修复的**TYPE_ERROR**（仅**12%**可修复）转变为更易修复的**DOMAIN_ERROR**（**96%**可修复）。
- 训练动态上，Cocktail验证损失低于单任务微调，例如**Qwen-32B: 0.155 vs 0.184**，支持其“跨任务正迁移”主张。
- 论文还给出一个能力阈值判断：约**10B参数附近**可能是从“只学会表面语法”过渡到“具备语义类型理解与自调试能力”的关键规模点。

## Link
- [http://arxiv.org/abs/2603.02504v2](http://arxiv.org/abs/2603.02504v2)
