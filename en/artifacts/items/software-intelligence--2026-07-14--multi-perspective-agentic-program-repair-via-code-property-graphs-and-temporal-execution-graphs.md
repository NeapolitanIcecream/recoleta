---
source: arxiv
url: https://arxiv.org/abs/2607.12605v1
published_at: '2026-07-14T10:33:29'
authors:
- Zhili Huang
- Ling Xu
- Hongyu Zhang
topics:
- automated-program-repair
- code-intelligence
- multi-agent-software-engineering
- program-analysis
- agentic-software-engineering
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Multi-Perspective Agentic Program Repair via Code Property Graphs and Temporal Execution Graphs

## Summary
CT-Repair improves automated program repair by organizing static and runtime evidence into queryable graphs and assigning separate agents to static, dynamic, and hybrid diagnoses. On Defects4J v3.0, it correctly repairs 489 of 854 Java bugs in a mixed-model configuration and 388 bugs under a controlled GPT-5.4-mini setting.

## Problem
- Raw execution traces are large and repetitive, making relevant failure evidence difficult for language models to retrieve; a 100-bug study found an average of 2.38 million runtime events per bug, with 99.95% classified as repetitive.
- Repeated patch sampling can produce different implementations without producing different root-cause hypotheses or repair strategies.
- The problem matters because APR needs compact behavioral evidence and genuinely diverse diagnoses to repair complex bugs within limited model context and generation budgets.

## Approach
- CT-Repair builds a Code Property Graph with Joern for syntax, control flow, data flow, and call relations, and a Temporal Execution Graph for timestamped method calls, states, branches, and execution order.
- A three-stage filtering pipeline removes unexecuted methods, structurally simple methods, and runtime records disconnected from valid execution flows before constructing the TEG.
- Three finite-state-machine-guided agents independently analyze each bug from static, dynamic, and hybrid perspectives, query relevant graph evidence, form root-cause hypotheses, and produce repair strategies.
- Strategy-guided round-robin generation turns each strategy into candidate patches, validates them through compilation and tests, scores failures fixed versus new failures introduced, and refines the strongest strategy when needed.

## Results
- On 854 real-world Java bugs from Defects4J v3.0, CT-Repair correctly repairs 489 bugs in its mixed-model configuration.
- With GPT-5.4-mini used in a controlled comparison, it correctly repairs 388 bugs: 19 more than ReinFix and 30 more than RepairAgent, a reported relative improvement of 5.15% over ReinFix.
- Combining the static, dynamic, and hybrid perspectives repairs 99 more bugs than the strongest individual perspective, supporting complementarity among the reasoning paths.
- Execution filtering narrows the candidate method scope by 94.85% on average, and behavior filtering reduces retained runtime records by a further 55.97%.
- The evidence is limited to the Defects4J Java benchmark and uses perfect fault localization; the excerpt does not establish performance on other languages, benchmarks, or imperfect localization settings.

## Link
- [https://arxiv.org/abs/2607.12605v1](https://arxiv.org/abs/2607.12605v1)
