---
kind: trend
trend_doc_id: 1791
granularity: day
period_start: '2026-07-07T00:00:00'
period_end: '2026-07-08T00:00:00'
topics:
- coding agents
- software verification
- agentic code review
- trajectory diagnostics
- agent reliability
- developer learning
run_id: materialize-outputs
aliases:
- recoleta-trend-1791
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-verification
- topic/agentic-code-review
- topic/trajectory-diagnostics
- topic/agent-reliability
- topic/developer-learning
language_code: en
pass_output_id: 310
pass_kind: trend_synthesis
---

# Coding agents need verifiers, reviewers, and trace-level repair

## Overview
The day’s research treats coding agents as systems that need external checks during work. Aria shows verifier-gated proof search at unusual scale; SWE-Review adds repository-aware review; TraceProbe measures how a run searches, edits, and validates. The current emphasis is reliability evidence inside the workflow, with final task scores treated as one signal among many.

## Findings

### Verifier-gated coding and proof generation
Aria is the sharpest result in the period. A general code agent writes Coq and Lean proofs while a harness rejects unsound outputs, altered lemmas, dropped obligations, divergent tactics, and unsafe shortcuts. The paper reports full coverage on all targeted proof sets: 4,257 Iris core lemmas, 217 Rust library lemmas built on Iris, 318 reglang theorems, and 72 Lean port lemmas.

SCOPE applies a related control pattern to ordinary code generation. A prover-initialized critic identifies missing semantic obligations in a draft program, then the coder revises against those subgoals. On LiveCodeBench V6, pass@1 reaches 39.4%, compared with 36.6% for Reflexion and 20.6% for coder-only generation. The strongest gains appear on tasks with concrete constraints that can be stated as subgoals.

### Repository-aware review and run diagnosis
SWE-Review makes code review part of the agent loop. The reviewer can inspect the repository, run commands, approve or request changes, and give repair guidance. On SWE-bench Verified, iterative generate-review-revise raises resolve rate for Qwen3-30B-A3B PRs to 56.9%, compared with a 27.5% no-review baseline. For Qwen3-Coder-30B-A3B, the same loop reaches 68.8%, compared with 50.9%.

TraceProbe adds process evidence to code-agent evaluation. It converts raw traces into nine action types and labels effects such as failed, reverted, off-anchor, or justified. In one SWE-Bench example, two agents both solve the task, but one finishes in 10 steps with no failed actions while another needs 49 steps with repeated recovery spans. That distinction matters for cost, review burden, and production trust.

### Agent infrastructure testing and runtime repair
LogicHunter targets failures in agent libraries such as LangChain, LlamaIndex, and CrewAI. It builds executable seed tests from source, type hints, schemas, documentation, and repository usage, then mutates valid API calls into behavioral probes. Its agent oracle inspects documentation, source, reproduction scripts, and runtime state before labeling a failure. The study reports 40 previously unknown bugs, with 30 confirmed and 26 fixed by developers.

AgentTether handles failures after a tool-using agent has already run. It turns a trajectory into linked transition units, localizes suspicious subtrajectories, and carries repair guidance into the next attempt. On 261 τ-bench tasks with Qwen3.7-max, it repaired 69.11% of initially failed tasks and beat blind retry by 26.02 percentage points overall.

### Developer skill support inside the IDE
The human side of agentic coding appears in two IDE-centered systems. Prompt Coach trains developers to write better code-generation prompts through scoring and Socratic questions tied to the local project. In a 15-developer study, one 60-minute session increased average prompt-quality score to 71.69, compared with 63.04 at baseline. The largest measured gains were in constraints, error handling, and context awareness.

SHIELD is less mature as evidence, but its target is concrete. It watches an agent’s code changes and reasoning trace, then turns selected concepts into probes, short lessons, and comprehension checks. The paper reports a working VSCode prototype and one payment-webhook walkthrough, but no user-study results or benchmark scores.
