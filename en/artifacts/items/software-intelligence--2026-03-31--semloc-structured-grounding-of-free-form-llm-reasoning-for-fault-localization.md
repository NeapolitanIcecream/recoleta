---
source: arxiv
url: http://arxiv.org/abs/2603.29109v1
published_at: '2026-03-31T00:56:43'
authors:
- Zhaorui Yang
- Haichao Zhu
- Qian Zhang
- Rajiv Gupta
- Ashish Kundu
topics:
- fault-localization
- llm-grounding
- semantic-analysis
- code-intelligence
- software-debugging
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# SemLoc: Structured Grounding of Free-Form LLM Reasoning for Fault Localization

## Summary
SemLoc is a fault localization method for bugs where passing and failing runs follow the same control flow, so coverage signals do not separate the faulty line. It turns LLM-written semantic constraints into executable checks, measures which checks fail across tests, and uses that evidence to rank suspicious code.

## Problem
- It targets semantic bugs such as wrong numeric relations, missing normalization, or incorrect boundary logic, where passing and failing executions can hit the same statements in the same order.
- Standard fault localization methods based on coverage, slicing, or trace structure lose signal in this setting, which makes debugging slow and expensive.
- Prior LLM-based localization often outputs free-form guesses or explanations that are hard to verify against runtime behavior and hard to compare across tests.

## Approach
- SemLoc asks an LLM to infer semantic constraints about intended program behavior from the buggy function, SSA-transformed code, and passing/failing tests.
- Each inferred constraint is forced into a closed intermediate representation with a category, a program anchor, and an executable boolean expression, so it can be checked at a precise code location.
- The system instruments the program, runs the test suite, and builds a semantic violation spectrum: a constraint-by-test matrix that records which semantic checks fail on which tests.
- It scores constraints with an SBFL-style Ochiai formula and maps those scores back to statements, producing a ranked fault list from semantic evidence rather than coverage alone.
- A counterfactual verification step proposes minimal repairs for top constraints, reruns tests, and separates primary causal violations from downstream effects or over-broad constraints.

## Results
- Evaluation uses **SemFault-250**, a corpus of **250 Python programs** with single semantic faults collected from real repositories and prior benchmarks.
- With **Claude Sonnet 4.6**, SemLoc reports **42.8% Top-1** and **68.0% Top-3** fault localization accuracy.
- Against named baselines, it beats **SBFL-Ochiai: 6.4% Top-1 / 13.2% Top-3** and **delta debugging: 0.0% / 0.0%** on this benchmark.
- It narrows inspection to **7.6% of executable lines**, described as a **5.7x reduction** relative to SBFL.
- Counterfactual verification improves **Top-1 accuracy from 30.8% to 42.8%**, a gain of **12.0 percentage points**.
- The paper also claims counterfactual verification identifies a **primary causal constraint for 60.8%** of programs.

## Link
- [http://arxiv.org/abs/2603.29109v1](http://arxiv.org/abs/2603.29109v1)
