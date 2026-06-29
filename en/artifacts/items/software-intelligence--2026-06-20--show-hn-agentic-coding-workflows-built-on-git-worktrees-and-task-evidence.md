---
source: hn
url: https://github.com/alex-reysa/glueRun-go
published_at: '2026-06-20T23:58:18'
authors:
- alexreysa
topics:
- code-intelligence
- multi-agent-software-engineering
- automated-software-production
- agent-orchestration
- git-worktrees
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Show HN: Agentic coding workflows built on Git worktrees and task evidence

## Summary
GlueRun-go is a local orchestration engine for running multiple AI coding agents against one Git repository with worktree isolation, leases, gates, audits, and recorded task evidence.

## Problem
- Parallel coding agents can overwrite each other, leave stale work behind, or finish without enough evidence for a human or another agent to judge the change.
- Long-running agent tasks can block repo control operations such as import, integrate, status, and stop.
- Per-repo script copies make upgrades and project-specific behavior hard to manage across many repositories.

## Approach
- The engine uses a three-tier scheduler: L0 origin loop, L1 area planners, and L2 worker agents.
- Each task runs in its own Git worktree and holds a JSON lease that records owner, retry count, and expiry.
- Workers write structured state packets with owned files, changed files, commands, tests, and evidence; an auditor checks the packet and gate result.
- A deterministic decider maps failure class and retries left to retry, amend-scope, escalate, or park, with a model call only as fallback.
- Repos pin an installed engine version and keep repo-specific behavior in config, local overrides, or opt-in modules.

## Results
- The excerpt reports engineering claims, not benchmark results on a standard dataset.
- Detached dispatch is on by default and makes `gluerun reconcile --actuate` return within seconds while workers continue in background; the legacy synchronous path waits for every worker.
- Crash detection improves from a 60-minute stale-lease window to about one reconcile cycle by using dispatch records, worker exit files, and PID liveness checks.
- The system includes 23 regression tests run by `bash tests/run.sh`.
- Runtime session resume uses 10 staleness gates and falls back to a fresh run if any gate fails or the runner refuses resume.

## Link
- [https://github.com/alex-reysa/glueRun-go](https://github.com/alex-reysa/glueRun-go)
