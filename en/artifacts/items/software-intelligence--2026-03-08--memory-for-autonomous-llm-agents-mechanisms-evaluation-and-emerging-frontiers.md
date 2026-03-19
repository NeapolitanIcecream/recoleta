---
source: arxiv
url: http://arxiv.org/abs/2603.07670v1
published_at: '2026-03-08T15:08:01'
authors:
- Pengfei Du
topics:
- llm-agent-memory
- agent-evaluation
- retrieval-augmented-memory
- reflective-agents
- hierarchical-memory
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Memory for Autonomous LLM Agents:Mechanisms, Evaluation, and Emerging Frontiers

## Summary
This is a survey of “memory” systems for autonomous LLM agents, systematically reviewing memory mechanisms, taxonomy, evaluation, and engineering challenges. The paper argues that memory is not simple retrieval, but a core capability that determines whether an agent can learn across sessions, avoid repeating mistakes, and continuously adapt to its environment.

## Problem
- Existing LLMs are fundamentally stateless, and a single context window cannot contain long interaction histories, lessons learned, and user preferences, causing agents to repeatedly explore, repeat mistakes, and forget across sessions.
- For autonomous agents, memory affects not only question-answering quality, but also directly impacts decision-making, planning, and action success, making it a key capability for moving from a “text generator” to an “adaptive agent.”
- The field lacks a unified formal framework, a systematic classification of mechanisms, and evaluation methods that can genuinely measure whether memory improves downstream agent performance.

## Approach
- The paper formalizes agent memory as a **write-manage-read** loop coupled with the perception-action loop: writing is not just appending, but also includes summarization, deduplication, priority scoring, contradiction handling, and deletion.
- It proposes a unified three-dimensional taxonomy that organizes existing methods by **temporal scope** (working/episodic/semantic/procedural), **representational substrate** (context text/vector store/structured DB/executable repo), and **control policy** (heuristic/prompted/learned).
- It provides an in-depth synthesis of five core mechanism families: in-context compression, retrieval-augmented storage, reflective self-improvement, hierarchical virtual context, and policy-learned memory management.
- On evaluation, the paper emphasizes shifting from static recall tests to multi-session agentic benchmarks coupled with decision-making and actions, and compares multiple recent benchmarks to reveal systematic gaps in current systems.
- It also discusses engineering realities such as write filtering, conflicting memory handling, latency/cost budgets, privacy governance, and deletion compliance.

## Results
- This is a **survey paper** and does not present experimental results for a new single algorithm; its main “results” are a structured synthesis and comparison of prior work.
- One key piece of evidence cited is that **Voyager**, when its skill library is removed, shows a **15.3×** slowdown in tech-tree milestone progression, indicating that procedural memory is almost a core performance factor for open-world agents.
- In **MemoryArena (2026)**, replacing an active-memory agent with a long-context-only baseline reduces the completion rate on cross-session interdependent tasks from **80%+** to about **45%**.
- In representative system comparisons, **Reflexion** reaches **91% pass@1** on **HumanEval**, while the non-reflective **GPT-4 baseline** is **80%**, showing that “reflective memory” can significantly improve coding-task performance.
- **ReAct** reports a **34% absolute gain** on **ALFWorld**; **Voyager** achieves **3.3× more unique items** and **15.3× faster tech-tree progression** in Minecraft, suggesting that memory design can yield gains comparable to model scaling.
- The paper also cites **RETRO**: a **7.5B** parameter model, with retrieval, can match **175B Jurassic-1** on **10** out of **16** benchmarks; and **LoCoMo** covers up to **35 sessions, 300+ turns, 9k–16k tokens**, yet humans still significantly outperform, indicating that long-term memory evaluation is far from saturated.

## Link
- [http://arxiv.org/abs/2603.07670v1](http://arxiv.org/abs/2603.07670v1)
