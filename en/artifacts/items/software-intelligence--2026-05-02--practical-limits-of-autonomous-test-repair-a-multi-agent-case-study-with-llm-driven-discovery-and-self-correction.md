---
source: arxiv
url: https://arxiv.org/abs/2605.01471v1
published_at: '2026-05-02T14:39:55'
authors:
- Hyukjoo Lee
topics:
- autonomous-testing
- test-repair
- llm-agents
- ui-testing
- multi-agent-systems
- software-engineering
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Practical Limits of Autonomous Test Repair: A Multi-Agent Case Study with LLM-Driven Discovery and Self-Correction

## Summary
The paper finds that a multi-agent LLM system can discover and repair some enterprise UI tests, but its autonomous repair loop often produces non-executable output, weak assertions, or reduced test scope.

## Problem
- Large enterprise UI test suites break when screens, selectors, navigation paths, and async loading behavior change.
- Manual repair does not scale, and locator-only repair misses semantic drift and new test targets.
- The study matters because a passing autonomous test run can hide lost coverage or weaker checks.

## Approach
- The system uses five agents: Explorer, Planner, Coder, Executor, and Self-Correction.
- Explorer uses RAG over anonymized feature docs and runtime DOM snapshots to find testable UI features.
- Planner turns each feature into a test scenario; Coder writes Playwright TypeScript; Executor runs it and records logs, status, timing, and DOM error context.
- Self-Correction revises failing tests using DOM parsers, selector verifiers, authentication checks, failure-artifact analysis, and a RAG-backed store of past failures.
- The improved workflow adds bounded retries, skip-list filtering, similarity-based deduplication, and RAG-grounded selector feedback.

## Results
- Feature discovery found 119 testable features across 10 screens from documentation, then added 15–30 runtime DOM-discovered features per run, for about 140 effective features.
- Multi-round RAG used 34 LLM calls for full feature discovery versus 11 calls for a hardcoded-query baseline, about 3x more calls.
- The evaluation covered 300 consecutive execution reports over 126 days, with 636 individual test-case executions.
- Only 187 of 300 reports produced executable test files, while 113 reports, or 37.7%, produced no test artifact.
- Across test-case executions, 204 passed, or 32.1%, and 432 failed, or 67.9%; 42 reports, or 14%, reached COMPLETED status.
- At the scenario-family level, 7 of 10 families converged, or 70%; first-pass success was 1 of 10, or 10%; the table reports a mean of 3.4 repair iterations to convergence, with a maximum observed retry depth of 16. The study also reports failure signatures in 300 reports: method or contract mismatch in 132, navigation or environment timeout in 120, selector or readiness failure in 96, assertion mismatch in 78, non-executable output in 113, visibility assertion failure in 72, closed browser or context in 48, and hallucinated API or selector in 36.

## Link
- [https://arxiv.org/abs/2605.01471v1](https://arxiv.org/abs/2605.01471v1)
