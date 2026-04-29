---
kind: ideas
granularity: day
period_start: '2026-04-26T00:00:00'
period_end: '2026-04-27T00:00:00'
run_id: f9f4ae89-06b0-46d4-b288-2d12297bfb6b
status: succeeded
topics:
- coding-agents
- agent-evaluation
- benchmarks
- software-testing
- gpu-optimization
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/benchmarks
- topic/software-testing
- topic/gpu-optimization
language_code: en
pass_output_id: 111
pass_kind: trend_ideas
upstream_pass_output_id: 110
upstream_pass_kind: trend_synthesis
---

# Executable validation loops

## Summary
Executable evidence is moving into everyday engineering workflows. The clearest openings here are agent CI that points to the failing step, requirements-grounded test generation for business logic, and profiler-guided GPU optimization loops that validate each edit by running code.

## Step-level regression tracing for agent CI
Add a step-level failure graph to agent CI runs. The immediate user is the team already shipping multi-step agents with tool calls, where a failed end-to-end check still leaves an engineer digging through traces by hand. AgentEval gives a concrete template: score planning, tool selection, parameter generation, execution, and synthesis separately, then trace downstream failures back through dependencies. In the reported pilot, this cut median root-cause identification time from 4.2 hours to 22 minutes and caught 23 pre-release regressions over four months. A cheap first version does not need the full taxonomy. Start with one workflow, log each step and its parent steps, add typed pass/fail checks for the most common failure points, and surface the lowest-scoring upstream step when a run breaks. If that view shortens triage for one recurring failure class, the workflow is worth expanding.

### Evidence
- [AgentEval: DAG-Structured Step-Level Evaluation for Agentic Workflows with Error Propagation Tracking](../Inbox/2026-04-26--agenteval-dag-structured-step-level-evaluation-for-agentic-workflows-with-error-propagation-tracking.md): Provides the main results on failure-detection recall, root-cause accuracy, propagated errors, and the four-month CI/CD pilot with 23 regressions and faster debugging.
- [AgentEval: DAG-Structured Step-Level Evaluation for Agentic Workflows with Error Propagation Tracking](../Inbox/2026-04-26--agenteval-dag-structured-step-level-evaluation-for-agentic-workflows-with-error-propagation-tracking.md): Confirms the paper's framing of agent runs as evaluation DAGs with step-level metrics and automated root-cause attribution.

## Requirements-grounded unit test generation for business logic bugs
Generate tests from product requirements for code that carries business rules. This fits teams maintaining enterprise services where correctness depends on approval rules, policy checks, pricing conditions, or workflow constraints that live in PRDs and internal docs more than in the code itself. SeGa shows why this is now practical: it converts requirement documents into structured functionality entries, retrieves the relevant parts for a target method, turns them into explicit business scenarios, and uses those scenarios to drive unit test generation. On four industrial Go projects with 60 business-logic bugs, it found 29, while the compared baselines found 4 to 7. In six production repositories, developers confirmed and fixed 16 previously unknown bugs. A good first deployment target is one service with stable requirement documents and a backlog of escaped logic bugs. Measure confirmed bug yield per generated test batch, not only coverage or compile rate.

### Evidence
- [Uncovering Business Logic Bugs via Semantics-Driven Unit Test Generation](../Inbox/2026-04-26--uncovering-business-logic-bugs-via-semantics-driven-unit-test-generation.md): Summarizes the requirements-driven test generation method and reports bug detection and production findings.
- [Uncovering Business Logic Bugs via Semantics-Driven Unit Test Generation](../Inbox/2026-04-26--uncovering-business-logic-bugs-via-semantics-driven-unit-test-generation.md): States the core problem of business logic bugs and the semantics-driven test generation approach from requirement documents.

## Profiler-guided GPU patch generation with execution checks
Build a profiler-to-patch loop for GPU kernels that proposes edits only for measured bottlenecks and validates them by execution. The first users are performance engineers and HPC developers who already have profiler reports but still need manual translation from counters and stall traces into code changes. Optimas provides a concrete operating pattern: compress profiler output into small diagnostic summaries, restrict edits to the implicated regions, require each edit to cite the evidence it addresses, then compile, run, check correctness, and record the speedup. The paper reports 3,410 experiments with performance-improving runs above 98.82% and average speedups from 8.02% to 79.09%. It also reports that a code-only baseline produced no valid optimizations in the authors' setup. A low-cost trial is to take one kernel family with repeatable benchmarks, summarize the top hot kernels and dominant stall signals into a compact prompt, and compare measured gains against your current manual tuning queue.

### Evidence
- [Optimas: An Intelligent Analytics-Informed Generative AI Framework for Performance Optimization](../Inbox/2026-04-26--optimas-an-intelligent-analytics-informed-generative-ai-framework-for-performance-optimization.md): Contains the main claims on diagnostic-guided optimization, execution-based validation, experiment count, success rate, and speedups.
- [Optimas: An Intelligent Analytics-Informed Generative AI Framework for Performance Optimization](../Inbox/2026-04-26--optimas-an-intelligent-analytics-informed-generative-ai-framework-for-performance-optimization.md): Establishes the operational pain that profilers expose bottlenecks but do not generate concrete code changes.
