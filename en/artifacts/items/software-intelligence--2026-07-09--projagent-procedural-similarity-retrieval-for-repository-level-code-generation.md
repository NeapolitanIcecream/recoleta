---
source: arxiv
url: https://arxiv.org/abs/2607.08691v1
published_at: '2026-07-09T16:50:54'
authors:
- QiHong Chen
- Aaron Imani
- Iftekhar Ahmed
topics:
- code-generation
- repository-level-generation
- procedural-retrieval
- code-intelligence
- agentic-workflow
- static-analysis
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# ProjAgent: Procedural Similarity Retrieval for Repository-Level Code Generation

## Summary
ProjAgent improves repository-level code generation by retrieving functions with similar computational procedures, even when their names and domains differ. It combines procedural, lexical, and semantic retrieval with static-analysis-based code repair.

## Problem
- Repository-level generation must handle cross-file dependencies, project APIs, types, and coding conventions.
- BM25, dense retrieval, and related methods can miss useful functions whose implementation steps resemble the target but use different vocabulary or serve another domain.
- Missing or misleading context can cause hallucinated APIs, invalid code, and lower generation accuracy.

## Approach
- Decompose repository functions and the target task into logical implementation steps, such as input validation or state transformation.
- Represent each step with an LLM reasoning-subspace projection derived from hidden states, then compare steps with cosine similarity.
- Reduce representation anisotropy by subtracting the mean and first principal component before similarity search.
- Use an agentic workflow to identify and validate procedurally similar functions, combine them with lexical and semantic context, and generate the target function with Qwen2.5-Coder-14B-Instruct.
- Run compiler and static-analysis feedback over generated code and iteratively repair detected errors.

## Results
- ProjAgent reaches 41.14% Pass@1 on the REPOCOD repository-level code-generation benchmark.
- The paper reports that this result outperforms existing retrieval-based baselines, but the provided excerpt does not include the baseline scores or the size of the improvement.
- The method retrieves cross-domain procedural matches such as validation steps in `BlackBody.evaluate` and `FLRW.m_nu`, despite low lexical overlap and no direct call dependency.
- PCA debiasing is reported to improve the discriminative value of procedural cosine similarity; the excerpt provides no separate ablation number.
- The provided text contains no further quantitative results for individual retrieval components or static-analysis repair.

## Link
- [https://arxiv.org/abs/2607.08691v1](https://arxiv.org/abs/2607.08691v1)
