---
source: hn
url: https://github.com/HeliosNova/nova
published_at: '2026-03-15T23:18:18'
authors:
- heliosnova
topics:
- self-hosted-ai
- continual-learning
- dpo-fine-tuning
- personal-memory
- knowledge-graph
- agentic-system
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Show HN: Nova–Self-hosted personal AI learns from corrections &fine-tunes itself

## Summary
Nova is a self-hostable personal AI assistant whose core selling point is that it continuously remembers and retrieves user corrections, and automatically performs DPO fine-tuning once enough samples have accumulated. It emphasizes local execution, keeping data on-device, and a complete self-improvement pipeline built around memory, a knowledge graph, tool use, and safety mechanisms.

## Problem
- Existing assistants typically **do not turn user corrections into persistent capability improvements**; the same mistakes may recur repeatedly, which hurts long-term usability and personalization.
- If a personal AI depends on the cloud, it introduces **privacy, data sovereignty, and deployment control** concerns; this is especially important for users who want local control of their data.
- One-shot conversational Q&A lacks a **systematic learning closed loop**: correction, memory, knowledge updates, training, evaluation, and deployment are often fragmented from one another.

## Approach
- The core mechanism is simple: **when a user corrects something once, the system stores what was wrong and what was right as a lesson, and prioritizes retrieving it for similar future questions**, thereby "remembering the lesson."
- Each correction also automatically generates a **DPO training pair** `{query, chosen, rejected}`; once samples accumulate to a certain scale, it triggers a closed loop of **automatic fine-tuning → A/B evaluation → deployment**.
- The system splits post-conversation learning into multiple modules: **correction detection (regex prescreen + LLM confirmation)**, fact extraction, reflexion-based failure analysis, curiosity-based knowledge gap discovery, and success patterns positive-sample collection.
- To support long-term memory and retrieval, Nova combines **conversation history, facts, lessons, skills, and a temporal knowledge graph**, and uses **ChromaDB vector retrieval + SQLite FTS5 + Reciprocal Rank Fusion** for document recall.
- From an engineering standpoint, it is a **local-first, provider-agnostic** async Python/FastAPI system that supports tool loops, MCP client/server, automatic model routing, and multi-layer security protections.

## Results
- The most concrete "result" given in the text is a **qualitative example**: it initially answers the capital of Australia as Sydney, and after the user corrects it to Canberra, **3 months later** it answers **Canberra** when asked again, suggesting the claimed persistent memory capability.
- Resource and deployment metrics: local GPU mode recommends **NVIDIA GPU 20GB+ VRAM**; a quantized mode is claimed to fit **16GB VRAM**; it also supports **cloud mode without a GPU**.
- Engineering scale metrics: the system provides **21 tools**, allows up to **5 rounds** in the tool loop, includes **14 proactive monitors**, the knowledge graph contains **20 canonical predicates**, and the environment has **75+ configuration items**.
- Test coverage metrics: the author claims **1,443 tests** across **57 files**, covering the brain pipeline, learning loop, tools, security, stress/concurrency, behavioral, and e2e.
- Specific safety and architecture claims: it supports **4 types of prompt injection detection**, **4 layers of access control**, and enables **HMAC-SHA256 skill signing** by default.
- **No quantitative model results on standard benchmarks are provided**: there are no reproducible experimental figures such as accuracy, win rate, A/B lift magnitude, or post-training improvement relative to baseline, so the claim that it is "more unique/stronger than other open-source projects" is currently mainly a product and systems-design claim.

## Link
- [https://github.com/HeliosNova/nova](https://github.com/HeliosNova/nova)
