---
kind: trend
trend_doc_id: 728
granularity: week
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-27T00:00:00'
topics:
- coding-agents
- evaluation
- repo-level-codegen
- execution
- agent-harness
run_id: materialize-outputs
aliases:
- recoleta-trend-728
tags:
- recoleta/trend
- topic/coding-agents
- topic/evaluation
- topic/repo-level-codegen
- topic/execution
- topic/agent-harness
language_code: en
pass_output_id: 112
pass_kind: trend_synthesis
---

# Coding-agent research is being judged by runnable proof, repo realism, and harness quality

## Overview
This week’s coding-agent research is strongest when claims end in runnable evidence. Benchmarks and systems keep asking whether code builds, executes, and survives workflow checks. The same corpus also keeps surfacing two constraints: repo-scale work still fails often, and harness choices can change results as much as the model.

## Clusters

### Executable evidence is the main standard
Evaluation kept tightening around executable proof. Daily trend documents across the week repeatedly favor systems scored by full runs, tool traces, state changes, and live workflow survival. The item-level evidence adds the same message at repository scale: RealBench tests code generation with real repositories, UML design inputs, and human-verified tests, and the best average Pass@1 is still 19.39%. The week reads as a demand for runnable artifacts, not polished code text.

#### Evidence
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): Item-level benchmark shows low repo-scale pass rates despite structured design inputs and test-backed evaluation.

### Repo-scale automation still breaks on setup and complexity
Repository-scale coding still has a hard ceiling. RealBench reports that performance falls from above 40% Pass@1 on repositories under 500 LOC to below 15% above 2000 LOC. RAT shows why environment setup matters so much in this regime: its automated configuration pipeline raises executable setup success across Python, Java, Rust, and JS/TS, but it also carries real cost in tokens and time. The practical story this week is simple: getting code to run is still a major part of the task.

#### Evidence
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): Benchmark provides concrete repo-size performance degradation and low overall Pass@1.
- [RAT: RunAnyThing via Fully Automated Environment Configuration](../Inbox/2026-04-25--rat-runanything-via-fully-automated-environment-configuration.md): Environment-configuration study quantifies setup gains along with token and latency costs.

### Harness design is becoming core model work
Agent quality depends heavily on the harness around the model. The week’s trend coverage points to scaffolding, documentation, and control surfaces as outcome-critical variables. HARBOR makes that claim concrete: in its manual tuning study, a modest flag set improved Terminal-Bench 2 results from 15/89 to 17/89, while later stacks with extra self-evaluation and reflection features fell to 13/89 and 12/89. Better agent behavior here comes from disciplined configuration work, not just choosing a stronger model.

#### Evidence
- [HARBOR: Automated Harness Optimization](../Inbox/2026-04-22--harbor-automated-harness-optimization.md): Item-level case study shows manual stacking of harness features can reduce pass rate.
