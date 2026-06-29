---
source: hn
url: https://github.com/ClickHouse/nerve
published_at: '2026-05-25T22:46:43'
authors:
- animetyan
topics:
- ai-agent-runtime
- self-hosted-agents
- multi-agent-software-engineering
- code-intelligence
- human-ai-interaction
- persistent-memory
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# Show HN: Nerve – self hosted runtime for AI agents

## Summary
Nerve is a self-hosted runtime that turns Claude Agent SDK agents into long-running personal or worker agents with memory, tasks, skills, crons, and human approval flows. It matters for agent-based software work because it packages persistence, scheduling, source ingestion, and approval gates into one deployable service.

## Problem
- Long-running agents need state across sessions, scheduled work, and ways to ask humans for decisions; a plain chat UI does not cover these needs.
- Team worker agents also need audit trails, plan approval, and safe handling of untrusted inputs before they monitor CI, review PRs, or edit code.
- The project targets self-hosting, so users can run the runtime with their own Claude API key or Claude subscription through a CLI proxy.

## Approach
- The runtime wraps the Claude Agent SDK in a single Python process with a FastAPI gateway, React web UI, Telegram channel, APScheduler jobs, and optional Claude OAuth proxy.
- It uses two memory layers: `MEMORY.md` for curated hot facts injected into prompts, and memU in SQLite for semantic recall over conversations, facts, preferences, and events.
- It stores tasks and skills as Markdown backed by SQLite indexes, so agents can read, create, update, and reuse procedures during later sessions.
- Worker mode starts from a plain-English mission, writes its own `TASK.md`, creates skills, sets cron jobs, proposes plans, and waits for human approval before implementation.
- Source ingestion pulls Telegram, Gmail, GitHub notifications, and GitHub events into a shared inbox with prompt-injection warnings and independent consumer cursors.

## Results
- The excerpt reports no benchmark, user study, ablation, or task-completion metric, so there is no quantitative evidence of agent accuracy or productivity gain.
- Claimed system scale: about 30 custom MCP tools, up to 4 concurrent agent sessions by default configuration, and 3 session modes for scheduled AI jobs.
- Claimed memory controls: 4 memory types (`profile`, `event`, `knowledge`, `behavior`), 3-level quality filtering, semantic deduplication at cosine similarity 0.85, and mutation audit logs.
- Claimed automation cadence: inbox processing every 15 minutes, task planning every 4 hours, skill extraction every 12 hours, and skill revision weekly in personal mode.
- Claimed safety and review features include plan approval, decline, and revision workflow, file snapshot diffs without git, 30-second script timeout for skill scripts, and full plan/session logs.

## Link
- [https://github.com/ClickHouse/nerve](https://github.com/ClickHouse/nerve)
