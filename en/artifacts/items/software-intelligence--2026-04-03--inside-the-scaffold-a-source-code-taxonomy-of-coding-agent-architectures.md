---
source: arxiv
url: http://arxiv.org/abs/2604.03515v1
published_at: '2026-04-03T23:30:02'
authors:
- Benjamin Rombaut
topics:
- coding-agents
- source-code-taxonomy
- agent-architecture
- software-engineering
- llm-scaffolds
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Inside the Scaffold: A Source-Code Taxonomy of Coding Agent Architectures

## Summary
This paper builds a source-code taxonomy of 13 open-source coding agent scaffolds. It argues that coding agents differ less by high-level labels like “planning” or “tool use” and more by concrete scaffold choices in control loops, tools, state, and context handling.

## Problem
- Research surveys group coding agents by abstract capabilities, but those labels cannot separate systems with very different scaffold code, cost, and failure modes.
- Trajectory studies show what agents do at runtime, but they do not inspect the source code that drives those behaviors.
- This matters because scaffold design affects reliability, token use, and evaluation, and current benchmark results often mix scaffold effects with model effects.

## Approach
- The authors analyze 13 open-source coding agents at pinned commit hashes, covering CLI tools, SWE-bench agents, and one minimal baseline.
- They derive a taxonomy from source-code inspection rather than documentation, grounding each claim in file paths and line numbers.
- Each agent is described across 12 dimensions in 3 layers: control architecture, tool and environment interface, and resource management.
- The study identifies five reusable loop primitives: ReAct, generate-test-repair, plan-execute, multi-attempt retry, and tree search.
- It compares how agents combine these primitives and how they differ in tool count, context compaction, state management, execution isolation, and model routing.

## Results
- The corpus includes **13 agents**, selected from an initial pool of **22** candidates.
- **11 of 13 agents** combine multiple loop primitives instead of using a single control structure.
- **7 of 13 agents** use a sequential **ReAct** loop as their primary control structure.
- Tool availability ranges from **0 tools** in Aider to **37 action classes** in Moatless Tools.
- Context compaction spans **7 distinct strategies**, and control designs range from fixed pipelines to full **Monte Carlo Tree Search**.
- The paper does **not report benchmark gains or new task-performance numbers**. Its main concrete claim is that coding-agent scaffolds resist clean discrete categories and are better described as compositions along continuous design spectra.

## Link
- [http://arxiv.org/abs/2604.03515v1](http://arxiv.org/abs/2604.03515v1)
