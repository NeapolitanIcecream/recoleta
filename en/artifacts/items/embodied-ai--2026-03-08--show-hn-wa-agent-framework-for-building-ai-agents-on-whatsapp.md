---
source: hn
url: https://github.com/ibrahimhajjaj/wa-agent
published_at: '2026-03-08T23:40:23'
authors:
- ibrahimwithi
topics:
- whatsapp-agent
- agent-framework
- llm-orchestration
- tool-use
- conversation-memory
relevance_score: 0.04
run_id: materialize-outputs
language_code: en
---

# Show HN: Wa-agent – Framework for building AI agents on WhatsApp

## Summary
This is an AI agent framework for WhatsApp, aiming to encapsulate infrastructure such as connections, queues, memory, tool invocation, and routing so that developers can build agents mainly through YAML configuration. It is more like an engineering middleware layer than a new model, emphasizing multi-agent support, persistent memory, and cost control.

## Problem
- Problem addressed: Existing WhatsApp bots usually just forward messages to an LLM, lacking capabilities such as **cross-session memory, tool use, multi-agent routing, rate limiting, and queuing**, making them hard to use in real production scenarios.
- Why it matters: In group chats, high-frequency messaging, and multi-task environments, without serialization, rate limiting, and memory mechanisms, the system can suffer from **chaotic responses, runaway costs, and lost context**.
- For developers, repeatedly writing “glue code” for WhatsApp connection, reconnection, message storage, and tool execution reduces the efficiency and maintainability of building agents.

## Approach
- Core method: Use a **YAML-driven agent framework** to declare the agent’s persona, LLM, tools, routing, memory, rate limiting, and human handoff rules, while the framework handles runtime orchestration.
- At the system level, the message flow goes through **the wu-cli WhatsApp connection layer → middleware → router → scheduler → Agent(tool loop)**; routing priority is **jid > group > keyword > default**.
- To ensure stability, the framework processes **the same chat serially** and different chats in parallel, and provides **per-chat / per-agent cooldown and rate limits** to prevent noisy group chats from exhausting the API budget.
- To enable long-term context, the framework reads wu-cli’s SQLite history and additionally maintains **conversation summaries** and **user profiles**; when the message count exceeds a threshold, it summarizes old conversations in the background and reuses them in future prompts instead of stuffing the full history in every time.
- Supports **tool calling, multi-step reasoning, scheduled tasks, human handoff, custom TypeScript tools, hot reload**, and is compatible with Anthropic, OpenAI, and Ollama.

## Results
- The text **does not provide standard benchmark tests or academic experimental results**, so there are no verifiable figures for accuracy, success rate, latency, or cost curves.
- Specific configuration/capability numbers given include: the `conversationWindow` example is **20/30**, `summarizeAfter` is summarization after **100** messages, and `maxSteps` allows up to **10** tool-calling steps.
- A rate-limiting example is **15** LLM calls per chat every **5 minutes**, and the `cooldownMs` example is **5000 ms**.
- When using Jina for `fetchUrl`, it is about **20 RPM** without a key and about **500 RPM** with a key.
- Runtime requirements include **Node.js >= 20**; on first startup, WhatsApp is linked by scanning a **QR code**, after which automatic reconnection is supported.
- The strongest concrete claim is that, compared with common WhatsApp bot glue code, this framework provides complete agent infrastructure including **multi-agent routing, cross-session memory, serialized chat queues, rate limiting/cooldown, scheduled tasks, and human handoff**.

## Link
- [https://github.com/ibrahimhajjaj/wa-agent](https://github.com/ibrahimhajjaj/wa-agent)
