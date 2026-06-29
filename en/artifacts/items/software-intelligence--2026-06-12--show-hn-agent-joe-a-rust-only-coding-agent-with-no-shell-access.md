---
source: hn
url: https://github.com/Kapperchino/agent-joe
published_at: '2026-06-12T23:13:59'
authors:
- kapperchino
topics:
- coding-agent
- rust
- terminal-ui
- shell-safety
- developer-tools
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Show HN: Agent Joe – a Rust only coding agent with no shell access

## Summary
Agent Joe is a Rust-only terminal coding agent that removes shell access to reduce the risk of arbitrary command execution. It targets safer local code work, but the author says it still trails Codex in quality.

## Problem
- CLI coding agents that connect to LLM providers can run arbitrary shell commands, which creates a terminal safety risk.
- General-purpose tools also expose many actions; this project narrows the action set to Rust-specific operations.

## Approach
- Build an open-source TUI coding tool that only works with Rust projects.
- Block shell access so the agent cannot execute arbitrary terminal commands.
- Limit the tool set to Rust-specific actions to reduce what the agent can do.
- Use a TUI similar to Claude Code and Codex, with Vim bindings enforced.

## Results
- The excerpt gives no benchmark numbers or dataset results.
- The author says it "works pretty well currently" and is usable as a Rust-only coding agent.
- The author also says it does not perform as well as Codex.
- The stated reasons for the gap are weaker prompts and the lack of a plan mode.
- The project is open source and presented as a proof-of-concept for safer coding-agent workflows.

## Link
- [https://github.com/Kapperchino/agent-joe](https://github.com/Kapperchino/agent-joe)
