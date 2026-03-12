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
relevance_score: 0.06
run_id: materialize-outputs
---

# NeuroProlog: Multi-Task Fine-Tuning for Neurosymbolic Mathematical Reasoning via the Cocktail Effect

## Summary
NeuroProlog 是一个把数学应用题转成可执行 Prolog 程序的神经符号框架，目标是让推理过程可验证、可执行、可修复。论文核心贡献是用一种多任务“Cocktail”微调，把数学公式、程序生成和答案对齐放进同一符号空间中联合学习，从而提升数学推理可靠性。

## Problem
- 现有 LLM 在数学推理上常能生成流畅但不合逻辑的答案，本质上更像模式匹配而非可验证推理。
- 许多神经符号方法只在推理时做事后校验，模型训练阶段并没有真正学会符号结构与形式逻辑。
- 这很重要，因为数学与形式推理场景需要**中间步骤可执行、可验证、可纠错**，否则模型难以稳健泛化到新组合问题。

## Approach
- 将数学推理统一表示为 **Prolog 程序生成**：把数学公式/概念翻译为规则（KB 任务），把自然语言题目翻译为可执行程序（SOLVE 任务）。
- 提出 **Cocktail 多任务训练**，联合优化三类互补监督：公式到规则翻译、自然语言到程序合成、程序与答案的一致性/执行验证信号，从共享符号表示中获得正迁移。
- 构建训练数据：200 条数学知识库（KB）条目、310 条问题求解示例，以及 7476 条 GSM8K-Prolog 样本；KB 覆盖 15+ 数学领域，并在 Prolog 中加入自然语言语义注释。
- 推理时采用 **execution-guided decoding**：先生成 Prolog，再交给 SWI-Prolog 执行；若失败，则依据 5 类错误（syntax/type/domain/instantiation/logical）给模型反馈，最多迭代修复 3 次。
- 使用同一个模型既做初次生成也做修复，不额外训练专门的纠错器，以衡量模型是否真正内化了符号语义与自调试能力。

## Results
- 在 GSM8K 上、跨 4 个模型规模（3B–32B）评估时，Cocktail 训练相对单任务基线取得一致提升：**Qwen-32B +5.23%（p<0.01）**、**GPT-OSS-20B +3.43%（p<0.01）**、**Llama-3B +5.54%（p<0.05）**。
- 最佳配置为 **GPT-OSS-20B，准确率 88.3%**；优于更大的程序合成系统 **ToRA-Code-34B 的 80.7%**，并接近/超过文中对比的 **OpenMath-70B 84.6%**，且参数量少 **3.5×**，显示更高参数效率。
- 论文还给出受控比较中的增益：相对 Prolog 单任务微调，Cocktail FT 达到 **GPT-OSS-20B +2.22%**、**Qwen-32B +0.38%**、**Llama-3B +5.24%**；但 **Qwen3-8B -2.28%**，说明约 **10B** 左右可能存在语义类型理解的容量门槛。
- 在 32B 规模上，执行引导修复的**总体纠错率达到 92.7%（k=3）**；同时错误分布从难修复的 **TYPE_ERROR** 转为更可修复的 **DOMAIN_ERROR**：前者修复率 **12%**，后者修复率 **96%**。
- 在 8B 规模上，Cocktail 训练虽减少/消除语法错误，但引入更多语义失败，表明小模型能学会表面程序格式，却未必学会类型安全和真正的符号语义。
- 训练动态方面，Cocktail 的最终验证损失低于单任务 Prolog 微调，例如 **Qwen-32B: 0.155 vs 0.184**，支持多任务正迁移的说法。

## Link
- [http://arxiv.org/abs/2603.02504v2](http://arxiv.org/abs/2603.02504v2)
