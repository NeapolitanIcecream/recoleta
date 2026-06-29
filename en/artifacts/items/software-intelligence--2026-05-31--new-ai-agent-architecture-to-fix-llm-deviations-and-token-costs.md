---
source: hn
url: https://github.com/botcircuits-ai/botcircuits-agent
published_at: '2026-05-31T23:21:43'
authors:
- nexcatara
topics:
- ai-agents
- workflow-automation
- llm-tool-use
- state-machines
- mcp
- human-ai-interaction
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# New AI Agent Architecture to fix LLM deviations and token costs

## Summary
BotCircuits proposes an agent design where a deterministic workflow engine controls multi-step flow and the LLM handles reasoning and tool calls inside each step. The excerpt is a product README, so it gives architecture and usage details but no benchmark evidence.

## Problem
- LLM-driven agents can drift during long tasks because the model decides both what to do and how to route the process.
- Multi-step automation can waste tokens when the model re-evaluates control flow at every step.
- Teams need agents that can run repeatable workflows through CLI, HTTP, chat, and scheduled jobs while keeping tool execution visible and configurable.

## Approach
- Workflows are JSON records under `.botcircuits/workflows/`; after a build step, each workflow becomes a callable tool.
- The LLM performs each `agentAction`, while the engine follows `start`, `next`, and compiled branch conditions.
- Natural-language branch conditions are compiled into typed `choices[]` entries with operators and values, and `flow.variables` tells the runtime how to coerce inputs before branching.
- Skills are disk folders with `SKILL.md` instructions and optional `allowed-tools`, so repeatable behavior can be added without changing the system prompt.
- MCP servers, built-in file/shell/code tools, a FastAPI gateway, and messaging channels extend where the agent can act.

## Results
- No benchmark results are provided for token cost, task success, latency, or deviation rate.
- The main concrete claim is architectural: runtime branching can happen without another LLM call after conditions are built.
- The README shows support for 3 LLM providers: Anthropic, OpenAI, and Gemini.
- Workflow authoring supports at least 2 step types: `start` and `agentAction`; branching uses `conditions` plus `next` fields.
- The gateway can route at least 4 channel types in one FastAPI process: WhatsApp, Slack, generic webhook, and cron.
- The example workflow has 11 steps: `step_1` through `step_10` plus `end`, with early termination controlled by `end_id`.

## Link
- [https://github.com/botcircuits-ai/botcircuits-agent](https://github.com/botcircuits-ai/botcircuits-agent)
