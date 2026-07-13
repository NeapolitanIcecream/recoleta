---
source: arxiv
url: https://arxiv.org/abs/2607.09072v1
published_at: '2026-07-10T03:33:47'
authors:
- Seongmin Lee
- Yaoxuan Wu
- Miryung Kim
topics:
- property-based-testing
- formal-verification
- agentic-software-engineering
- spark-testing
- code-generation-validation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Agentic Proof and Property-Based Testing via Property-Templates in Data-Intensive Computing

## Summary
DualVeri uses reusable property templates to help agents prove and test recurring correctness properties in Apache Spark. It combines Lean 4 proofs over a Spark model with property-based tests against PySpark, reducing synthesis errors and cost across 400 candidate properties.

## Problem
- AI-generated code increases the supply of candidate properties, but validating whether each property is correct and whether its test checks the intended behavior remains expensive.
- Data-intensive systems contain large families of similar properties, yet shared structure does not guarantee truth; the study cites 37,971 type-consistent aggregation candidates, including false claims such as global mean equaling the mean of partition means.
- Formal proof covers a model and all modeled inputs, while property-based testing exercises the real implementation. Using only one can miss model gaps or implementation failures.

## Approach
- DualVeri expresses four Spark property families as parameterized templates with typed holes: aggregation decomposition, UDF rewrite, higher-order expression rewrite, and operator subsumption.
- A proof template pre-proves the reusable lift from a local law to a pipeline-level theorem. The agent fills the property-specific holes and proves only the local law in Lean 4.
- A PBT template generates typed data, surrounding Spark workloads, and executable checks against PySpark. The agent fills the same property-specific holes instead of writing each test architecture from scratch.
- The study evaluates 100 candidate properties per family, or 400 total, and compares template-guided synthesis with template-free proof and PBT synthesis.
- Proof and testing results are cross-checked: a passing test with no proof suggests missing formal modeling, while a counterexample to a proved property exposes a model-to-runtime mismatch.

## Results
- Property templates increased successful agentic proof synthesis by up to 2.6x, with a 1.6x average improvement, and reduced proof hallucinations by 59% at lower cost.
- Template-guided PBT reduced intent misalignments from 22 to 1 and lowered synthesis cost by up to 5.7x, with a 3.8x average reduction.
- The four templates produced 136 successfully synthesized proofs and 387 faithful property-based tests.
- Template-guided PBT exceeded a state-of-the-art Spark fuzzer on code coverage and approached unguided LLM-based PBT.
- The two tracks produced both a proof and a passing test for 130 properties, while disagreements identified gaps between the Lean model and PySpark runtime semantics.

## Link
- [https://arxiv.org/abs/2607.09072v1](https://arxiv.org/abs/2607.09072v1)
