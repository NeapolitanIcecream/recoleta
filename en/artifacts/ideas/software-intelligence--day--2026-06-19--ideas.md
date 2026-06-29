---
kind: ideas
granularity: day
period_start: '2026-06-19T00:00:00'
period_end: '2026-06-20T00:00:00'
run_id: e26c38e2-1326-4a69-8a5b-f01076a9d611
status: succeeded
topics:
- coding agents
- agent security
- agent observability
- model routing
- small language models
- software engineering AI
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-security
- topic/agent-observability
- topic/model-routing
- topic/small-language-models
- topic/software-engineering-ai
language_code: en
pass_output_id: 269
pass_kind: trend_ideas
upstream_pass_output_id: 268
upstream_pass_kind: trend_synthesis
---

# Controlled agent operations

## Summary
Agent teams now have concrete control patterns to test: deterministic replay for stale-state failures, pre-release source audits for multi-file security flaws, and session-locked model routing for routine knowledge work. The public evidence is mostly product or article claims, so the useful move is a narrow local trial with measured false positives, cost, latency, and rollback behavior.

## Temporal fact ledger for stale-state incidents in production agents
Production agent teams can add a deterministic replay step to incident response for failures caused by changed facts. StaleTrace describes a narrow design: ingest the agent’s tool calls plus recorded fact events, replay those facts into a temporal ledger with validity windows, and compare what the agent used with what was valid at that moment. The output is a root cause, blast radius, and incident report.

The first useful build is an adapter for one production agent that exports tool calls, customer or account state changes, and timestamps into a replayable log. Teams should test it on a small set of past incidents where the current database state hid what the agent saw at decision time. The public claim to copy is the deterministic audit path: no LLM calls, no embeddings, and the same inputs producing the same verdict. The missing measurement is whether the replay catches real stale-state failures faster than the team’s current trace and log review.

### Evidence
- [Show HN: StaleTrace – A temporal ledger that catches stale-state agent bugs](../Inbox/2026-06-19--show-hn-staletrace-a-temporal-ledger-that-catches-stale-state-agent-bugs.md): Summarizes StaleTrace’s temporal ledger design, input types, deterministic audit claim, and lack of benchmark results.
- [Show HN: StaleTrace – A temporal ledger that catches stale-state agent bugs](../Inbox/2026-06-19--show-hn-staletrace-a-temporal-ledger-that-catches-stale-state-agent-bugs.md): Shows the product flow: feed tool calls and recorded facts, replay validity windows, surface stale or conflicting state, and generate an incident report.

## Pre-release source-code audit for multi-file security flaws
Security teams can trial an agentic static audit as a release gate for code paths that ordinary SAST and live testing often miss: authorization chains, feature-flagged flows, admin routes, mobile app logic, and multi-repository changes. Aikido Code Audit claims to follow references across files and modules, return root cause and code evidence, and generate an AutoFix pull request.

A practical test is a two-week audit on significant releases before merge. Route only findings with code evidence into developer triage, then measure confirmed issue rate, duplicate rate, fix time, and overlap with the latest pentest or manual review. Aikido reports early users finding a median of about 25 issues per codebase and claims 70–80% coverage of what a full pentest surfaces at about one-tenth the cost, but the excerpt gives no public dataset or reproducible protocol. Treat the vendor numbers as a reason to run a controlled release-gate trial, with false positives and fix acceptance measured locally.

### Evidence
- [Aikido Code Audit](../Inbox/2026-06-19--aikido-code-audit.md): Summarizes the product claim, target vulnerability class, reported early-user numbers, and missing public evaluation protocol.
- [Aikido Code Audit](../Inbox/2026-06-19--aikido-code-audit.md): Describes the intended workflow before significant releases, cross-file reference following, code evidence, and AutoFix pull request.
- [Aikido Code Audit](../Inbox/2026-06-19--aikido-code-audit.md): Lists source-only coverage examples such as ReDoS, admin-only routes, multiple repos, feature-flagged paths, undeployed changes, and mobile apps.

## Session-locked model routing test for office document and spreadsheet tasks
Teams with high inference bills for document, email, and spreadsheet assistants can test a router that sends routine work to a smaller model and difficult work to a frontier model, then keeps that model fixed for the session. The reported GDPVal-AA setup routes between GPT-5.5 and GPT-5.4 Mini, reaches 1759 ELO versus 1769 for GPT-5.5 alone, and keeps routing overhead below $0.01 per request.

The build should be small: classify task type and difficulty, choose the model once at session start, log cost, latency, cache hit rate, and user correction rate, and run a blind review on a sample of final outputs. The session lock matters because mid-session model swaps can break prompt caches and change output behavior. The evidence also points to domain-tuned small models as candidates for specialized workloads, including MAI-Code-1-Flash at about 5B active parameters scoring 51.2% on SWE-Bench Pro versus 35.2% for Claude Haiku 4.5 while using up to 60% fewer tokens.

### Evidence
- [Knowledge workers don't need frontier models](../Inbox/2026-06-19--knowledge-workers-don-t-need-frontier-models.md): Summarizes the routing approach, GDPVal-AA scores, router overhead, session locking, and claimed cost and latency gains.
- [Knowledge workers don't need frontier models](../Inbox/2026-06-19--knowledge-workers-don-t-need-frontier-models.md): Gives the GDPVal-AA setup, model choices, leaderboard context, and ELO comparison.
- [Knowledge workers don't need frontier models](../Inbox/2026-06-19--knowledge-workers-don-t-need-frontier-models.md): Reports MAI-Code-1-Flash size, SWE-Bench Pro result, token reduction claim, and use inside GitHub Copilot’s auto-picker.
