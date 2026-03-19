---
source: arxiv
url: http://arxiv.org/abs/2603.01345v1
published_at: '2026-03-02T00:56:32'
authors:
- Thiago Santos
- Sebastiao Xavier
- Luiz Gustavo de Oliveira Carneiro
- Gustavo de Souza
topics:
- multi-objective-optimization
- visual-analytics
- llm-code-generation
- mcdm
- reproducible-workflows
relevance_score: 0.8
run_id: materialize-outputs
language_code: en
---

# PymooLab: An Open-Source Visual Analytics Framework for Multi-Objective Optimization using LLM-Based Code Generation and MCDM

## Summary
PymooLab is an open-source visual analytics framework built on top of pymoo, aiming to integrate modeling, experiment orchestration, result analysis, and decision support in multi-objective optimization into a single reproducible workflow. Its core selling point is using LLMs to generate pymoo-compatible code while directly providing experiment management and MCDM decision support in the interface.

## Problem
- Existing multi-objective optimization frameworks are mostly **code-centric**, requiring users to handwrite problem definitions, algorithm configurations, and post-processing pipelines, which creates a high barrier for domain experts without a software engineering background.
- Experimental reproducibility is often compromised: hyperparameters, evaluation budgets, random seeds, and runtime metadata are scattered across scripts, making them hard to record and audit consistently.
- Even when optimization algorithms can produce a Pareto front, users still lack easy-to-use visualization and decision support tools to understand trade-offs and select compromise solutions, limiting practical deployment value.

## Approach
- Build a GUI + backend bridging architecture on top of **pymoo**, decoupling interface interaction from optimization execution while preserving compatibility with the native pymoo ecosystem.
- Provide a **Test Module** and an **Experiment Module**: the former is for diagnostic validation of a single algorithm / single problem / single run, while the latter is for unified orchestration, aggregation, and statistical testing across multiple algorithms, multiple problems, and repeated runs.
- Introduce an **LLM Prompt Agent** that automatically converts natural-language problem descriptions into Python classes conforming to the pymoo vectorized interface, and integrates them into the local registry through syntax checking, compilation validation, and hot loading.
- Built-in **MCDM** decision support directly applies TOPSIS and weighted-sum methods to the final Pareto approximation set in the analysis interface, producing compromise points, scores, and traceable JSON decision snapshots.
- Strengthen deterministic execution and downstream reuse by recording hyperparameters, evaluation budgets, random seeds, backend selections, and structured result payloads; for computationally intensive scenarios, it can use pymoo's **JAX** acceleration path.

## Results
- The paper's main contribution is **system/framework design and workflow demonstration**. The excerpt **does not provide quantitative performance results on standard benchmarks**, nor does it report metrics such as HV, IGD, percentage runtime improvement, user study outcomes, or ablation experiment numbers.
- Explicitly claimed capabilities include converting experiments that originally required scripts for multiple algorithms / multiple problems / multiple runs into GUI-based orchestration, with export support for **CSV** and **LaTeX** statistical tables.
- In both single tests and large-scale experiments, the system automatically records metadata such as **hyperparameters, evaluation budgets, random seeds** to support auditing and reproducibility; however, it does not provide quantitative indicators such as reproduction success rate or error reduction.
- The LLM agent can turn natural-language requirements into executable pymoo-compatible code. The specific example given in the paper is "**implementing the IGD metric using p-norm for an arbitrary number of objectives**"; however, it does not provide code generation accuracy, pass rate, or time savings relative to manual coding.
- The MCDM module currently supports **TOPSIS** and **normalized weighted sum** methods, can highlight the selected compromise point in a 2D Pareto plot, and save the selection result as a **JSON sidecar**; however, it does not provide quantitative comparisons of decision quality or user efficiency.

## Link
- [http://arxiv.org/abs/2603.01345v1](http://arxiv.org/abs/2603.01345v1)
