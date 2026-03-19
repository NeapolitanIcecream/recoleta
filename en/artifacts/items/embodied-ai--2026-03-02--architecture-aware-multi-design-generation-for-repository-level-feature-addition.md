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
- software-engineering
- architecture-aware-retrieval
- multi-design-generation
- impact-analysis
- llm-code-agents
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Architecture-Aware Multi-Design Generation for Repository-Level Feature Addition

## Summary
RAIM is a code generation framework for repository-level new feature addition, aiming to maintain architectural consistency and reduce regressions when making cross-file, cross-module changes. It improves the success rate of LLMs on complex codebase evolution tasks through "architecture-aware localization + multi-design generation + impact-analysis-based selection."

## Problem
- It addresses **repository-level new feature addition**: automatically generating cross-file patches in an existing large codebase based on documentation or requirement changes, rather than only fixing a single function or a single bug.
- This matters because adding features accounts for a large share of real-world software maintenance; the task requires understanding the global architecture, dependency relationships, and correct insertion points, otherwise existing functionality can easily be broken.
- The main problems with existing methods are **architectural blindness** and **single-path greedy generation**: they treat the repository as unstructured text retrieval, and often accept the first seemingly workable patch, lacking systematic regression and impact evaluation.

## Approach
- First, it builds a **repository-level code graph** representing files, classes, functions, and relationships such as `imports`, `calls`, and `extends`, then uses multi-round search for file-level and function-level localization to identify the truly relevant modification points.
- In function localization, it combines **LLM semantic judgment** with **embedding retrieval**: it first gets candidates from the feature description and file skeleton, then continues iterative retrieval along code-graph neighbors, and finally uses the LLM to rerank and select the most relevant functions.
- Instead of directly generating a single patch, it first asks the model to propose multiple **implementation designs**, each specifying which targets to modify/create and the high-level modification logic, thereby expanding the solution space.
- For each design, it independently localizes line-level edit positions and generates candidate patches, then performs **impact-aware selection**: combining static code subgraph analysis, regression test analysis, and new-feature test analysis to score patches on dimensions such as relevance, code quality, upstream/downstream safety, and regression safety, and select the best one.

## Results
- On **NoCode-bench Verified**, RAIM achieves a **39.47% success rate**, which the paper describes as a new **SOTA** for this task.
- Compared with the strongest baseline, **Agentless**, RAIM achieves a **36.34% relative improvement**.
- Using the open-source model **DeepSeek-v3.2**, RAIM still reaches a **34.21% success rate**, and the paper claims it surpasses some baseline systems powered by leading closed-source models.
- The method shows generalization across **7 LLMs**, with reported performance gains ranging from **9.7%–221.4%**.
- On complex **cross-file modification tasks**, the paper reports a **191.7% relative improvement**, indicating that architecture-aware localization and multi-design selection are especially effective in dependency-heavy scenarios.
- The qualitative conclusion of the ablation study is that **multi-design generation** and **impact validation** are key modules; the excerpt does not provide more detailed ablation numbers.

## Link
- [http://arxiv.org/abs/2603.01814v1](http://arxiv.org/abs/2603.01814v1)
