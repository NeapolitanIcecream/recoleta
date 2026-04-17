---
source: arxiv
url: http://arxiv.org/abs/2604.10761v1
published_at: '2026-04-12T18:09:53'
authors:
- "Agust\xEDn Balestra"
- "Agust\xEDn Nolasco"
- Facundo Molina
- Diego Garbervetsky
- Renzo Degiovanni
- Nazareno Aguirre
topics:
- dynamic-specification-inference
- llm-based-testing
- counterexample-generation
- code-intelligence
- program-analysis
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Improving Dynamic Specification Inference with LLM-Generated Counterexamples

## Summary
This paper adds an LLM-based counterexample step to dynamic specification inference so invalid inferred assertions can be removed with executable tests. On 43 Java methods, the method improves precision over SpecFuzzer while keeping recall unchanged.

## Problem
- Dynamic specification inference tools such as Daikon and SpecFuzzer infer likely preconditions, postconditions, and invariants from execution traces, but their output depends on test-suite coverage.
- Weak or incomplete test suites let many false positives survive: assertions that match observed runs but are invalid in general.
- These invalid assertions matter because they add manual review work and can hurt downstream uses such as verification, test generation, debugging, and repair.

## Approach
- The pipeline starts with SpecFuzzer, which generates candidate postconditions and filters them against an existing test suite.
- For each inferred postcondition, an LLM gets the full class code, the target method, and the candidate assertion, then judges whether the assertion is valid.
- If the LLM judges the assertion invalid, it must generate an executable JUnit test that acts as a counterexample. The test is compiled, with up to three repair attempts if needed.
- All compiling counterexample tests are added to the original test suite, and SpecFuzzer is run again on this augmented suite to remove assertions falsified by the new tests.
- The evaluation uses 43 Java methods from GAssert and EvoSpex-related benchmarks, plus automated SAT/SMT-based ground-truth checkers. The tested models are GPT-5.1, Llama 3.3 70B, and DeepSeek-R1.

## Results
- GPT-5.1-generated counterexamples discard 1,877 invalid specifications inferred by SpecFuzzer, reducing noise by 10.09%.
- Llama 3.3 70B discards 1,048 invalid assertions, reducing noise by 5.63%.
- DeepSeek-R1 discards 2,173 invalid assertions, reducing noise by 11.68%, the best invalid-assertion reduction reported in the excerpt.
- SpecFuzzer+GPT-5.1 reaches 74.17% precision, 54.57% recall, and 53.94% F1 against benchmark ground truth, with about 7% precision improvement over SpecFuzzer and no recall loss.
- Llama 3.3 70B improves SpecFuzzer precision by about 3.5%.
- DeepSeek-R1 improves SpecFuzzer precision by about 8%, also without affecting recall according to the abstract.

## Link
- [http://arxiv.org/abs/2604.10761v1](http://arxiv.org/abs/2604.10761v1)
