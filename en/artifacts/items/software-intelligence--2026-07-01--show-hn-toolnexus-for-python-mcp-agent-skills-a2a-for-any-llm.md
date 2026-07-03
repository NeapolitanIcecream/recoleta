---
source: hn
url: https://pypi.org/project/toolnexus/
published_at: '2026-07-01T22:59:33'
authors:
- muthuishere
topics:
- llm-agents
- mcp
- agent-tools
- a2a
- multi-agent-systems
- developer-tools
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Show HN: Toolnexus for Python – MCP, agent skills,a2a for any LLM

## Summary
Toolnexus is a Python toolkit that connects LLM agents to MCP servers, local skills, custom functions, HTTP endpoints, built-in tools, and A2A agents through one tool interface. It targets developers who want a small agent runtime with streaming, retries, memory, metrics, and tool execution across model providers.

## Problem
- LLM agents often need several tool sources at once: MCP servers, local skills, custom code, REST APIs, shell and file tools, and peer agents.
- Teams need the same agent code to work across OpenAI-style, Anthropic-style, OpenRouter, Gemini schema adapters, and local execution loops.
- Production use needs memory, streaming, retries, metrics, and failure isolation around remote agents.

## Approach
- `create_toolkit(...)` loads tools from `mcp.json`, a `skills/` folder, Python functions, HTTP endpoints, 10 built-in tools, and remote A2A agent cards.
- `create_client(...)` points at an OpenAI- or Anthropic-style endpoint and runs a loop that sends tool schemas, executes tool calls, and returns a `RunResult`.
- `ask(prompt, tk, id=...)` stores and reloads transcripts through `ConversationStore`; `stream(...)` emits text and tool events and saves the thread on completion.
- A2A support exposes `SKILL.md` skills through a JSON-RPC 2.0 subset with Agent Card discovery, `SendMessage`, and `GetTask`; outbound A2A skills appear as tools.
- Metrics are exposed through `on_metric` callbacks and Prometheus text without third-party dependencies.

## Results
- The excerpt reports no benchmark, accuracy, latency, reliability, or user-study results.
- It claims a working agent can be built in 5 lines when using the default built-in tools.
- It ships 10 built-in tools: `bash`, `read`, `write`, `edit`, `grep`, `glob`, `webfetch`, `question`, `apply_patch`, and `todowrite`.
- The Python package is version 0.4.0, supports Python 3.11 or newer, and publishes a 117.4 kB source archive plus a 53.2 kB wheel.
- The same library behavior is claimed across 5 language ports: Python, JavaScript, Go, Java, and C#.
- A2A support is limited in v1: JSON-RPC 2.0, Agent Card discovery, `SendMessage`, and polling `GetTask` are included; streaming, push, and auth are absent.

## Link
- [https://pypi.org/project/toolnexus/](https://pypi.org/project/toolnexus/)
