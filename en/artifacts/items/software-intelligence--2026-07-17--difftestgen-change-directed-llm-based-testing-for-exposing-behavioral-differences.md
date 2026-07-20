---
source: arxiv
url: https://arxiv.org/abs/2607.16024v1
published_at: '2026-07-17T14:57:59'
authors:
- Huimin Hu
- Cristian Cadar
- Michael Pradel
topics:
- code-intelligence
- automated-testing
- llm-test-generation
- differential-testing
- software-maintenance
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# DiffTestGen: Change-Directed LLM-Based Testing for Exposing Behavioral Differences

## Summary
DiffTestGen uses change-directed LLM test generation to expose behavioral differences between pre-change and post-change versions of Python projects. It combines static call-graph guidance, project documentation, iterative error correction, and union-coverage feedback.

## Problem
- Existing test generators often fail to exercise code modified by a pull request, especially when changed functions are private or difficult to reach through public APIs.
- This matters because undetected behavioral differences can cause regressions, compatibility problems, and reliability issues, while downstream regression detectors depend on tests that execute changed code.

## Approach
- Analyze each pull request’s AST and diff to identify changed functions, classify them as public, private, or special methods, and find publicly accessible entry points.
- Use static call-graph analysis, API documentation, signatures, docstrings, imports, and usage guidance to tell an LLM how to reach the changed code without directly calling private functions.
- Generate tests, repair syntax and runtime errors through feedback loops, and execute stable tests on isolated old and new program environments.
- Iteratively provide targeted coverage feedback using union coverage, which combines changed-line coverage in both program versions, until coverage reaches 100% or stops improving.

## Results
- On 463 pull requests from two datasets of open-source Python projects, DiffTestGen exposed behavioral differences in 78.2% of PRs and achieved 90.7% average union coverage.
- On the two datasets separately, it exposed differences in 61.8% and 79.7% of PRs, with average union coverage of 64.5% and 92.7%.
- Compared with the reported baselines, it exposed 99 more PRs and increased code coverage by 12.5 and 15.6 percentage points on the two datasets, respectively.
- Integration with the Testora regression detector showed that DiffTestGen’s behavioral differences can reveal regression bugs missed by the best existing approaches.

## Link
- [https://arxiv.org/abs/2607.16024v1](https://arxiv.org/abs/2607.16024v1)
