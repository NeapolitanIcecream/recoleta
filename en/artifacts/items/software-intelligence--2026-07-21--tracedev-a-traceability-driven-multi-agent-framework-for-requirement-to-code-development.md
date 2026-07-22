---
source: arxiv
url: https://arxiv.org/abs/2607.18886v1
published_at: '2026-07-21T09:14:59'
authors:
- Mingyu Chen
- Yakun Zhang
- Zihao Xie
- Yixing Luo
- Jinrui Xu
- Cuiyun Gao
- Kaiqi Zhao
- Yunming Ye
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
- requirements-traceability
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# TraceDev: A Traceability-Driven Multi-agent Framework for Requirement-to-Code Development

## Summary
TraceDev is a five-agent framework that generates repository-level code from complex, multi-step use cases. Its central mechanism is a heterogeneous traceability graph linking requirements, design models, and code so agents can detect omissions and refine artifacts.

## Problem
- Existing requirements-to-code systems often use simplified, single-sentence tasks that do not represent use cases with multiple functional points and semantic constraints.
- They generally lack explicit traceability between requirements, designs, and implementations, making omissions and cross-stage semantic errors difficult to detect.
- This matters because incomplete or incorrect repository-level implementations reduce functional correctness, maintainability, and confidence in automated software production.

## Approach
- TraceDev uses five role-specific LLM agents: Requirement Refiner, Designer, Developer, Tester, and Validator.
- The Requirement Refiner normalizes use-case terminology, infers missing subjects, rewrites ambiguous steps, and applies iterative syntactic verification.
- The Designer creates PlantUML class and sequence diagrams; the Developer generates code from those designs; and the Tester generates and executes tests, sending failures back for bounded self-correction.
- The Validator builds a heterogeneous directed graph containing requirement entities, design elements, and code files. LLM semantic matching links requirements to designs, while AST-based matching links designs to code and exposes missing implementations.

## Results
- Across the ETOUR and SMOS datasets, the evaluation covers 125 use cases and compares TraceDev with ChatDev and MetaGPT.
- On ETOUR, TraceDev reports a 71.72% semantic-coverage rate, exceeding ChatDev by 51.66% and MetaGPT by 75.14%.
- On ETOUR, TraceDev achieves a 53.63% success rate, exceeding ChatDev by 129.19% and MetaGPT by 186.64%.
- On SMOS, TraceDev achieves a 56.82% success rate, surpassing the baselines by up to 340.80%.
- The excerpt does not provide ablation results, statistical significance, execution cost, or complete per-dataset metrics, so it supports improved benchmark performance but not a separate causal measurement of the traceability graph's contribution.

## Link
- [https://arxiv.org/abs/2607.18886v1](https://arxiv.org/abs/2607.18886v1)
