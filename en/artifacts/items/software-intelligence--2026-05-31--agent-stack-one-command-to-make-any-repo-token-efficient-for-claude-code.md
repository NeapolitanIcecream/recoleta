---
source: hn
url: https://github.com/drmahdikazempour/agent-stack
published_at: '2026-05-31T21:51:06'
authors:
- mahdikaz
topics:
- claude-code
- token-optimization
- code-intelligence
- developer-agents
- repo-automation
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Agent-stack – one command to make any repo token-efficient for Claude Code

## Summary
agent-stack is a one-command setup tool that configures Claude Code and Cursor for lower-token work in a software repo. It matters because repo agents often waste context on file discovery, noisy logs, oversized instructions, and manual hook setup.

## Problem
- Claude Code token-saving tools are split across separate utilities for shell compression, code maps, usage measurement, handoff, hooks, and editor rules.
- Setting up a repo can require choosing 5-10 tools, merging hooks, writing CLAUDE.md, mirroring Cursor rules, and measuring usage by hand.
- The practical cost is higher input-token use and more setup time before an agent can work on a codebase.

## Approach
- The main command, `npx @drmahdikazempour/agent-stack init --all`, detects the host, repo type, package manager, and profile, then generates Claude Code and Cursor files.
- It writes and verifies `CLAUDE.md`, `AGENTS.md`, `.claudeignore`, skills, hooks, Cursor rules, and `.agent-stack/graph.md`, with backups and rollback on failure.
- A built-in code map indexes source files and exported symbols, so the agent can grep one compact file before opening source files.
- A built-in `compress` command removes ANSI codes, folds duplicate lines, and trims long command output before it enters context.
- Usage measurement relies on `ccusage`; a Stop hook logs turns to `.agent-stack/usage.jsonl`, and `measure --since 7d` compares current input tokens/day with the stored baseline.

## Results
- Setup claim: `init --all` takes a repo from no setup to an optimized Claude Code and Cursor setup in under 2 minutes.
- Example install output claims 20 generated files, 2 wired hooks, a verified `CLAUDE.md`, a generated code map, and a 7-day baseline of 12,340 tokens/day.
- The generated `CLAUDE.md` is capped at ≤800 startup tokens and checked by `doctor`.
- The code map example indexes 142 files and 906 top-level symbols, letting the agent open 1 target file instead of reading many files during symbol search.
- The output compressor claims about 60% fewer characters on a 500-line log.
- The measurement example reports 7,180 current input tokens/day versus a 12,340 baseline, a 41.8% reduction, with a target of at least 40%; these are README claims rather than an independent benchmark.

## Link
- [https://github.com/drmahdikazempour/agent-stack](https://github.com/drmahdikazempour/agent-stack)
