---
source: arxiv
url: http://arxiv.org/abs/2604.22028v1
published_at: '2026-04-23T19:43:53'
authors:
- Beatriz Souza
- Chang Lou
- Suman Nath
- Michael Pradel
topics:
- runtime-checking
- llm-for-code
- test-to-checker
- software-reliability
- silent-failure-detection
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# FlyCatcher: Neural Inference of Runtime Checkers from Tests

## Summary
FlyCatcher infers project-specific runtime checkers from existing tests so software can catch silent semantic failures during execution. It combines LLM-based checker synthesis with static analysis and validation, and adds a shadow-state mechanism for stateful properties.

## Problem
- Many software failures are silent: the program keeps running but violates intended behavior, which can corrupt data or produce wrong results.
- Writing semantic runtime checkers by hand is hard and uncommon, even though these checkers can catch failures that tests miss.
- Converting a concrete test into a checker is difficult because the checker must generalize test workloads, interpret constants correctly, and track evolving program state.

## Approach
- FlyCatcher takes a target test, related context tests, and validation tests, then infers a runtime checker from them.
- It uses CodeQL-based static analysis plus an LLM to identify state-changing methods that the checker should monitor.
- It prompts an LLM to generate checker code that updates a per-object **shadow state**, an abstract map of relevant properties such as tracked children or counts.
- The checker compares real runtime behavior against the shadow state to enforce the semantic property encoded by the original test under new workloads.
- Generated checkers go through a feedback loop with compile checks, structural checks, and dynamic validation on held-out tests; failures produce feedback for another synthesis attempt.

## Results
- Evaluation uses **400 tests** from **4** complex open-source Java systems.
- FlyCatcher infers **334** checkers, and **300** are judged correct through cross-validation.
- Compared with **T2C**, it produces **2.6x** more correct checkers.
- In mutation testing, FlyCatcher-generated checkers detect **5.2x** more mutants than T2C-generated checkers.
- Average checker generation cost is **15 seconds**, **183k LLM tokens**, and about **USD 0.60** per checker.
- Runtime overhead ranges from **2.7% to 40.3%**, depending on the target system.

## Link
- [http://arxiv.org/abs/2604.22028v1](http://arxiv.org/abs/2604.22028v1)
