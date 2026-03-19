---
source: hn
url: https://arxiv.org/abs/2603.09172
published_at: '2026-03-14T23:37:12'
authors:
- 1024core
topics:
- ramsey-numbers
- combinatorics
- llm-search
- code-mutation
- automated-discovery
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Researchers improve lower bounds for some Ramsey numbers using AlphaEvolve

## Summary
This paper uses AlphaEvolve, an LLM-based code mutation agent, to automatically generate search algorithms and improve the lower bounds of five classical Ramsey numbers. Its significance is that it unifies what were previously highly customized, problem-specific combinatorial search workflows into a reusable meta-algorithm.

## Problem
- The problem the paper addresses is: how to construct larger counterexamples for classical Ramsey numbers in order to raise their **lower bounds**; this has long been a difficult problem in combinatorics.
- This matters because Ramsey numbers are extremely fundamental yet notoriously hard objects in discrete mathematics, and many of the best results rely on complex computational search.
- Previous methods typically involved manually designing specialized search algorithms for one or a small number of instances, with weak generalizability and often incomplete reproduction details.

## Approach
- The core method uses **AlphaEvolve**, an LLM-based **code mutation agent**, to automatically propose, modify, and improve programs for searching combinatorial structures.
- Put simply: the system does not directly guess the answer, but continuously “writes and edits search code,” letting the code look for graph constructions that can certify higher lower bounds.
- The authors position it as a **single meta-algorithm**: the same automated mechanism can be used for multiple Ramsey number instances, rather than hand-crafting a specialized algorithm for each target.
- In addition to pursuing new results, the authors also used the method to recover lower bounds corresponding to known exact values, and to reproduce the current best known lower bounds in many other cases, in order to validate the breadth of the approach.

## Results
- Improved the lower bounds of **5** classical Ramsey numbers: **R(3,13)** increased from **60 to 61**.
- **R(3,18)** increased from **99 to 100**.
- **R(4,13)** increased from **138 to 139**.
- **R(4,14)** increased from **147 to 148**.
- **R(4,15)** increased from **158 to 159**.
- In addition, the authors claim that the method **successfully recovered the lower bounds corresponding to all known exact Ramsey numbers**, and **matched the current best known lower bounds** in **many other cases**; the abstract does not provide more detailed quantitative coverage or systematic comparison data against specific prior algorithms.

## Link
- [https://arxiv.org/abs/2603.09172](https://arxiv.org/abs/2603.09172)
