---
kind: ideas
granularity: week
period_start: '2026-06-15T00:00:00'
period_end: '2026-06-22T00:00:00'
run_id: ef2ae8ce-8db0-4172-a5e5-47968001177f
status: succeeded
topics:
- coding agents
- agent evaluation
- software verification
- program repair
- agent memory
- benchmark contamination
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-evaluation
- topic/software-verification
- topic/program-repair
- topic/agent-memory
- topic/benchmark-contamination
language_code: en
pass_output_id: 275
pass_kind: trend_ideas
upstream_pass_output_id: 274
upstream_pass_kind: trend_synthesis
---

# Coding Agent Acceptance Controls

## Summary
Coding-agent adoption is moving toward concrete acceptance checks: failure-tested repository instructions, trace gates around agent work, and pre-assignment exams for unfamiliar corpora. The useful work is in the support layer around the model: what the agent was told, what it actually did, what evidence it used, and which checks passed before a human reviews the result.

## Failure-tested AGENTS.md files for repository-specific coding agents
Teams using coding agents can make repository guidance part of the test workflow. A practical version starts with a short AGENTS.md file, generates synthetic bug-fix probes for that repository, asks the agent to attempt fixes, and edits the guidance only where the failed runs show missing or misleading instructions. The resulting file should name subsystem entry points, test commands, known brittle paths, and quality gates in compact form.

Probe-and-Refine gives a concrete shape to this workflow. On 500 SWE-bench Verified instances, refined guidance reached a 33.0% mean resolve rate, compared with 28.3% for a static knowledge base and 25.5% with no context. The reported gain came mainly from more evaluable patches, not higher per-patch precision. That matters for maintainers because a bad instruction file often sends an agent to the wrong file or leaves it stuck before a meaningful patch exists.

A cheap adoption test is to run the same agent on a small set of recent fixed bugs with three guidance variants: no file, a hand-written file, and a probe-refined file. Track whether the agent finds the right files, runs the right tests, and produces a patch that reaches review. If the refined file only adds generic advice, it should be rejected like any other unhelpful repository artifact.

### Evidence
- [Probe-and-Refine Tuning of Repository Guidance for Coding Agents](../Inbox/2026-06-18--probe-and-refine-tuning-of-repository-guidance-for-coding-agents.md): Reports the Probe-and-Refine method, the SWE-bench Verified resolve-rate comparison, and the finding that refined guidance mainly increases evaluable patch coverage.
- [Probe-and-Refine Tuning of Repository Guidance for Coding Agents](../Inbox/2026-06-18--probe-and-refine-tuning-of-repository-guidance-for-coding-agents.md): Describes the operational knowledge AGENTS.md-style files are meant to capture, including entry points, tests, conventions, and debugging strategies.

## Trace gates for accepting coding-agent pull requests
Agent-generated pull requests need a small action log beside the diff. The useful record is simple: files read, repository searches, edits, commands, tests, retries, and submission. A CI gate can then check rules such as “tests ran after the final edit,” “the agent inspected the touched subsystem before editing,” and “the task did not submit after repeated test failures.” These checks give reviewers evidence about the work path before they spend time reading the patch.

ProcGrep shows why this is practical. It turns coding-agent trajectories into action sequences such as `read_file`, `search_repo`, `edit`, `run_test`, and `submit`, then supports deterministic structural queries over those traces. On SWE-bench Verified traces from 10 agents, procedural fingerprints attributed unseen trajectories to the correct agent with 85.7% accuracy, and ProcGrep reached F1=1.000 on an episodic trace-search task at microsecond latency per decision.

GlueRun-go points to an implementation pattern for teams already running parallel agents. Each worker runs in a separate Git worktree, holds a JSON lease, writes a state packet with changed files, commands, tests, and evidence, and sends gate results into an audit and recovery path. The project evidence is engineering evidence, not a standard benchmark, but the shape is useful: isolate the work, record the task evidence, and make gate failure a first-class outcome.

### Evidence
- [Agent trajectories as programs: fingerprinting and programming coding-agent behavior](../Inbox/2026-06-15--agent-trajectories-as-programs-fingerprinting-and-programming-coding-agent-behavior.md): Defines ProcGrep’s action-trace representation, deterministic trace queries, SWE-bench Verified attribution result, and episodic-search result.
- [Show HN: Agentic coding workflows built on Git worktrees and task evidence](../Inbox/2026-06-20--show-hn-agentic-coding-workflows-built-on-git-worktrees-and-task-evidence.md): Describes Git worktree isolation, JSON leases, state packets, gate results, audit verdicts, and recovery actions for parallel coding-agent work.
- [Show HN: Agentic coding workflows built on Git worktrees and task evidence](../Inbox/2026-06-20--show-hn-agentic-coding-workflows-built-on-git-worktrees-and-task-evidence.md): Shows the concrete state-packet and gate-result flow used after worker runs.

## Corpus exams before assigning agents to unfamiliar repositories or documentation
Before giving an agent a new codebase, internal library, or private documentation set, teams can run a short open-book corpus exam. The agent receives the same corpus it will use on the real task, then answers hidden questions under several token budgets. Useful questions ask where behavior is implemented, which API is current, what configuration is unsafe, and which docs support the answer. The score should reward accurate answers at lower inference cost, because brute-force search is a poor operating mode for routine engineering work.

StudyBench makes this evaluation concrete. It pairs a corpus with a hidden exam across DSPy code, OpenClaw code, and recent machine-learning literature, then measures performance as inference tokens increase. The reported DSPy result for Qwen3.5-9B is a warning sign for agent deployment: forcing 20 search iterations raised the lenient score from 9.6 to 29.4, which means relevant evidence can be present and still go unused without better study behavior. On OpenClaw, two frontier models stayed barely above 10% even with more search.

A team can start with 20 to 40 private questions drawn from recent incidents, API migrations, and maintainer review comments. Passing the exam should require cited file paths or document references. Failed answers are useful even when the agent later writes code, because they identify the missing notes, stale docs, and retrieval paths that will cause bad patches.

### Evidence
- [Machine Studying](../Inbox/2026-06-21--machine-studying.md): Describes StudyBench, its corpus-plus-hidden-exam setup, token-budget expertise metric, and early results showing weak use of available evidence.
- [Machine Studying](../Inbox/2026-06-21--machine-studying.md): Frames the practical setting of agents working with new libraries, research papers, and private corpora after training.
- [Show HN: Vitrus – the company brain that tells you what it doesn't know](../Inbox/2026-06-20--show-hn-vitrus-the-company-brain-that-tells-you-what-it-doesn-t-know.md): Shows a source-backed memory design that returns citations, stale or unsupported verdicts, and deterministic gap reports for human and agent workflows.
