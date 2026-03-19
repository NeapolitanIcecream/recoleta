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
- agentic-ai
- neurosymbolic-reasoning
- mathematical-discovery
- multi-agent-deliberation
- formal-verification
- combinatorial-design
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Agentic Neurosymbolic Collaboration for Mathematical Discovery: A Case Study in Combinatorial Design

## Summary
Through a case study involving collaboration among humans, an LLM agent, and symbolic computation tools, this paper shows that AI can participate in open-ended mathematical discovery, rather than merely solving preset problems. The core outcome is a proof of the tight lower bound for the imbalance problem of Latin squares in combinatorial design when $n\equiv 1\pmod{3}$, together with formal verification in Lean 4.

## Problem
- The paper addresses the following question: when $n\equiv 1\pmod{3}$, what is the minimum achievable imbalance of a Latin square? Perfect balance was already known to be impossible in this case, but the minimum positive imbalance had remained open.
- This matters because Latin squares are foundational objects in combinatorial design and experimental design, and spatial balance is directly related to design quality; at the same time, it is also a representative problem for testing whether AI can participate in “genuine mathematical discovery.”
- The authors also seek to answer a methodological question: in collaboration among humans, LLMs, and symbolic tools, what exactly does each contribute, and which parts are reliable or unreliable?

## Approach
- The core mechanism is an **agentic neurosymbolic** workflow: the LLM agent proposes hypotheses, writes code, calls SageMath/Rust solvers/simulated annealing, and organizes the results into conjectures and proof drafts; humans handle strategic pivots; symbolic tools provide rigorous verification and search.
- The research initially tried to start from “perfect permutations/zero imbalance,” but algebraic reverse analysis failed; based on this, the human made a key pivot and reframed the problem as “what is the minimum positive imbalance?”
- The agent then discovered a hidden structure from numerical experiments: all row-pair distances are even. Put simply, the “theoretical optimum” here is not an integer, while the actual distances must be even, so each pair of rows must deviate more, which doubles the naive lower bound and ultimately yields the global lower bound.
- The authors further propose **near-perfect permutations**: making the shift-related values fall only on the two even numbers closest to optimal, thereby constructing cyclic Latin squares that attain this lower bound.
- The system also used parallel multi-model review and a two-layer persistent memory. The former was mainly used for error-finding, while the latter preserved project state, dead-end records, and knowledge files across multiple days and sessions without updating model parameters.

## Results
- Main mathematical result: for all $n\equiv 1\pmod{3}$ $n\times n$ Latin squares, the imbalance satisfies the lower bound $I(L)\ge 4n(n-1)/9$; the paper claims this bound is **tight** and resolves the open problem in this case.
- Key comparison: when $n=13$, the naive lower bound is only $n(n-1)/6=26$, but simulated annealing search found an optimum only around $69.3$, prompting the agent to discover the “parity constraint”; the final theoretical lower bound becomes $4n(n-1)/9=208/3\approx 69.3$, matching the search result.
- Small-scale exact verification: for $n=4$, after exhaustively enumerating all $576$ Latin squares, the minimum imbalance is exactly $16/3=4\cdot4\cdot3/9$, precisely matching the new lower bound.
- Constructive result: the authors define near-perfect permutations and report finding examples achieving the optimum for all $n\equiv 1\pmod{3}$ with $4\le n\le 52$. For example, when $n=10$ the optimal imbalance is $40$, for $n=22$ it is $616/3$, and for $n=52$ it is $3536/3$.
- Computational efficiency: the table reports search times for near-perfect permutations, ranging from under 1 second for small cases such as $n=4,7,10,13$, to 74 seconds for $n=40$, 139 seconds for $n=43$, and 32 seconds for $n=52$.
- Formal verification: the lower-bound theorem was formalized in Lean 4 + Mathlib, in about **340 lines** of Lean code.
- Methodological finding: parallel review by frontier LLMs is fairly reliable for **criticism and error detection**, successfully catching mistakes such as “incorrectly generalizing the cyclic case to the general case”; but it is unreliable for constructive mathematical claims—for example, one such model claimed the inverse map could achieve imbalance of $O(n^{5/2})$, whereas experiments instead showed about $\Theta(n^{3.6})$.

## Link
- [http://arxiv.org/abs/2603.08322v1](http://arxiv.org/abs/2603.08322v1)
