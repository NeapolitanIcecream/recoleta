---
source: hn
url: https://github.com/momoraul/Lupen
published_at: '2026-06-21T23:32:03'
authors:
- momoraul
topics:
- ai-coding-tools
- cost-accounting
- code-agent-logs
- local-verification
- developer-tooling
relevance_score: 0.63
run_id: materialize-outputs
language_code: en
---

# Show HN: Lupen – an itemized, verified receipt for Claude Code and Codex spend

## Summary
Lupen is a macOS app and CLI that itemizes Claude Code and Codex spending from local JSONL logs. It recomputes costs from token counts and public price tables so users can trace spend to sessions, turns, steps, and sub-agents.

## Problem
- Daily AI coding spend totals hide which provider, session, turn, tool loop, or sub-agent caused the cost; this matters when one runaway session costs more than the rest of the day.
- Claude Code and Codex write detailed local logs, but raw JSONL files are hard to inspect by hand.
- Prompts, file paths, images, and URLs are sensitive, so cost analysis needs to work without uploading logs.

## Approach
- Reads local session files from `~/.claude/projects/**/*.jsonl` for Claude Code and `~/.codex/sessions/**/rollout-*.jsonl` or `$CODEX_HOME/sessions/**/rollout-*.jsonl` for Codex.
- Builds a local index that groups activity as Session → Turn → Step → SkillGroup → SubAgent, with provider-specific modes for Claude Code and Codex.
- Uses Anthropic `stop_reason` fields to set turn boundaries, keeping tool-use loops inside the same turn.
- Recomputes each cost from raw token counts and public pricing, then diffs the result against reported totals.
- Adds a CLI over the same local index for reports, search, resume commands, budget checks, and verification.

## Results
- The excerpt gives no benchmark, accuracy study, or user study results.
- Claimed cost granularity: per Session, Turn, Step, SkillGroup, and SubAgent, with a 4-way token breakdown in the first public release.
- Example provider total shown: `$50 today · Claude Code · 12 sessions · 84 turns`.
- Verification checks Claude Code per-request totals and Codex `token_count` rollout events; `lupen verify` exits with code `4` on cost drift.
- Budget automation supports gates such as `lupen budget --over 20 --last 7d`, also exiting with code `4` when the budget is exceeded.
- Limit tracking estimates `$ per 1%` of 5-hour limit usage over the last 7 days, with menu-bar thresholds at 70%, 90%, and 100%.

## Link
- [https://github.com/momoraul/Lupen](https://github.com/momoraul/Lupen)
