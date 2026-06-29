---
source: arxiv
url: https://arxiv.org/abs/2606.16886v1
published_at: '2026-06-15T15:59:10'
authors:
- Muhammad A. A. Pirzada
- Julian Parsert
- Weiqi Wang
- Konstantin Korovin
- Lucas C. Cordeiro
topics:
- software-verification
- loop-invariants
- code-intelligence
- local-llms
- neuro-symbolic-ai
- formal-methods
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Neuro-Symbolic Software Verification: Hyper-charging Local Language Models with Symbolic Reasoning at Scale

## Summary
VerIbmc combines ESBMC with local open-weight LLMs to synthesize loop invariants for C verification. The paper claims strong solve rates without sending source code to cloud APIs.

## Problem
- Formal verification often fails when a tool lacks a strong loop invariant for a loop.
- Existing LLM-based invariant tools often depend on proprietary cloud models, which creates privacy, cost, reproducibility, and deployment issues for production code.
- The problem matters because safety-critical and security-sensitive software needs proof workflows that can run inside an organization.

## Approach
- VerIbmc first runs ESBMC on the unannotated program and stops if ESBMC can already prove or refute it.
- It then enumerates simple symbolic invariant atoms such as `x <= y`, `x == c`, or `x >= c`, and asks ESBMC which atoms are inductive.
- If symbolic atoms do not prove the program, a local LLM proposes more invariants. ESBMC checks each candidate and returns structured feedback.
- The pipeline keeps three stores of atoms: provable, disprovable, and unknown. Later prompts include these stores so the LLM can avoid failed paths and build on proven facts.
- The paper tests Chain-of-Thought and Tree-of-Thought prompting, including several reasoning styles, while accepting only invariants verified by ESBMC.

## Results
- The evaluation covers 520 benchmark problems across 5 benchmark families; 499 remain after excluding 21 cases with unavoidable overflow.
- The best single setup, GPT-OSS-120B, solves 431 of 499 problems, or 86.4%.
- The symbolic phase alone solves 75 problems without any LLM call.
- Symbolic feedback gives the weakest model up to 35 extra solved benchmarks: Llama-3.1-8B improves from 307 to 342 solved cases.
- The study uses 5 open-weight models ranging from 7B to 120B parameters, 4 inference strategies, and reports 10,400 per-problem outcomes.
- On the 4 benchmark suites shared with the strongest cloud-API tools, VerIbmc is reported as competitive while running on a single local machine.

## Link
- [https://arxiv.org/abs/2606.16886v1](https://arxiv.org/abs/2606.16886v1)
