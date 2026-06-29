---
source: arxiv
url: https://arxiv.org/abs/2606.04799v1
published_at: '2026-06-03T12:25:50'
authors:
- Changhua Pei
- Zheyuan Li
- Zexin Wang
- Hang Cui
- Xiaohui Nie
- Qi Zhou
- Fang Situ
- Cheng Zhang
- Xin Zhang
- Xidao Wen
- Gaogang Xie
- Jingjing Li
- Dan Pei
topics:
- aiops
- observability
- root-cause-analysis
- llm-agents
- knowledge-graph
- query-language
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# UModel: An Agent-Ready Observability Data Modeling Method at Scale

## Summary
UModel organizes observability data as linked objects so LLM agents can query telemetry, topology, and operations knowledge during root cause analysis. The paper claims an 8% gain in root cause localization on the AIOps 2025 Challenge dataset and reports large-scale Alibaba Cloud deployment.

## Problem
- RCA for networked systems needs logs, metrics, traces, topology, and expert knowledge in one view; current observability stacks split these across tools such as Prometheus, Elasticsearch, and tracing systems.
- LLM agents often lack schema meaning, units, query rules, and entity relationships, so they make invalid queries or miss causal paths during diagnosis.
- The problem matters because over 40% of real industrial faults are reported as zero-shot failures, where supervised RCA models that rely on past incidents can fail.

## Approach
- UModel converts operational resources into objects: services, pods, hosts, metrics, logs, traces, events, runbooks, and tools.
- It links these objects in a semantic graph, using EntitySet, DataSet, EntitySetLink, and DataLink to connect topology, telemetry, and knowledge.
- U-SPL gives agents one pipeline-style query language for schema lookup, entity search, and graph traversal instead of separate PromQL, SQL, log, and trace queries.
- USearch handles entity and telemetry retrieval with keyword search, filtering, fuzzy matching, ranking, and top-k control.
- GSearch lets agents walk dependency graphs, such as service call paths, to inspect likely fault propagation paths.

## Results
- On the AIOps 2025 Challenge dataset, remodeling the data with UModel improved root cause localization precision by 8% over the naive agent-based approach; the excerpt does not provide the absolute precision values.
- The introduction also describes this as an 8% RCA accuracy improvement, but the excerpt does not clarify whether the 8% is absolute percentage points or relative gain.
- Alibaba Cloud has deployed UModel in production for more than 1 year.
- The deployment has served tens of thousands of users and unified thousands of standardized models across subsystems including Kubernetes, network, container services, APM, and cloud infrastructure monitoring.
- The system is reported to handle millions of operations per second with sub-second or second-level query latency for large data retrieval.

## Link
- [https://arxiv.org/abs/2606.04799v1](https://arxiv.org/abs/2606.04799v1)
