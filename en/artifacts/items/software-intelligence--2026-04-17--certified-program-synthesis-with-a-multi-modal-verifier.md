---
source: arxiv
url: http://arxiv.org/abs/2604.16584v1
published_at: '2026-04-17T14:56:45'
authors:
- Yueyang Feng
- Dipesh Kafle
- Vladimir Gladshtein
- Vitaly Kurin
- "George P\xEErlea"
- Qiyuan Zhao
- "Peter M\xFCller"
- Ilya Sergey
topics:
- program-synthesis
- formal-verification
- lean-theorem-prover
- property-based-testing
- code-generation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Certified Program Synthesis with a Multi-Modal Verifier

## Summary
This paper introduces LeetProof, a certified program synthesis pipeline that uses one verifier for testing, automated proof, and interactive proof work inside Lean. The main claim is that this staged, multi-modal design finds bad specifications early and produces more fully certified programs than a Lean-only single-mode baseline under the same budget.

## Problem
- Certified program synthesis must generate code, a formal specification, and a machine-checkable proof from natural language, but generated specifications are often wrong: too weak to rule out bad programs or too strong to admit any valid one.
- Existing vericoding systems are tied to one verification style, such as SMT-heavy auto-active tools or interactive provers, which limits transfer across tasks and tools.
- The paper reports that about 10% of reference specifications in the VERINA and CLEVER benchmarks are defective, so weak specification checking can corrupt evaluation and training targets.

## Approach
- The system, LeetProof, is built on Velvet inside Lean. Velvet supports three modes in one setting: property-based testing, SMT-backed verification-condition discharge, and interactive Lean proof scripting.
- The pipeline runs in stages: generate a formal specification from the natural-language task, validate that specification with generated tests and randomized property-based testing, synthesize a Velvet program plus loop invariants, then prove the remaining verification conditions.
- For specification validation, it checks three things on test cases: the input satisfies the precondition, the expected output satisfies the postcondition, and alternative outputs do not also satisfy the postcondition. This catches under-specification such as using `result = true -> P` instead of `result = true <-> P`.
- For program and invariant synthesis, the LLM proposes code and invariants, then the verifier generates verification conditions, tries automated tactics, and uses property-based testing to find counterexamples to bad invariants or buggy code before proof effort is spent.
- Residual proof obligations that automation cannot solve are handed to AI-assisted Lean proving tools, with access to Mathlib search and auxiliary lemmas, and can be delegated to stronger external AI provers such as Aristotle.

## Results
- On specification inference, the paper claims **97.4% semantic accuracy on VERINA** for its property-based-testing-based specification generator.
- Randomized specification testing found defects in about **10%** of published reference specifications in **VERINA** and **CLEVER**.
- The authors introduce a new benchmark of **50 imperative-style LeetCode problems** with complexity annotations.
- The paper states that LeetProof achieves a **significantly higher rate of fully certified solutions** than a **single-mode Lean baseline at the same fixed budget**, and that this holds across **two frontier LLM backends**. The excerpt does not provide the exact certified-solution counts or percentages.
- In one worked example, automated tactics discharge **14 of 18** verification conditions, leaving **4** residual obligations for interactive or AI-assisted proof.
- The excerpt gives no full table of end-to-end benchmark numbers, so the strongest quantitative claims available here are the **97.4%** specification accuracy, the **~10%** benchmark defect rate, the **50-problem** benchmark size, and the **14/18 VC** automation result in the example.

## Link
- [http://arxiv.org/abs/2604.16584v1](http://arxiv.org/abs/2604.16584v1)
