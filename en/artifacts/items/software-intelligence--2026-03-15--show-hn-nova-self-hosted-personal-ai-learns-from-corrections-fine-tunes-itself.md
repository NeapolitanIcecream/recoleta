---
source: hn
url: https://github.com/HeliosNova/nova
published_at: '2026-03-15T23:18:18'
authors:
- heliosnova
topics:
- self-hosted-ai
- continual-learning
- dpo-finetuning
- personal-assistant
- knowledge-graph
- agentic-systems
relevance_score: 0.8
run_id: materialize-outputs
language_code: en
---

# Show HN: Nova–Self-hosted personal AI learns from corrections &fine-tunes itself

## Summary
Nova is a self-hostable personal AI assistant whose core selling point is turning user corrections into persistent memory, training samples, and automatic fine-tuning, so it keeps getting smarter locally over time. It integrates retrieval, tool use, a knowledge graph, reflection, and safety mechanisms into an end-to-end learning loop.

## Problem
- Existing assistants typically **do not learn permanently from user corrections**, so the same mistakes can recur, reducing long-term personalization and reliability.
- Cloud assistants often require data to be sent out; this matters for individuals and developers who value privacy, sovereignty, and local control.
- For a personal AI to be truly useful, it must not only answer questions, but also accumulate memory, discover knowledge gaps, and improve itself once enough data has been gathered.

## Approach
- Nova converts post-conversation “corrections” into multiple reusable assets: **lesson storage**, **DPO training pairs**, and knowledge graph updates; when similar questions arise later, it retrieves these learning results first.
- The reasoning pipeline is engineered: it loads history/facts/lessons/KG, uses **rules for intent classification** at the top layer, then uses **ChromaDB vector retrieval + SQLite FTS5 + Reciprocal Rank Fusion** to recall information, assembles the prompt, generates a response, and can enter a tool loop of up to 5 rounds.
- After responding, it continues “background learning”: **correction detection**, **fact extraction**, **reflexion** (silent failure detection), **curiosity engine** (detecting unknowns/tool failures and queuing research), and **success patterns** (positive reinforcement for high-scoring answers).
- Once enough DPO samples have accumulated, the system triggers **automatic fine-tuning** and performs **A/B evaluation** before deployment; the model layer is provider-agnostic and can switch between local models and cloud models.
- The system emphasizes autonomy, control, and safety: local deployment, dual MCP client/server roles, dynamic tool integration, 4 classes of prompt injection detection, SSRF protection, training data poisoning defenses, signed skills, and Docker hardening.

## Results
- The text **does not provide quantitative results on standard benchmark datasets**, nor does it report systematic experimental results such as accuracy, win rate, latency, or cost.
- The most concrete performance claim is a behavioral example: after being corrected that “the capital of Australia is Canberra,” when asked the same question again **3 months later**, it can answer correctly, indicating its claimed **persistent learning** ability.
- The project claims to have a complete automatic improvement loop: each correction generates **1 DPO training pair** (`query, chosen, rejected`), and once enough samples exist it automatically executes **train -> eval -> deploy**.
- In terms of engineering scale, the author cites **~74 async Python files**, **21 tools**, **up to 5 rounds of tool looping**, **14 active monitoring tasks**, a temporal knowledge graph with **20 canonical predicates**, and **75+ configuration options**.
- For testing, the project claims to include **1,443 tests** covering **57 files**, spanning the brain pipeline, learning loop, tools, channels, security, stress/concurrency, behavioral, and e2e.
- For deployment requirements, the full local main-model setup requires an **NVIDIA GPU with 20GB+ VRAM**; it also claims to support a **cloud mode with no GPU** and a **quantized mode with 16GB VRAM**.

## Link
- [https://github.com/HeliosNova/nova](https://github.com/HeliosNova/nova)
