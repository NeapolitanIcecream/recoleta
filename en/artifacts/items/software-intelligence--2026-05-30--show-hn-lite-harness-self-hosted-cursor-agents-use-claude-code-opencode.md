---
source: hn
url: https://github.com/LiteLLM-Labs/lite-harness
published_at: '2026-05-30T23:51:21'
authors:
- detente18
topics:
- coding-agents
- self-hosted-agents
- code-intelligence
- human-ai-interaction
- agent-orchestration
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Show HN: Lite-Harness – Self-Hosted Cursor Agents (Use Claude Code/OpenCode)

## Summary
Lite-Harness is a self-hosted server for deploying AI coding agents from Claude Code, Codex, OpenCode, Cursor, and related tools. It gives teams one place to run scheduled agents, manage sessions, store secrets, and route approval requests.

## Problem
- Teams running opencode and claude-code as separate servers have to maintain multiple services, API shapes, session stores, MCP inputs, and prompt configs.
- This matters because shared coding-agent work breaks down when each harness keeps its own sessions, tools, and approval path.

## Approach
- Wraps each supported harness behind an OpenCode-compatible API server.
- Ships as one Docker container connected to a LiteLLM gateway with `LITELLM_API_BASE`, `LITELLM_API_KEY`, and `MASTER_KEY`.
- Runs agents on cron in isolated Linux sandboxes through E2B or Daytona when keys are set.
- Stores vault keys and routes human approval through an Inbox UI before actions such as LinkedIn DMs.
- Persists history and model context by mounting a data directory or setting `DB_PATH`.

## Results
- No benchmark results, accuracy metrics, or user study numbers are provided in the excerpt.
- Claims support for 4 harnesses: `opencode`, `claude-code`, `github-copilot`, and `codex`.
- The example deploys an agent scheduled every 4 hours on weekdays with human approval before each send.
- The server runs locally through Docker on port `4096`.
- The example deployment creates 1 agent, attaches vault keys, schedules it, and starts 1 test run.

## Link
- [https://github.com/LiteLLM-Labs/lite-harness](https://github.com/LiteLLM-Labs/lite-harness)
