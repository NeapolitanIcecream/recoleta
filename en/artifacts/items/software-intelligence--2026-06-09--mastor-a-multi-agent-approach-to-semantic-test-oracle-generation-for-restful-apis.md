---
source: arxiv
url: https://arxiv.org/abs/2606.10465v1
published_at: '2026-06-09T06:35:21'
authors:
- Sida Deng
- Rubing Huang
- Zhenzhen Yang
- Man Zhang
- Xuan Xie
- Rongcun Wang
topics:
- rest-api-testing
- test-oracle-generation
- multi-agent-systems
- code-intelligence
- automated-testing
- llm-agents
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# MASTOR: A Multi-Agent Approach to Semantic Test Oracle Generation for RESTful APIs

## Summary
MASTOR generates semantic test oracles for RESTful APIs by reading implementation source code and coordinating LLM-based agents. It targets faults that status-code checks, crash checks, and schema checks often miss.

## Problem
- REST API tests often verify only HTTP status codes, runtime failures, or schema conformance, so they can miss business-logic errors and state-dependent inconsistencies.
- Correct behavior can depend on controller branches, service logic, repository calls, model fields, exception paths, and relationships between endpoints.
- API specifications alone may omit constraints such as input length guards, response-field filtering rules, and side effects hidden behind a successful HTTP response.

## Approach
- MASTOR has two phases: source analysis and oracle generation.
- A source extraction agent builds a Source context for each endpoint by reading the transitive import closure of relevant source files and recording input constraints, response schemas, and source evidence.
- The single-operation path generates status oracles and field oracles for each endpoint using source-grounded facts.
- The multi-operation path generates behavioral consistency oracles for endpoint sequences using cross-operation associations found during source analysis.
- Challenger agents review generated oracles once, give repair hints, trigger targeted regeneration, and then normalization filters structurally invalid oracles.

## Results
- The benchmark covers 13 open-source RESTful API projects, 296 endpoint operations, and 251,303 lines of code from WFD and PRAB.
- MASTOR generated 10,022 oracles and reached an average mutation score of 75.4% across the 13 APIs.
- Individual API mutation scores ranged from 69.0% to 95.9%.
- On 50 selected endpoint operations using only status and field oracles, MASTOR scored 69.9% versus 39.8% for Direct Prompting, a gain of 30.1 percentage points.
- On the same 50-operation comparison, MASTOR scored 69.9% versus 20.5% for SATORI, a gain of 49.4 percentage points.
- The reported median inference cost was $0.56 per API using DeepSeek V4 Pro and Qwen3.6-Plus.

## Link
- [https://arxiv.org/abs/2606.10465v1](https://arxiv.org/abs/2606.10465v1)
