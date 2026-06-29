---
source: arxiv
url: https://arxiv.org/abs/2605.27051v1
published_at: '2026-05-26T14:04:40'
authors:
- Muhammad A. A. Pirzada
- Weiqi Wang
- Yiannis Charalambous
- Konstantin Korovin
- Lucas C. Cordeiro
topics:
- formal-verification
- code-intelligence
- llm-contract-synthesis
- bounded-model-checking
- program-analysis
- software-engineering-agents
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# ConVer: Using Contracts and Loop Invariant Synthesis for Scalable Formal Software Verification

## Summary
ConVer uses LLM-written C function contracts and loop invariants to make ESBMC verification scale past whole-program bounded model checking. It claims that top-down contract synthesis plus counterexample-guided refinement verifies many C benchmark programs with little manual annotation.

## Problem
- Bounded model checkers such as ESBMC and CBMC must unroll loops and inline call chains, so nested functions and loops can make SMT queries too large.
- Manual function contracts reduce this cost, but they need verification engineers and are hard to apply across many C programs.
- The paper targets programs with a top-level assertion where only the function behavior needed for that assertion has to be specified.

## Approach
- ConVer extracts the top-level assertion and non-main functions, then asks an LLM to derive ESBMC preconditions, postconditions, and assigns clauses for each function.
- At the system level, ESBMC checks the top assertion after replacing function calls with contract stubs. At the function level, ESBMC checks each function body against its own contract.
- When a check fails, SMART ICE parses ESBMC counterexamples into positive, negative, and implication examples. ConVer refines contracts with CEGAR, then uses CEGIS after up to 5 CEGAR iterations.
- For hard functions, pre-abstraction scores static complexity, creates loose over-approximate contracts, and later replaces them with verified precise contracts when possible.
- For loops, ConVer synthesizes ESBMC loop invariants when bounded unrolling is insufficient. ESBMC makes the pass/fail decision, not the LLM.

## Results
- Frama-C suite: 45 C programs; ConVer reports 82-96% verification success across three LLM backends. Among converged programs, 93-95% needed only 1 CEGAR-CEGIS iteration.
- LF2C-Simple suite: 17 programs; ConVer reports 82-88% success.
- X.509 parser benchmark: 6 programs; ConVer reports 33-50% success.
- VerifyThis suite: 11 recursive and loop-intensive programs; the Pre-Abstraction strategy reports 55-64% success.
- LF-Hard suite: 24 Lingua Franca benchmarks converted to C with ESBMC-LF; ConVer reports 67% success overall.
- Baseline comparison: the excerpt says ConVer is evaluated against SOTA tools, but it gives 0 exact SOTA success rates, runtimes, or numeric margins in the provided text.

## Link
- [https://arxiv.org/abs/2605.27051v1](https://arxiv.org/abs/2605.27051v1)
