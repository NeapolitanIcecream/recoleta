---
source: hn
url: https://github.com/oussamaKH63/peekai
published_at: '2026-06-21T23:38:15'
authors:
- ousskh63
topics:
- ai-agent-observability
- python-agents
- local-first-debugging
- llm-tracing
- multi-agent-workflows
- developer-tools
relevance_score: 0.64
run_id: materialize-outputs
language_code: en
---

# Show HN: PeekAI – Local-first observability for Python AI agents

## Summary
PeekAI is a local Python tracing and debugging tool for AI agents. It records LLM calls, tool calls, tokens, costs, errors, and replay runs without sending trace data to a hosted service.

## Problem
- Python agent developers need to inspect LLM calls, tool use, token counts, cost, latency, and failures during development.
- Hosted tools such as LangSmith and Weights & Biases can require accounts, cloud data upload, and setup before traces are visible.
- Local storage matters when traces may contain prompts, outputs, tool responses, or user data that a developer does not want to send to a third party.

## Approach
- `peekai.init()` monkey-patches supported SDK clients at startup, so existing OpenAI, Anthropic, or LiteLLM calls can be traced without changing each call site.
- Decorators such as `@peekai.agent`, `@peekai.tool`, and `@peekai.trace` create a parent-child span tree for agent workflows.
- Traces are stored in a local SQLite database at `~/.peekai/peekai.db` by default, with an optional custom `db_path`.
- The CLI exposes trace listing, trace viewing, stats, map visualization, replay, and cleanup commands.
- Replay can re-run a past trace, swap the model, or inject a changed tool response, then save the replay as a new trace for side-by-side comparison.

## Results
- The excerpt reports no formal benchmark, accuracy result, latency study, or comparison against LangSmith, Weights & Biases, or OpenTelemetry-based tools.
- The included multi-agent demo trace records 3 spans: `researcher`, `writer`, and `format_output`.
- The same demo reports total runtime of 3.6s, 236 tokens, and estimated cost of $0.000222.
- The demo breaks down LLM usage into 102 tokens and $0.000115 for the `researcher` call, plus 134 tokens and $0.000107 for the `writer` call.
- The local UI runs at `http://localhost:8501` and has 4 pages: Dashboard, Traces, Trace View, and Replay.
- The package lists 3 SDK integration targets in configuration: OpenAI, Anthropic, and LiteLLM.

## Link
- [https://github.com/oussamaKH63/peekai](https://github.com/oussamaKH63/peekai)
