---
source: arxiv
url: http://arxiv.org/abs/2604.05349v1
published_at: '2026-04-07T02:42:28'
authors:
- Donghee Hong
- Minjong Kim
- Sooyoung Cha
- Jaemin Jo
topics:
- visual-analytics
- symbolic-execution
- parameter-tuning
- software-testing
- human-in-the-loop
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# Symetra: Visual Analytics for the Parameter Tuning Process of Symbolic Execution Engines

## Summary
Symetra is a visual analytics system for tuning symbolic execution engines such as KLEE with human guidance. It helps users inspect which parameter settings affect branch coverage, find complementary configurations, and refine the search space for later tuning runs.

## Problem
- Symbolic execution engines expose many tunable parameters, and their interactions are hard to understand, so users often fall back to default settings that miss coverage.
- Automated tuners can improve branch coverage, but they give little insight into why a configuration works, which configurations are redundant, or which settings cause failures.
- Users often need several complementary configurations that cover different branches, not just one high-scoring run.

## Approach
- Symetra adds a human-in-the-loop visual interface on top of tuning runs. It treats the tuner as a black box and visualizes relationships between parameter configurations and branch coverage.
- The system gives two main overviews: a Parameter View for parameter impact on coverage values, and a Coverage View for coverage-pattern similarity across trials.
- For parameter impact, it fits an XGBoost surrogate model and uses SHAP values to estimate how each parameter and parameter value contributes to branch coverage, including comparison with default values.
- For coverage patterns, it embeds branch-coverage vectors with UMAP using Jaccard similarity so users can spot clusters, redundancy, and complementary trial groups.
- Users can create and compare trial groups, inspect merged coverage gains, and then narrow the parameter space by removing weak or failure-prone settings before the next experiment.

## Results
- The paper claims experts using Symetra improved over fully automated tuning in both branch coverage and tuning efficiency.
- It reports three evaluation modes: case studies, expert interviews, and a quantitative human-in-the-loop tuning process.
- The excerpt gives concrete scale numbers for the tuning setting: 61 KLEE parameters were included out of 148 total, experiments used a few hundred to a few thousand trials, and each trial was capped at 2 minutes.
- Benchmark programs named in the excerpt are gawk with 10,720 branches, gcal with 15,799 branches, and grep with 8,225 branches.
- An example interface state shows gcal with 2,200 trials and 15,799 branches; another example shows grep with 2,200 trials and 8,225 branches.
- The excerpt does not provide the actual quantitative improvement numbers against automated baselines, so the exact coverage or efficiency gains cannot be reported from the provided text.

## Link
- [http://arxiv.org/abs/2604.05349v1](http://arxiv.org/abs/2604.05349v1)
