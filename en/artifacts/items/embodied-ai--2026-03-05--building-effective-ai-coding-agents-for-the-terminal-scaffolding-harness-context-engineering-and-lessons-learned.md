---
source: arxiv
url: http://arxiv.org/abs/2603.05344v2
published_at: '2026-03-05T16:21:08'
authors:
- Nghi D. Q. Bui
topics:
- terminal-agent
- coding-agent
- context-engineering
- agent-scaffolding
- tool-safety
- compound-ai-systems
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned

## Summary
This paper introduces OpenDev, an open-source AI coding agent system design report for the terminal, focusing on how to make long-horizon coding tasks safer, more stable, and more context-efficient. Its main contribution is not a new algorithm, but rather an engineering architecture and a set of practical lessons for real development environments.

## Problem
- Terminal-native coding agents need to operate over **long sessions**, but LLM context windows are limited, which can lead to context bloat, forgetting early information, and degraded reasoning.
- Agents can execute shell commands, modify files, and start processes; without protective mechanisms, they can easily perform **destructive operations**, which is critical in real software development.
- The system must also balance **extensibility, cost, latency, and capability**: the more tools and sub-agents are added, the larger the prompts become, the harder control becomes, and the more practical usability declines.

## Approach
- Proposes OpenDev: a **terminal-first** open-source command-line coding agent that uses a four-layer architecture (UI, Agent, Tool & Context, Persistence) to separate interface, reasoning, tools, context, and persistence responsibilities.
- Uses a **compound AI system** approach for workflow-specific model selection: binding different stages such as thinking, critique, and execution to different LLMs, enabling configurable trade-offs among cost, latency, and capability.
- Adopts a **dual-mode / dual-layer agent** design: Plan Mode allows only read-only tools for safe planning, while Normal Mode performs read-write operations; capability scope is further restricted through sub-agents and tool whitelists.
- Extends the ReAct loop by adding **explicit thinking, optional self-critique, and context compaction** before actions, combined with event-driven system reminders, modular prompt assembly, and cross-session memory to maintain stable behavior during long tasks as much as possible.
- Reduces risk through a **five-layer defense-in-depth safety mechanism**: prompt-layer guardrails, schema-level tool restrictions, runtime approval, tool-level validation, and lifecycle hooks; it also uses lazy tool/MCP discovery to control prompt size.

## Results
- The paper **does not provide quantitative experimental results on standard benchmarks**, nor does it report figures such as accuracy, success rate, or cost comparisons on SWE-bench, Terminal-Bench, or LongCLI-Bench.
- The core positioning of the article is as a **system design and experience report**, explicitly stating that it is "**not to present a novel algorithmic breakthrough**," but rather to disclose the architecture, design trade-offs, and lessons learned of a production-grade terminal coding agent.
- Specific systematic claims include: using a **4-layer system architecture** to organize components; adopting **5 independent protection layers** for safety; using an extended execution loop including compaction/thinking/self-critique/action; and supporting **per-workflow model binding** at the architectural level.
- On the engineering side, it provides relatively concrete and verifiable design details, such as a **4-level hierarchy** of concurrent session → agent → workflow → LLM, sub-agent isolation, lazy loading of external tools, cross-session memory, and event-driven reminders, serving as a blueprint for building terminal-native AI coding agents.

## Link
- [http://arxiv.org/abs/2603.05344v2](http://arxiv.org/abs/2603.05344v2)
