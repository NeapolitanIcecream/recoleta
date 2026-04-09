---
source: arxiv
url: http://arxiv.org/abs/2604.00280v1
published_at: '2026-03-31T22:12:15'
authors:
- Md Rakib Hossain Misu
- Iris Ma
- Cristina V. Lopes
topics:
- formal-specification-synthesis
- program-verification
- jml
- llm-agents
- benchmark-evaluation
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# VeriAct: Beyond Verifiability -- Agentic Synthesis of Correct and Complete Formal Specifications

## Summary
This paper argues that verifier pass rate is a weak target for formal specification synthesis and introduces VeriAct to generate JML specs that are verifiable, correct, and complete. It also proposes Spec-Harness, an evaluation method that checks whether verifier-accepted specs actually capture program behavior.

## Problem
- The task is automatic synthesis of formal Java Modeling Language (JML) specifications for Java methods.
- Existing systems often judge success by whether OpenJML accepts the specification, but a verifier can accept specs that are too weak, partial, or wrong.
- This matters because weak specifications miss real behavior, reject valid inputs, or allow invalid outputs, which hurts verification, testing, and software reliability.

## Approach
- The authors first compare classical methods (Daikon, Houdini) and prompt-based LLM methods (SpecGen, AutoSpec, FormalBench prompts) on two benchmarks: SpecGenBench and FormalBench.
- They then apply GEPA prompt optimization, using structured verifier feedback instead of a simple pass/fail reward, to improve prompt-based synthesis.
- They introduce **Spec-Harness**, an automated evaluation framework that checks specification correctness and completeness through symbolic verification plus input/output mutation-style checks grounded in Hoare-triple reasoning.
- They propose **VeriAct**, an agentic closed loop where an LLM plans and writes specs, runs code and verification tools, reads Spec-Harness feedback, and iteratively repairs the spec until it better matches the method behavior.

## Results
- Dataset size: 120 tasks from SpecGenBench and 662 usable tasks from FormalBench after filtering from 700.
- Classical baselines on verifier pass rate: Houdini reached **104/120 (86.7%)** on SpecGenBench and **359/662 (54.2%)** on FormalBench; Daikon reached **22/120 (18.3%)** and **87/662 (13.1%)**.
- Best prompt-based verifier pass rates were lower than Houdini: SpecGen **80/120 (66.7%)** and **200/659 (30.3%)**; AutoSpec **70/120 (58.3%)** and **185/662 (27.9%)**; FormalBench prompts **77/120 (64.2%)** and **238/662 (36.0%)**.
- Prompt sensitivity was large. For SpecGen, average verifier rate dropped from the best setting to **43.1%** on SpecGenBench and **20.1%** on FormalBench.
- The main qualitative claim is that many verifier-accepted specifications, including prompt-optimized ones, are still incorrect or incomplete when checked by Spec-Harness.
- The excerpt states that VeriAct outperforms prompt-based and prompt-optimized baselines on correctness and completeness across two benchmarks, but it does not include the final VeriAct numeric gains in the provided text.

## Link
- [http://arxiv.org/abs/2604.00280v1](http://arxiv.org/abs/2604.00280v1)
