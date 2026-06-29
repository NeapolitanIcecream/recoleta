---
source: arxiv
url: http://arxiv.org/abs/2603.29088v1
published_at: '2026-03-31T00:06:44'
authors:
- Fabian Gloeckle
- Mantas Baksys
- Darius Feher
- Kunhao Zheng
- Amaury Hayat
- Sean B. Holden
- Gabriel Synnaeve
- Peter O'Hearn
topics:
- formal-verification
- imperative-code-generation
- lean-theorem-proving
- multi-agent-systems
- code-intelligence
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# WybeCoder: Verified Imperative Code Generation

## Summary
WybeCoder is a hybrid agent system for generating and formally verifying imperative programs. It combines SMT-based verification with interactive Lean proof work, and it reports much higher solve rates than earlier verified-code benchmarks for this setting.

## Problem
- LLMs improved code generation and theorem proving, but formal verification of generated software still lags, especially for imperative code with mutable state and loops.
- Existing work usually handles either functional programs in theorem provers or imperative programs in auto-active systems like Dafny; each misses part of the problem.
- This matters because generated code still needs costly human review, and testing or fuzzing cannot give full correctness guarantees.

## Approach
- The system follows a prove-as-you-generate loop: generate imperative code, generate invariants, run verification condition generation, send routine obligations to CVC5, and send hard leftovers to Lean.
- It uses two agent styles: a sequential refinement agent and a subgoal-decomposition multi-agent system that extracts proof obligations, solves them in parallel, and reconstructs the full proof.
- When a proof subgoal fails, agents can request targeted code or invariant changes. Named invariants and deterministic goal names let the system transfer solved subproofs across revisions.
- The authors translated the Verina and Clever functional-verification benchmarks into imperative Velvet/Lean tasks to evaluate this setup.
- To reduce specification leakage and functional cheating, they allow functional specs but require imperative implementations, then filter with an LLM-based imperativeness judge.

## Results
- Best reported Verina result: **74.1% solve rate** with **Claude 4.5 Opus** using the **sequential agent** at **32 turns × 16 agents**.
- Best reported Clever-Loom result: **62.1% solve rate** with **Claude 4.5 Opus** using the **sequential agent** at **32 turns × 16 agents**.
- On Verina, sequential-agent scores are **64.6% (GPT-5)**, **55.6% (Gemini 3 Pro)**, **63.3% (Claude 4.5 Sonnet)**, and **74.1% (Claude 4.5 Opus)**. The listed baseline is **20.0%** for **DS Prover V2 7B**.
- On Clever-Loom, sequential-agent scores are **53.8% (GPT-5)**, **32.8% (Gemini 3 Pro)**, **59.6% (Claude 4.5 Sonnet)**, and **62.1% (Claude 4.5 Opus)**, versus **8.7%** for the **COPRA** baseline.
- The paper highlights a low-budget gain on Verina from **18%** in prior reported results to **55%** with their setup, and it cites **15% to 55%** improvement for hybrid verification in small-budget settings.
- Their leakage control had a large effect: one GPT-5 subgoal-decomposition setting on Verina dropped from **75.1%** without the imperativeness guard to **51.9%** with it, which the authors treat as a more honest measure of imperative verified code generation.

## Link
- [http://arxiv.org/abs/2603.29088v1](http://arxiv.org/abs/2603.29088v1)
