---
source: arxiv
url: https://arxiv.org/abs/2606.05001v1
published_at: '2026-06-03T15:19:40'
authors:
- Pranshav Gajjar
- Ali Mamaghani
- Dinesh Bharadia
- Vijay K Shah
topics:
- code-intelligence
- software-engineering-agents
- telecom-software
- benchmarking
- llm-as-judge
- srsran
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# TeleSWEBench: A Commit-Driven Benchmark for Evaluating LLM-Powered Software Engineering in Telecommunications

## Summary
TeleSWEBench is a 734-task benchmark for testing LLM software-engineering agents on real srsRAN 5G commits. It shows current agents still struggle with telecom code: the strongest tools produce up to 25% ship-ready changes.

## Problem
- Telecom networks now depend on large C++ wireless stacks; code changes can affect 5G protocol behavior, timing, and state machines.
- General coding benchmarks such as SWE-bench, HumanEval, and MBPP do not test repository-scale 3GPP logic in systems like srsRAN 5G.
- Existing telecom LLM evaluations focus on question answering or code understanding, leaving no direct test for multi-file code generation in telecom repositories.

## Approach
- The benchmark mines real developer commits from the srsRAN 5G repository across 2023-2025, starting from more than 15,000 commits.
- It keeps commits with repository-native tests and turns them into 734 coding tasks: 142 Easy, 279 Medium, and 313 Difficult.
- Difficulty controls how much location detail the prompt gives: Easy includes exact files and edits, Medium gives affected areas and facts, and Difficult gives only a high-level goal.
- The evaluation has two stages: file localization first, then functional correctness only for exact-file-match patches.
- The paper also proposes TeleJudge, a hierarchical LLM judge that scores file-level diffs and combines them into a patch verdict alongside executable unit tests.

## Results
- TeleSWEBench contains 734 questions with executable tests, built from srsRAN 5G commits; task scope ranges from 1 to 300 files.
- In Stage 1 localization, QwenCoder-2.5 has the best Easy exact-match rate at 37.8%, while Qwen3 has the best cumulative exact-match rate at 14.0% among the listed models.
- Localization drops on harder tasks: QwenCoder-2.5 falls from 37.8% exact match on Easy to 5.3% on Difficult.
- Many larger models often make no code changes: GLM-4.7 has a 92.2% cumulative No Changes rate, and Gemma4 has 86.8%.
- The abstract reports that the strongest evaluated ASE tools reach up to 25% ship-ready changes.
- The evaluated model set includes Qwen3.5 at 397B parameters with a 1M-token context, Kimi K2.5 at 1T parameters with a 262K-token context, GPT-OSS at 120B, Gemma 4 at 31B, and QwenCoder 2.5 at 1.5B.

## Link
- [https://arxiv.org/abs/2606.05001v1](https://arxiv.org/abs/2606.05001v1)
