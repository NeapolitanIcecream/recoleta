---
source: arxiv
url: http://arxiv.org/abs/2604.01527v2
published_at: '2026-04-02T01:52:55'
authors:
- Smriti Jha
- Matteo Paltenghi
- Chandra Maddila
- Vijayaraghavan Murali
- Shubham Ugare
- Satish Chandra
topics:
- ai-coding-agents
- benchmarking
- software-engineering
- monorepo-evaluation
- code-intelligence
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents

## Summary
ProdCodeBench is a benchmark for AI coding agents built from real developer-assistant sessions in an industrial monorepo. Its main contribution is a curation method that keeps the original user prompts, backs out the landed code change, and uses stable execution tests as the grading signal.

## Problem
- Public coding-agent benchmarks often miss production conditions: they over-index on open-source repositories, structured issue text, and narrower language mixes.
- Companies need fast offline evaluations for model choice and harness changes, but monorepos make reproducible evaluation hard because old tooling, indexes, and services are hard to replay.
- Many real developer requests are not directly testable, and naive test selection in large repos can pick flaky or irrelevant tests, which corrupts pass/fail signals.

## Approach
- Build tasks from single-turn, real developer-agent conversations that led to a committed diff, preserving the verbatim prompt and linking it to the landed code change through AI provenance logging.
- Hide the ground-truth solution by backing out the landed diff from the current repository state, then evaluate agents on that backed-out version.
- Filter prompts to remove cases that leak the solution diff, template/system prompts, and prompts judged non-testable by an LLM classifier.
- Retrieve candidate tests for each diff, then run a test-relevance agent plus repeated pre-change/post-change executions to keep only stable relevant tests and classify them as fail-to-pass (F2P) or pass-to-pass (P2P).
- Keep the benchmark rolling rather than fixed so samples stay executable, current, and less prone to contamination in a changing monorepo.

## Results
- Across four foundation models on the F2P subset, solve rates range from **53.2% to 72.2%**; **Claude Opus 4.5** is the top model.
- About **75%** of benchmark tasks contain at least one F2P test; the other **25%** rely on P2P-only evaluation.
- The benchmark covers **7 programming languages**, reflecting a polyglot production codebase rather than a single-language setup.
- Each model evaluation is run **3 times**, and the paper reports **95% confidence intervals** for solve rates.
- In manual validation, the task-testability classifier matches human consensus in **96.67% (29/30)** of sampled cases.
- Test relevance validation uses two annotators with initial agreement above **80%**; the paper reports **2 false negatives** and **1 false positive** in a **15-pair** sample, and also states that a no-op agent gets **0.0%** solve rate.

## Link
- [http://arxiv.org/abs/2604.01527v2](http://arxiv.org/abs/2604.01527v2)
