---
kind: trend
trend_doc_id: 665
granularity: day
period_start: '2026-04-26T00:00:00'
period_end: '2026-04-27T00:00:00'
topics:
- coding-agents
- agent-evaluation
- benchmarks
- software-testing
- gpu-optimization
run_id: materialize-outputs
aliases:
- recoleta-trend-665
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-evaluation
- topic/benchmarks
- topic/software-testing
- topic/gpu-optimization
language_code: en
pass_output_id: 110
pass_kind: trend_synthesis
---

# Executable evidence now sets the pace for coding and agent research

## Overview
This period’s strongest work tightens the link between generation and executable evidence. KISS Sorcar, AgentEval, and ClawMark all score systems on what they can finish, trace, or survive in live workflows. SeGa and Optimas extend the same idea into requirements-based testing and profiler-guided optimization, with concrete gains on real bugs and measured speedups.

## Clusters

### Execution discipline in coding agents
Coding-agent papers keep adding execution discipline around long tasks. KISS Sorcar uses forced continuation summaries, tool access, and git worktree isolation to keep repo edits reviewable and recoverable. It reports a 62.2% pass rate on Terminal Bench 2.0 with Claude Opus 4.6, slightly above Claude Code at 58% and Cursor Composer 2 at 61.7%. The details matter: only 43.8% of tasks pass in all five trials, and 19 tasks always fail. The result is better repo handling, not stable autonomy.

#### Evidence
- [KISS Sorcar: A Stupidly-Simple General-Purpose and Software Engineering AI Assistant](../Inbox/2026-04-26--kiss-sorcar-a-stupidly-simple-general-purpose-and-software-engineering-ai-assistant.md): Summary and benchmark results for KISS Sorcar

### Benchmarks are testing failure paths, not just final answers
Evaluation work is getting more granular and more operational. AgentEval scores plan, tool, parameter, execution, and synthesis steps as a dependency graph, then traces downstream failures back to likely source steps. On 150 human-annotated cases it reaches 0.89 failure-detection recall, above 0.41 for end-to-end checks and 0.67 for flat step scoring. In a four-month pilot, it found 23 pre-release regressions and cut median root-cause identification time from 4.2 hours to 22 minutes. ClawMark pushes the same pressure into benchmarking: 100 multi-day office tasks, five stateful services, 1,072 raw multimodal artifacts, and rule-based scoring. The top weighted score is 75.8, but strict task success peaks at 20.0%, which keeps the benchmark tied to complete workflow completion rather than partial progress alone.

#### Evidence
- [AgentEval: DAG-Structured Step-Level Evaluation for Agentic Workflows with Error Propagation Tracking](../Inbox/2026-04-26--agenteval-dag-structured-step-level-evaluation-for-agentic-workflows-with-error-propagation-tracking.md): Step-level DAG evaluation metrics and pilot results
- [ClawMark: A Living-World Benchmark for Multi-Turn, Multi-Day, Multimodal Coworker Agents](../Inbox/2026-04-26--clawmark-a-living-world-benchmark-for-multi-turn-multi-day-multimodal-coworker-agents.md): Benchmark design and task-success results for dynamic coworker agents

### External evidence is steering code generation
Grounding generation in external evidence shows up in both testing and optimization. SeGa builds tests from product requirements, not only code context. On four industrial Go projects with 60 business-logic bugs, it detects 29 bugs; the compared baselines find 4 to 7. In six production repositories, developers confirmed and fixed 16 previously unknown bugs found by the system. Optimas does the same kind of grounding for GPU tuning. It compresses profiler output into compact diagnostic summaries, then requires edits to target the measured bottlenecks. The paper reports 3,410 experiments, more than 98.82% performance-improving runs, and average speedups ranging from 8.02% to 79.09%. A code-only baseline produced no valid optimizations in the authors' setup.

#### Evidence
- [Uncovering Business Logic Bugs via Semantics-Driven Unit Test Generation](../Inbox/2026-04-26--uncovering-business-logic-bugs-via-semantics-driven-unit-test-generation.md): Requirement-grounded test generation and industrial bug-finding results
- [Optimas: An Intelligent Analytics-Informed Generative AI Framework for Performance Optimization](../Inbox/2026-04-26--optimas-an-intelligent-analytics-informed-generative-ai-framework-for-performance-optimization.md): Profiler-guided GPU optimization pipeline and large-scale experiment results
