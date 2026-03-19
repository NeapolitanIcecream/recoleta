---
source: hn
url: https://advanced-stack.com/fields-notes/qwen35-opencode-lm-studio-agentic-coding-on-m1.html
published_at: '2026-03-02T23:10:13'
authors:
- advanced-stack
topics:
- agentic-coding
- local-llm
- qwen
- lm-studio
- telegram-bot
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# 2x Qwen 3.5 on M1 Mac: 9B builds a bot, 0.8B runs it

## Summary
This article is not an academic paper, but a hands-on field note: the author shows how to run OpenCode + LM Studio + Qwen3.5 locally on a 16GB, roughly 6-year-old MacBook M1 to build a working Telegram bot. The core conclusion is: although it is slow, by splitting responsibilities into “a larger model writes code, a smaller model handles replies,” local private agentic coding is already practically usable.

## Problem
- The problem being addressed is: **can agentic coding be done offline on older, resource-constrained local hardware, and can it actually deploy a usable small application**.
- This matters because many small teams or individual developers want to **keep code and data from leaving the local machine / internal network**, while still retaining a workflow similar to cloud coding agents.
- Conventional wisdom is that this kind of task usually requires stronger hardware or cloud services; this article tries to show that devices with a low barrier to entry like an **M1 16GB** can also be “usable.”

## Approach
- The method is very direct: use **OpenCode** as the agentic coding frontend, connected to **LM Studio’s local OpenAI-compatible API**, all running on the same machine.
- It uses a **two-model split**: **Qwen3.5-9B-GGUF (Q4_K_M)** handles planning, editing, and code generation; **Qwen3.5-0.8B-GGUF** handles local inference replies after the Telegram bot receives messages.
- The system flow is: user prompts OpenCode → the 9B model generates/modifies `bot.py` → the Telegram bot receives messages → forwards them to `http://localhost:1234/v1/chat/completions` → the 0.8B model returns a response → the bot replies to the user.
- In one short session, the author iterated from “generate a `/ip` Telegram bot” to “bridge Telegram with the local LM Studio service,” showing that this setup supports simple multi-turn requirement refinement.
- To fit local machine constraints, the author set the context window to **32k**; this coding session actually used about **16k tokens** and nearly maxed out **16GB RAM**.

## Results
- The most important result is: on a **roughly 6-year-old MacBook M1 (16GB RAM)**, the author successfully ran the full pipeline: **Qwen3.5-9B generated a working Telegram bot, then modified it into a chatbot that calls a local Qwen3.5-0.8B API**.
- Configuration details include: **OpenCode 1.2.10**, **LM Studio 0.4.6**, **Metal llama.cpp 2.5.1**, coding model **Qwen3.5-9B-GGUF Q4_K_M**, and reply model **Qwen3.5-0.8B-GGUF**.
- The author claims it took only **one short session plus a small number of follow-ups** to go from idea to working flow, but **does not provide formal benchmarks, latency, tokens/s, success rate, or quantitative comparisons with other models/hardware**.
- The most specific resource figures given are: a configured **32k context window**, actual usage of about **16k tokens** for this task, and basically **fully consuming 16GB of memory**.
- The performance conclusion is qualitative: the author explicitly says it is “**very slow**” on M1, but “**absolutely usable**” for **short coding loops, script generation, local automation, and sensitive/offline tasks**.
- In terms of baseline comparison, there is only a weak comparison: the author believes this setup **still cannot replace a higher-end coding stack**, and **does not replace OpenClaw**; but compared with relying entirely on the cloud, it offers stronger **privacy and local operability**.

## Link
- [https://advanced-stack.com/fields-notes/qwen35-opencode-lm-studio-agentic-coding-on-m1.html](https://advanced-stack.com/fields-notes/qwen35-opencode-lm-studio-agentic-coding-on-m1.html)
