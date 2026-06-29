---
source: arxiv
url: http://arxiv.org/abs/2604.23190v1
published_at: '2026-04-25T07:45:41'
authors:
- Renhong Huang
- Dongdong Hua
- Yifei Sun
- Sitao Ding
- Hanyang Yuan
- Daixin Wang
- Yang Yang
topics:
- environment-configuration
- code-agents
- repository-level-execution
- benchmarking
- multi-agent-systems
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# RAT: RunAnyThing via Fully Automated Environment Configuration

## Summary
RAT is a language-agnostic agent framework that configures runnable environments for arbitrary code repositories. It targets a core failure point in repository-level code agents and reports higher setup success than prior methods on a new 2,000+ repository benchmark.

## Problem
- Repository-level software agents often fail before they can test or run code because the project environment is missing, broken, or unclear.
- Existing setup methods depend on curated artifacts such as Dockerfiles, CI logs, or language-specific rules, which limits coverage on messy real-world repositories.
- This matters because execution is required for verification, benchmark creation, training data synthesis, reinforcement from runtime feedback, and reliable deployment.

## Approach
- RAT builds environments with a multi-stage agent pipeline: detect the repository’s main language, inspect project files and docs, pick a starting container image, then iteratively install and verify dependencies inside a sandbox.
- Its ImageRetriever module uses repository semantics plus Docker Hub search to choose a better base image than a fixed default such as `python:3.10` or `openjdk:17`.
- The agent runs with either a fixed standard plan or an automated plan that writes progress into `plan.md` as external memory for longer configuration sessions.
- RAT adds task-specific tools for reading and editing files, parsing CI configs, switching language versions, retrieving similar past issues, recovering from errors, and generating smoke tests when a repo has no tests.
- The paper also introduces RATBench, an exec-verified benchmark of 2,000+ GitHub repositories across Python, Java, Rust, and JavaScript/TypeScript, sampled to cover different project sizes, popularity levels, and artifact availability.

## Results
- On RATBench, RAT reports ESSR of **63.2%** on Python, **41.3%** on Java, **98.7%** on Rust, and **68.7%** on JS/TS.
- Against SWE-agent with the same backbone (DeepSeek-V3), RAT improves ESSR by **47.7 points** on Python (63.2 vs 15.5), **12.0 points** on Java (41.3 vs 29.3), **42.0 points** on Rust (98.7 vs 56.7), and **16.9 points** on JS/TS (68.7 vs 51.8). The paper states an average gain of **29.6%** over strong baselines.
- On Python-specific baselines, RAT beats Repo2Run by **18.4 points** (63.2 vs 44.8), pipreqs by **27.4 points** (63.2 vs 35.8), Zero-shot by **48.0 points** (63.2 vs 15.2), and Installamatic by **56.5 points** (63.2 vs 6.7).
- Across Python evaluation settings, RAT reports **50.5% ESSR** in S1 (artifact-guided), **69.5%** in S2 (artifact-free), and **92.0%** in S3 (test-deficient with synthesized checks), with token use and latency of **451.3K / 41.6 min**, **455.2K / 59.4 min**, and **122.2K / 14.4 min**.
- Ablations on Python show the base system at **63.2% ESSR**, versus **40.5%** without ImageRetriever, **55.7%** without the specialized toolset, and **40.5%** with automated planning only. Full RAT uses **421.9K tokens** and **24.3 min** on average in this setting.

## Link
- [http://arxiv.org/abs/2604.23190v1](http://arxiv.org/abs/2604.23190v1)
