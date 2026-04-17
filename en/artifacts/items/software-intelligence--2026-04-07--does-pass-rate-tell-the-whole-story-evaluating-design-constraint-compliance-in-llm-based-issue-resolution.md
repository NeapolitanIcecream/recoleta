---
source: arxiv
url: http://arxiv.org/abs/2604.05955v1
published_at: '2026-04-07T14:47:27'
authors:
- Kai Yu
- Zhenhao Zhou
- Junhao Zeng
- Ying Wang
- Xueying Du
- Zhiqiang Yuan
- Junwei Liu
- Ziyu Zhou
- Yujia Wang
- Chong Wang
- Xin Peng
topics:
- llm-agents
- issue-resolution
- benchmarking
- design-constraints
- code-review-mining
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Does Pass Rate Tell the Whole Story? Evaluating Design Constraint Compliance in LLM-based Issue Resolution

## Summary
This paper argues that test pass rate misses a large part of patch quality in LLM-based issue resolution. It introduces SWE-Shield, a benchmark that measures whether generated patches follow project-specific design constraints mined from real pull requests.

## Problem
- Existing issue-resolution benchmarks mainly score patches by test pass rate, but accepted patches also need to follow project design constraints such as architecture choices, error handling, API consistency, and maintainability rules.
- Many of these constraints are not encoded in tests and are only implied in pull request review discussions, so a test-passing patch can still be unacceptable in real development.
- Without a way to extract, link, and verify these constraints, current benchmark scores overstate how useful LLM agents are for real repository work.

## Approach
- The paper builds **SWE-Shield**, a design-aware benchmark aligned with SWE-bench-Verified and SWE-bench-Pro, covering **495 issues**, **1,787 validated constraints**, **6 repositories**, and **10,885 extracted constraints** before validation.
- It introduces **DesignHunter**, a two-stage LLM pipeline: first it extracts atomic design suggestions from code review threads, then it groups and synthesizes them into structured design constraints with problem, options, conditions, and reference code.
- To connect constraints to issues, the pipeline uses explicit traceability and semantic matching, followed by manual validation.
- For evaluation, it adds an **LLM-based verifier** that checks whether a generated patch satisfies the linked design constraints, since these constraints are non-executable and often context-dependent.

## Results
- On **SWE-Shield-verified**, agents reach **70.25%–75.95% Pass Rate**, but **design satisfaction rate (DSR)** is only **32.64%–50.20%**.
- On **SWE-Shield-pro**, Pass Rate reaches **42.69%**, while design violations remain high, with **design violation rate (DVR)** up to **45.85%**.
- Functional correctness has little statistical relation to design compliance in most settings: **Cramér’s V ≤ 0.11**, and the paper reports no significant association in most chi-square tests.
- Across foundation models under the same **swe-agent** setup on **SWE-Shield-pro**, DSR changes by only **12 percentage points**, even when Pass Rate differs much more, which suggests many design failures are shared across models.
- Adding issue-specific design guidance lowers violations, with **DVR decreasing by up to 6.35 percentage points**, but remaining violation rates still stay **above 30%**.
- The main claim is that test-based evaluation materially overestimates patch quality, because fewer than half of resolved issues are fully design-satisfying in many settings.

## Link
- [http://arxiv.org/abs/2604.05955v1](http://arxiv.org/abs/2604.05955v1)
