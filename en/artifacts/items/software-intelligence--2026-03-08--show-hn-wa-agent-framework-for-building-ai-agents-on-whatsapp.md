---
source: hn
url: https://github.com/ibrahimhajjaj/wa-agent
published_at: '2026-03-08T23:40:23'
authors:
- ibrahimwithi
topics:
- whatsapp-agents
- agent-framework
- multi-agent-routing
- conversation-memory
- tool-using-agents
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Show HN: Wa-agent – Framework for building AI agents on WhatsApp

## Summary
wa-agent is an engineering framework for building autonomous AI agents on WhatsApp, focused on solving infrastructure problems such as message ingestion, memory, tool invocation, routing, and operational controls. It configures agent behavior primarily through YAML, allowing developers to build multi-agent WhatsApp applications faster.

## Problem
- Many existing WhatsApp bots simply forward messages to an LLM, lacking cross-session memory, tool usage, multi-agent routing, and production-grade flow control.
- In high-message-volume group chats or multi-user scenarios, without queues, rate limiting, and cooldown mechanisms, responses can easily become chaotic, costs can spiral out of control, or the system can become unstable.
- Repeatedly writing glue code for WhatsApp agents—covering connection handling, context management, scheduling, and human handoff—reduces development efficiency and makes reliable deployment harder.

## Approach
- Use **YAML configuration** to define agent persona, LLM, tools, routing, memory, triggers, and human handoff rules, while the framework handles the underlying runtime.
- Use **Vercel AI SDK v6** for the agent loop and tool execution, and **wu-cli** for WhatsApp connection handling, reconnection, and message storage.
- Adopt a clear pipeline: message filtering and handoff checks → routing (`jid > group > keyword > default`) → scheduler (cooldown, rate limiting, per-chat serial queue) → agent execution (context construction, tool loop, reply, background summarization, and user profile updates).
- Implement cross-session memory through **conversation summaries + user profiles**: after exceeding a threshold, old messages are summarized in the background and user facts are continuously extracted, avoiding the need to inject full history every time.
- Supports **multiple agents**, **custom tools**, **scheduled tasks**, **hot reload**, **human escalation**, and multiple LLM backends (Anthropic/OpenAI/Ollama).

## Results
- The article **does not provide standard benchmark tests or academic experimental results**, and reports no quantitative metrics such as accuracy, success rate, latency, cost, or human evaluation scores.
- It provides clear configurable operating limits and mechanisms, such as `maxSteps: 10` (up to 10 tool-calling steps per message), `rateLimitPerWindow: 15` (at most 15 LLM calls per chat every 5 minutes), and `cooldownMs: 5000` (5-second cooldown).
- The memory mechanism provides specific default/example parameters: `conversationWindow: 20/30`, `summarizeAfter: 100`, `userProfiles: true`, claiming it can preserve long-term context without injecting the full history.
- The URL fetching capability provides throughput figures: about **20 RPM** without a Jina key, and about **500 RPM** with a key.
- The strongest claimed engineering benefits include: **strictly serial** processing within the same chat and **parallel** processing across different chats; support for automatic reconnection, per-chat/per-agent rate limiting, group chat budget protection, as well as human handoff and scheduled tasks.

## Link
- [https://github.com/ibrahimhajjaj/wa-agent](https://github.com/ibrahimhajjaj/wa-agent)
