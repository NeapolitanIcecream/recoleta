---
source: arxiv
url: https://arxiv.org/abs/2606.10106v1
published_at: '2026-06-08T19:35:37'
authors:
- Sanderson Oliveira de Macedo
topics:
- agent-harnesses
- coding-agents
- software-engineering-ai
- agent-control
- context-management
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# What makes a harness a harness: necessary and sufficient conditions for an agent harness

## Summary
The paper defines an agent harness as the runtime layer that wraps one or more language models and lets them work on an external environment through a loop, tools, context management, and control. It gives a membership test for coding-agent systems rather than a new agent or benchmark.

## Problem
- Agent harness is used for products, eval scaffolds, SDKs, IDE plugins, and orchestrators, which makes system comparison unclear.
- The distinction matters because coding agents edit repositories and run commands; prompts alone cannot verify that the agent’s claimed success matches repository state.
- The paper targets a reference definition that can include and exclude concrete systems consistently.

## Approach
- It uses conceptual analysis of research papers, official docs, glossaries, and engineering reports.
- It traces the term from horse tack to software test harnesses, ML evaluation harnesses, and runtime agent harnesses.
- It defines 4 required runtime conditions: an agent loop, a tool interface that can change the environment, task-aware context management, and control mechanisms independent of model obedience.
- It turns those conditions into tests T1-T4, then checks boundaries against agent frameworks, agent SDKs, IDE plugins, eval harnesses, and orchestrators.
- It applies the test to 6 systems: Claude Code, Codex CLI, Aider, Cline, OpenHands, and SWE-agent.

## Results
- The paper claims a necessary and sufficient definition with 4 conditions: loop, tools, context management, and control.
- It applies the inclusion test to 6 real coding-agent harnesses and reports consistent classification.
- It separates the concept from 5 neighboring categories: agent framework, agent SDK, IDE plugin, eval harness, and orchestrator.
- It gives concrete thresholds for 3 conditions: T2 requires changing the environment, T3 requires task-aware context selection, and T4 requires controls that do not depend on model cooperation.
- It reports no benchmark accuracy, pass-rate, cost, or latency results; the contribution is a shared definition and decision test, not measured agent performance.

## Link
- [https://arxiv.org/abs/2606.10106v1](https://arxiv.org/abs/2606.10106v1)
