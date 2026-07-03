---
source: arxiv
url: https://arxiv.org/abs/2607.02469v1
published_at: '2026-07-02T17:35:20'
authors:
- Jiale Amber Wang
- Kaiyuan Wang
- Pengyu Nie
topics:
- coding-agents
- code-intelligence
- software-testing
- test-generation
- test-update
- benchmarking
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# TestEvo-Bench: An Executable and Live Benchmark for Test and Code Co-Evolution

## Summary
TestEvo-Bench is an executable, timestamped benchmark for testing whether coding agents can update or add tests after real code changes. It covers 746 Java test-generation tasks and 509 test-update tasks mined from 152 open-source projects.

## Problem
- Existing test-generation benchmarks often use a fixed code snapshot, so they do not check whether an agent understands a new behavior introduced by a code change.
- Many test-update datasets rely on diffs or static dependency signals without enough build and runtime context to verify that a produced test compiles, runs, and targets the changed behavior.
- The problem matters because code agents need to maintain regression tests during software changes, and stale or missing tests hide behavior changes from developers.

## Approach
- The benchmark mines adjacent commits from Java Maven repositories, keeps pairs that build and pass tests, and records method-level code and test diffs.
- It uses runtime dependency tracing and cross-revision execution to tie each test to the changed production methods.
- Test generation asks an agent to add a test that passes on the new revision and fails on the old revision.
- Test update starts from the new code with old tests restored, then asks the agent to edit those tests so they pass and exercise the changed behavior.
- The runner reports success, pass and failure categories, focal-line coverage with JaCoCo, and mutation score with Universal Mutator.

## Results
- The dataset starts from 59,950 candidate co-evolution records and retains 13,868 classified records from 152 repositories.
- The released snapshot contains 746 test-generation tasks with 1,961 target methods and 509 test-update tasks with 1,138 target methods.
- On test generation, Claude Code + Claude Opus 4.7 and Gemini CLI + Gemini 3.1 Pro both reach 77.5% Success; their Redundant rate is 19.9%, and MutOnPass is 56.6% and 55.0%.
- On test update, Gemini CLI + Gemini 3.1 Pro reaches 74.6% Success, ahead of Claude Code + Claude Opus 4.7 at 74.4%; MutOnPass is 44.9% and 44.6%.
- SWE-Agent is lower on generation: 66.1% with Claude Opus 4.7 and 68.6% with Gemini 3.1 Pro; harness failures account for 14.1% and 10.1%.
- A full evaluation takes about 72 machine-hours across both tracks, and the paper reports lower success on newer tasks and under per-task cost caps, but the excerpt does not give those exact drops.

## Link
- [https://arxiv.org/abs/2607.02469v1](https://arxiv.org/abs/2607.02469v1)
