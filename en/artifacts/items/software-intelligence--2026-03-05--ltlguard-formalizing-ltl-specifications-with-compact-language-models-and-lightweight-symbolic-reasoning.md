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
language_code: en
---

# LTLGuard: Formalizing LTL Specifications with Compact Language Models and Lightweight Symbolic Reasoning

## Summary
LTLGuard aims to translate natural-language requirements into LTL formal specifications more reliably, with a focus on achieving high-quality, locally deployable, privacy-preserving formalization on **compact open-weight models with 4B–14B parameters**. The core idea is to let small models generate under syntactic constraints first, then use lightweight symbolic reasoning to check and iteratively repair syntax errors and cross-formula conflicts.

## Problem
- The problem it addresses is converting **ambiguous, easily polysemous** natural-language requirements into LTL formulas that are **syntactically correct, as semantically faithful as possible, and mutually consistent**.
- This matters because formal requirements are the foundation of verification, monitoring, and correctness assurance, but industrial adoption is hindered by the **high barrier of manual formalization**, the inherent ambiguity of requirements text, and issues of **privacy, cost, and controllability** with large models.
- Small/medium models are better suited for local deployment, but on niche logic tasks such as temporal logic they often produce **syntax errors, hallucinations, and mutually contradictory specifications**.

## Approach
- It replaces “asking the LLM to translate in one shot” with a **modular pipeline**: system prompting + **retrieval-augmented few-shot learning** (RAFSL) + **grammar-constrained decoding** + **parser-feedback repair** + **LTL consistency checking**.
- RAFSL dynamically retrieves the most relevant examples from an NL-LTL example library based on semantic similarity and adds them to the prompt, helping small models “cram” temporal-logic patterns on the fly without fine-tuning.
- During generation, **LTL grammar constraints** (SynCode/DFA masking) restrict the next token to valid grammatical paths only, so the model is more likely to produce directly parseable formulas.
- If parsing fails, debugging information is fed back to the model for iterative correction; if multiple formulas are inconsistent when combined, BLACK checks **SAT/UNSAT** and returns an **unsat core** to explain the source of the conflict.
- In essence, the core mechanism can be understood simply as: **letting the small model handle “guessing formulas,” while the parser and solver provide fallback correction and conflict detection**.

## Results
- In an ablation study on 70 NL-LTL pairs, **Mistral-7B** improved from Vanilla’s **10.0% syntactic correctness / 7.1% semantic correctness** to the full system V7’s **92.8% syntactic correctness / 38.5% semantic correctness**; the best semantic configuration, V6, reached **40.0%**.
- **Phi-3-mini-4B** improved from **47.1% / 24.2%** to V6’s **91.4% syntactic correctness / 64.2% semantic correctness**; V7 achieved **92.8%** syntax and **35.7%** semantics, showing that different component combinations have a clear impact on semantic performance for small models.
- **Mistral-Nemo-12B** improved from **51.4% / 31.4%** to V4’s **92.8% syntactic correctness / 67.1% semantic correctness**. **Qwen2.5-14B** was already strong in Vanilla (**95.7% / 68.5%**), and V6 further increased semantic correctness to **78.6%** while maintaining **97.1%** syntactic correctness.
- On the **nl2spec hard 36-example** benchmark, the best setting (V6 + Qwen2.5-14B) achieved **100.0% syntactic correctness, 75.0% semantic accuracy (S1), 77.8% semantic accuracy (S2)** when RAFSL overlap was present; after removing overlap, it still achieved **97.2% syntactic correctness, 50.0% (S1), 63.9% (S2)**.
- Compared with prior methods reproduced in the paper, LTLGuard significantly outperformed **NL2LTL 2.7%**, **T5 5.5%**, **nl2spec initial Bloom 13.8%**, **nl2spec initial Codex 44.4%**, **nl2spec initial+example Codex 58.3%**, and approached the level of **nl2spec interactive Codex 86.1%**, while using **smaller open-weight models and requiring no fine-tuning**.
- The paper also emphasizes that because natural-language requirements are themselves ambiguous, some “errors” are actually **reasonable alternative formalizations that differ from the annotation**; however, the paper tries to reflect this as much as possible through “equivalence checking” and the two evaluation schemes S1/S2.

## Link
- [http://arxiv.org/abs/2603.05728v1](http://arxiv.org/abs/2603.05728v1)
