---
source: hn
url: https://benkaiser.dev/ai-first-software-development/
published_at: '2026-03-02T23:27:35'
authors:
- benkaiser
topics:
- mcp
- ai-first-apps
- llm-tools
- consumer-agents
- software-development
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# AI First Application Development

## Summary
This article proposes the idea of **"AI First Application Development"**: consumer-facing MCP (Model Context Protocol) servers and chat clients may become the primary interaction layer for applications, while traditional web/mobile/desktop UIs recede to a secondary role. Through two examples—Joey MCP Client and Mob CRM—the author illustrates an application development and usage model centered on LLM + MCP.

## Problem
- The article addresses the problem that **ordinary consumers cannot easily use remote MCP servers directly**. At present, mainstream platforms mostly restrict MCP capabilities to paid tiers, developer modes, or enterprise subscriptions, which hinders the adoption of AI-native applications.
- This matters because MCP can integrate multiple independent services into a single natural-language conversation, allowing users to simply “state what they want” instead of switching back and forth across multiple applications and interfaces.
- For developers, traditional UI development is costly and has a long feedback loop, while the author argues that AI-first applications can lower the barrier to building and iterating if MCP is used as the main entry point.

## Approach
- The core method is simple: **turn application capabilities into MCP servers callable by an LLM, then use a chat client to connect the model with those servers**, allowing users to complete tasks through conversation that would otherwise require multi-step UI interactions.
- The author built a consumer-usable chat interface, **Joey MCP Client**: it connects to multiple LLMs through OpenRouter, lets users manually configure remote MCP servers, and allows a specific model and MCP combination to be selected for each conversation.
- Joey supports calling multiple MCPs simultaneously, image input/output, OAuth authentication for MCP servers, and emphasizes features such as no telemetry, self-buildable source code, and usage-based payment to reduce barriers to adoption and privacy concerns.
- To validate the “AI-first application” form, the author also built **Mob CRM**: a personal CRM accessed primarily through MCP, where users only need to describe social interactions in natural language, and the LLM then automatically creates contacts, relationships, and activity records through several tool calls.
- The author further argues that developing MCP servers is similar to building CLI/REST tools; because they are text-based, easy to test, and easy for LLMs to interpret, they are better suited to AI-assisted development than building full web/mobile UIs.

## Results
- The article **does not provide formal experiments, benchmark data, or quantitative evaluation results**, so there are no reportable numerical comparisons for accuracy, latency, cost, or performance versus existing systems.
- The strongest concrete effectiveness claim comes from the Mob CRM example: a single natural-language input such as “I met John today… also met Jane… talked about slurpees” can trigger **a small number of tool calls** by the LLM to automatically create contacts, establish relationships, and record activity notes; the author contrasts this with avoiding the manual UI work of “**30 different clicks**” in a traditional CRM.
- Functional claims for Joey MCP Client include support for **using multiple MCP servers at once**, support for **images**, support for **OAuth to MCP servers**, and support for session-level selection of **OpenRouter LLM + MCP servers**.
- The author’s main “breakthrough” claim is not an experimental result, but rather a product- and paradigm-level judgment: in the future, consumers will increasingly use applications through MCP-enabled chat interfaces, and companies will “need MCP servers tomorrow just as they need mobile apps today.”

## Link
- [https://benkaiser.dev/ai-first-software-development/](https://benkaiser.dev/ai-first-software-development/)
