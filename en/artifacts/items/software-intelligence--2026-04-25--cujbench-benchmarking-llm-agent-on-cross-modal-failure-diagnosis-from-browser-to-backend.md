---
source: arxiv
url: http://arxiv.org/abs/2604.23455v1
published_at: '2026-04-25T22:10:53'
authors:
- Haoming Meng
topics:
- llm-agents
- failure-diagnosis
- benchmarking
- cross-modal-reasoning
- browser-to-backend
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# CUJBench: Benchmarking LLM-Agent on Cross-Modal Failure Diagnosis from Browser to Backend

## Summary
CUJBench is a benchmark for diagnosing software failures that start with browser-visible symptoms and extend into backend telemetry. It packages each incident as a deterministic snapshot so different LLM agents can be compared on the same cross-modal diagnosis task.

## Problem
- Existing root-cause analysis benchmarks focus on backend logs, traces, and metrics, while web-agent benchmarks focus on completing tasks in working apps. Neither tests diagnosis that links a broken user journey in the browser to backend causes.
- Real incident diagnosis often starts with screenshots, network requests, or console errors, then moves to traces, logs, and recent changes. Benchmarks miss this browser-to-backend reasoning path.
- Live environments add noise and make agent comparisons unreliable, so a useful benchmark needs fixed evidence and repeatable tool outputs.

## Approach
- The paper builds **CUJBench**, a benchmark of failed critical user journeys (CUJs) captured as frozen multi-modal snapshots with frontend evidence, backend observability, and operational context.
- It uses two open-source applications, OpenTelemetry Demo and Tractor Store, to cover backend-dominant, browser-dominant, and cross-modal failures.
- The corpus contains **87 labeled scenarios** across **five fault families**: baseline, browser proxy faults, backend flag faults, compound faults, and frontend mutations.
- Scenario creation uses an **LLM-assisted generation pipeline** that produced **120 candidates**, then filters them through a multi-agent review loop with two SRE reviewers, a senior reviewer, and human verification. **87 of 120** scenarios were admitted.
- Evaluation uses a fixed tool interface with deterministic cached responses, including browser tools such as screenshots and HAR/network data, backend tools such as logs and traces, and context tools such as recent changes and service topology.

## Results
- On the benchmark, six frontier models reach only **19.7% overall accuracy**, with a reported **ceiling of 52%**, so the task is far from solved.
- The paper evaluates **six models** under **three baselines**: retrieval-only, browser-only, and full-toolset.
- A main empirical claim is that **browser-only agents outperform full-toolset agents in aggregate**, which suggests that extra tools often push agents into broader but less focused evidence search.
- The benchmark analysis says the main bottleneck is **cross-modal synthesis**: agents often retrieve the key evidence but fail to connect it to the true cause.
- Prior backend-only work cited in the paper reports low perfect RCA accuracy on OpenRCA, at **3.9% to 12.5%** across five frontier models, which frames CUJBench as a harder and broader diagnosis setting.
- The excerpt does not include a per-model score table, per-dataset split metrics, or exact browser-only vs full-toolset deltas.

## Link
- [http://arxiv.org/abs/2604.23455v1](http://arxiv.org/abs/2604.23455v1)
