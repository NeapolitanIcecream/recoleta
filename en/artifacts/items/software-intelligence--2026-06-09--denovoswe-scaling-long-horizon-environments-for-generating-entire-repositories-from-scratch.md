---
source: arxiv
url: https://arxiv.org/abs/2606.10728v1
published_at: '2026-06-09T11:37:15'
authors:
- Jiale Zhao
- Guoxin Chen
- Fanzhe Meng
- Wayne Xin Zhao
- Ruihua Song
- Ji-Rong Wen
- Kai Jia
topics:
- software-agents
- code-generation
- repository-generation
- software-benchmarks
- multi-agent-systems
- training-data
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# DeNovoSWE: Scaling Long-Horizon Environments for Generating Entire Repositories from Scratch

## Summary
DeNovoSWE is a 4,818-instance training set for agents that generate complete software repositories from documentation. Fine-tuning Qwen3-30B-A3B on it raises BeyondSWE-Doc2Repo score from 5.8% to 47.2%.

## Problem
- Code-agent training data is mostly issue-fix data, so it gives little supervision for planning and building whole repositories.
- Whole-repository generation needs documentation that matches executable behavior, tests that can verify the result, and sandboxing that blocks access to the original code.
- This matters for automated software production because the task spans files, APIs, dependencies, and component interactions.

## Approach
- The pipeline selects real repositories with stable Docker environments, at least 90% original test pass rate, and more than 50% test coverage.
- It splits each repository into functional capabilities, maps tests and traced functions/classes to those capabilities, and documents direct plus behavior-critical indirect components.
- Draft, critic, and repair agents write and revise capability-level documentation inside a sandbox, then merge it into one document-to-repository task.
- Cleanup removes source code, tests, package caches, build artifacts, and Git history; runtime command rules and LLM trace audits block attempts to recover the reference implementation.
- Difficulty-aware filtering keeps training trajectories using per-instance thresholds based on executable line count, two LLM difficulty scores, and observed rollout pass rates.

## Results
- DeNovoSWE contains 4,818 document-to-repository instances, about 46× larger than NL2RepoBench's 104 tasks and much larger than BeyondSWE-Doc2Repo's 50 tasks.
- Fine-tuning Qwen3-30B-A3B on DeNovoSWE raises BeyondSWE-Doc2Repo performance from 5.8% to 47.2%, a +41.4 percentage-point gain.
- Dataset repositories average 205.0 unit tests, with median 79.0, P75 197.0, P90 464.0, and maximum 8,903.
- Average test coverage is 85.5%, with median 89.6%, P75 96.5%, P90 99.9%, and maximum 100%.
- Evaluation spans repository structure: measured source files average 19.3, with median 9.0, P75 21.0, P90 42.0, and maximum 1,995.

## Link
- [https://arxiv.org/abs/2606.10728v1](https://arxiv.org/abs/2606.10728v1)
