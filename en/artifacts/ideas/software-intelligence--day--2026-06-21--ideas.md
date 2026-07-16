---
kind: ideas
granularity: day
period_start: '2026-06-21T00:00:00'
period_end: '2026-06-22T00:00:00'
run_id: 24dac59b-b283-4a94-bdf2-ee5d570aaf0d
status: succeeded
topics:
- agent evaluation
- coding agents
- open weights
- local observability
- cost governance
- architecture boundaries
tags:
- recoleta/ideas
- topic/agent-evaluation
- topic/coding-agents
- topic/open-weights
- topic/local-observability
- topic/cost-governance
- topic/architecture-boundaries
language_code: en
pass_output_id: 273
pass_kind: trend_ideas
upstream_pass_output_id: 272
upstream_pass_kind: trend_synthesis
---

# Coding Agent Operating Controls

## Summary
Agent teams now have concrete checks for three recurring failure points: cheaper coding agents crossing module boundaries, coding sessions creating unclear spend, and agents entering unfamiliar corpora without proven working knowledge.

## YAML module contracts wired into coding-agent hooks and CI
Teams using cheaper coding agents can make module boundaries executable. ANMA’s pattern is plain: developers write YAML contracts for each module, then `anma sync` generates Claude Code guidance, edit-blocking hooks, backend configs, CI checks, and optional `CODEOWNERS` entries.

The useful adoption test is a small repo with known dependency rules. Run the same boundary-sensitive task with a cheaper model on a plain checkout and on a checkout with generated guidance plus `anma check` in CI. ANMA reports that Claude Haiku 4.5 violated a Python boundary in 13 of 19 plain-repo runs and 0 of 20 ANMA runs. A TypeScript follow-up reports 18 violations in 20 control runs and 0 of 20 with ANMA. The authors also say Claude Opus 4.8 respected the Python boundary without ANMA, so the practical target is cost-sensitive agent use and CI governance for human or agent-written diffs.

### Sources
- [Show HN: ANMA, boundary contracts for cheaper AI coding agents](../Inbox/2026-06-21--show-hn-anma-boundary-contracts-for-cheaper-ai-coding-agents.md): Summarizes ANMA’s YAML contracts, generated Claude Code guidance, hooks, CI checks, benchmark results, and the narrower claim for cheaper agents.
- [Show HN: ANMA, boundary contracts for cheaper AI coding agents](../Inbox/2026-06-21--show-hn-anma-boundary-contracts-for-cheaper-ai-coding-agents.md): Gives the Python benchmark result and states the value as insurance for cheaper agents plus CI governance.
- [Show HN: ANMA, boundary contracts for cheaper AI coding agents](../Inbox/2026-06-21--show-hn-anma-boundary-contracts-for-cheaper-ai-coding-agents.md): Lists the generated files, `anma sync --check`, `anma check`, warning mode, JSON output, and exit codes for CI use.

## Local cost gates for Claude Code and Codex sessions
Coding-agent spend can be checked at the session and turn level before it becomes a finance surprise. Lupen reads local Claude Code and Codex JSONL logs, groups activity by session, turn, step, skill group, and sub-agent, then recomputes costs from token counts and public price tables.

A practical workflow is to run a local report at the end of each agent-heavy day and add `lupen budget --over 20 --last 7d` or `lupen verify` to scripts used by power users. Both checks can exit with code 4, which gives teams a simple way to catch cost drift or runaway sessions without uploading prompts, file paths, images, or URLs to a hosted service. The evidence is feature-level rather than a benchmark, so teams should validate it against their own provider invoices and raw logs during a short pilot.

### Sources
- [Show HN: Lupen – an itemized, verified receipt for Claude Code and Codex spend](../Inbox/2026-06-21--show-hn-lupen-an-itemized-verified-receipt-for-claude-code-and-codex-spend.md): Describes Lupen’s local JSONL ingestion, grouping model, recomputed costs, verification, budget checks, and exit code 4.
- [Show HN: Lupen – an itemized, verified receipt for Claude Code and Codex spend](../Inbox/2026-06-21--show-hn-lupen-an-itemized-verified-receipt-for-claude-code-and-codex-spend.md): Shows the local spend breakdown by provider, session, turn, step, skill group, and sub-agent.
- [Show HN: Lupen – an itemized, verified receipt for Claude Code and Codex spend](../Inbox/2026-06-21--show-hn-lupen-an-itemized-verified-receipt-for-claude-code-and-codex-spend.md): Documents CLI reports, verification and budget gates, local-only operation, and attachment tracking.

## Corpus study exams before assigning agents to unfamiliar repositories or literature
Teams can test whether an agent has learned an unfamiliar corpus before giving it open-ended work. Machine Studying defines this as a pre-task study phase over a document corpus, followed by hidden downstream questions. StudyBench applies the setup to DSPy code, OpenClaw code, and recent machine-learning literature, and its metric rewards accuracy at lower inference-token budgets.

The practical version is a small internal exam for a private repo, product manual, or research library. Give the agent time to study the corpus using its normal tools, keep the exam hidden, then score answers under fixed token budgets. The early result warns against assuming that search access solves the problem: Qwen3.5-9B on DSPy improved from 9.6 to 29.4 lenient score only when forced to use 20 search iterations, and the reported fine-tuning baselines did not reliably raise agent expertise.

### Sources
- [Machine Studying](../Inbox/2026-06-21--machine-studying.md): Defines StudyBench, the corpus-study setup, the expertise metric, domains, tool setup, and early results.
- [Machine Studying](../Inbox/2026-06-21--machine-studying.md): Explains that studying can change weights, prompts, tools, indexes, notes, or harness state before downstream evaluation is known.
- [Machine Studying](../Inbox/2026-06-21--machine-studying.md): Reports gaps in expertise on post-cutoff domains and difficulty improving agent expertise with early supervised or self-supervised methods.
