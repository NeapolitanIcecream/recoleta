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
- hybrid-data-lake
- dag-planning
- agentic-systems
- rag
- enterprise-search
relevance_score: 0.04
run_id: materialize-outputs
language_code: en
---

# Agentic DAG-Orchestrated Planner Framework for Multi-Modal, Multi-Hop Question Answering in Hybrid Data Lakes

## Summary
A.DOT is an agentic planning framework for question answering over enterprise hybrid data lakes. It compiles natural language questions into executable DAG plans to perform multi-hop reasoning between structured tables and unstructured documents. It emphasizes parallel execution, plan validation, error repair, caching, and evidence-trail tracking to improve correctness, completeness, and verifiability.

## Problem
- The paper addresses **multi-modal, multi-hop question answering over hybrid data lakes**: user questions often require retrieval and reasoning back and forth between SQL tables and documents/vector stores, while existing RAG or simple tool-calling approaches usually just retrieve from each separately and stitch results together afterward.
- This matters because enterprise settings require not only **correct answers**, but also **efficiency, limited data leakage, and traceable provenance**; brute-force retrieval can introduce redundant computation, hallucination risks, and compliance issues.
- Existing methods generally lack unified support for **explicit multi-hop planning, cross-modal intermediate-variable passing, parallel execution, plan reuse, and auditable evidence trails**.

## Approach
- The core method is to **generate a DAG execution plan from a natural language question in one shot**: each node is an atomic sub-question that accesses only one data source (SQL or vector store), and edges represent dependencies.
- The system first performs **structural validation + semantic validation**, checking schema validity, variable references, acyclicity, join-key types, and whether the plan deviates from user intent; if validation fails, the DataOps module diagnoses, repairs, or replans.
- During execution, it runs independent nodes in parallel according to the DAG’s **topological order**, and passes downstream only the minimal fields actually needed (such as `document_id`) as variables, reducing context burden, memory usage, and data leakage.
- The system also adds **paraphrase-aware plan caching**, allowing reuse of DAG plans for semantically equivalent questions; meanwhile it records each step’s inputs, outputs, and evidence sources to form verifiable data lineage.

## Results
- On the **HybridQA dev** dataset (**3,466** QA samples), A.DOT improves over the strongest baseline, **Standard RAG**, with **Answer Correctness increasing from 56.2 to 71.0 (+14.8 absolute points)**.
- Under the same setup, **Answer Completeness increases from 62.3 to 73.0 (+10.7 absolute points)**. Evaluation uses Unitxt metrics, with the LLM-as-a-judge being **Mistral Large 2**; the reasoning model is **LLaMA-3 70B**.
- Other baseline scores are: **ReAct 40.2 / 44.3** and **LLM Compiler 27.8 / 30.8**. A.DOT leads clearly, indicating stronger multi-hop reasoning across structured and unstructured sources.
- In an ablation study on **500** samples, full A.DOT reaches **71.8 correctness / 74.3 completeness**; removing **DataOps** drops performance to **60.0 / 61.8**, removing **Plan Validator** yields **68.0 / 69.6**, and removing both yields **67.9 / 69.6**.
- The paper also claims advantages such as **lower latency, parallel execution, plan reuse, and auditable evidence trails**, but the excerpt does not provide quantitative data for latency, cache hit rate, or real deployment throughput.

## Link
- [http://arxiv.org/abs/2603.14229v1](http://arxiv.org/abs/2603.14229v1)
