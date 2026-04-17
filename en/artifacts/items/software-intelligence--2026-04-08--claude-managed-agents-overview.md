---
source: hn
url: https://platform.claude.com/docs/en/managed-agents/overview
published_at: '2026-04-08T23:48:50'
authors:
- NicoJuicy
topics:
- managed-agents
- agent-runtime
- code-execution
- developer-platform
- multi-agent
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Claude Managed Agents Overview

## Summary
Claude Managed Agents is a hosted runtime for running Claude as an autonomous agent with tools, code execution, web access, and persistent session state. It targets teams that want agent behavior without building their own execution loop, container runtime, and event plumbing.

## Problem
- Building an autonomous coding or research agent usually requires custom work for the agent loop, tool calling, runtime isolation, session state, and streaming outputs.
- That infrastructure work matters because it affects security, latency, reliability, and how easily developers can steer or interrupt long-running tasks.
- The excerpt frames Managed Agents as a way to avoid that setup and use a managed environment instead.

## Approach
- The product splits agent execution into four main objects: an agent definition, an environment, a session, and an event stream.
- The agent definition stores the model, system prompt, tools, MCP servers, and skills, then reuses that configuration by ID across sessions.
- The environment is a cloud container with installed languages and packages, network access rules, and mounted files.
- A session binds the agent and environment, then accepts user events while Claude runs tools, executes code, browses the web, and streams results through server-sent events.
- The system also supports server-side event history, mid-run steering or interruption, and built-in prompt caching and compaction for efficiency.

## Results
- The excerpt gives no benchmark results, eval scores, latency numbers, or cost comparisons.
- It claims Claude can operate in a fully managed environment with file reading, command execution, web browsing, and secure code execution.
- It claims built-in performance features such as prompt caching and compaction to improve output quality and efficiency, but gives no measured gain.
- It states that outcomes, multiagent, and memory are in research preview, which suggests planned support for more advanced agent workflows, but the excerpt gives no technical detail or validation.
- The product is currently in beta and requires the `managed-agents-2026-04-01` beta header.

## Link
- [https://platform.claude.com/docs/en/managed-agents/overview](https://platform.claude.com/docs/en/managed-agents/overview)
