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
- search-augmented-agents
- cross-repository-reasoning
- repository-generation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# BeyondSWE: Can Current Code Agent Survive Beyond Single-Repo Bug Fixing?

## Summary
BeyondSWE proposes a new benchmark for evaluating code agents that goes beyond local bug fixing within a single repository, and uses it to test the capabilities of current frontier code models on more realistic software engineering tasks such as cross-repository work, domain knowledge, dependency migration, and generating repositories from documentation. The paper also introduces SearchSWE, which uses a unified "coding + retrieval" framework to analyze whether external search truly improves code agent performance.

## Problem
- Existing SWE benchmarks mostly evaluate **single-repo, local, function-level** bug fixing, which is far removed from real software engineering scenarios that commonly involve cross-repository dependencies, domain knowledge, whole-repository migration, and generating systems from specifications.
- As a result, we still do not know how far current code agents are from becoming "truly usable software engineering agents"; this matters because development tasks in industry often require **external knowledge acquisition** and **large-scale code changes**.
- The core question the paper asks is: **Can current code agents survive in settings that go beyond single-repo bug fixing?**

## Approach
- The authors build the **BeyondSWE** benchmark, expanding evaluation along two dimensions: **resolution scope** (from local fixes to whole-repository transformation/full generation) and **knowledge scope** (whether knowledge outside the codebase is required).
- The benchmark contains 4 task categories, **500 instances** in total, drawn from **246 real GitHub repositories**: **CrossRepo** (solving problems with the help of external repositories), **DomainFix** (requiring specialized domain knowledge), **DepMigrate** (whole-repository migration caused by breaking upstream dependency upgrades), and **Doc2Repo** (directly generating a complete repository from natural-language specifications).
- To ensure reproducibility, the authors use an LLM agent to automatically construct Docker environments, and retain only stable samples through strict checks: before the patch, **P2P must pass and F2P must fail**; after the patch, both must pass. During evaluation, the patch is also applied in a **fresh container** to avoid environment contamination.
- They propose the **SearchSWE** framework, which adds **web search** and **browser** tools on top of the local Docker coding environment, allowing agents to alternate among repository exploration, code modification, and external information retrieval; at the same time, a target-repository access blocking mechanism is used to prevent cheating.

## Results
- BeyondSWE is substantially more difficult overall: the paper says current code agents achieve only about **45%** success on this benchmark, far below the commonly cited **80%+** level on SWE-bench Verified mentioned for comparison in the paper, indicating a clear capability gap for going "beyond single-repo bug fixing."
- Under the **OpenHands** framework, the best average performance is only about **41.82%** (**Gemini 3 Pro**); others include **GLM-4.7 41.20%**, **DeepSeek-V3.2 40.01%**, and **Kimi-K2 39.81%**, and no model dominates across all tasks.
- By task: **CrossRepo** is best on **Seed-Coder 44.72%**; **DomainFix** is best on **GLM-4.7 36.11%**; **DepMigrate** is best on **Gemini 3 Pro 41.81%**; **Doc2Repo** reaches its highest test pass rate with **DeepSeek-V3.2 54.99%**, but the number of "fully correct" repositories is at most only **2**, showing that generating a complete system from specifications is especially difficult.
- The gains from SearchSWE are **unstable**. For example, **Gemini 3 Pro** improves under SearchSWE from an average score of **41.82%** to **43.84%**, including **DomainFix +7.5%** (31.94%→39.44%) and **DepMigrate +2.3%** (41.81%→44.07%); but **Doc2Repo -1.3** (52.03→50.73).
- Some models benefit little from search or even degrade. For example, **Seed-Coder** drops on **CrossRepo** from **44.72%** to **38.89%** (**-5.8%**), and its average score falls from **36.90%** to **34.01%**. This supports the paper's core conclusion: **search capability and coding capability have not yet been effectively unified**.
- In terms of benchmark scale, BeyondSWE covers broader changes than existing SWE-style benchmarks: it involves an average of **5.6 files** and **209.9 lines** modified, significantly higher than **1.3 files/11.6 lines** for SWE-bench Verified, **2.7 files/65.1 lines** for SWE-bench Live, and **4.1 files/107.4 lines** for SWE-bench Pro.

## Link
- [http://arxiv.org/abs/2603.03194v1](http://arxiv.org/abs/2603.03194v1)
