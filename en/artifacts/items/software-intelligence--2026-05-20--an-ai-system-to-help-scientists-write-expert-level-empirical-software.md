---
source: hn
url: https://www.nature.com/articles/s41586-026-10658-6
published_at: '2026-05-20T23:54:12'
authors:
- anigbrowl
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- generative-engineering
- ai-for-science
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# An AI system to help scientists write expert-level empirical software

## Summary
ERA is an LLM plus tree-search system that writes scientific software for empirical tasks and optimizes a task-specific quality metric. The excerpt claims it beats strong human or institutional baselines across bioinformatics, epidemiology, and other scientific domains.

## Problem
- Scientific discovery can slow down when researchers must write custom software for computational experiments by hand.
- Many empirical tasks have large design spaces, so one-pass code generation can miss better algorithms or model variants.
- Better automated software generation matters because it can test more ideas and reduce the time needed to build experiment-specific tools.

## Approach
- ERA uses an LLM to propose, implement, and revise scientific software.
- Tree search keeps multiple candidate solution paths, scores them with a quality metric, and expands the strongest branches.
- The system can read and use external research ideas, then test whether the resulting code improves the metric.
- It treats software creation as iterative optimization: generate code, evaluate it, keep strong variants, and search again.

## Results
- Bioinformatics: ERA discovered 40 novel methods for single-cell data analysis that outperformed the top human-developed methods on a public leaderboard.
- Epidemiology: ERA generated 14 COVID-19 hospitalization forecasting models that outperformed the CDC ensemble and all other individual models in the reported benchmark.
- Other domains: the excerpt says ERA produced expert-level software in 4 additional areas: geospatial analysis, zebrafish neural activity prediction, numerical integration, and time-series forecasting.
- The excerpt reports no aggregate metric values, error rates, or leaderboard scores beyond the counts of 40 methods and 14 models plus the stated baseline wins.

## Link
- [https://www.nature.com/articles/s41586-026-10658-6](https://www.nature.com/articles/s41586-026-10658-6)
