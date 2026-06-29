---
kind: ideas
granularity: day
period_start: '2026-06-04T00:00:00'
period_end: '2026-06-05T00:00:00'
run_id: 4f4e099a-184b-4335-bee0-5177dc0c722a
status: succeeded
topics:
- coding agents
- agent evaluation
- harness repair
- agent memory
- repository context
- software engineering
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/harness-repair
- topic/agent-memory
- topic/repository-context
- topic/software-engineering
language_code: en
pass_output_id: 231
pass_kind: trend_ideas
upstream_pass_output_id: 230
upstream_pass_kind: trend_synthesis
---

# Coding Agent Feedback Loops

## Summary
Coding-agent evaluation is becoming more useful when it records the whole operating loop: the request, the trace, the feedback, the harness change, and the next attempt. The practical work is to build small evaluators around failed trajectories, browser-visible UI behavior, and measured repository memory before scaling agent use across more teams.

## Trace-based harness repair queue for coding agents
Teams running coding agents should add a repair queue for failed trajectories. The queue should store tool calls, observations, file changes, final submissions, and the harness code version that produced each run. A reviewer or repair agent can then assign each failure to a concrete harness area such as tool schema, context assembly, lifecycle control, logging, verification, sandboxing, or policy checks.

HarnessFix gives a useful pattern: convert raw traces into step-level records, link each bad outcome to a harness layer, generate a scoped patch, and validate that the patch reduces the target flaw without broad regressions. RHO adds a lighter deployment loop for teams without labeled validation sets: pick hard and varied past failures, rerun them, let the agent compare its own rollouts, and accept the harness update preferred over the baseline. A small first test could use 20 to 30 recent failed coding-agent jobs, with a held-out slice of similar issues used only after candidate patches are chosen.

### Evidence
- [From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws](../Inbox/2026-06-04--from-failed-trajectories-to-reliable-llm-agents-diagnosing-and-repairing-harness-flaws.md): HarnessFix grounds harness repair in failed execution traces, harness layers, scoped patches, and held-out gains across four benchmarks.
- [Retrospective Harness Optimization: Improving LLM Agents via Self-Preference over Trajectory Rollouts](../Inbox/2026-06-04--retrospective-harness-optimization-improving-llm-agents-via-self-preference-over-trajectory-rollouts.md): RHO shows a self-supervised harness update loop using past trajectories, hard-task selection, rollout comparison, and held-out pass-rate gains without external grading.

## Browser-feedback test runs for generated web applications
Web teams evaluating coding agents should test agents through a deployed UI, not only through source diffs or unit tests. A practical setup is a hidden product-requirements file, an intentionally incomplete user request, browser tests for visible behavior, and two or three feedback rounds where failures are converted into plain-language user feedback.

Asuka-Bench shows why this is worth building for web-app agents. It starts with underspecified requests, hides the full clarified requirements, tests rendered browser behavior, and sends direct failure feedback into later rounds. Across 13 model-runtime configurations, three-round weighted Task Pass Rate spans 51.8% to 90.1%, so the loop separates configurations that may look similar in one-shot code generation. The first internal version can be small: 10 common UI tasks, Playwright checks arranged by prerequisite behavior, and a score split between first-pass success and recovery after feedback.

### Evidence
- [Asuka-Bench: Benchmarking Code Agents on Underspecified User Intent and Multi-Round Refinement](../Inbox/2026-06-04--asuka-bench-benchmarking-code-agents-on-underspecified-user-intent-and-multi-round-refinement.md): Asuka-Bench evaluates web-app code agents with hidden requirements, browser-rendered checks, multi-round feedback, and large performance spread across configurations.

## Metric-gated repository memory for software-engineering agents
Repository memory should have an admission test before it is added to a coding agent’s context. A useful gate compares the same task with and without a candidate memory and keeps the memory only when measured outcomes stay unchanged or improve, with at least one gain on success, localization, resolve efficiency, or related task metrics.

MemOp reports this kind of utility test for software-engineering agents, with accepted memories trained from trajectory-based rejection sampling and evaluated on SWE-Bench Verified. The reported gains include up to 5.25 percentage points in single-episode success rate and at least 9.79% lower compute cost. CL-Bench adds a check on adoption: full-context in-context learning with Claude Sonnet 4.6 beats several dedicated memory systems on aggregate normalized reward and gain. A team can start by measuring its best long-context baseline against a memory-gated variant on repeated tasks from the same repository before saving agent-written notes for general reuse.

### Evidence
- [Enhancing Software Engineering Through Closed-Loop Memory Optimization](../Inbox/2026-06-04--enhancing-software-engineering-through-closed-loop-memory-optimization.md): MemOp defines memory utility by downstream task metrics and reports success-rate and compute-cost gains for software-engineering agents.
- [Continual Learning Bench: Evaluating Frontier AI Systems in Real-World Stateful Environments](../Inbox/2026-06-04--continual-learning-bench-evaluating-frontier-ai-systems-in-real-world-stateful-environments.md): CL-Bench finds that full-context in-context learning outperforms several dedicated memory systems on aggregate results, which supports baseline comparison before memory adoption.
