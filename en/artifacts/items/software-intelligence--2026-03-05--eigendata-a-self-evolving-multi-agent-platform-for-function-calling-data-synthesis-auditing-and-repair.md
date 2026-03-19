---
source: arxiv
url: http://arxiv.org/abs/2603.05553v1
published_at: '2026-03-05T04:58:38'
authors:
- Jiaao Chen
- Jingyuan Qi
- Mingye Gao
- Wei-Chen Wang
- Hanrui Wang
- Di Jin
topics:
- multi-agent-systems
- function-calling
- data-synthesis
- benchmark-repair
- outcome-aware-evaluation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# EigenData: A Self-Evolving Multi-Agent Platform for Function-Calling Data Synthesis, Auditing, and Repair

## Summary
EigenData is a data infrastructure for function-calling agents that uses multiple agents to automatically generate, audit, and repair databases, tool environments, and multi-turn trajectories. The paper focuses on how it repairs the BFCL-V3 benchmark and proposes an outcome-aware evaluation that better reflects whether real tasks succeed.

## Problem
- Function-calling agents require high-quality, domain-specific training data, but manually constructing databases, tool implementations, and multi-turn trajectories is costly, slow, and difficult to keep globally consistent.
- Existing synthetic data/benchmarks often have systematic problems: bugs in function schemas or implementations, ambiguous user intent, and unreliable reference trajectories, which distort training and evaluation signals.
- Traditional evaluation based on turn-by-turn matching of function calls does not necessarily reflect whether a task was truly completed; a model may appear to "call correctly," while the database state and final result are actually wrong.

## Approach
- The paper proposes a self-evolving multi-agent platform in which the top-level orchestrator **EigenCore** coordinates three subsystems: **DatabaseAgent** generates realistic and consistent domain databases, **CodingAgent** generates and tests executable tools/environments, and **DataAgent** synthesizes and optimizes multi-turn function-calling trajectories.
- The system is end-to-end: from database schema and data population, to API/environment code, to SFT/RL trajectory generation; there is cross-component feedback between modules, so when inconsistencies are found, targeted repair is possible instead of rerunning the entire pipeline.
- CodingAgent uses a two-stage closed loop of "generate → unit test → debug → integration test," and employs JudgeAgent to determine whether failures come from code errors or test errors, improving the reliability of automatically generated environments.
- DataAgent uses hierarchical multi-agent generation and self-evolving prompt optimization: it first optimizes prompts on a small-scale pilot based on reviewer feedback, then performs continuous quality monitoring and correction during large-scale generation.
- In the case study, EigenData is used to systematically audit and repair BFCL-V3: it simultaneously fixes function schemas, code implementations, reference trajectories, and intent ambiguity, and adds outcome-aware evaluation that focuses on whether the final database state, key function calls, and handling of critical information are correct.

## Results
- The paper's core empirical conclusion is that **the repaired BFCL-V3 + outcome-aware metrics** produce model rankings that are **significantly more consistent** with human judgments of **functional correctness**; however, the excerpt **does not provide specific values** for correlation coefficients, accuracy, or ranking changes.
- The authors claim that EigenData can **systematically identify and automatically repair** schema, implementation, and reference trajectory errors in BFCL-V3, and disambiguate ambiguous intent; however, the excerpt **does not provide quantitative statistics** on the number of errors, repair rate, or coverage.
- Compared with the original BFCL-V3's turn-level function matching, the new evaluation focuses on whether the **database state changes correctly**, whether **key functions are actually invoked**, and whether **critical information is correctly processed/communicated**, thereby exposing failure modes that the original evaluation cannot detect.
- The paper also provides usable artifacts: it releases the **corrected BFCL-V3** data and a **CLI** supporting data generation, schema refinement, auditing, and repair; however, the excerpt **does not report** runtime cost, throughput, or the proportion of manual effort saved.

## Link
- [http://arxiv.org/abs/2603.05553v1](http://arxiv.org/abs/2603.05553v1)
