---
source: arxiv
url: http://arxiv.org/abs/2604.01442v1
published_at: '2026-04-01T22:28:52'
authors:
- Vasudev Vikram
- Rohan Padhye
topics:
- fuzzing
- llm-agents
- test-generation
- coverage-guided-fuzzing
- program-analysis
- java
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Fuzzing with Agents? Generators Are All You Need

## Summary
Gentoo uses an LLM coding agent to write target-specific fuzz input generators from source code and optional predicate-level feedback. Across 7 Java benchmarks, the paper claims these agent-written generators often beat human-written generators on branch coverage and make coverage-guided mutation mostly unnecessary.

## Problem
- Fuzzers for structured inputs often fail because random or lightly mutated inputs do not satisfy the syntax and semantic constraints needed to reach deep program logic.
- Hand-written domain-specific generators can solve this, but they take substantial manual effort and are tightly tied to one target.
- The paper asks whether an AI coding agent can automatically write such strong generators, reducing or removing the need for coverage guidance and mutation.

## Approach
- Gentoo gives an LLM coding agent terminal access, the fuzz target, and the library source code, then asks it to iteratively write and refine a JQF input generator.
- Gentoo-S adds static predicate ranking: it builds an interprocedural control-flow graph, computes branch dominance scores with WALA, and tells the agent which branch outcomes gate the most code.
- Gentoo-L replaces the static analysis with agent-produced predicate ranking from source inspection. Gentoo-Base uses no predicate guidance.
- During fuzzing, Gentoo-S and Gentoo-L collect per-predicate branch counts, so the agent can see which high-value branches are rarely taken and add generation logic for those conditions.
- The core idea is simple: inspect the program, infer what input structure and semantics unlock hard branches, then encode those rules directly in the generator instead of relying on mutation to discover them.

## Results
- Evaluation covers **7 real-world Java libraries** and compares **3 Gentoo variants** against **human-written generators**.
- Agent-synthesized generators achieve higher branch coverage than human-written generators on **6 of 7 benchmarks**, with **4 of 7** showing a **statistically significant** gain.
- The reported average coverage improvement over human-written generators is **11% to 21%**, depending on configuration.
- For agent-synthesized generators, running with coverage-guided mutation instead of random generation gives only **under 3%** improvement in typical cases, and the paper says these differences are **not statistically significant**.
- For human-written generators, coverage guidance is reported as **statistically significant** on all benchmarks, which supports the claim that Gentoo generators already encode enough structure and semantics that mutation adds little.
- Predicate-guided refinement improves coverage over each method's first iteration by **18% to 57% on average** for **Gentoo-S** and **Gentoo-L** respectively, though final coverage across Gentoo-Base, Gentoo-S, and Gentoo-L is described as broadly similar.

## Link
- [http://arxiv.org/abs/2604.01442v1](http://arxiv.org/abs/2604.01442v1)
