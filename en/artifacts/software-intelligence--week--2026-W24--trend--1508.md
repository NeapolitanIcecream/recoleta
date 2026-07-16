---
kind: trend
trend_doc_id: 1508
granularity: week
period_start: '2026-06-08T00:00:00'
period_end: '2026-06-15T00:00:00'
topics:
- coding agents
- agent governance
- software engineering benchmarks
- agent memory
- runtime enforcement
- formal methods
run_id: materialize-outputs
aliases:
- recoleta-trend-1508
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-governance
- topic/software-engineering-benchmarks
- topic/agent-memory
- topic/runtime-enforcement
- topic/formal-methods
language_code: en
pass_output_id: 258
pass_kind: trend_synthesis
---

# Coding agents are being measured by controls, memory, and cost

## Overview
This week’s large language model (LLM) coding work treats autonomy as an operations problem. Claw-SWE-Bench, Trace, and PROJECTMEM show the center of gravity: compare agent harnesses fairly, enforce user rules at runtime, and keep project state across sessions.

## Findings

### Runtime enforcement and action limits
Agent control moved into the execution loop. Trace compiles user corrections into rules with applicability checks and verifiers, then blocks completion until active checks pass. In ClawArena, it reduced held-out preference violations to 37.6% in distribution and 2.0% out of distribution.

The enterprise-security work adds a broader control model for production agents. It checks plans, delegation chains, capability sets, and session state before actions reach tools. Agent Joe gives a smaller product example: a Rust-only coding agent with no shell access, built to cut the risk of arbitrary terminal commands. Claude Code’s nested sub-agents show why these limits matter. Nesting improves context isolation, but the cited examples include 887,000 tokens per minute and a $47,000 invoice after 23 sub-agents.

#### Sources
- [Getting Better at Working With You: Compiling User Corrections into Runtime Enforcement for Coding Agents](../Inbox/2026-06-11--getting-better-at-working-with-you-compiling-user-corrections-into-runtime-enforcement-for-coding-agents.md): Trace summary with runtime checks and violation-rate results.
- [A Five-Plane Reference Architecture for Runtime Governance of Production AI Agents](../Inbox/2026-06-10--a-five-plane-reference-architecture-for-runtime-governance-of-production-ai-agents.md): Runtime governance architecture with capability and audit controls.
- [Show HN: Agent Joe – a Rust only coding agent with no shell access](../Inbox/2026-06-12--show-hn-agent-joe-a-rust-only-coding-agent-with-no-shell-access.md): Agent Joe summary describing no-shell Rust-only action limits.
- [Claude Code v2.1.172: Sub-Agents Can Now Spawn Sub-Agents](../Inbox/2026-06-13--claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents.md): Nested sub-agent limits, cost claims, and token-spend examples.

### Harness accounting and agent benchmarks
Benchmark work focused on the agent harness, not only the base model. Claw-SWE-Bench fixes task set, prompt, Docker workspace, budget, patch extraction, and evaluator so harnesses can be compared under the same contract. Its results are large enough to matter operationally: with the same GLM 5.1 model, a minimal OpenClaw adapter reached 19.1% Pass@1, while the full adapter reached 73.4%.

AgentBeats takes a related evaluation problem and makes the benchmark itself a judge agent. The paper reports a five-month competition with 298 judge agents and 467 subject agents. EsoLang-Bench adds another stress test. It separates six coding agents by 88.4 percentage points, far wider than the 6.6-point spread reported on SWE-Bench Verified in the same summary.

#### Sources
- [Claw-SWE-Bench: A Benchmark for Evaluating OpenClaw-style Agent Harnesses on Coding Tasks](../Inbox/2026-06-10--claw-swe-bench-a-benchmark-for-evaluating-openclaw-style-agent-harnesses-on-coding-tasks.md): Claw-SWE-Bench summary with controlled harness design and Pass@1 results.
- [AgentBeats: Agentifying Agent Assessment for Openness, Standardization, and Reproducibility](../Inbox/2026-06-11--agentbeats-agentifying-agent-assessment-for-openness-standardization-and-reproducibility.md): AgentBeats summary with judge-agent assessment and competition scale.
- [Frontier Coding Agents Use Metaprogramming to Adapt to Unfamiliar Programming Languages](../Inbox/2026-06-09--frontier-coding-agents-use-metaprogramming-to-adapt-to-unfamiliar-programming-languages.md): EsoLang-Bench summary with agent spread and unfamiliar-language results.

### Persistent state for multi-agent coding
State became a first-class engineering object. PROJECTMEM records issues, attempts, fixes, decisions, and notes in an append-only local log. It exposes that memory through the Model Context Protocol (MCP), a tool interface for connecting agents to external context and actions. Its pre-action gate warns before the agent repeats a failed fix or edits a fragile file.

DeLM shows the multi-agent version of the same need. Agents share verified gists about facts, failed hypotheses, constraints, and partial solutions, then pull work asynchronously from a queue. On SWE-bench Verified with Gemini 3 Flash, it reports 65.7% Avg.@1 at $0.12 per task, compared with $0.24 to $0.26 for listed baselines. Claude Code’s nested agents add a commercial example of separate context frames, though the cost evidence argues for explicit spend caps.

#### Sources
- [PROJECTMEM: A Local-First, Event-Sourced Memory and Judgment Layer for AI Coding Agents](../Inbox/2026-06-10--projectmem-a-local-first-event-sourced-memory-and-judgment-layer-for-ai-coding-agents.md): PROJECTMEM summary with event log, MCP access, and pre-action warnings.
- [Decentralized Multi-Agent Systems with Shared Context](../Inbox/2026-06-09--decentralized-multi-agent-systems-with-shared-context.md): DeLM summary with shared verified context and SWE-bench cost/performance results.
- [Claude Code v2.1.172: Sub-Agents Can Now Spawn Sub-Agents](../Inbox/2026-06-13--claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents.md): Claude Code nested sub-agent summary with separate context frames and spend risks.

### Proof signals and safer software work
Several sources treat verification as part of the agent work loop. Jane Street’s formal-methods essay argues that agent-written code increases review pressure, and that proof tools can give agents feedback beyond tests. The piece gives the old cost baseline clearly: seL4 took 25 person-years to verify 8,700 lines of C, with about 23 lines of proof per line of code.

ComAct shows a different path to safer action: make professional software control executable and inspectable. In CAD workflows, the agent writes Python scripts over COM interfaces, then uses code validity and task success as evaluation signals. The reported ComCADBench covers 1,000 tasks across SolidWorks, Inventor, and AutoCAD, with GUI-based agents near zero success in the summary.

#### Sources
- [Formal Methods and the Future of Programming](../Inbox/2026-06-14--formal-methods-and-the-future-of-programming.md): Formal-methods summary with proof feedback claims and seL4 cost baseline.
- [ComAct: Reframing Professional Software Manipulation via COM-as-Action Paradigm](../Inbox/2026-06-11--comact-reframing-professional-software-manipulation-via-com-as-action-paradigm.md): ComAct summary with COM-based execution, ComCADBench, and reported results.
