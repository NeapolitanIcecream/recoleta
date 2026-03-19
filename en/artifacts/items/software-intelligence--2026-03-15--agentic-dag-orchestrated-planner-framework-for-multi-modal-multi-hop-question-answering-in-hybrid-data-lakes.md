---
source: arxiv
url: http://arxiv.org/abs/2603.14229v1
published_at: '2026-03-15T05:34:16'
authors:
- Kirushikesh D B
- Manish Kesarwani
- Nishtha Madaan
- Sameep Mehta
- Aldrin Dennis
- Siddarth Ajay
- Rakesh B R
- Renu Rajagopal
- Sudheesh Kairali
topics:
- multi-hop-qa
- dag-planning
- hybrid-data-lake
- agentic-framework
- evidence-tracing
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Agentic DAG-Orchestrated Planner Framework for Multi-Modal, Multi-Hop Question Answering in Hybrid Data Lakes

## Summary
A.DOT is an agentic planning framework for question answering over enterprise hybrid data lakes. It compiles natural language questions into executable DAG plans to support multi-hop reasoning across structured tables and unstructured documents. It aims to improve correctness, completeness, latency, and auditability at the same time, while providing explicit evidence chains and data lineage.

## Problem
- Existing enterprise RAG/tool-calling solutions usually perform brute-force retrieval separately over SQL databases and vector stores, then stitch results together afterward. This is inefficient, prone to over-retrieval and data leakage, and also lacks explicit multi-hop reasoning capability.
- Questions in hybrid data lakes often require repeated switching between tables and documents; without planned execution, models are prone to hallucination, choosing the wrong data source, and making answer provenance hard to trace.
- This matters because enterprise settings require not only correct answers, but also low latency, verifiability, auditability, and traceable data lineage.

## Approach
- The core mechanism is to decompose a natural language question into multiple “atomic sub-questions” in a **single LLM planning** step, generating a dependency-aware DAG; each node targets only one data source type (SQL or vector store).
- The system first performs **structural validation + semantic validation**: checking schema validity, variable dependencies, acyclicity, whether intent is preserved, and whether aggregations/joins are executable; when issues arise, they are handed to DataOps for diagnosis, repair, or re-planning.
- During execution, the system runs according to DAG topological order, with **independent nodes executed in parallel**, and uses variable binding to pass only the minimal necessary intermediate results (such as document_id), reducing load and leakage risk.
- The framework also adds **paraphrase-aware plan caching**, enabling reuse of DAG plans for equivalent queries; at the same time, it records each step’s operations, inputs and outputs, and evidence sources to form a verifiable lineage/evidence trail.

## Results
- On the **HybridQA dev set** (**3,466** QA pairs), the main reported results for A.DOT are: **Answer Correctness 71.0** and **Answer Completeness 73.0**.
- Compared with the strongest baseline, **Standard RAG** (Correctness **56.2**, Completeness **62.3**), A.DOT improves correctness by **14.8 percentage points** and completeness by **10.7 percentage points**.
- Other baseline results are: **ReAct 40.2 / 44.3** and **LLM Compiler 27.8 / 30.8**, indicating that sequential tool calling alone or weaker DAG orchestration is insufficient for cross-modal multi-hop reasoning.
- In a **500**-sample ablation study, full A.DOT reaches **71.8 / 74.3**; removing **DataOps** drops performance to **60.0 / 61.8**; removing **Plan Validator** yields **68.0 / 69.6**; removing both gives **67.9 / 69.6**.
- The paper also claims the system is being evaluated for integration with **IBM Watsonx.data Premium**, but no public quantitative results are yet provided for deployment performance, user studies, or large-scale performance testing.

## Link
- [http://arxiv.org/abs/2603.14229v1](http://arxiv.org/abs/2603.14229v1)
