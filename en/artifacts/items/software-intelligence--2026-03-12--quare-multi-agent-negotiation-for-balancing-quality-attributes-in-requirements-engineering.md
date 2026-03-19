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
- multi-agent-systems
- requirements-engineering
- llm-agents
- negotiation-protocol
- software-quality
- kaos-modeling
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# QUARE: Multi-Agent Negotiation for Balancing Quality Attributes in Requirements Engineering

## Summary
QUARE is a multi-agent framework for requirements engineering that explicitly turns conflicts among different quality attributes into a "negotiation" process, rather than having a single LLM make implicit trade-offs. Its core claim is that, compared with larger models, structured role division, negotiation protocols, and automated verification are more effective at improving the quality of requirements analysis.

## Problem
- In requirements engineering, it is often necessary to satisfy mutually conflicting quality attributes such as **safety, efficiency, sustainability, trustworthiness, and responsibility/compliance** at the same time, and manually balancing these constraints is both time-consuming and error-prone.
- Existing LLM methods are mostly based on monolithic reasoning or implicit aggregation, making it difficult to **explicitly surface conflicts, explain the rationale behind trade-offs, and preserve stakeholder intent**.
- Requirement issues are critical in software projects; the paper notes that **more than 70% of failed projects** can be traced to requirements-related defects, so automated and traceable requirements analysis is important.

## Approach
- QUARE decomposes requirements analysis into **5 quality-specialized agents** (Safety, Efficiency, Green, Trustworthiness, Responsibility) plus **1 orchestrator**. All agents share the same LLM backbone, but role isolation is achieved through different system prompts.
- It uses a **dialectical negotiation protocol**: agents first propose requirements, then other agents critique constraint conflicts, and finally the coordinator synthesizes the outcome; conflicts are categorized into **resource-bound** and **logical incompatibility**, and negotiation proceeds for at most **3 rounds**.
- To identify conflicts, the system first uses a **BERT embedding cosine similarity threshold of 0.85** to find potential overlaps, and then uses an LLM to determine whether they are redundant or one of the two conflict types.
- The negotiated results are converted into **KAOS goal models**, followed by **topology/DAG validation**, rule checking, and RAG-supported hallucination and compliance verification (such as **ISO 26262, ISO 27001**), and finally output as standardized engineering artifacts.
- In the experiments, **gpt-4o-mini-2024-07-18** was used on **5 case studies** (the MARE and iReDev benchmarks and an industrial autonomous-driving specification), compared against single-agent, multi-agent without negotiation, MARE, and iReDev.

## Results
- The paper claims that QUARE achieves **98.2% compliance coverage**, representing a **+105%** improvement over the baseline.
- It reaches **94.9% semantic preservation**, which is **+2.3 percentage points** higher than the best baseline.
- The verifiability score reaches **4.96/5.0**.
- The number of generated requirements is **25–43%** higher than in existing multi-agent RE frameworks.
- Negotiation converged within the **3-round limit** in all scenarios; the experiments used **3 random seeds**, a unified configuration, and **180 total runs**.
- The abstract and excerpt do not provide a complete itemized table of values for each dataset and each baseline, but the strongest quantitative conclusion is that QUARE overall outperforms the compared methods in **compliance coverage, semantic preservation, verifiability, and requirement output volume**.

## Link
- [http://arxiv.org/abs/2603.11890v1](http://arxiv.org/abs/2603.11890v1)
