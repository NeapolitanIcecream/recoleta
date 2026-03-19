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
- personal-crm
relevance_score: 0.05
run_id: materialize-outputs
language_code: en
---

# AI First Application Development

## Summary
This is an opinion and product introduction article about “AI-first” application development. It argues that MCP servers should become the primary entry point for how users interact with applications, while traditional mobile/web UIs recede to a secondary role.

## Problem
- The problem the article aims to solve is that ordinary consumers currently **cannot easily use remote MCP servers directly**; these capabilities are mostly restricted to paid subscriptions, developer mode, or enterprise features.
- This matters because if LLMs gradually become the unified interaction layer, users will want to complete tasks across calendars, ticket booking, food ordering, weather, messaging, and other services within a single conversation, rather than repeatedly switching between apps.
- For developers, traditional UI development is costly and slow to iterate; the author argues that if MCP is used as the primary interface, much of the burden of building frontend interaction layers can be skipped, enabling faster construction of “AI first” applications.

## Approach
- The core mechanism is simple: package application capabilities as remotely callable **MCP servers**, then use a chat client to let an LLM orchestrate multiple services in conversation to complete tasks.
- The author implemented a consumer-usable client, **Joey MCP Client**: it connects to different LLMs through OpenRouter, lets users manually configure remote MCP servers, and choose a model and server combination for each session.
- The client supports using multiple MCPs at the same time, image input/output, OAuth authentication for MCP server, and features such as available source code, no telemetry, and no ads.
- To demonstrate the form of an “AI first application,” the author also built **Mob CRM**: users describe social interactions in natural language, and the LLM then automatically creates contacts, relationships, and activity records through several tool calls, replacing the large amount of manual clicking and data entry in traditional CRM systems.
- The author’s argument to developers is that MCP server development is similar to building CLI/REST tools: inputs and outputs are more text-oriented, testable, and easy for LLMs to understand, so it is better suited to AI-assisted development than building full Web/Mobile UIs.

## Results
- The article **does not provide formal experiments, datasets, or benchmark results**, so there are no quantitative metrics, error bars, or systematic comparisons with existing methods to report.
- The strongest concrete product claim in the article is that Joey MCP Client already implements **1 client + OpenRouter integration + support for multiple remote MCP servers**, and can combine multiple services within a single session.
- Explicitly supported features include **simultaneous use of multiple MCPs, image support, OAuth authentication, source-available/buildable code, no telemetry, and no ads**, but no numbers are given for user scale, success rate, latency, or cost.
- The Mob CRM example claims it can transform a single natural-language narrative into several tool calls to create contacts, relationships, and activity records; the article gives only a qualitative comparison, saying it is more natural and less cumbersome than the “**30 different clicks**” of traditional CRM, but provides no task success rate or percentage time savings.
- The article’s forward-looking conclusion is that companies may all need to provide MCP server in the future, or else lose user reach in a world where “LLM as the entry point” dominates; however, this is a trend judgment rather than empirical proof.

## Link
- [https://benkaiser.dev/ai-first-software-development/](https://benkaiser.dev/ai-first-software-development/)
