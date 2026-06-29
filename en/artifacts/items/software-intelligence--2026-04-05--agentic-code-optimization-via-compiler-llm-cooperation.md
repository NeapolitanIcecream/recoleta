---
source: arxiv
url: http://arxiv.org/abs/2604.04238v1
published_at: '2026-04-05T19:44:02'
authors:
- Benjamin Mikek
- Danylo Vashchilenko
- Bryan Lu
- Panpan Xu
topics:
- code-optimization
- compiler-llm
- multi-agent-systems
- llvm
- program-synthesis
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Agentic Code Optimization via Compiler-LLM Cooperation

## Summary
This paper proposes ACCLAIM, a multi-agent system that mixes standard compiler passes with LLM rewrites at source, IR, and assembly levels. The goal is to get LLM-discovered optimizations without giving up compiler reliability, and the reported evaluation shows up to **1.25×** mean speedup over **clang -O3**.

## Problem
- Compilers are reliable, but they can miss optimizations that need higher-level reasoning about what the program is doing.
- LLMs can find larger rewrites, but they often generate wrong code; the paper cites incorrect-code rates from **10% to 90%**, and one prior result reports **42%** incorrect rewrites for the best unaugmented model.
- This matters because even small runtime gains can matter at scale, and current LLM optimization methods usually work at only one abstraction level instead of across the full compiler pipeline.

## Approach
- The paper defines optimization as a search over **rewrites** and **lowerings** across multiple abstraction levels such as **C source**, **LLVM IR**, and **x86 assembly**.
- It builds **ACCLAIM**, a multi-agent system with a **guiding agent**, **level-specific optimization agents** for each abstraction level, and a **testing agent**.
- The guiding agent chooses when to call normal compiler components and when to call an LLM optimizer, then uses test feedback to keep, retry, or backtrack on candidate programs.
- The testing agent checks **correctness** as proportion of tests passed and measures **performance** as runtime improvement over the original program.
- The key idea is simple: let the LLM rewrite code where semantic reasoning helps, then let the compiler apply its normal verified passes before or after those rewrites.

## Results
- The main reported result is **mean speedup of 1.25× against clang -O3** on a standard set of **C programs**.
- The abstract states that compiler-LLM cooperation **outperforms both existing compiler optimizations and level-specific LLM baselines**, under equal compute budgets for the compared methods.
- The paper also says the method beats **naive multi-level baselines** with the same computation budget.
- In the motivating example, an LLM changes a population-count computation from **O(k log k)** to **O(log k)** at source level, or to **O(k)** at IR level by introducing **@llvm.ctpop.i32**.
- After that IR rewrite, LLVM vectorization places **8 repetitions** of the population-count call per loop iteration as **2 instructions with 4 operations each**, and the paper says this can cut runtime by **4×** on hardware with constant-time popcount support.
- The excerpt does not provide fuller benchmark tables, dataset sizes, variance, or per-baseline numbers beyond the **1.25×** headline result.

## Link
- [http://arxiv.org/abs/2604.04238v1](http://arxiv.org/abs/2604.04238v1)
