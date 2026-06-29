---
kind: trend
trend_doc_id: 1345
granularity: day
period_start: '2026-06-04T00:00:00'
period_end: '2026-06-05T00:00:00'
topics:
- coding agents
- agent evaluation
- harness repair
- agent memory
- repository context
- software engineering
run_id: materialize-outputs
aliases:
- recoleta-trend-1345
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-evaluation
- topic/harness-repair
- topic/agent-memory
- topic/repository-context
- topic/software-engineering
language_code: en
pass_output_id: 230
pass_kind: trend_synthesis
---

# Full operating loops define agentic coding evaluation

## Overview
The day’s strongest signal is operational evaluation for coding agents. Papers test feedback rounds, harness repair, stateful memory, and repository knowledge under deployment-like conditions. The practical question is whether an agent improves after evidence appears in traces, UI tests, commits, or repeated tasks.

## Clusters

### Closed-loop code-agent evaluation
Asuka-Bench evaluates web-app agents under vague initial requests and multi-round user feedback. The benchmark hides the full product requirements, tests rendered browser behavior, and sends direct failure feedback into later rounds. The reported spread is large: after three rounds, weighted task pass rate ranges from 51.8% to 90.1% across 13 model-runtime configurations.

ADK Arena treats Agent Development Kits (ADKs) as measurable engineering choices. One coding agent builds benchmark agents for 51 Python kits inside isolated Docker environments. Generation succeeds in 57% of runs, while cost varies 5.6x across kits. The best single-benchmark agents reach 80% task resolution, and the median kit reaches 32%.

#### Evidence
- [Asuka-Bench: Benchmarking Code Agents on Underspecified User Intent and Multi-Round Refinement](../Inbox/2026-06-04--asuka-bench-benchmarking-code-agents-on-underspecified-user-intent-and-multi-round-refinement.md): Summary covers Asuka-Bench task design, feedback loop, dataset size, and reported pass-rate spread.
- [ADK Arena: Evaluating Agent Development Kits via LLM-as-a-Developer](../Inbox/2026-06-04--adk-arena-evaluating-agent-development-kits-via-llm-as-a-developer.md): Summary covers ADK Arena methodology, 51 kits, generation success, cost range, and task-resolution results.

### Harness repair from failed trajectories
Two papers make the agent harness a target for measured repair. Retrospective Harness Optimization selects hard past tasks, reruns them, asks the agent to diagnose its own rollouts, and chooses a harness update through self-preference. On SWE-Bench Pro, it raises held-out pass rate from 0.59 to 0.78 without external grading.

HarnessFix gives the repair process finer grounding. It converts failed traces and harness code into step-level records, links failures to execution, tooling, context, lifecycle, observability, verification, or governance layers, and applies scoped patches. Across SWE-Bench Verified, Terminal-Bench 2.0 Verified, GAIA, and AppWorld, the paper reports 15.2% to 50.0% held-out performance gains over initial harnesses.

#### Evidence
- [Retrospective Harness Optimization: Improving LLM Agents via Self-Preference over Trajectory Rollouts](../Inbox/2026-06-04--retrospective-harness-optimization-improving-llm-agents-via-self-preference-over-trajectory-rollouts.md): Summary describes RHO's trajectory selection, self-validation, self-preference, and benchmark gains.
- [From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws](../Inbox/2026-06-04--from-failed-trajectories-to-reliable-llm-agents-diagnosing-and-repairing-harness-flaws.md): Summary describes HarnessFix trace representation, harness-layer diagnosis, scoped repairs, and reported gains.

### Memory and repository context
Memory work is being judged by downstream task effect, not by whether a note looks useful. MemOp accepts a memory only when it leaves all measured metrics unchanged or better and improves at least one. It reports up to 5.25 percentage-point single-episode success gains and at least 9.79% compute-cost reduction.

CL-Bench adds a caution: dedicated memory systems do not automatically beat full-context in-context learning. Across six domains, full-context in-context learning with Claude Sonnet 4.6 leads the aggregate results, while Mem0 and ACE trail it on normalized reward and gain.

Repository adaptation is another route. Code2LoRA generates repository-specific low-rank adapters from codebase embeddings, with an evolution mode updated by commit diffs. On RepoPeftBench, the static version reaches 63.8% cross-repository exact match, and the evolution version reaches 60.3% cross-repository exact match on evolving repositories.

#### Evidence
- [Enhancing Software Engineering Through Closed-Loop Memory Optimization](../Inbox/2026-06-04--enhancing-software-engineering-through-closed-loop-memory-optimization.md): Summary covers MemOp's utility test, training data, downstream metrics, success gains, and cost reduction.
- [Continual Learning Bench: Evaluating Frontier AI Systems in Real-World Stateful Environments](../Inbox/2026-06-04--continual-learning-bench-evaluating-frontier-ai-systems-in-real-world-stateful-environments.md): Summary covers CL-Bench design and the finding that full-context in-context learning beats dedicated memory systems on average.
- [Code2LoRA: Hypernetwork-Generated Adapters for Code Language Models under Software Evolution](../Inbox/2026-06-04--code2lora-hypernetwork-generated-adapters-for-code-language-models-under-software-evolution.md): Summary covers Code2LoRA's repository-specific adapters, evolution mode, RepoPeftBench, and exact-match results.
