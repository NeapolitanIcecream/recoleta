---
source: arxiv
url: http://arxiv.org/abs/2603.08322v1
published_at: '2026-03-09T12:42:56'
authors:
- Hai Xia
- Carla P. Gomes
- Bart Selman
- Stefan Szeider
topics:
- neurosymbolic-ai
- mathematical-discovery
- combinatorial-design
- latin-squares
- llm-agents
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Agentic Neurosymbolic Collaboration for Mathematical Discovery: A Case Study in Combinatorial Design

## Summary
This paper demonstrates, through a collaboration case involving humans, an LLM agent, and symbolic tools, how a neurosymbolic system can produce new mathematical discoveries in combinatorial design. The core result resolves the open problem of the minimum imbalance of Latin squares in the case \(n\equiv 1\pmod 3\), and provides a tight lower bound that is formally verified in Lean 4.

## Problem
- The paper aims to solve the following question: when \(n\equiv 1\pmod 3\), a Latin square cannot achieve perfect spatial balance, so **what is the smallest possible imbalance**? This is an open problem in combinatorial design.
- This question matters because Latin squares are widely used in **experimental design**, and spatial balance is directly related to the fairness of treatment assignment; theoretically, it also bears on whether AI can participate in genuine mathematical discovery.
- The authors are also concerned with **the discovery process itself**: what contributions were made respectively by neural models, symbolic computation, and human researchers, and which parts truly drove the emergence of the new result.

## Approach
- The core mechanism is simple: an LLM agent is responsible for proposing conjectures, writing code, orchestrating tools, and organizing proofs; symbolic tools such as SageMath, Rust exhaustive solvers, and simulated annealing are responsible for **rigorous verification, search, and enumeration**; humans provide the crucial research pivot.
- The key research pivot was not to keep searching for constructions with zero imbalance, but to instead ask: **since zero is impossible, what is the minimum positive imbalance**? This pivot was proposed by a human and opened up a new optimization problem.
- From numerical results, the agent identified a hidden structure: the distance between any two rows is always **even**. Put simply, this parity constraint makes the deviation of each pair of rows at least twice what intuition had originally suggested, thereby raising the lower bound from the naive estimate to \(4n(n-1)/9\).
- To attain this lower bound, the authors introduce a new construction concept, **near-perfect permutations**: their shift correlation takes only the two optimally allowed values \(a\) or \(a+2\); from these, circulant Latin squares are then constructed.
- The paper also adds multi-model review and persistent memory: multiple frontier LLMs work in parallel on **critique and error detection**, while project state files / a knowledge base maintain research continuity across about 15 sessions over 5 days; the final lower bound is formally proved in **Lean 4**.

## Results
- Main mathematical result: for all \(n\times n\) Latin squares with \(n\equiv 1\pmod 3\), the paper proves the tight lower bound **\(I(L)\ge 4n(n-1)/9\)**, and claims this resolves the open problem for this case.
- The result is **tight**: circulant Latin squares constructed from near-perfect permutations achieve equality; for example, when \(n=4\), exhaustive enumeration of all **576** Latin squares shows that the minimum imbalance is exactly **\(16/3\)**, consistent with the formula **\(4\cdot4\cdot3/9\)**.
- Computational verification: simulated annealing found near-perfect permutations for all \(n\equiv 1\pmod 3\), **4\le n\le 52**, and all attain the optimal value **\(I^*=4n(n-1)/9\)**. Example entries in the table include: for \(n=13\), **\(I^*=208/3\)** (time **<1 s**); for \(n=25\), **\(800/3\)** (**2 s**); for \(n=40\), **\(2080/3\)** (**74 s**); for \(n=52\), **\(3536/3\)** (**32 s**).
- A quantified example of the discovery trigger: at \(n=13\), the naive lower bound is **26**, but simulated annealing optimization initially found only **69.3**, a gap of about **2.7×**; this anomaly prompted the agent to discover the crucial parity structure that “all distances are even.”
- Formal verification: the main lower-bound theorem was completed in **Lean 4 + Mathlib**, in about **340 lines** of code, covering Fixed Sum, the Parity Lemma, and the main inequality.
- Conclusion on multi-model collaboration: parallel frontier LLMs were effective at **critique / error detection**, and once discovered the “circulant trap” in a proof draft; but they were unreliable on constructive claims—for example, they claimed the inversion map could achieve imbalance **\(O(n^{5/2})\)**, while experiments showed the actual behavior is about **\(\Theta(n^{3.6})\)**.

## Link
- [http://arxiv.org/abs/2603.08322v1](http://arxiv.org/abs/2603.08322v1)
