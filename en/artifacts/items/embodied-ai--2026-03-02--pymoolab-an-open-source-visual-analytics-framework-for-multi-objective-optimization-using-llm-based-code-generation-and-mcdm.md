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
- pymoo
- reproducibility
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# PymooLab: An Open-Source Visual Analytics Framework for Multi-Objective Optimization using LLM-Based Code Generation and MCDM

## Summary
PymooLab is an open-source visual analytics framework built on top of pymoo, designed to lower the programming barrier for multi-objective optimization and integrate experiment configuration, execution monitoring, result analysis, and decision support into a single workflow. Its core features are LLM-assisted code generation, auditable and reproducible experiment records, and embedded MCDM decision tools.

## Problem
- Existing multi-objective optimization frameworks are mostly code-centric: users must handwrite problem definitions, algorithm configurations, and analysis scripts, creating a high barrier for non-programmers.
- This fragmented workflow weakens reproducibility: hyperparameters, evaluation budgets, random seeds, and experiment metadata are easy to omit or manage inconsistently.
- Even after obtaining a Pareto front, users still lack a unified visualization and multi-criteria decision-support interface, making it difficult to make practical choices among candidate solutions.

## Approach
- Build a GUI + backend bridging architecture on top of pymoo, integrating testing, batch experiments, LLM modeling, extensibility, and MCDM analysis into a unified platform.
- Use an LLM Prompt Agent to convert natural-language requirements into vectorized Python code compatible with pymoo, and connect it to the local registry through syntax checking, compilation validation, and hot reloading.
- Support asynchronous diagnostics for single-algorithm, single-problem, single-run scenarios through the Test Module, with real-time display of convergence curves, Pareto fronts, and logs, so configuration issues can be identified before large-scale experiments.
- Use the Experiment Module to manage multi-algorithm, multi-problem, repeated experiments, uniformly configure FE budgets, seed strategies, and parallel execution, and export CSV/LaTeX statistical tables plus Wilcoxon/Friedman analyses.
- Embed MCDM directly into the analysis interface (such as TOPSIS and weighted sum) to select compromise solutions from the final Pareto solution set, and save decision snapshots as JSON for audit tracking.

## Results
- The paper’s main contribution is at the **system and workflow level**, rather than proposing a new optimization algorithm; the evidence provided is mainly architectural descriptions, interface demonstrations, and feature comparisons, and **the excerpt does not provide quantitative performance improvements on standard benchmarks**.
- It explicitly claims support for complete recording of experiment metadata, including **hyperparameters, evaluation budgets, random seeds**, to strengthen reproducibility, but does not report quantified results such as “reproducibility improved by X%.”
- It explicitly claims support for improved scalability in high-dimensional evaluations through pymoo’s native **JAX** acceleration pathway, but the excerpt **does not provide runtime, throughput, or speedup figures**.
- In terms of feature coverage, the authors position it as a more complete end-to-end platform than pymoo’s native code-based workflow: integrating **visual experimentation, LLM modeling, statistical summarization, and MCDM decision-making**, and making the source code publicly available, but without providing quantitative comparative experiments against frameworks such as PlatEMO, DESDEO, or pagmo.
- Demonstrative results include: the system can automatically summarize repeated experiment results into **mean ± standard deviation** tables, supports exporting **CSV** and **LaTeX**, supports nonparametric tests such as **Wilcoxon** and **Friedman**, and supports MCDM methods such as **TOPSIS** and **normalized weighted-sum**. These are explicit feature claims, but not performance metrics.

## Link
- [http://arxiv.org/abs/2603.01345v1](http://arxiv.org/abs/2603.01345v1)
