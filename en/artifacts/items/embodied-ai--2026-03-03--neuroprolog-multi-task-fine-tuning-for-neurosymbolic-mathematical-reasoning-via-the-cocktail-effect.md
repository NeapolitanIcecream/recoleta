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
language_code: en
---

# NeuroProlog: Multi-Task Fine-Tuning for Neurosymbolic Mathematical Reasoning via the Cocktail Effect

## Summary
NeuroProlog is a neurosymbolic framework that converts math word problems into executable Prolog programs, with the goal of making the reasoning process verifiable, executable, and repairable. The paper’s core contribution is a multi-task “Cocktail” fine-tuning strategy that jointly learns mathematical formulas, program generation, and answer alignment in the same symbolic space, thereby improving the reliability of mathematical reasoning.

## Problem
- Existing LLMs often generate fluent but illogical answers in mathematical reasoning, functioning more like pattern matching than verifiable reasoning.
- Many neurosymbolic methods only perform post-hoc verification at inference time; during training, the model does not truly learn symbolic structure and formal logic.
- This matters because mathematical and formal reasoning scenarios require **intermediate steps to be executable, verifiable, and correctable**, otherwise models struggle to generalize robustly to new compositional problems.

## Approach
- Represent mathematical reasoning uniformly as **Prolog program generation**: translate mathematical formulas/concepts into rules (the KB task), and translate natural language problems into executable programs (the SOLVE task).
- Propose **Cocktail multi-task training**, jointly optimizing three complementary supervision signals: formula-to-rule translation, natural language-to-program synthesis, and program–answer consistency/execution verification, enabling positive transfer from shared symbolic representations.
- Construct training data consisting of 200 mathematical knowledge base (KB) entries, 310 problem-solving examples, and 7476 GSM8K-Prolog samples; the KB covers 15+ mathematical domains and includes natural-language semantic annotations in Prolog.
- Use **execution-guided decoding** at inference: first generate Prolog, then execute it with SWI-Prolog; if execution fails, feed back one of 5 error types (syntax/type/domain/instantiation/logical) to the model and iteratively repair up to 3 times.
- Use the same model for both initial generation and repair, without training a separate error corrector, to measure whether the model has truly internalized symbolic semantics and self-debugging ability.

## Results
- On GSM8K, across 4 model scales (3B–32B), Cocktail training consistently improves over single-task baselines: **Qwen-32B +5.23% (p<0.01)**, **GPT-OSS-20B +3.43% (p<0.01)**, and **Llama-3B +5.54% (p<0.05)**.
- The best configuration is **GPT-OSS-20B, 88.3% accuracy**; it outperforms the larger program synthesis system **ToRA-Code-34B at 80.7%**, and approaches/exceeds the **OpenMath-70B 84.6%** comparison reported in the paper, while using **3.5×** fewer parameters, demonstrating higher parameter efficiency.
- The paper also reports gains in controlled comparisons: relative to single-task Prolog fine-tuning, Cocktail FT achieves **GPT-OSS-20B +2.22%**, **Qwen-32B +0.38%**, and **Llama-3B +5.24%**; however, **Qwen3-8B -2.28%**, suggesting a capacity threshold around **10B** for semantic type understanding.
- At the 32B scale, execution-guided repair reaches an **overall correction rate of 92.7% (k=3)**; at the same time, the error distribution shifts from harder-to-fix **TYPE_ERROR** to more repairable **DOMAIN_ERROR**: the former has a **12%** repair rate, while the latter has a **96%** repair rate.
- At the 8B scale, Cocktail training reduces/eliminates syntax errors but introduces more semantic failures, indicating that small models can learn superficial program format without necessarily learning type safety and true symbolic semantics.
- In terms of training dynamics, Cocktail achieves lower final validation loss than single-task Prolog fine-tuning, for example **Qwen-32B: 0.155 vs 0.184**, supporting the claim of positive transfer from multi-task learning.

## Link
- [http://arxiv.org/abs/2603.02504v2](http://arxiv.org/abs/2603.02504v2)
