---
source: arxiv
url: http://arxiv.org/abs/2603.05344v2
published_at: '2026-03-05T16:21:08'
authors:
- Nghi D. Q. Bui
topics:
- coding-agents
- terminal-agents
- context-engineering
- tool-using-llms
- software-engineering
- agent-safety
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Building Effective AI Coding Agents for the Terminal: Scaffolding, Harness, Context Engineering, and Lessons Learned

## Summary
This paper introduces OpenDev, an open-source AI coding agent system for the terminal. Its focus is not on proposing new algorithms, but on summarizing how to make terminal agents safer, more extensible, and capable of sustained long-running operation. The paper’s core value lies in organizing scaffolding, runtime orchestration, context engineering, and safety mechanisms into a reusable engineering blueprint.

## Problem
- Although terminal-native coding agents are closer to developers’ real workflows, they encounter **long-horizon task** issues such as exhausting the context window, declining reasoning quality, and behavioral drift.
- These agents can directly execute shell commands, modify files, and run processes. Without systematic constraints, they can easily perform **destructive operations**, making safety more critical than in ordinary IDE autocompletion.
- Agents also need to support a growing number of tools and capabilities, but putting all tools/instructions into the prompt causes **prompt bloat**, hurting cost, latency, and effectiveness. This matters for software foundation models and automated software production because real software engineering tasks often span multiple steps, sessions, and toolchains.

## Approach
- Proposes **OpenDev**: an open-source, terminal-first command-line coding agent with a four-layer architecture (UI, Agent, Tool & Context, Persistence) that separates build-time **scaffolding** from runtime **harness**.
- Uses a **compound AI system** design: different workflows/stages can be bound to different LLMs; it also adopts a **dual-agent / dual-mode** structure that separates read-only planning (Plan Mode) from executable modification (Normal Mode) to reduce risk and balance cost, latency, and capability.
- Extends standard ReAct by adding explicit **thinking** and optional **self-critique** phases before actions, and directly embedding **adaptive context compaction** into the loop so that older observations are progressively compressed when context approaches its limit.
- Controls context burden through **conditional prompt assembly**, **event-driven system reminders**, **cross-session memory**, and **lazy tool discovery**: instructions/skills/tools are injected only when relevant, reducing prompt redundancy and mitigating instruction fade-out.
- Employs a **five-layer defense-in-depth safety architecture**: prompt-level guardrails, schema-level tool restrictions, runtime approval, tool-level validation, and lifecycle hooks, with multiple independent layers intercepting dangerous operations.

## Results
- The paper **does not provide explicit quantitative experimental results or benchmark scores**; the excerpt does not report accuracy, pass rate, cost, or latency numbers for SWE-bench, Terminal-Bench, or LongCLI-Bench.
- The strongest concrete claim is that OpenDev provides a systematic technical report for an **open-source, terminal-native, interactive** coding agent, which the authors claim is the first relatively complete public disclosure of the engineering design of such a system in the literature.
- Concrete system-level outputs include a **4-layer overall architecture**, **5 model roles**, a **6-stage execution loop**, a **5-layer safety mechanism**, and a **4-level hierarchical organization** of session → agent → workflow → LLM.
- The authors claim these mechanisms bring several engineering benefits: better cost/latency/capability trade-offs, safer terminal execution, higher context efficiency, and accumulation of project knowledge across sessions; however, the excerpt **does not provide verifiable numerical comparisons** showing superiority over Claude Code, Aider, OpenHands, or SWE-Agent.

## Link
- [http://arxiv.org/abs/2603.05344v2](http://arxiv.org/abs/2603.05344v2)
