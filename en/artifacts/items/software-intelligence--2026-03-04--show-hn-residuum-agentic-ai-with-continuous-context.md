---
source: hn
url: https://github.com/Grizzly-Endeavors/residuum
published_at: '2026-03-04T23:40:51'
authors:
- BearFlinn
topics:
- agent-framework
- continuous-memory
- multi-channel-agents
- context-management
- proactive-scheduling
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Show HN: Residuum | Agentic AI with continuous context

## Summary
Residuum is a personal AI agent framework centered on “no session boundaries” continuous context, allowing the same agent to share memory continuously across CLI, Discord, and webhooks. It aims to solve the problems of traditional agents having to rebuild context for each new session and wasting tokens on periodic proactive checks.

## Problem
- Existing AI agent frameworks typically operate on a **session** basis, so new conversations lose continuous context and users must repeatedly restate history.
- Relying on RAG or fixed memory files only partially compensates, because the model still treats each conversation as an isolated event; older context also requires the agent to first **guess that it should retrieve** it.
- Common proactive/heartbeat mechanisms periodically trigger full LLM calls to check whether there is work to do, creating unnecessary token costs.

## Approach
- Replace session-based interaction with **one agent, one continuous thread**: compress conversation history into an observation log that remains in context continuously, rather than temporarily retrieving recent memory each time.
- For older historical details, provide a **deep retrieval** mechanism that combines BM25 + vector embeddings for hybrid search; recent working memory is kept directly in context.
- Through **multi-channel aggregation**, unify messages from CLI, Discord, webhooks, and more into the same agent and the same memory, enabling continuous cross-channel conversation.
- Use **YAML pulse scheduling** to move timing/trigger logic out of the LLM: users define what to check, when, and where to send notifications, and the LLM is triggered only when due and can run on a cheap model.
- The system uses a **file-first** and modular design, stores state in readable files, is compatible with OpenClaw skills, and supports multiple model providers with failover.

## Results
- The text **does not provide standard benchmarks, public datasets, or formal experimental metrics**, so there are no verifiable quantitative SOTA results.
- Compared with OpenClaw, the author claims to solve its “**roughly two-day context cliff**” problem: older context no longer mainly depends on the agent first guessing and searching, but remains available through a continuous observation log.
- Compared with OpenClaw triggering a full LLM heartbeat every **30 minutes**, Residuum claims that YAML pulse scheduling removes this kind of LLM-handled scheduling logic, thereby reducing token waste; however, no savings ratio is provided.
- Compared with NanoClaw (described in the text as about **500 lines of TypeScript**, emphasizing minimalism and container isolation), Residuum highlights differentiated capabilities including continuous memory compression, structured proactive scheduling, background task delegation and model layering, and a unified multi-channel thread.
- Specific engineering facts provided include: implemented in Rust; supports Linux (x86_64, aarch64) and macOS Apple Silicon; requires Rust **1.85+**; supports Anthropic, OpenAI, Google, and Ollama, with built-in provider failover.

## Link
- [https://github.com/Grizzly-Endeavors/residuum](https://github.com/Grizzly-Endeavors/residuum)
