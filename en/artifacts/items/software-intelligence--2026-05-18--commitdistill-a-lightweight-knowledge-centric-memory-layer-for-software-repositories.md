---
source: arxiv
url: https://arxiv.org/abs/2605.18284v1
published_at: '2026-05-18T12:14:28'
authors:
- Divya Chukkapalli
- Thejesh Avula
- Aditya Aggarwal
- Harsimran Singh
- Amith Tallanki
topics:
- code-intelligence
- repository-memory
- software-agents
- retrieval-augmented-generation
- developer-tools
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# CommitDistill: A Lightweight Knowledge-Centric Memory Layer for Software Repositories

## Summary
CommitDistill turns git commit history into a local, typed memory store for developers and coding agents. Its strongest result is better short-context fact retrieval than BM25 and `git log --grep`, while downstream LLM bug-fix localization shows no measured gain over no retrieval.

## Problem
- Software projects store useful engineering knowledge in commit messages, pull requests, and issues, but developers and coding assistants often miss it during later work.
- Raw repository retrieval can waste context on long diffs or noisy prose, and external embedding services can be unsuitable for regulated or private codebases.
- The paper targets a narrow use case: find prior constraints, fixes, and failure patterns from local git history at decision time.

## Approach
- CommitDistill extracts three unit types from commit messages: Facts for constraints, Skills for fixes or actions, and Patterns for recurring failures.
- Extraction uses deterministic regex heuristics, text cleanup, length filters, deduplication by content hash, and commit provenance metadata.
- Retrieval uses length-normalized TF-IDF over the extracted units, with type boosts for Patterns and Skills and a prior-weight multiplier.
- A minimum score threshold, calibrated at θ=2.5, makes the tool return no result when the query is weak or out of scope.
- The prototype runs locally in pure Python, has no third-party dependencies, and stores units as plain JSON in `.knowledge/units.json`.

## Results
- On five public repositories, `psf/requests`, `pallets/flask`, `expressjs/express`, `redis/redis`, and `junit-team/junit5`, the case study covers 25,000 commits and extracts 1,167 typed units.
- Human annotation on 40 Python units reports useful precision of 0.525 with Cohen’s κ = 0.633.
- Under a 256-character per-query budget on a 12-query fact benchmark, CommitDistill reaches 0.750 hit rate, compared with BM25 at 0.333 and `git log --grep` at 0.083.
- The current retriever reports 31/36 hits on the broader query comparison, and all 36 evaluation queries return in under 50 ms end to end.
- Warm-cache extraction across 25,000 commits takes 3.47 seconds on the reported laptop setup; extraction over 10,000 commits completes in under 4 seconds.
- In a paired LLM-as-judge evaluation with n=200 time-travel bug-fix tasks and two judges, no retrieval condition gives a statistically detectable mean lift over the no-retrieval control, and CD-Hybrid is indistinguishable from BM25 head to head.

## Link
- [https://arxiv.org/abs/2605.18284v1](https://arxiv.org/abs/2605.18284v1)
