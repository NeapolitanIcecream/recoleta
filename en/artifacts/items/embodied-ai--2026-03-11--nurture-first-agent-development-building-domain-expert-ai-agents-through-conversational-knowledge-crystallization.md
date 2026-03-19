---
source: arxiv
url: http://arxiv.org/abs/2603.10808v1
published_at: '2026-03-11T14:14:53'
authors:
- Linghao Zhang
topics:
- llm-agents
- knowledge-crystallization
- memory-augmented-agents
- human-ai-collaboration
- agent-development-methodology
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Nurture-First Agent Development: Building Domain-Expert AI Agents Through Conversational Knowledge Crystallization

## Summary
This paper proposes a development methodology for domain-expert agents: **Nurture-First Development (NFD)**, which argues that agents should be continuously “nurtured” through real conversations rather than being built once and for all in advance with code or prompts. The core idea is to periodically distill fragmented expert knowledge from everyday interactions into reusable, structured knowledge assets.

## Problem
- The paper aims to solve the problem of how to effectively encode **tacit, personalized, and continuously changing** domain-expert knowledge into AI agents, rather than relying only on the capabilities of general-purpose large models.
- Traditional **code-first** methods emphasize explicit rules and struggle to capture expert judgment; **prompt-first** methods rely on static prompts and run into context-window and maintenance issues as complexity grows.
- This matters because many high-value scenarios (such as finance, medicine, law, and research) depend on continuously evolving practical experience and contextual judgment. Static configurations quickly become outdated, creating a deployment gap where “the capability exists, but it is not trustworthy.”

## Approach
- The paper proposes **NFD**: development and deployment are no longer separate; agents are launched first with minimal scaffolding and then continuously grow through everyday conversations with domain practitioners.
- The core mechanism is the **Knowledge Crystallization Cycle**: fragmented experience is first gathered through conversations, then periodically refined, validated, and written into structured knowledge for future reuse.
- It designs a **Three-Layer Cognitive Architecture** that divides knowledge into three layers: **Constitutional** (identity/principles, low change), **Skill** (task skills and reference materials, medium change), and **Experiential** (interaction logs and case memory, high change).
- It proposes the **Dual-Workspace Pattern** and **Spiral Development Model**: one workspace is used for everyday “nurturing-style” use, while the other is used for surgical-style organization and upgrading of knowledge; the system gradually improves its capabilities over multiple cycles.
- The paper also provides formal definitions, including knowledge states, crystallization operations, and efficiency metrics, and uses a financial analysis agent for U.S. stock research as a case study.

## Results
- The paper’s main contributions are a **methodology, architecture, and formal framework**, rather than improved model performance on standard benchmarks; the excerpt **does not provide verifiable quantitative experimental results**.
- It explicitly claims that the key difference of NFD compared with code-first / prompt-first is that development and deployment are a **continuous, concurrent** process, rather than developing first and launching later.
- Table 1 provides several qualitative comparisons: **time to first value** changes from code-first’s “**weeks–months**” and prompt-first’s “**hours–days**” to NFD’s “**minutes** (minimal scaffolding) and continued growth.”
- The paper argues that NFD’s scaling bottleneck is no longer mainly engineering labor or context-window limits, but **memory search quality**; this is a new system design trade-off rather than a conclusion already validated through numerical experiments.
- At the case-study level, the authors present a financial research agent for **U.S. equity analysis** as an illustration of the paradigm’s operability, but the excerpt does not report task success rate, accuracy, cost, user studies, or numerical comparisons with baseline systems.

## Link
- [http://arxiv.org/abs/2603.10808v1](http://arxiv.org/abs/2603.10808v1)
