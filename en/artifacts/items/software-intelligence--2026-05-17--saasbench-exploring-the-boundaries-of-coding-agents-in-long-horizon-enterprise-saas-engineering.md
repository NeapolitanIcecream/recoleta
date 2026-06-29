---
source: arxiv
url: https://arxiv.org/abs/2605.17526v1
published_at: '2026-05-17T16:15:56'
authors:
- Qingnan Ren
- Shun Zou
- Shiting Huang
- Ziao Zhang
- Kou Shi
- Zhen Fang
- Yiming Zhao
- Yu Zeng
- Qisheng Su
- Lin Chen
- Yong Wang
- Zehui Chen
- Xiangxiang Chu
- Feng Zhao
topics:
- coding-agents
- software-engineering-benchmark
- saas-development
- full-stack-generation
- agent-evaluation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# SaaSBench: Exploring the Boundaries of Coding Agents in Long-Horizon Enterprise SaaS Engineering

## Summary
SaaSBench tests whether coding agents can build deployable enterprise SaaS systems from long product requirements. The paper finds that current agents fail often on setup, configuration, and cross-component integration, with the best reported Pass@1 at 20.68%.

## Problem
- Existing coding benchmarks focus on snippets, repository edits, or simple project generation, so they miss the complexity of enterprise SaaS work.
- Real SaaS products require frontend, backend, database, authentication, deployment, and business workflows to work together; failures in one layer can block the rest.
- Flat unit-test or end-to-end scoring can over-penalize downstream failures and can miss which engineering capability failed.

## Approach
- SaaSBench contains 30 tasks across 6 SaaS domains, built from real open-source SaaS repositories and market-grounded product categories.
- Each task includes a long PRD, an ambiguity-resolution knowledge base, a standardized Docker runtime, and a DAG-based test suite.
- The benchmark has 4,362.7 PRD lines on average, 5,370 executable validation nodes, 6,167 prerequisite edges, 8 programming languages, 6 database types, and 13 frontend/backend frameworks.
- Evaluation runs validation nodes in dependency order and labels blocked checks as skipped dependency rather than direct failures.
- Scoring uses binary checks, weighted partial-credit checks, and LLM-as-judge checks for cases such as page layout quality.

## Results
- The best overall result is Claude Code with Claude Opus 4.7: 20.68% Pass@1 and 18.50% node coverage on SaaSBench.
- The best OpenHands result is Claude Opus 4.7: 18.12% Pass@1 and 18.24% node coverage.
- Across agent backends, Claude Code averages 11.64% Pass@1, while OpenHands averages 9.26% Pass@1.
- Under Claude Code, the next strongest results after Claude Opus 4.7 are GLM 5.1 at 13.60% Pass@1 and DeepSeek V4 Pro at 13.19% Pass@1.
- Under OpenHands, the next strongest results after Claude Opus 4.7 are DeepSeek V4 Pro at 10.97% Pass@1 and GLM 5.1 at 10.23% Pass@1.
- The paper reports that over 95% of task failures occur before agents reach deep business logic, mainly during system setup, integration, premature stopping, or repeated debugging loops.

## Link
- [https://arxiv.org/abs/2605.17526v1](https://arxiv.org/abs/2605.17526v1)
