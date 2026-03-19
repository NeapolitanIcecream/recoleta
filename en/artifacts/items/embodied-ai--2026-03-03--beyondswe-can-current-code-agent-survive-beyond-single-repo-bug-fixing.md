---
source: arxiv
url: http://arxiv.org/abs/2603.03194v1
published_at: '2026-03-03T12:52:01'
authors:
- Guoxin Chen
- Fanzhe Meng
- Jiale Zhao
- Minghao Li
- Daixuan Cheng
- Huatong Song
- Jie Chen
- Yuzhi Lin
- Hui Chen
- Xin Zhao
- Ruihua Song
- Chang Liu
- Cheng Chen
- Kai Jia
- Ji-Rong Wen
topics:
- code-agents
- software-engineering-benchmark
- swe-bench
- web-search-augmentation
- repository-generation
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# BeyondSWE: Can Current Code Agent Survive Beyond Single-Repo Bug Fixing?

## Summary
This paper introduces **BeyondSWE**, a benchmark for evaluating whether code agents can go beyond the traditional SWE-bench setting of “single-repo localized bug fixing,” and presents **SearchSWE**, a baseline framework with search capabilities. The results show that current frontier code agents still have a clearly insufficient overall success rate on tasks that are closer to real-world software engineering.

## Problem
- Existing SWE benchmarks are mostly limited to **single-repository, localized function-level fixes**, and cannot cover scenarios common in real development such as cross-repository retrieval, domain-knowledge reasoning, dependency migration, and generating systems from documentation.
- This matters because real-world software engineering often requires **using external knowledge** and performing **repository-level transformations**, rather than just making small patches within a given repository; if evaluations do not cover these capabilities, they will overestimate the true practical usefulness of code agents.
- The paper asks: **Can current code agents still work effectively once they leave single-repo bug fixing?**

## Approach
- The authors build the **BeyondSWE** benchmark, extending evaluation along two dimensions: **resolution scope** (from localized fixes to whole-repository migration/full-repository generation) and **knowledge scope** (whether knowledge outside the repository is required).
- The benchmark contains 4 task types: **CrossRepo** (solving problems with the help of external repositories), **DomainFix** (requiring specialized knowledge such as bioinformatics or quantum science), **DepMigrate** (whole-repository migration caused by breaking updates in upstream dependencies), and **Doc2Repo** (generating a complete repository from natural-language specification documents).
- In total there are **500 instances from 246 real GitHub repositories**; each instance provides an issue description, Docker environment, and test suite, and reproducibility, leakage prevention, and resistance to test-modification cheating are ensured through multiple rounds of automated and manual quality checks.
- The paper proposes **SearchSWE**: beyond the local container operations of conventional code agents, it adds a **search tool** and **browser tool**, allowing the agent to alternate among repository exploration, code modification, and web search, while using a blocklist to prevent direct access to answers from the target repository.

## Results
- BeyondSWE is clearly larger in scale and complexity than existing SWE benchmarks: on average, each task involves **5.6 files, 209.9 lines of code, and 246 repository sources**; by comparison, SWE-bench-Verified involves only **1.3 files and 11.6 lines**, indicating that BeyondSWE tasks are closer to real engineering complexity.
- Under **OpenHands**, the best average performance is only about **41.82%** (Gemini 3 Pro), and the paper concludes that the overall success rate of current code agents on BeyondSWE is **only about 45%**, far below the **80%+** level cited in the paper for **SWE-bench Verified**, showing a clear capability gap.
- By task, under OpenHands the best **CrossRepo** result is **44.72%** (Seed-Coder), the best **DomainFix** is **36.11%** (GLM-4.7), the best **DepMigrate** is **41.81%** (Gemini 3 Pro), and the best **Doc2Repo Pass Rate** is **54.99%** (DeepSeek-V3.2); however, the number of **fully correct Doc2Repo** repositories is at most **2**, showing that building a complete system from specifications remains very difficult.
- The gains from SearchSWE are **unstable**: for example, **Gemini 3 Pro** improves in average score from **41.82% to 43.84%** under SearchSWE, including **DomainFix +7.5** and **DepMigrate +2.3**; but **Seed-Coder** drops on CrossRepo from **44.72% to 38.89% (-5.8)**, indicating that “being able to search” and “being able to code” have not yet been effectively unified by current models.
- CrossRepo generally benefits more from search, while **Doc2Repo** is often more negatively affected by it; based on this, the paper claims a core finding: **current LLM search capability and coding capability are two separately mature but not yet truly integrated skill sets.**

## Link
- [http://arxiv.org/abs/2603.03194v1](http://arxiv.org/abs/2603.03194v1)
