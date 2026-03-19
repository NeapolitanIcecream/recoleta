---
source: hn
url: https://github.com/Grizzly-Endeavors/residuum
published_at: '2026-03-04T23:40:51'
authors:
- BearFlinn
topics:
- agent-framework
- continuous-memory
- personal-agent
- multi-channel
- task-scheduling
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Show HN: Residuum | Agentic AI with continuous context

## Summary
Residuum is a personal AI agent framework with “no session boundaries,” aiming to let the same agent continuously retain context and memory across all channels. Its core selling points are persistent contextual memory, single-threaded interaction across channels, and removing scheduled proactive tasks from LLM reasoning to reduce cost.

## Problem
- Existing AI agent frameworks typically operate on a **session** basis: each new conversation requires re-providing background, resulting in a poor experience for long-term continuous collaboration.
- Some systems attempt to patch this with RAG or fixed memory files, but the model still treats each conversation as an isolated event, meaning old context depends on “remembering to search for it.”
- Proactive agents often periodically trigger full LLM turns to check for pending tasks, causing unnecessary token consumption and scheduling overhead.

## Approach
- Replace sessions with a **continuous thread**: one agent shares the same conversation thread across all channels such as CLI, Discord, and webhooks.
- Compress conversation history into a **dense observation log** that is always kept in context, allowing the model to use recent history directly without retrieval.
- Provide **hybrid retrieval** (BM25 + vector embeddings) for older content, looking back into old episodes only when full details are needed.
- Use **YAML pulse scheduling** to define “what to check, when to check it, and where to send results,” moving timing logic out of the LLM; the model is triggered only when a task is due, and can run on a cheaper model.
- Adopt a file-first and modular design: state is stored in readable files, and Memory, Projects, Pulses, and Skills can be composed independently, while remaining compatible with the OpenClaw skill format.

## Results
- The text **does not provide formal experimental or benchmark results**; there are no datasets, evaluation metrics, ablation studies, or statistical significance figures.
- Clear system-level claims include: **no need for session switching**, with the same agent continuously sharing context across CLI, Discord, and webhooks.
- Compared with OpenClaw, the author claims it solves the “**context memory cliff after two days**” problem: old context does not fall out of the workflow simply because search is not triggered.
- Compared with approaches that trigger a full LLM heartbeat every 30 minutes, Residuum claims to avoid continuously consuming frontier-model calls for scheduling logic through **structured pulse scheduling**, but **does not provide specific token or cost reduction figures**.
- Engineering facts provided include: support for Linux (x86_64, aarch64) and macOS (Apple Silicon), support for Anthropic, OpenAI, Google, and Ollama, and provider failover.

## Link
- [https://github.com/Grizzly-Endeavors/residuum](https://github.com/Grizzly-Endeavors/residuum)
