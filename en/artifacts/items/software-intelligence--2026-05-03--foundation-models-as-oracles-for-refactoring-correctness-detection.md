---
source: arxiv
url: https://arxiv.org/abs/2605.02096v1
published_at: '2026-05-03T23:31:18'
authors:
- Rohit Gheyi
- Rian Melo
- Jonhnanthan Oliveira
- Marcio Ribeiro
- Baldoino Fonseca
topics:
- code-intelligence
- software-foundation-models
- refactoring
- program-analysis
- llm-evaluation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Foundation Models as Oracles for Refactoring Correctness Detection

## Summary
The paper tests whether foundation models can flag faulty Java refactorings without task-specific training. It reports high zero-shot accuracy on real IDE bug reports, with proprietary models ahead of open models.

## Problem
- Automated refactoring in IntelliJ IDEA, Eclipse, and NetBeans can introduce compilation errors or behavior changes while appearing to be a safe code transformation.
- Traditional checks depend on handcrafted preconditions, static analysis, dynamic analysis, or tests; these checks are costly to maintain and can miss Java corner cases.
- The problem matters because developers use refactoring tools often, and missed correctness bugs reduce trust in automated software maintenance.

## Approach
- The authors build an evaluation set of 226 real Java refactoring bugs from IDE reports spanning 2005 to 2024.
- The dataset contains 185 compilation-error cases and 41 behavior-change cases across 47 refactoring types.
- Each instance includes the original Java program and the faulty refactored program; compilation-error labels are checked with OpenJDK Temurin 21.0.7+6.
- Behavior-change cases are validated with one JUnit test each, where the test passes on the original program and fails on the refactored program.
- Models receive zero-shot prompts asking whether the refactoring preserves correctness; the study also uses metamorphic testing to check whether predictions stay stable under semantics-preserving code changes.

## Results
- On 226 bugs, GPT-OSS-20B reaches 80.5% first-run accuracy.
- GPT-5.4 reaches 93.8% first-run accuracy on the same task.
- The benchmark covers 47 refactoring types; the largest groups include Move Method with 32 cases, Inline Method with 20, Pull Up Method with 18, Extract Local Variable with 15, and Rename Method with 14.
- Gemma-4-31B has the strongest reported result among open models, but the excerpt does not provide its exact accuracy.
- Gemini-3.1-Pro-Preview has the best reported result overall, but the excerpt does not provide its exact accuracy.
- Metamorphic testing finds that predictions are mostly consistent under intended semantics-preserving code variations, which supports the claim that the models are doing more than exact input matching.

## Link
- [https://arxiv.org/abs/2605.02096v1](https://arxiv.org/abs/2605.02096v1)
