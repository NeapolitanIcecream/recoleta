---
source: arxiv
url: https://arxiv.org/abs/2605.22175v1
published_at: '2026-05-21T08:45:50'
authors:
- Yuxuan Sun
- Yuze Zhao
- Yufeng Wang
- Yao Du
- Zhiyuan Ma
- Jinbo Wang
- Mengdi Zhang
- Kai Zhang
- Zhenya Huang
topics:
- test-generation
- mutation-testing
- software-engineering-agents
- code-intelligence
- benchmarking
- llm-evaluation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# SWE-Mutation: Can LLMs Generate Reliable Test Suites in Software Engineering?

## Summary
SWE-Mutation is a benchmark for testing whether LLMs can write test suites that catch realistic software bugs. It uses agent-generated mutants of SWE-bench issues and shows that current models often create tests that run but miss the target bug or miss subtle faulty variants.

## Problem
- LLM software agents need high-quality test suites for issue verification, repair trajectory generation, and reinforcement learning feedback.
- Existing generated tests are often shallow, and common mutation methods can create easy bugs that overrate test quality.
- Repository-level and multilingual test-suite evaluation is still limited, especially for defects that require project context.

## Approach
- The benchmark has two tasks: test generation from scratch and test repair of an incomplete or weak test suite.
- Each instance pairs a real repository issue with 3-5 mutants derived from the golden fix; good tests should fail on the original bug, pass on the golden fix, and kill mutants.
- The mutant generator uses four steps: locate changed files and failure traces, inject semantically plausible bugs, check syntax and failure against Fail-to-Pass tests, then select mutants that survive model-generated tests.
- The dataset contains 2,636 mutants from 800 instances: 1,664 mutants across 500 SWE-bench Verified Python instances and 972 mutants across 300 multilingual instances in 9 languages.
- Evaluation uses Pass@1 for valid test patches, VRR for tests that reproduce the issue and pass on the fix, and RDR for the share of surviving mutants detected by generated tests.

## Results
- On Python test repair with Claude Code, Claude Sonnet 4.5 reached 99.80% Pass@1, 59.20% VRR, and 81.15% RDR, the best reported result in Table 2.
- On Python test generation with Claude Code, Claude Sonnet 4.5 reached 98.00% Pass@1, 40.40% VRR, and 71.71% RDR; with Mini-Swe-Agent it reached 96.20%, 29.80%, and 63.70%.
- DeepSeek-V3.1 on Python test generation with Mini-Swe-Agent reached 88.20% Pass@1, 10.20% VRR, and 36.15% RDR. This is a large gap between executable tests and useful tests.
- Agent-generated mutants made the benchmark harder than conventional mutants: average RDR dropped from 71.04% to 39.81%.
- On the 9-language test repair subset with Mini-Swe-Agent, Claude Sonnet 4.5 averaged 91.33% Pass@1, 33.33% VRR, and 58.33% RDR; DeepSeek-V3.1 averaged 86.00%, 20.33%, and 36.67%.
- Replacing the Claude Sonnet 4 mutant generator with DeepSeek-V3.1 or Qwen3-Coder changed RDR by within 1.5 percentage points, with evaluator rank correlations of 0.96 and 0.93.

## Link
- [https://arxiv.org/abs/2605.22175v1](https://arxiv.org/abs/2605.22175v1)
