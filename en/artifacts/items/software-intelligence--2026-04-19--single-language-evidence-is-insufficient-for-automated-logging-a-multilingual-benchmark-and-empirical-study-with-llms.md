---
source: arxiv
url: http://arxiv.org/abs/2604.17529v1
published_at: '2026-04-19T16:43:17'
authors:
- Renyi Zhong
- Yichen Li
- Yulun Wu
- Jinxi Kuang
- Yintong Huo
- Michael R. Lyu
topics:
- automated-logging
- multilingual-benchmark
- code-generation
- llm-evaluation
- software-maintenance
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Single-Language Evidence Is Insufficient for Automated Logging: A Multilingual Benchmark and Empirical Study with LLMs

## Summary
This paper argues that automated logging cannot be evaluated reliably with Java-only snapshot datasets. It introduces MultiLogBench, a multilingual benchmark across six languages and tests seven LLMs on both snapshot and revision-history logging tasks.

## Problem
- Automated logging asks a model to decide **where** to insert a log, **which API/framework** to call, **what severity level** to use, **what message** to write, and **which variables** to include.
- Prior evidence is mostly based on **single-language, Java-heavy repository snapshots**, so it does not show whether findings transfer across language ecosystems such as Python, Go, C++, JavaScript, and C#.
- Snapshot-only evaluation also misses the maintenance setting where developers add logs during real code changes, which matters if model behavior shifts on revision-history data.

## Approach
- The authors build **MultiLogBench**, a benchmark covering **six languages**: Java, Python, Go, C++, JavaScript, and C#.
- The benchmark has **three branches**: **63,965** repository-snapshot instances, **744** revision-history cases mined from real log-introducing commits, and a paired transformed revision-history branch for robustness checks.
- They evaluate **seven contemporary LLMs** with one unified protocol over several subproblems: logging-site localization, framework-anchor matching, severity prediction, message generation, variable recovery, and cascaded end-to-end quality.
- They also analyze performance by structural context inside functions, with attention to hard positions such as loops and nested callables.

## Results
- MultiLogBench contains **63,965** snapshot instances and **744** revision-history cases across **6** language ecosystems and **7** LLMs; this is the main benchmark contribution.
- The paper reports **clear cross-language variation** in automated logging performance. It states that **framework-anchor matching** is the **most language-sensitive** component.
- Structural context affects difficulty: **loop** sites and **nested-callable** sites are reported as the hardest cases.
- Model rankings are **stable only at the top tier**. Lower-ranked and mid-tier models reorder across languages, so a leaderboard from one language can mislead model selection.
- On **revision-history** data, the paper says **absolute performance declines** and ranking stability weakens, but the main cross-language patterns still remain.
- The excerpt does **not provide task metrics or exact score values** for the seven models, so no numeric comparison against specific baselines is available here.

## Link
- [http://arxiv.org/abs/2604.17529v1](http://arxiv.org/abs/2604.17529v1)
