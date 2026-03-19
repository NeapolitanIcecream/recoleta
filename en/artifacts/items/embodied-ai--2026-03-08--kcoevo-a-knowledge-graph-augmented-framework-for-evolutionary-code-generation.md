---
source: arxiv
url: http://arxiv.org/abs/2603.07581v1
published_at: '2026-03-08T10:39:48'
authors:
- Jiazhen Kang
- Yuchen Lu
- Chen Jiang
- Jinrui Liu
- Tianhao Zhang
- Bo Jiang
- Ningyuan Sun
- Tongtong Wu
- Guilin Qi
topics:
- code-migration
- knowledge-graph
- llm-code-generation
- api-evolution
- version-aware-reasoning
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# KCoEvo: A Knowledge Graph Augmented Framework for Evolutionary Code Generation

## Summary
KCoEvo proposes a framework that augments LLMs with a knowledge graph for cross-version code migration, splitting the task into two stages: "figuring out how APIs evolved" and "generating new code along that evolution path." The core goal is to reduce cases where the model generates outdated APIs, version-incompatible code, and non-executable outputs.

## Problem
- The paper addresses the problem that **continuous evolution of third-party library APIs causes old code to break and makes maintenance difficult**. This is important in modern software development because projects typically depend on many direct and indirect packages, and version changes continually undermine compatibility.
- Although existing LLMs can write code, they lack an explicit structured representation of **cross-version API relationships and temporal evolution**, so they often output outdated APIs, semantically inconsistent code, or version-incompatible code.
- Ordinary RAG or prompting methods can only provide shallow context and struggle to support **controllable, queryable, traversable** reasoning for version migration.

## Approach
- First, it constructs two types of knowledge graphs: a **static API graph** to represent structural relationships within a single version, and a **dynamic alignment graph** to represent cross-version migration relationships such as retain, remove, rename, relocate, and so on.
- It decomposes code migration into two steps: **evolution path retrieval** first finds a feasible migration path from the old API to the new API in the graph; **path-informed code generation** then has the LLM generate code for the new version based on that path.
- Graph construction is based on open-source repositories and package metadata, using ASTs to extract functions, classes, methods, parameters, return values, docstrings, and more, and then using rules to mine cross-version changes from version diffs.
- At query time, it first retrieves the relevant subgraph, then uses **BFS graph traversal** and version metadata to dynamically align old and new APIs and obtain candidate evolution trajectories.
- Training supervision comes from **synthetic annotations automatically generated from real API diffs**, reducing manual labeling costs and improving scalability.

## Results
- On the VersiCode benchmark, **all models in the +KG setting outperform their original Base models**, on metrics including CDC@1 and EM@1, showing that structured evolutionary knowledge can significantly improve code migration correctness and executability.
- **DeepSeek-V3** improves on Major→Major from **59.52→96.83 (CDC@1)** and **59.52→100.00 (EM@1)**; on Major→Minor from **32.83→79.29** and **33.84→94.44**; on Minor→Major from **9.26→75.00** and **15.74→95.37**.
- **Qwen2.5-Coder-32B-Instruct** also improves substantially: on Major→Minor, **EM@1 16.16→92.42 (+76.26)**; on Minor→Major, **EM@1 7.41→87.96 (+80.55)**.
- **Llama-3-70B-Instruct-Turbo** reaches **EM@1 16.67→79.80 (+63.13)** on Major→Minor and **EM@1 10.19→69.44 (+59.25)** on Minor→Major, showing clear benefits for complex cross-version migration.
- **Gemini-1.5-Pro-Latest** reaches **92.93 CDC@1 / 98.48 EM@1** on Major→Minor and **72.22 CDC@1 / 98.15 EM@1** on Minor→Major.
- Even the strong model **GPT-5** gains: on Major→Major, **EM@1 95.23→100.00**; on Minor→Minor, **EM@1 72.23→100.00**. This shows that explicit structured knowledge remains valuable even for high-performance LLMs; compared with code-block RAG in Table 3, ordinary retrieval provides limited gains and is usually clearly weaker than the KG-based method.

## Link
- [http://arxiv.org/abs/2603.07581v1](http://arxiv.org/abs/2603.07581v1)
