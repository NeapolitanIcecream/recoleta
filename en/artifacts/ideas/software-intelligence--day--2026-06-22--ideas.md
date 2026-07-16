---
kind: ideas
granularity: day
period_start: '2026-06-22T00:00:00'
period_end: '2026-06-23T00:00:00'
run_id: 8f892998-d9d4-4e5a-8477-ebd258d8b2d3
status: succeeded
topics:
- LLM agents
- coding agents
- enterprise benchmarks
- procedural memory
- software security
- context recovery
- SysML
- Text-to-SQL
tags:
- recoleta/ideas
- topic/llm-agents
- topic/coding-agents
- topic/enterprise-benchmarks
- topic/procedural-memory
- topic/software-security
- topic/context-recovery
- topic/sysml
- topic/text-to-sql
language_code: en
pass_output_id: 277
pass_kind: trend_ideas
upstream_pass_output_id: 276
upstream_pass_kind: trend_synthesis
---

# Coding Agent Readiness Checks

## Summary
Coding-agent adoption has three practical pressure points: recovering the files a repository task actually needs, testing agents on delivered workplace artifacts, and checking AI-built applications before deployment. The evidence supports small operational changes that teams can pilot with existing repositories, session logs, and security review queues.

## Task-level repository context recovery before coding-agent edits
Teams using coding agents on large repositories should add a pre-edit context recovery step that starts with a few high-confidence files, then expands through imports, configuration bindings, dependency injection, tests, and module proximity. The output can be a bounded context packet: full text for likely edit targets, compact metadata for supporting files, and an explicit list of links that explain why each file is present.

This is a practical fit for platform engineering and developer-experience teams that already see agents patch the obvious file while missing registration code, test fixtures, or configuration paths. A cheap pilot is to take recent resolved tickets, ask maintainers to mark the relevant files, and compare the current retrieval stack against an anchor-and-expansion pass on full recall, token cost, and downstream patch success. DeepDiscovery reports gains on industrial repositories with more than 25,000 files, including Full Recall Rate improvements of 2.5 to 7.4 percentage points on medium tasks and 1.6 to 9.2 points on large-subproject tasks, plus an 8.2-point solve-rate gain on SWE-bench Verified.

### Sources
- [From Fragments to Paths: Task-Level Context Recovery for Large Industrial Codebases](../Inbox/2026-06-22--from-fragments-to-paths-task-level-context-recovery-for-large-industrial-codebases.md): Summarizes DeepDiscovery’s Location-Inference workflow, industrial repository scale, file-recovery gains, and SWE-bench Verified solve-rate result.
- [From Fragments to Paths: Task-Level Context Recovery for Large Industrial Codebases](../Inbox/2026-06-22--from-fragments-to-paths-task-level-context-recovery-for-large-industrial-codebases.md): Describes the failure mode where semantic retrieval misses configuration registration, dependency injection, event propagation, and cross-module constraints.

## Session-derived workplace agent tests with deliverable, cost, and skill-transfer scoring
Enterprise teams should turn a sample of real agent sessions into reproducible tests before widening agent use across departments. Each test should include recovered input files, the requested deliverable, hard rules, a text or visual rubric, and a fresh sandbox run for each harness-model pairing. The score should report artifact completion, quality, runtime, token use, cost, and tool calls together.

Reusable skill files need the same discipline. A `SKILL.md` update should pass held-out tasks for the same task class, then transfer checks across roles or model backbones before promotion. EnterpriseClawBench shows that the best Lite result across 32 harness-model combinations reaches 0.663, leaving many delivery and quality failures visible. AFTER shows that versioned procedural skills can improve accuracy, while narrow skill evolution can lose accuracy when moved across roles. A first deployment check can use 30 to 50 historical sessions and a small set of recurring skills, then block rollout for configurations that save time while failing deliverables or breaking transfer.

### Sources
- [EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions](../Inbox/2026-06-22--enterpriseclawbench-benchmarking-agents-from-real-workplace-sessions.md): Details the conversion of enterprise sessions into reproducible tasks with files, deliverables, role labels, rubrics, sandbox execution, and cost/runtime/tool-call reporting.
- [EnterpriseClawBench: Benchmarking Agents from Real Workplace Sessions](../Inbox/2026-06-22--enterpriseclawbench-benchmarking-agents-from-real-workplace-sessions.md): Explains why enterprise evaluation needs harness-model combinations, artifact delivery quality, time, cost, and task-class-level skill evaluation.
- [Managing Procedural Memory in LLM Agents: Control, Adaptation, and Evaluation](../Inbox/2026-06-22--managing-procedural-memory-in-llm-agents-control-adaptation-and-evaluation.md): Reports AFTER’s versioned skill artifacts, refinement gains, cross-model transfer results, and cross-role transfer losses.

## Pre-deployment security review for AI-authored web applications
Organizations allowing AI agents to build and deploy web apps should add a release gate aimed at repeated AI-generated vulnerability patterns. The review should check broken access control, secret exposure, injection, unfiltered input, placeholder logic, cryptographic failures, and insecure deployment settings. Agent-assisted audit output should be deduplicated and routed to human security reviewers for exploitability confirmation on public-facing apps.

The same workflow can attach security requirements to architecture and code for systems where traceability matters, such as payment, identity, or device-control software. EVerest shows the value of linking requirements, architecture, documentation, and code: its dataset includes 84 security requirements and 1,445 fine-grained labels, and the construction process found a real CWE-1295 plain-text token storage weakness. The vibe-coding study gives the adoption blocker: in 200 deployed AI-authored web apps, reviewers validated 1,471 exploitable vulnerabilities after deduplication and exploitability checks.

### Sources
- [Understanding the (In)Security of Vibe-Coded Applications](../Inbox/2026-06-22--understanding-the-in-security-of-vibe-coded-applications.md): Reports the VibeApps corpus, deployed-web-app audit process, validated vulnerability count, reviewer agreement, and recurring vulnerability categories.
- [Understanding the (In)Security of Vibe-Coded Applications](../Inbox/2026-06-22--understanding-the-in-security-of-vibe-coded-applications.md): Describes unaudited security-critical decisions in vibe-coded apps, including credentials, access control, database queries, and insecure configuration.
- [The EVerest Dataset for Secure Software Engineering](../Inbox/2026-06-22--the-everest-dataset-for-secure-software-engineering.md): Summarizes EVerest’s security requirements, architecture and code links, fine-grained labels, and disclosed CWE-1295 token-storage weakness.
