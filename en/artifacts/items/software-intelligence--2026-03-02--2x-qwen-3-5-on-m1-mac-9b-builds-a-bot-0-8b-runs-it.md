---
source: hn
url: https://advanced-stack.com/fields-notes/qwen35-opencode-lm-studio-agentic-coding-on-m1.html
published_at: '2026-03-02T23:10:13'
authors:
- advanced-stack
topics:
- agentic-coding
- local-llm
- qwen3.5
- lm-studio
- telegram-bot
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# 2x Qwen 3.5 on M1 Mac: 9B builds a bot, 0.8B runs it

## Summary
This is a hands-on technical report showing how to run OpenCode + LM Studio locally on a roughly 6-year-old MacBook M1 with 16GB of memory, using Qwen3.5-9B for agentic coding and Qwen3.5-0.8B for chat inference. The core conclusion is: although it is slow, it is already usable for small, private, offline software-generation tasks.

## Problem
- The problem being addressed is: how to complete agentic coding and application runtime locally on **older consumer-grade hardware** without relying on cloud models.
- This matters because many small teams or individual developers need **data privacy, offline availability, and a low infrastructure barrier**, but such workflows are usually assumed to require stronger hardware or cloud services.
- The article also implicitly answers an engineering question: whether it is possible to use a **larger model for code generation** and a **smaller model for runtime conversation**, thereby reducing the cost of local deployment.

## Approach
- It uses a split-responsibility dual-model architecture: OpenCode calls local **Qwen3.5-9B-GGUF (Q4_K_M)** for code planning, editing, and iteration; the Telegram bot then forwards user messages to the **Qwen3.5-0.8B-GGUF** behind a local API to generate replies.
- The inference backend is **LM Studio 0.4.6 + Metal llama.cpp 2.5.1**, exposed through the OpenAI-compatible endpoint `http://localhost:1234/v1/chat/completions`, forming a unified access layer.
- The actual task pipeline is simple: user prompts OpenCode → the 9B model generates/rewrites `bot.py` → the Telegram bot receives messages → forwards them to the local LM Studio service → the 0.8B model returns results → the bot sends them back to Telegram.
- The author first had the model generate a simple `/ip` bot, then asked it to rewrite it as a bridge between Telegram and local LM Studio, validating a short loop from “idea” to “working program.”

## Results
- The full workflow ran successfully on a **MacBook M1 (16GB RAM, about 6 years old)**: **Qwen3.5-9B** handled agentic coding, and **Qwen3.5-0.8B** handled local chat replies.
- The author claims that in **one short session with a small number of follow-ups**, they generated a **working Telegram bot** from a requirements description, and then further converted it into a version connected to a local OpenAI-compatible service.
- The runtime configuration provides concrete numbers: a **32k context window**, with the coding session actually using about **16k tokens**, and it “basically maxed out” **16GB RAM**.
- The article does not provide strict benchmarks such as **latency, throughput, success rate, or quantitative metrics like HumanEval/SWE-bench**, so there is no standardized performance comparison data.
- The strongest concrete conclusion is engineering feasibility: even on an old M1, for **short code loops, script generation, local automation, and sensitive offline tasks**, this local agentic software-production workflow is “slow, but usable.”

## Link
- [https://advanced-stack.com/fields-notes/qwen35-opencode-lm-studio-agentic-coding-on-m1.html](https://advanced-stack.com/fields-notes/qwen35-opencode-lm-studio-agentic-coding-on-m1.html)
