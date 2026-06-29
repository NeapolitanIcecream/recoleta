---
kind: trend
trend_doc_id: 1590
granularity: week
period_start: '2026-06-15T00:00:00'
period_end: '2026-06-22T00:00:00'
topics:
- coding agents
- agent evaluation
- software verification
- program repair
- agent memory
- benchmark contamination
run_id: materialize-outputs
aliases:
- recoleta-trend-1590
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-evaluation
- topic/software-verification
- topic/program-repair
- topic/agent-memory
- topic/benchmark-contamination
language_code: en
pass_output_id: 274
pass_kind: trend_synthesis
---

# Coding agents need traces, gates, and scoped memory to earn trust

## Overview
This week’s large language model (LLM) agent work treats autonomy as an evidence problem. The strongest claims pair task success with traces, executable tests, scoped authority, and source-backed memory. ProcGrep, SWE-Future, and Machine Studying show the current emphasis: judge agents by what they did, what they knew, and which checks held.

## Clusters

### Trace-level agent evaluation
Agent evaluation is getting more operational. ProcGrep turns coding-agent trajectories into action sequences such as file reads, repository searches, edits, tests, and submissions. On SWE-bench Verified traces, its procedural fingerprints attribute unseen trajectories to the correct agent with 85.7% accuracy, and its deterministic trace search beats LLM judges on the reported episodic-search task.

SWE-Future addresses another evaluation weakness: public GitHub issue and pull-request replay. It forecasts future repository task families from pre-snapshot evidence, validates them against later pull-request metadata, then synthesizes executable tasks. The daily trend evidence adds a practical warning: the same model can score differently under another agent harness, so benchmark claims need the harness in view.

#### Evidence
- [Agent trajectories as programs: fingerprinting and programming coding-agent behavior](../Inbox/2026-06-15--agent-trajectories-as-programs-fingerprinting-and-programming-coding-agent-behavior.md): ProcGrep summary with trajectory representation, attribution accuracy, trace search results, and cost/behavior comparisons.
- [SWE-Future: Forecast-Conditioned Data Synthesis for Future-Oriented Software Engineering Agents](../Inbox/2026-06-17--swe-future-forecast-conditioned-data-synthesis-for-future-oriented-software-engineering-agents.md): SWE-Future summary with forecast-conditioned task synthesis, validation rates, and final dataset details.

### Failure evidence for repair and repository guidance
Repair work is using runtime evidence to make agent edits easier to judge. PRACREPAIR adds execution traces and validation trace diffs to automated program repair. It reports 162 correct fixes on Defects4J V1.2 and 171 on V2.0 with GPT-4o, while keeping patch refinement tied to diagnostics rather than pass/fail feedback alone.

Repository guidance is also being tested against failures. Probe-and-Refine generates synthetic bug-fix probes, diagnoses where guidance failed, and edits compact repository instructions. On 500 SWE-bench Verified instances, it reports a 33.0% mean resolve rate versus 28.3% for a static knowledge base and 25.5% with no context. The gain comes mainly from agents reaching evaluable patches more often.

#### Evidence
- [PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices](../Inbox/2026-06-16--pracrepair-llm-empowered-automated-program-repair-inspired-by-human-like-debugging-practices.md): PRACREPAIR summary with trace-based repair loop, Defects4J results, and refinement procedure.
- [Probe-and-Refine Tuning of Repository Guidance for Coding Agents](../Inbox/2026-06-18--probe-and-refine-tuning-of-repository-guidance-for-coding-agents.md): Probe-and-Refine summary with method, SWE-bench Verified results, and coverage-driven gain.

### Execution control and source-backed memory
Tooling work treats agent action as something that needs custody. GlueRun-go runs parallel coding agents in separate Git worktrees, assigns JSON leases, records state packets, and feeds gate results into an audit and recovery path. Its public evidence is engineering-focused, with regression tests and claims about faster crash detection, not a standard benchmark result.

Memory systems are adding explicit sources and gap reporting. Vitrus stores company knowledge in Markdown, answers with citations, and reports stale, unsupported, contradicted, or missing information. Its API checks verify endpoint names, arguments, types, and permissions before calls run. The reported evaluations are mostly project gates and controlled tests, so the stronger claim is about design discipline, not broad generalization.

#### Evidence
- [Show HN: Agentic coding workflows built on Git worktrees and task evidence](../Inbox/2026-06-20--show-hn-agentic-coding-workflows-built-on-git-worktrees-and-task-evidence.md): GlueRun-go summary with worktree isolation, leases, gates, audits, and engineering evidence limits.
- [Show HN: Vitrus – the company brain that tells you what it doesn't know](../Inbox/2026-06-20--show-hn-vitrus-the-company-brain-that-tells-you-what-it-doesn-t-know.md): Vitrus summary with sourced answers, deterministic gap detection, API verification, and reported eval gates.

### Corpus expertise as an agent benchmark
Machine Studying frames a hard evaluation question: can an agent read a new corpus before the exam and convert it into usable expertise? StudyBench tests this on DSPy code, OpenClaw code, and recent machine-learning literature. The metric rewards accuracy at lower inference-token budgets, so brute-force search is penalized.

The early results caution against treating search, long context, or simple fine-tuning as enough. On DSPy, forcing Qwen3.5-9B to use 20 search iterations raises the lenient score from 9.6 to 29.4, which shows that evidence can be present and still underused. On OpenClaw, two frontier models remain barely above 10% even with more search. The issue is becoming relevant for coding agents that must work inside unfamiliar codebases and private documentation.

#### Evidence
- [Machine Studying](../Inbox/2026-06-21--machine-studying.md): Machine Studying summary with StudyBench design, expertise metric, domains, and early results.
