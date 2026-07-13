---
source: arxiv
url: https://arxiv.org/abs/2607.08983v1
published_at: '2026-07-09T23:13:46'
authors:
- Sijia Gu
- Noor Nashid
- Ali Mesbah
topics:
- coding-agents
- automated-test-generation
- code-coverage
- contextual-bandits
- program-analysis
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# SCATE: Learning to Supervise Coding Agents for Cost-Effective Test Generation

## Summary
Scate automatically supervises coding agents during unit-test generation so they spend effort on difficult coverage gaps instead of stopping early. It uses a contextual bandit to choose ordinary generation, program analysis, or termination based on class complexity, current coverage, and generation cost.

## Problem
- Coding agents often stop after covering simple paths, leaving complex branches untested; the paper reports a Gemini CLI example with about 42% line coverage and 31% branch coverage.
- Human supervision is currently needed to decide when to retry, add analysis, or stop, which increases labor and can waste API tokens.
- Better automated supervision matters because test coverage affects defect detection and the cost of maintaining generated tests.

## Approach
- Scate builds a seven-feature context from LOC, weighted methods per class, response for a class, line coverage, branch coverage, and missed complexity, plus an intercept.
- A persistent LinUCB contextual bandit selects one of three actions: Default generation, Analysis with the Scate MCP program-analysis tool, or Stop.
- The reward combines relative line and branch coverage gains, progress on complex uncovered code, token cost, and a penalty for actions that produce no coverage gain.
- The MCP tool extracts uncovered control-flow paths and external calls, then gives the agent up to 10 under-covered methods with prioritized paths and dependency information.

## Results
- On a Defects4J-based dataset, Scate with Gemini CLI improved line coverage by 32.3% and branch coverage by 30.9% over the unsupervised agent-only baseline.
- With Claude Code, Scate improved line coverage by 6.0% and branch coverage by 5.9% over the corresponding unsupervised baseline.
- The framework reportedly outperformed state-of-the-art non-agentic test-generation methods on all evaluation metrics.
- The excerpt provides relative coverage improvements but does not give absolute final coverage, token savings, dataset size, or statistical significance values.

## Link
- [https://arxiv.org/abs/2607.08983v1](https://arxiv.org/abs/2607.08983v1)
