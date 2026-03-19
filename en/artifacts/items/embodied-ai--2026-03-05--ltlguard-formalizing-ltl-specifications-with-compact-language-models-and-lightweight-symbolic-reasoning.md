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
language_code: en
---

# LTLGuard: Formalizing LTL Specifications with Compact Language Models and Lightweight Symbolic Reasoning

## Summary
LTLGuard aims to translate natural-language requirements into LTL formulas more reliably, especially for compact open-source models that can be deployed locally. It combines constrained generation, retrieval-augmented examples, and lightweight symbolic reasoning to improve syntactic correctness, semantic accuracy, and cross-formula consistency.

## Problem
- The paper addresses how to automatically formalize **ambiguous natural-language requirements** into LTL specifications that are **syntactically correct, as semantically faithful as possible, and mutually consistent**.
- This matters because requirements formalization is a major bottleneck for bringing formal verification into practice; while large models are powerful, they often raise issues of privacy, cost, energy use, and controllability, whereas small/medium models are often unreliable on temporal logic.
- The difficulty is that natural language is inherently ambiguous: the same requirement may correspond to multiple reasonable but non-equivalent LTL interpretations, and multiple requirements may also conflict with one another.

## Approach
- The core method is a **modular toolchain**: it first uses a compact language model to generate candidate LTL formulas, then applies **syntax-constrained decoding** to force outputs to conform to LTL grammar as much as possible.
- It uses **RAFSL** (retrieval-augmented few-shot learning) to retrieve the top-k examples from an NL-LTL example library by semantic similarity, then inserts the relevant examples into the prompt to help the small model “translate by looking at examples.”
- After generation, it performs **syntactic parsing/error correction**; if parsing fails, it feeds the error message back to the model for iterative repair until a parseable formula is obtained.
- It then uses **BLACK** for LTL satisfiability/consistency checking; if multiple specifications conflict, it provides explanations such as the **unsat core**, and feeds the conflict information back to the model to assist repair.
- Put simply, instead of trusting the model to get it right in one shot, the system lets the model repeatedly revise inside a closed loop of **example prompting + grammar guardrails + parser feedback + logical checking**.

## Results
- In ablation experiments on 70 NL-LTL pairs, **Mistral-7B** improved from vanilla **10.0%** syntactic correctness / **7.1%** semantic correctness to **92.8% / 38.5%** with the full system **V7**; its best semantic score appeared at **V6: 40.0%**.
- **Phi-3-mini-4B** improved from **47.1% / 24.2%** to **92.8% / 35.7%** with **V7**, while its best semantic score reached **64.2% at V6**.
- **Mistral-Nemo-12B** improved from **51.4% / 31.4%** to **92.8% / 67.1% at V4** (the best for this model). **Qwen2.5-14B** improved from **95.7% / 68.5%** to **97.1% / 78.6% at V6** (best semantic result).
- On the 36-example **nl2spec hard** benchmark, LTLGuard (Qwen2.5-14B, V6) achieved: **100.0% syntax, 75.0% S1 semantics, and 77.8% S2 semantics in Exp.1 with overlapping retrieval sets**; **97.2% syntax, 50.0% S1, and 63.9% S2 in Exp.2 after removing overlap**.
- Compared with prior methods on the same hard benchmark: **NL2LTL achieved 2.7%**, **fine-tuned T5 achieved 5.5%**, **nl2spec initial + Codex achieved 58.3%**, and **nl2spec interactive + Codex achieved 86.1%**. Under a **non-interactive, compact open-source model** setting, LTLGuard outperforms all reported non-interactive baselines and approaches the best interactive Codex result.
- The paper also explicitly notes that because of natural-language ambiguity, some generated formulas may be **reasonable interpretations** even if they are not equivalent to the annotation; accordingly, the authors report both **ambiguity-intolerant (S1)** and **ambiguity-friendly (S2)** semantic evaluations.

## Link
- [http://arxiv.org/abs/2603.05728v1](http://arxiv.org/abs/2603.05728v1)
