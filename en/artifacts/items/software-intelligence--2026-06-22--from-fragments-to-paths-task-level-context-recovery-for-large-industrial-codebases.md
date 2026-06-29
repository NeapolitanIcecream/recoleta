---
source: arxiv
url: https://arxiv.org/abs/2606.22906v1
published_at: '2026-06-22T06:44:51'
authors:
- Jiawei He
- Weisong Sun
- Mengyu Shi
- Jie Jia
- Tong Bian
- Xikai Yang
- Dong Sun
topics:
- code-intelligence
- repository-understanding
- software-agents
- context-retrieval
- automated-software-engineering
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# From Fragments to Paths: Task-Level Context Recovery for Large Industrial Codebases

## Summary
DeepDiscovery recovers task-level context in large codebases by finding reliable task anchors, then expanding along code, configuration, test, and organization links. The paper claims better relevant-file recovery in industrial repositories and a higher solve rate on SWE-bench Verified.

## Problem
- LLM coding systems often retrieve local code snippets, while repository tasks need connected files across interfaces, business logic, configuration, tests, and dependencies.
- Large industrial repositories change often, so pre-built vector indexes or static graphs can go stale and add maintenance cost.
- Missing bridge files, such as registration, dependency-injection, or test-to-implementation files, can reduce automated coding success.

## Approach
- DeepDiscovery uses a two-stage Location-Inference workflow: Location finds a small set of high-confidence task anchors, and Inference expands from those anchors to recover a broader implementation path.
- The Location stage scores candidate files using semantic and lexical match, compressed structural summaries, rule-template matches, and task-conditioned artifact-role priors.
- The Inference stage expands over a multi-relation repository graph covering explicit dependencies, implicit links such as configuration-to-code bindings, and organizational links such as folder and module proximity.
- A budget-aware priority score chooses expansion actions by estimated gain divided by cost, with default settings of 8 anchors, a 0.15 expansion stopping threshold, and a 0.62 full-text promotion threshold.
- The final context is metadata-first: most selected entities keep compact metadata, while likely modified or high-value files get full text.

## Results
- On 27 medium-scale tasks with 135 manually annotated gold relevant files, DeepDiscovery reports the best file-recovery quality among five baselines: DeepWiki, CodeWiki, RAG, GraphRAG, and AST+GraphRAG.
- The industrial repository setting covers 2.67 million lines of code and more than 25,000 files.
- In organization-internal industrial evaluations, DeepDiscovery improves Full Recall Rate by 2.5 to 7.4 percentage points on 27 medium-scale tasks across multiple AI coding systems.
- On 40 large-subproject industrial tasks, it improves Full Recall Rate by 1.6 to 9.2 percentage points across multiple AI coding systems.
- On SWE-bench Verified, the system with DeepDiscovery reaches a 78.6% Solve Rate, 8.2 percentage points above the corresponding baseline.

## Link
- [https://arxiv.org/abs/2606.22906v1](https://arxiv.org/abs/2606.22906v1)
