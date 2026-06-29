---
source: hn
url: https://github.com/lSAAGl/loop-harness
published_at: '2026-06-10T23:02:01'
authors:
- LordIsBack
topics:
- coding-agents
- software-engineering-automation
- agent-orchestration
- code-review
- ci-triage
- human-ai-interaction
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Loop Harness Is Here

## Summary
Loop-Harness is a shell-based orchestrator that runs Claude Code agents on scheduled repository tasks, checks their output with a second Claude session, and ships only approved changes. It targets unattended code maintenance tasks such as CI triage, PR review, issue grooming, dependency updates, and doc sync.

## Problem
- Coding agents with shell access can damage repositories when they run unattended; teams need isolation, narrow tool access, and a review gate.
- Routine maintenance work needs polling, state tracking, deduplication, retries, logs, and output handling; one-off prompts do not provide those controls.
- The problem matters because write-capable loops can commit code, open PRs, post comments, and push branches into live development workflows.

## Approach
- A scheduler picks due loops per repository using an `every` cadence or a 5-field cron expression.
- Each write run gets a fresh git worktree on a `loop/<name>/<ts>` branch, so the agent does not modify the user’s checkout.
- The primary `claude -p` session receives a task skill file and a scoped `allowed_tools` list. It stages commits, `PR_BODY.md`, or outbox files, but it cannot directly post or push.
- A verifier `claude -p` session inspects the diff and staged outputs, runs cheap checks, and must print `VERDICT: PASS` before the orchestrator ships anything.
- Per-loop JSON state records `last_run`, processed item IDs, failures, retries, and metrics, so repeated polling and duplicate triggers can be safe.

## Results
- The excerpt reports no controlled benchmark, ablation, or comparison against another agent harness.
- The sample dashboard shows `pr-reviewer` with 112 runs, 98% success, 31 items processed, 64s average duration, and 2 failures on a 3-minute cadence.
- The sample dashboard shows `triage-ci` with 38 runs, 95% success, 9 items processed, 241s average duration, and 2 failures on a 10-minute cadence.
- The sample dashboard shows `dependency-updater`, `doc-sync`, and `issue-groomer` at 100% success, with 4, 4, and 9 runs; 6, 2, and 14 items; and 312s, 198s, and 87s average duration.
- Concrete operational claims include one worktree per write run, a verifier gate with an exact pass verdict, scoped Claude tools, default `max_retries: 2`, default `timeout_minutes: 15`, and shutdown that waits up to 5 minutes for active loops.

## Link
- [https://github.com/lSAAGl/loop-harness](https://github.com/lSAAGl/loop-harness)
