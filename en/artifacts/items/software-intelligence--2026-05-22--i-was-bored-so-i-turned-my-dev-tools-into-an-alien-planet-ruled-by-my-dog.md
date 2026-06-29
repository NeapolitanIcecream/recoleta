---
source: hn
url: https://github.com/bkawa-bot/planet-maiko
published_at: '2026-05-22T23:40:14'
authors:
- bkawa-bot
topics:
- developer-tools
- agent-orchestration
- local-rag
- code-review
- human-ai-interaction
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# I was bored so I turned my dev tools into an alien planet ruled by my dog

## Summary
Planet Maiko is a local developer workbench that pulls tasks, code review, agent sessions, and tool notifications into one desktop workflow. It targets context switching and agent babysitting rather than a research benchmark.

## Problem
- Developers lose focus when GitHub, Slack, calendars, issue trackers, PagerDuty, and AI agents each demand attention in separate tools.
- The project matters because multi-agent software work creates coordination overhead: agents can stall, costs can rise, and humans still need to decide what to do next.
- The author wants a single local tool that can summarize work, suggest next actions, and keep private work data on the laptop.

## Approach
- Planet Maiko runs locally with Python 3.10+ and Node.js 18+, with setup through `python3 bootstrap.py` and daily use through `maiko up`.
- It connects to developer systems such as PagerDuty, Linear, Calendar, and GitHub, then combines their state into one work dashboard.
- It includes agent orchestration, an agent chat view, in-app diff review, custom automations, cost-aware model routing, local RAG embeddings, and experimental model fine-tuning.
- The plugin model asks users to add new data sources by writing 1 Python class.
- Its memory layer builds a local RAG store, including guidelines drawn from prior GitHub history, so the tool can give work-aware recommendations without sending data to a hosted service.

## Results
- The excerpt reports 0 benchmark metrics, 0 user-study results, and 0 comparisons against baselines such as Cursor, GitHub Copilot, Devin-style agents, or issue-tracker assistants.
- It claims support for 4 named integrations: PagerDuty, Linear, Calendar, and GitHub.
- It claims local execution with no telemetry, no hosted account, no cloud dependency, and no paid tiers.
- It claims one-day workflow coverage across morning planning, PR review, agent session management, issue updates, task updates, automations, and notifications.
- The strongest concrete contribution is product integration: a free open-source local tool that combines RAG memory, agent control, code review, and developer-system plugins in one app.

## Link
- [https://github.com/bkawa-bot/planet-maiko](https://github.com/bkawa-bot/planet-maiko)
