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
language_code: en
---

# NeuroProlog: Multi-Task Fine-Tuning for Neurosymbolic Mathematical Reasoning via the Cocktail Effect

## Summary
NeuroProlog proposes a neurosymbolic framework that converts math problems into executable Prolog programs, and uses multi-task “Cocktail” fine-tuning so the model learns both mathematical knowledge representation and solution-program generation at the same time. Its goal is to enable LLMs not just to “sound like they are reasoning,” but to produce formal reasoning processes that are verifiable, executable, and repairable.

## Problem
- Existing LLMs often rely on pattern matching in mathematical reasoning, making them prone to producing answers that seem fluent but are logically incorrect, while intermediate steps are hard to verify.
- Many neurosymbolic methods only perform post-hoc checking at inference time; the model itself does not truly learn symbolic structure and executable reasoning during training.
- This matters because mathematical and programmatic reasoning require **reliability, interpretability, and verifiability**, especially in scenarios involving compositional generalization and error recovery.

## Approach
- Unify mathematical reasoning as **generating Prolog programs**: translate mathematical formulas/concepts into rules, translate word problems into executable programs, and then obtain answers through execution.
- Use multi-task Cocktail training to jointly optimize three kinds of supervision signals: **KB** (formula-to-Prolog-rule), **SOLVE** (natural language problem-to-program), and semantic alignment/execution verification between programs and answers.
- The training data includes about **200 math knowledge base entries**, **310 manually constructed solution examples**, and **7476 GSM8K-Prolog problems**, all using a unified Prolog representation.
- During inference, adopt **execution-guided decoding**: first generate and execute a program; if it fails, provide feedback to the model based on the error type (syntax, type, domain, instantiation, logical error), and iteratively repair it up to **3 times**.
- The core intuition is simple: first teach the model “how mathematical concepts are written as rules,” then teach it “how to assemble a problem using those rules,” so that abstract knowledge can transfer to concrete problem solving.

## Results
- On **GSM8K**, evaluated across **4 model scales (3B–32B)**, Cocktail training delivers consistent gains over single-task baselines: **Qwen-32B +5.23% (p<0.01)**, **GPT-OSS-20B +3.43% (p<0.01)**, and **Llama-3B +5.54% (p<0.05)**.
- The best configuration is **GPT-OSS-20B, 88.3%/88.34% accuracy**, outperforming the larger program synthesis system **ToRA-Code-34B (80.7%)**, and approaching/surpassing the compared **OpenMath-70B (84.6%)**, while using about **3.5×** fewer parameters.
- The paper also reports gains relative to single-task Prolog fine-tuning: **GPT-OSS-20B +2.22%**, **Qwen-32B +0.38%**, **Llama-3B +5.24%**; but **Qwen3-8B -2.28%**, indicating that medium-scale models may still be insufficient to stably learn type-safe symbolic reasoning.
- Execution-guided repair performs especially well on large models: at the **32B** scale, the overall **correction rate is 92.7% (k=3)**; Cocktail training transforms previously hard-to-fix **TYPE_ERROR**s (only **12%** repairable) into easier-to-fix **DOMAIN_ERROR**s (**96%** repairable).
- In training dynamics, Cocktail achieves lower validation loss than single-task fine-tuning, for example **Qwen-32B: 0.155 vs 0.184**, supporting its claim of “positive transfer across tasks.”
- The paper also suggests a capability threshold: around **10B parameters** may be the key scale at which models transition from “only learning surface syntax” to “acquiring semantic type understanding and self-debugging ability.”

## Link
- [http://arxiv.org/abs/2603.02504v2](http://arxiv.org/abs/2603.02504v2)
