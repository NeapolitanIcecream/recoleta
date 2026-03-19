---
source: arxiv
url: http://arxiv.org/abs/2603.09678v1
published_at: '2026-03-10T13:47:15'
authors:
- Aman Sharma
- Paras Chopra
topics:
- llm-evaluation
- ood-generalization
- code-generation
- benchmarking
- reasoning
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# EsoLang-Bench: Evaluating Genuine Reasoning in Large Language Models via Esoteric Programming Languages

## Summary
EsoLang-Bench uses five esoteric programming languages that appear extremely rarely in pretraining data to test whether large language models can truly "reason," rather than merely memorizing common coding patterns. The paper shows that models that are near the ceiling on mainstream coding benchmarks almost completely fail on these truly out-of-distribution tasks.

## Problem
- The paper addresses whether existing code generation benchmarks overestimate LLMs' true reasoning ability, because high scores may mainly come from training data memorization, contamination, and pattern matching.
- This matters because if models can only "apply templates" on high-frequency languages and common problem types, then their generalization, test-time learning, and real intelligence are being misjudged.
- The authors aim to build a benchmark with low contamination risk and almost no incentive for "benchmark gaming," specifically to measure transferable computational reasoning ability.

## Approach
- Proposes **EsoLang-Bench**: it contains **80** language-agnostic algorithmic problems, divided into **4** difficulty tiers; evaluated across **5** esoteric languages, yielding **400** problem-language combinations.
- Selects five Turing-complete but extremely data-scarce languages: **Brainfuck, Befunge-98, Whitespace, Unlambda, Shakespeare**; their public repository counts are **1,000–100,000×** smaller than Python's, and the figure also shows a gap on the order of about **5,000×**.
- Evaluates **5** frontier models and compares **5** prompting/scaffolding strategies: zero-shot, few-shot, self-scaffolding, textual self-scaffolding, ReAct; it also examines tool-augmented agentic coding systems.
- The core mechanism is simple: take basic algorithmic problems equivalent to those in Python and move them into nearly unseen new languages, then provide documentation, interpreter feedback, and opportunities for iteration to see whether models can learn and apply them on the fly like humans.
- Success is judged through interpreter execution and exact matching on **6** test cases, so as to distinguish "can talk about it" from "can actually do it" as much as possible.

## Results
- The paper's central result is a huge capability gap: the common **85–95%** level on standard coding benchmarks drops to only **0–11%** on equivalent esoteric-language tasks.
- The abstract states that frontier models achieve only **0–11%** overall on this benchmark, and **everything above Easy difficulty is 0%**; Table 2 also explicitly reports **Medium/Hard/Extra-Hard = 0%**.
- Figure 1 shows that, across five languages and multiple strategies, under the best self-scaffolding setup **GPT-5.2 reaches only 6.2%**, and "all models remain below **7%** even with advanced scaffolding."
- Figure 2 further provides an equivalent Python comparison: **the best model achieves only 3.8% (GPT-5.2) vs 100% on equivalent Python tasks**.
- Few-shot and self-reflection-style methods bring basically no significant gains; based on this, the authors argue that ICL performance on this kind of OOD task depends on pretraining coverage rather than reflecting genuine rapid learning ability.
- The error analysis says **59%** of failures are compilation errors, indicating that models first get stuck at the most basic syntax and execution level rather than at high-level algorithm design.

## Link
- [http://arxiv.org/abs/2603.09678v1](http://arxiv.org/abs/2603.09678v1)
