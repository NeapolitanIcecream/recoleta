---
source: arxiv
url: http://arxiv.org/abs/2604.03035v1
published_at: '2026-04-03T13:44:40'
authors:
- KN Ajay Shastry
- Ganesh Senrayan
- Shrey Satapara
- Pranoy Panda
- Chaitanya Devaguptapu
topics:
- coding-agents
- benchmarking
- software-evolution
- repository-level-evaluation
- multi-step-reasoning
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution

## Summary
This paper introduces SWE-STEPS, a dataset and evaluation framework for coding agents that work through dependent pull-request sequences instead of isolated tasks. The main claim is that standard single-PR benchmarks overstate agent ability and miss damage to long-term code quality.

## Problem
- Existing coding-agent benchmarks evaluate one pull request at a time on a clean repository state, which does not match real software development where changes accumulate.
- That setup misses spillover effects from earlier agent-written code, including regressions, growing test obligations, technical debt, and higher code complexity.
- This matters because an agent that passes isolated tasks can still fail across a multi-step development sequence and leave the repository harder to maintain.

## Approach
- The authors build an automated framework that mines git history to extract chains of related PRs, their metadata, changed symbols, and associated tests.
- They create **SWE-STEPS**, a dataset with **168 tasks** and **963 PRs** across **6 Python repositories**, with task chains of **3 to 11 PRs**.
- Each task includes an initial repo state, an ordered sequence of PR requests, and verification suites split into **FAIL_TO_PASS** tests for new functionality and **PASS_TO_PASS** tests for regression checks.
- They evaluate agents in three settings: **Individual PR** (isolated, SWE-bench-style reset), **Global Memory / conversational coding** (state persists across PRs), and **PRD-based coding** (all requirements given up front, final accumulated test suite checked at the end).
- Evaluation covers both functional success and repository health, using static analysis metrics such as **cognitive complexity** and **technical debt** compared with the human-written ground truth.

## Results
- **Dataset scale:** **168 tasks**, **963 PRs**, **6 repositories**; chains have **3 to 11 PRs**.
- **Task complexity:** average issue text length is **3,656 words** versus **195.1** for SWE-Bench and **239.8** for SWE-Gym; average edited files are **17.1** versus **1.7** and **2.5**.
- **Performance inflation:** isolated PR evaluation overstates success by up to **20 percentage points**. Example from the Mini split: **Claude Sonnet 4.5** drops from **66.25%** in the Individual setting to **43.75%** in a continuous setting.
- On the Lite split, **Gemini 3 Flash** drops from **56.52%** in the Individual setting to **36.59%** in the Global setting.
- Across tested LLMs, introducing stateful multi-step evaluation reduces performance by about **15% to 25%** relative to isolated evaluation.
- The paper also claims agents worsen repository health versus human developers by producing code with higher **cognitive complexity** and more **technical debt**, measured with **SonarQube**, but the excerpt does not provide exact numeric deltas for those metrics.

## Link
- [http://arxiv.org/abs/2604.03035v1](http://arxiv.org/abs/2604.03035v1)
