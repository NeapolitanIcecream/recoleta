---
source: arxiv
url: http://arxiv.org/abs/2603.05553v1
published_at: '2026-03-05T04:58:38'
authors:
- Jiaao Chen
- Jingyuan Qi
- Mingye Gao
- Wei-Chen Wang
- Hanrui Wang
- Di Jin
topics:
- function-calling
- synthetic-data
- multi-agent-systems
- benchmark-repair
- evaluation-metrics
relevance_score: 0.12
run_id: materialize-outputs
language_code: en
---

# EigenData: A Self-Evolving Multi-Agent Platform for Function-Calling Data Synthesis, Auditing, and Repair

## Summary
EigenData is a multi-agent platform for function-calling agent data that covers the full pipeline of database construction, executable environment generation, trajectory synthesis, auditing, and repair. The paper focuses on its systematic auditing and repair of the BFCL-V3 benchmark, and proposes an outcome-aware evaluation that better reflects real task success.

## Problem
- Function-calling agents require high-quality, domain-specific, executable data, but manually building databases, tool implementations, and multi-turn trajectories is both expensive and error-prone.
- Existing synthetic data/benchmarks often have three types of problems: bugs in function schemas or implementations, ambiguity in user intent and annotations, and evaluation that only checks turn-by-turn function matching rather than whether the task result is actually correct.
- These issues can mislead training and model selection: a model may "get the call format right" while still failing to update the database state correctly or truly accomplish the user's goal.

## Approach
- The core method is a multi-agent platform coordinated by **EigenCore**, which splits the data lifecycle into three parts: **DatabaseAgent** generates realistic and consistent domain databases, **CodingAgent** generates and tests executable tools/environments, and **DataAgent** generates and optimizes multi-turn function-calling trajectories.
- The key system mechanism is a self-evolving closed loop of "generate → test → debug → regenerate": on the code side, unit tests, integration tests, and a judge are used for fault attribution; on the data side, review and programmatic verification continuously refine prompts and samples.
- There is cross-component feedback among the modules: if downstream components detect inconsistencies in schemas, code, databases, or trajectories, EigenCore sends structured feedback upstream and repairs only the relevant parts instead of rerunning the entire pipeline.
- In the BFCL-V3 case, EigenData does not only generate new data; it also audits existing benchmarks, identifies, and automatically repairs systematic errors in function schemas, implementations, reference trajectories, and user intent.
- The paper also proposes outcome-aware evaluation: instead of primarily comparing whether turn-by-turn trajectories exactly match the reference answer, it checks whether the final database state, key function calls, and handling of critical information are correct.

## Results
- The paper claims that EigenData successfully **systematically identified and automatically repaired** errors in schemas, implementations, reference trajectories, and user intent in BFCL-V3, but the excerpt **does not provide specific repair counts or proportions**.
- The paper claims that the repaired benchmark together with outcome-aware metrics yields model rankings with a **significantly higher correlation with human judgments of functional correctness**, but the excerpt **does not provide correlation coefficients or specific values**.
- The paper explicitly states that the new evaluation leads to model rankings **"substantially different"** from the original BFCL-V3, indicating that traditional turn-level matching may mask real functional failures; however, the excerpt **does not list specific numerical ranking changes**.
- At the architecture level, it presents a practically deployable system: it supports generating databases, environments, and trajectories from scratch, and also supports auditing/repairing existing benchmarks only, and has released a CLI and a repaired BFCL-V3 code repository.
- In terms of quantitative results, the currently provided text **does not contain clearly citable experimental numbers, dataset sizes, improvement magnitudes, or percentage comparisons with specific baselines**.

## Link
- [http://arxiv.org/abs/2603.05553v1](http://arxiv.org/abs/2603.05553v1)
