---
source: arxiv
url: https://arxiv.org/abs/2607.01929v1
published_at: '2026-07-02T09:23:48'
authors:
- Jiayi Zhang
- Kai Huang
- Yang Liu
- Chunyang Chen
topics:
- code-intelligence
- software-agents
- program-repair
- swe-bench
- multimodal-reasoning
- repository-graphs
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Beyond Textual Repository Exploration: Dual-Modal Structural Reasoning for Agentic Issue Resolution

## Summary
DualView adds visual and text graph views to software issue-resolution agents so they can inspect repository structure before editing code. The paper claims this improves SWE-bench performance, with the best reported run solving 388 SWE-bench Pro instances.

## Problem
- Issue-resolution agents spend much of their work budget reading repository text; the paper cites 76.1% of a coding agent’s token budget on SWE-bench Verified going to file reading with tools such as grep and cat.
- Text-only exploration makes agents rebuild module links, call paths, class inheritance, and local data flow across many steps, which can cause missed localization in large repositories.
- Existing graph-based code tools often serialize graphs as text, which hides multi-hop paths, fan-in and fan-out, and dense dependency regions.

## Approach
- DualView gives the agent four queryable graph views: Module Coupling Graph for subsystems, Function Call Graph for caller-callee paths, Class Hierarchy Graph for inheritance and implementations, and Program Dependence Graph for statement-level data and control flow.
- Each query returns two synchronized outputs from the same graph slice: a rendered node-link image and a concise text record with names, paths, line numbers, relation types, and query scope.
- The agent uses these graph tools when it needs structure, then returns to normal tools such as search, file inspection, and editing for source-level work.
- In simple terms, DualView lets the agent look at a map of the codebase and then use the text labels to open the right files and lines.

## Results
- On SWE-bench Pro, DualView reports up to 388 resolved instances.
- On SWE-bench Pro with OpenCode and Kimi K2.5, DualView solves 46 more instances than the stated baseline configuration.
- The paper says gains hold across multiple agent architectures and model families on SWE-bench Pro and SWE-bench Verified, but the excerpt does not provide the full per-model table.
- Ablations claim visual graph outputs beat equivalent textual graph descriptions, and combined visual plus textual graph outputs perform best; the excerpt gives no exact ablation numbers.
- The paper packages the interface as reusable tools and MCP services, and says the implementation is released as open source.

## Link
- [https://arxiv.org/abs/2607.01929v1](https://arxiv.org/abs/2607.01929v1)
