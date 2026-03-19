---
source: arxiv
url: http://arxiv.org/abs/2603.01814v1
published_at: '2026-03-02T12:50:40'
authors:
- Mingwei Liu
- Zhenxi Chen
- Zheng Pei
- Zihao Wang
- Yanlin Wang
- Zibin Zheng
topics:
- repository-level-code-generation
- architecture-aware-retrieval
- multi-design-generation
- change-impact-analysis
- llm-software-engineering
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Architecture-Aware Multi-Design Generation for Repository-Level Feature Addition

## Summary
RAIM targets repository-level new feature addition, addressing the problem that LLMs in large codebases often "cannot see the architecture clearly and only follow a single path when modifying code." Through architecture-aware localization, multi-design generation, and impact-analysis-based selection, it achieves a new SOTA on NoCode-bench Verified.

## Problem
- The paper addresses **repository-level feature addition**: automatically implementing new functionality across an entire codebase based on documentation/specification changes, rather than merely fixing a single function or a single bug.
- This is important because adding new features requires understanding system architecture across files, finding the correct insertion points, and avoiding damage to existing functionality; the paper also notes that about **60%** of software maintenance cost is spent on feature addition rather than defect repair.
- The problems with existing methods are that they are "architecture-blind" to repository structure and often treat the codebase as unstructured text retrieval; at the same time, they use greedy single-path patch generation and lack systematic assessment of modification impact, making regressions easy to introduce.

## Approach
- RAIM first constructs a **repository-level code graph**, connecting files, classes, functions, and relationships such as `imports` / `calls` / `extends`. It performs multi-round search to first localize files and then functions, thereby identifying dispersed cross-file modification points.
- In function localization, it combines **LLM semantic judgment** and **embedding retrieval**: it first finds relevant functions from candidate files, then expands and reranks along code-graph neighbors over multiple rounds, gradually narrowing down to the truly relevant edit locations.
- It does not directly generate a single patch. Instead, it first asks the model to propose **multiple implementation designs (multi-design)**, where each design describes what targets to modify/create and the intent of the changes; it then generates corresponding patches for each design, expanding the solution space and reducing the chance of getting stuck in local optima.
- Finally, it uses **impact-aware patch selection** to choose the best patch: it performs static structural impact analysis, related regression test analysis, and new-feature test analysis, then scores candidates comprehensively across dimensions such as relevance, code quality, upstream/downstream safety, and regression safety.

## Results
- On **NoCode-bench Verified**, RAIM achieves a **39.47% success rate**, becoming the new SOTA; this is a **36.34%** improvement relative to the strongest baseline, **Agentless**.
- When using the open-source model **DeepSeek-v3.2**, RAIM still reaches a **34.21% success rate**; the paper claims this surpasses some baseline systems that use leading closed-source models.
- The paper states that RAIM demonstrates stable generalization across **7 LLMs**, with overall performance gains ranging from **9.7%–221.4%**.
- On complex **cross-file modification tasks**, RAIM reports a **191.7% relative improvement**, indicating that its architecture-aware localization and multi-design mechanism are especially effective for cross-module dependencies.
- The qualitative conclusion from the ablation study is that **multi-design generation** and **impact validation** are key modules that better handle complex dependencies and reduce coding errors; the excerpt does not provide more detailed ablation numbers.

## Link
- [http://arxiv.org/abs/2603.01814v1](http://arxiv.org/abs/2603.01814v1)
