---
source: hn
url: https://arxiv.org/abs/2603.09172
published_at: '2026-03-14T23:37:12'
authors:
- 1024core
topics:
- llm-based-search
- combinatorial-optimization
- ramsey-numbers
- code-mutation-agent
- automated-discovery
relevance_score: 0.63
run_id: materialize-outputs
language_code: en
---

# Researchers improve lower bounds for some Ramsey numbers using AlphaEvolve

## Summary
This paper shows that AlphaEvolve, an LLM-based code mutation agent, can automatically discover search algorithms for combinatorial structures, and uses it to improve the lower bounds of 5 classical Ramsey numbers. Its significance is that, whereas the past typically required hand-designing specialized search programs for each specific problem, this work claims to produce these results in a unified way using a single meta-algorithm.

## Problem
- The paper addresses the problem of how to automatically construct combinatorial structures for improving lower bounds on Ramsey numbers, without having to manually invent a specialized search algorithm for each specific parameter setting.
- This matters because classical Ramsey lower bounds are mostly obtained through computational search, but existing methods are usually “one custom algorithm per problem,” with poor reusability and scalability.
- If a general-purpose intelligent code generation/mutation system can reliably produce high-quality search algorithms, it could accelerate mathematical discovery and automated scientific exploration.

## Approach
- The core method is AlphaEvolve, an LLM-based code mutation agent. Put simply, it repeatedly modifies search code, runs it, evaluates whether the result is better, and keeps the more effective versions.
- It does not directly output a Ramsey construction itself, but instead generates/improves the “program that searches for the answer,” effectively turning the problem into an evolutionary process over automated search algorithms.
- The authors use it as a single “meta-algorithm” that produces corresponding search strategies for different Ramsey number instances, rather than hand-writing a separate heuristic for each instance.
- In addition to finding new lower bounds, the authors also use it to recover lower bounds corresponding to known exact values, and to reach the current best known lower bounds in many other cases, as a way to validate the method’s generality.

## Results
- The paper claims to improve the lower bound for **R(3,13)** from **60 to 61**.
- It improves **R(3,18)** from **99 to 100**.
- It improves **R(4,13)** from **138 to 139**.
- It improves **R(4,14)** from **147 to 148**, and **R(4,15)** from **158 to 159**.
- Beyond these 5 new results, the authors claim that their method **successfully recovered the lower bounds corresponding to all known exact Ramsey numbers**.
- The authors also claim to have **matched the current best known lower bounds** in **many other cases**; the provided excerpt does not give more detailed counts of instances, computational cost, or systematic comparison figures against other automated methods.

## Link
- [https://arxiv.org/abs/2603.09172](https://arxiv.org/abs/2603.09172)
