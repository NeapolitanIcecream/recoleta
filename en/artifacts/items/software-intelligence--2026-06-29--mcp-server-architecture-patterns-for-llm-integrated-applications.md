---
source: arxiv
url: https://arxiv.org/abs/2606.30317v1
published_at: '2026-06-29T13:59:41'
authors:
- Carson Rodrigues
- Oysturn Vas
topics:
- model-context-protocol
- llm-tools
- agent-infrastructure
- software-architecture
- tool-use
- human-ai-interaction
relevance_score: 0.76
run_id: materialize-outputs
language_code: en
---

# MCP Server Architecture Patterns for LLM-Integrated Applications

## Summary
The paper gives MCP server authors a pattern catalog for building LLM-connected tools, resources, and service wrappers. Its main claim is that LLM clients change API design because they choose tools through names, descriptions, and schemas.

## Problem
- MCP adoption produced many servers quickly, but developers lack published guidance on how to split tools, manage state, aggregate servers, and wrap complex APIs.
- This matters because LLMs select tools by reading natural-language descriptions and schemas, so poor server design can reduce tool-selection accuracy, expose prompt-injection paths, or create brittle integrations.
- The paper targets MCP server maintenance and evolution, especially for production LLM applications that connect to databases, APIs, workflows, and session-based tools.

## Approach
- The authors studied 15 MCP servers: 5 production ANSYR voice AI servers and 10 public servers from the official MCP registry.
- They extracted tool, resource, and prompt registrations; transport setup; session handling; upstream delegation; and domain-specific validation from each server.
- They coded recurring structures into 5 patterns: Resource Gateway, Tool Orchestrator, Stateful Session Server, Proxy Aggregator, and Domain-Specific Adapter.
- They also describe 4 anti-patterns: God Tool, Unsanitized Resource Content, Synchronous Long-Running Operations, and Missing or Vague Tool Descriptions.
- The simplest mechanism is pattern mining: inspect real MCP servers, group repeated design choices, then test whether independent raters can apply the labels.

## Results
- The catalog is derived from 15 servers: 5 production servers and 10 public servers. It reports 5 architecture patterns and 4 anti-patterns.
- On 54 held-out MCP servers, two independent LLM raters reached Cohen’s κ = 0.76 with a 95% CI of [0.62, 0.88] and 81.5% raw agreement. Agreement with author labels was 68.5% for Claude Haiku 4.5 and 75.9% for Claude Sonnet 4.
- A pilot using author-written canonical descriptions scored 97%, which the authors reject as an easier test because the descriptions exposed the architecture too directly.
- Transport latency on loopback was 0.01 ms p50 for stdio and 0.39 ms p50 for streamable-http. Cross-host same-region paths are modeled as about 30 ms p50 baseline plus protocol overhead.
- Tool-selection accuracy dropped below 90% between 10 and 15 tools per context for Claude Haiku 4.5, and between 20 and 30 tools for Claude Sonnet 4.
- The strongest practical claim is that static tool aggregation can hurt LLM selection once the visible tool set grows past those model-specific ranges, so scoped aggregation or retrieval over tools is safer for large MCP deployments.

## Link
- [https://arxiv.org/abs/2606.30317v1](https://arxiv.org/abs/2606.30317v1)
