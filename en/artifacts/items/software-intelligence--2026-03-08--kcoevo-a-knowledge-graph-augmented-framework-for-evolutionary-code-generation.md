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
- code-generation
- api-migration
- knowledge-graph
- llm-reasoning
- software-evolution
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# KCoEvo: A Knowledge Graph Augmented Framework for Evolutionary Code Generation

## Summary
KCoEvo addresses the problem of **code migration generation that breaks as API versions evolve**: standard LLMs often produce outdated or incompatible APIs, while this method uses a knowledge graph to explicitly represent API evolution paths and constrain generation. The paper decomposes migration into two steps—“first find the evolution path, then generate code following the path”—and significantly improves accuracy and executability across multiple models and migration types.

## Problem
- Target problem: automatically migrate code that depends on older versions of third-party libraries into code compatible with newer versions, while preserving the original functionality.
- Importance: modern projects rely heavily on third-party libraries, and frequent API changes can break code and increase maintenance costs; the authors note that a typical project may contain **20–70 transitive dependencies**, while having only **6–10 direct dependencies**.
- Existing LLM shortcomings: they lack an explicit structured representation of evolution knowledge such as **cross-version relationships, deprecation/renaming/migration**, so they tend to generate outdated APIs, semantically inconsistent code, or outputs that cannot execute.

## Approach
- Construct a two-layer API knowledge graph: the **static API graph** represents structural relationships within a single version, and the **dynamic alignment graph** represents cross-version evolutionary relationships such as retain, remove, rename, and relocate.
- Split migration into two stages: first perform **evolution path retrieval** to retrieve feasible migration trajectories from old APIs to new APIs from the graph; then perform **path-informed code generation**, where the LLM generates target code based on these paths.
- During dynamic alignment, the system first locates API nodes from the query code, then uses **BFS graph traversal** combined with version metadata and relation types to identify valid cross-version candidate paths.
- The planning module directly reuses the LLM rather than training a separate new model: the LLM first converts the aligned subgraph into an explicit “evolution plan,” and then the reasoning/generation module completes code migration according to that plan.
- Training supervision comes from data **automatically synthesized from real API diffs**, rather than large-scale manual annotation, improving scalability and reducing labor costs.

## Results
- On the VersiCode benchmark, the method improves over base LLMs across all migration types. Example: for **DeepSeek-V3** on **Major→Major**, CDC@1 rises from **59.52** to **96.83**, and EM@1 rises from **59.52** to **100.00** (**+37.31** and **+40.48**, respectively).
- Gains are even larger in more difficult cross-version migrations. For **DeepSeek-V3**, EM@1 on **Major→Minor** increases from **33.84** to **94.44** (**+60.60**), and on **Minor→Major** from **15.74** to **95.37** (**+79.63**).
- **Qwen2.5-Coder-32B-Instruct** also benefits substantially: on **Major→Minor**, EM@1 increases from **16.16** to **92.42** (**+76.26**); on **Minor→Major**, from **7.41** to **87.96** (**+80.55**).
- High-performing closed-source models still benefit. The **GPT-5** baseline is already strong, but with KG added, on **Minor→Minor** CDC@1 rises from **46.30** to **92.60** (**+46.30**), and EM@1 from **72.23** to **100.00** (**+27.77**); on **Minor→Major**, CDC@1 rises from **82.83** to **100.00**.
- Compared with code-block RAG, standard retrieval augmentation provides limited gains or even degrades performance. For example, for **Qwen2.5-7B-Instruct** on **Major→Major**, the baseline EM@1 is **38.89**; with **Downstream Code** it becomes **38.10**, and with **Library Source** it is still only **38.10**. This suggests that structured evolution knowledge is more effective than raw code retrieval.
- The paper’s core claim is that the knowledge graph not only improves **accuracy/EM@1**, but also improves the syntactic and execution success reflected by **CDC@1**, while providing stronger controllability and more interpretable migration paths.

## Link
- [http://arxiv.org/abs/2603.07581v1](http://arxiv.org/abs/2603.07581v1)
