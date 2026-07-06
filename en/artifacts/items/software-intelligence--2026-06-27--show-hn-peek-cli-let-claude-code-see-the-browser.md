---
source: hn
url: https://github.com/puffinsoft/peek-cli
published_at: '2026-06-27T22:50:37'
authors:
- ReactRocks
topics:
- coding-agents
- browser-screenshots
- developer-tools
- human-ai-interaction
- agent-safety
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# Show HN: Peek-CLI: Let Claude Code See the Browser

## Summary
peek-cli gives coding agents a read-only way to capture screenshots from open browser tabs. It targets agents that need to inspect a running web app without giving them control over the browser.

## Problem
- Coding agents often need visual feedback from localhost apps, UI tests, or browser-based workflows, but many setups do not let them see the browser.
- Direct browser control can create safety risk because an agent might click, type, inject scripts, or change user data.
- The tool matters for agent-assisted frontend work because screenshots can help an agent verify UI state and debug visual output.

## Approach
- A Chrome extension captures screenshots from open tabs and streams them through a local WebSocket daemon.
- The CLI starts the daemon with `peeked start`, lists visible tabs with `peeked list`, and saves a tab screenshot with `peeked at <url>`.
- Agents use a plugin or skill to request screenshots through the CLI, with setup paths shown for Claude Code and Codex.
- The security model is read-only: the excerpt claims the agent can request screenshots but cannot access the browser, inject scripts, or perform actions.
- The user must connect the agent once on each startup, which adds a manual approval step.

## Results
- No benchmark results, user study, latency numbers, or accuracy metrics are provided in the excerpt.
- The tool claims support for at least 3 named agent clients: Claude Code, Codex, and Copilot.
- The example flow shows 3 core CLI commands: `peeked start`, `peeked list`, and `peeked at <url>`.
- The security claim has 1 allowed agent action: capture a screenshot.
- The project is open source under the MIT license, and the Chrome extension requires manual installation while approval is pending.

## Link
- [https://github.com/puffinsoft/peek-cli](https://github.com/puffinsoft/peek-cli)
