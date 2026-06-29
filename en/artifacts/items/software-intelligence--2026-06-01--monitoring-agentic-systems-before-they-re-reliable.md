---
source: arxiv
url: https://arxiv.org/abs/2606.02494v1
published_at: '2026-06-01T17:01:53'
authors:
- Marisa Ferrara Boston
- Glen Hanson
- Effi Georgala
- JD Hudgens
- Heather Frase
topics:
- agentic-systems
- agent-monitoring
- ai-ops
- fmea-triage
- reliability-engineering
- human-in-the-loop
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Monitoring Agentic Systems Before They're Reliable

## Summary
This paper claims early production agentic systems need structural monitoring before task-level error detection works. It tests a variance-based monitoring and FMEA triage method on a synthetic audit-agent testbed and finds that monitor scope predicts the kind of failure found.

## Problem
- Early agentic systems often fail because stages, tools, or data paths are poorly integrated, so task-level monitors may miss the real cause.
- Mean accuracy and threshold alerts can hide rare high-risk failures in regulated workflows such as audit, finance, healthcare, and legal services.
- Human reviewers need severity routing because raw monitoring findings can create more review work than teams can handle.

## Approach
- The method scores agent behavior across three dimensions: quality, suitability, and efficiency.
- It uses three monitoring scopes: within-run monitors for variation inside one execution, cross-run monitors for variation across repeated executions, and structural monitors for integration gaps.
- Variance is a main signal. The paper uses z-scores with thresholds of 2.0 for most evaluators and 3.0 for timing-sensitive evaluators, plus coefficient of variation to characterize monitor classes.
- Findings are sent into an FMEA-style triage process with four severity levels: L1 catastrophic, L2 critical, L3 marginal, and L4 negligible.
- The evaluation uses 120 synthetic audit document bundles: 20 clean bundles and 100 error bundles across 5 error subtypes, 4 difficulty levels, and 5 document sets per cell, processed in 220 runs.

## Results
- Within-run monitors found deterministic stage defects with low variation: CV = 0.02. These produced high-volume, low-severity L3 findings.
- Cross-run monitors found stochastic integration consequences with high variation: CV = 1.25, with 24% of findings classified as L2 critical.
- The structural monitor found an integration gap with perfect consistency: CV = 0.00 across runs.
- Injected task-level errors were statistically indistinguishable from clean baselines, including 100 injected errors, supporting the claim that structural defects can mask task-level signals in immature systems.
- Deterministic triage routed all 10,210 L3 findings to automated monitoring and all 243 L2 findings to human investigation, reported as a 43x reduction in analyst review volume.
- The abstract also reports that 97% of findings went to automated tracking and about 2% went to human investigation for variable system behavior.

## Link
- [https://arxiv.org/abs/2606.02494v1](https://arxiv.org/abs/2606.02494v1)
