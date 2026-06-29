---
kind: ideas
granularity: week
period_start: '2026-06-08T00:00:00'
period_end: '2026-06-15T00:00:00'
run_id: 918fe7a0-24e9-4425-a9e9-4380d2d34aba
status: succeeded
topics:
- coding agents
- agent governance
- software engineering benchmarks
- agent memory
- runtime enforcement
- formal methods
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-governance
- topic/software-engineering-benchmarks
- topic/agent-memory
- topic/runtime-enforcement
- topic/formal-methods
language_code: en
pass_output_id: 259
pass_kind: trend_ideas
upstream_pass_output_id: 258
upstream_pass_kind: trend_synthesis
---

# Coding Agent Runtime Controls

## Summary
Coding-agent adoption now has concrete work to do around the runtime loop: enforce repeated user corrections before completion, compare agent harnesses under one scoring contract, and give agents a local record of prior fixes and failed attempts before they edit a file.

## Pre-completion verifiers for repeated coding-agent corrections
Teams using coding agents can add a small enforcement layer for recurring user corrections: extract durable rules from chat history, attach an applicability check, and run a verifier before the agent can mark a task complete. The first useful rules are ordinary ones developers already repeat, such as cleaning temporary debug files, asking before modifying state, avoiding a banned command, or running a required test before proposing a patch.

Trace gives a concrete pattern for this. It rewrites user corrections into atomic rules, resolves them against a per-user rule library, and compiles each rule into an applicability check, an instruction, and a verifier. In the reported diagnostic set, Mem0 still left 57.5% of applicable preference checks violated. On ClawArena, Trace cut held-out preference violations from 100.0% to 37.6% in distribution and to 2.0% out of distribution.

A practical pilot would start with 20 recent coding-agent transcripts, select the five corrections that users repeated most often, and implement them as blocking checks in the agent’s finish step. The measure is simple: count how often those five corrections are violated in held-out tasks and how many extra user turns the agent needs.

### Evidence
- [Getting Better at Working With You: Compiling User Corrections into Runtime Enforcement for Coding Agents](../Inbox/2026-06-11--getting-better-at-working-with-you-compiling-user-corrections-into-runtime-enforcement-for-coding-agents.md): Trace describes correction mining, rule compilation, runtime verifiers, and reported violation-rate reductions.
- [Getting Better at Working With You: Compiling User Corrections into Runtime Enforcement for Coding Agents](../Inbox/2026-06-11--getting-better-at-working-with-you-compiling-user-corrections-into-runtime-enforcement-for-coding-agents.md): The source gives concrete examples of executable coding-agent corrections, including cleanup, command, and workspace conditions before termination.

## Fixed-harness evaluation runs for coding-agent selection
Engineering teams comparing coding agents should test the harness as a product component, with the task set, prompt template, Docker workspace, wall-clock budget, patch extraction, prediction format, evaluator, API cost, and wall-clock time held constant. This is useful for procurement and internal adoption because an agent’s result can change with the adapter and execution contract, even when the base model is unchanged.

Claw-SWE-Bench shows the size of the effect. On its 350-instance multilingual benchmark, OpenClaw with a minimal direct-diff adapter reached 19.1% Pass@1, while the full adapter reached 73.4% with the same GLM 5.1 model. Across sweeps, harness choice changed Pass@1 by up to 27.4 percentage points under fixed models. The Lite-80 subset tracked the full benchmark closely and cost about 22.9% of a full run, which makes repeated harness checks more practical.

A team evaluating two or three coding-agent products can borrow this structure without adopting the whole benchmark. Pick a small set of internal issue-resolution tasks, require every system to return a repository diff under the same timeout and tool permissions, and report pass rate next to total tokens, cache reads, wall time, and failed patch extraction cases.

### Evidence
- [Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks](../Inbox/2026-06-10--claw-swe-bench-a-benchmark-for-evaluating-openclaw-style-agent-harnesses-on-coding-tasks.md): Claw-SWE-Bench fixes the evaluation contract and reports large differences from adapter and harness choices under fixed models.
- [Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks](../Inbox/2026-06-10--claw-swe-bench-a-benchmark-for-evaluating-openclaw-style-agent-harnesses-on-coding-tasks.md): The paper abstract reports the 19.1% versus 73.4% Pass@1 adapter result and notes cost differences among similarly accurate systems.

## Local project event logs with edit prechecks for coding agents
Repository teams can reduce repeated debugging loops by giving coding agents a local event log before they edit files. The useful minimum is an append-only record of issues, attempts, fixes, decisions, and notes, plus a precheck on file edits that warns about prior failed fixes, open issues, or fragile files tied to the path.

PROJECTMEM is a concrete implementation of this pattern. It stores plain-text typed events, rebuilds compact AI-readable summaries deterministically, exposes them through MCP and CLI tools, and includes `precheck_file(path)` before an edit. The paper estimates that rebuilding project context can consume 5,000 to 20,000 tokens per session, and reports a released Python package with 14 MCP tools, 19 CLI commands, and 37 automated tests. Its evaluation is a two-month self-study across 10 projects, so task-success claims still need a controlled check.

A cheap adoption test is to add the log to one maintenance-heavy repository for two weeks. Track how often the agent repeats a failed fix, how many tokens are spent re-reading context at session start, and how often precheck warnings prevent edits to known high-risk files.

### Evidence
- [PROJECTMEM: A Local-First, Event-Sourced Memory and Judgment Layer for AI Coding Agents](../Inbox/2026-06-10--projectmem-a-local-first-event-sourced-memory-and-judgment-layer-for-ai-coding-agents.md): PROJECTMEM describes the local event log, MCP access, pre-action warning layer, and reported implementation details.
- [PROJECTMEM: A Local-First, Event-Sourced Memory and Judgment Layer for AI Coding Agents](../Inbox/2026-06-10--projectmem-a-local-first-event-sourced-memory-and-judgment-layer-for-ai-coding-agents.md): The abstract gives the 5,000–20,000 token context-rebuilding estimate and the append-only event-log design.
