---
source: arxiv
url: http://arxiv.org/abs/2603.11890v1
published_at: '2026-03-12T13:03:01'
authors:
- Haowei Cheng
- Milhan Kim
- Foutse Khomh
- Teeradaj Racharak
- Nobukazu Yoshioka
- Naoyasu Ubayashi
- Hironori Washizaki
topics:
- requirements-engineering
- multi-agent-negotiation
- llm-agents
- kaos-modeling
- compliance-verification
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# QUARE: Multi-Agent Negotiation for Balancing Quality Attributes in Requirements Engineering

## Summary
QUARE is a multi-agent framework that decomposes requirements engineering into multiple “quality-stance agents” that negotiate with one another, aiming to make traceable trade-offs among safety, efficiency, sustainability, trustworthiness, and responsibility. The paper argues that, compared with monolithic or implicitly aggregated LLM methods, explicit negotiation and automated verification are more effective at producing complete, compliant, and semantically faithful requirements models.

## Problem
- Requirements engineering often must satisfy mutually conflicting quality attributes at the same time, such as safety, performance, privacy, and compliance; manually balancing these constraints is time-consuming and error-prone.
- Existing LLM RE methods mostly rely on single-agent reasoning or implicit aggregation, making it difficult to **explicitly identify, classify, and resolve** cross-quality conflicts, which reduces transparency in the rationale behind trade-offs.
- A large share of software project failures is related to requirements problems; in safety-critical scenarios such as autonomous driving, such defects directly affect system reliability and regulatory compliance.

## Approach
- It uses 5 quality-specialized agents (Safety, Efficiency, Green, Trustworthiness, Responsibility) plus 1 Orchestrator, decomposing requirements analysis by quality dimension rather than by task dimension.
- It designs a 5-stage pipeline: parallel requirement generation, dialectical negotiation, KAOS goal model integration and topology validation, RAG+rule-based compliance verification, and standardized engineering artifact generation.
- The core mechanism is explicit negotiation: agents conduct multi-round “proposal–critique–synthesis” dialogues around conflicting requirements, with up to 3 rounds; conflicts are first screened using embedding similarity, then classified by the LLM as redundancy, resource conflict, or logical incompatibility.
- Negotiation results are converted into structured KAOS goal graphs, and engineering usability is ensured through DAG/topology validity checks and retrieval-augmented verification against standards such as ISO 26262, ISO 27001, and ISO/IEC/IEEE 29148.
- In evaluation, beyond traditional semantic preservation and consistency, the paper also introduces geometric metrics in a five-dimensional quality space, such as CHV and MDC, to measure the breadth and dispersion of requirements coverage.

## Results
- Across 5 case studies (MARE, iReDev benchmarks, and an industrial autonomous-driving specification), QUARE reports **98.2% compliance coverage**, an improvement of **+105%** over both types of baselines.
- Semantic preservation reaches **94.9% semantic preservation**, **+2.3 percentage points** higher than the best baseline.
- Verifiability reaches **4.96/5.0**.
- The number of generated requirements is **25–43%** higher than existing multi-agent RE frameworks.
- The paper states that negotiation converges within **at most 3 rounds** in all scenarios; experiments used **gpt-4o-mini-2024-07-18**, with 5 cases, 4 settings, and 3 random seeds, for a total of **180 runs**.
- The paper does not provide specific values for all geometric metrics (such as CHV, MDC, and CRR) in the given excerpt, but the strongest quantitative conclusion is that it comprehensively outperforms single-agent, no-negotiation multi-agent, MARE, and iReDev baselines in compliance coverage, semantic preservation, and number of requirements.

## Link
- [http://arxiv.org/abs/2603.11890v1](http://arxiv.org/abs/2603.11890v1)
