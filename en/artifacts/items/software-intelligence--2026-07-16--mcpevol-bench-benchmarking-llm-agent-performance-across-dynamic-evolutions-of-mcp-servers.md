---
source: arxiv
url: https://arxiv.org/abs/2607.14642v1
published_at: '2026-07-16T07:09:49'
authors:
- Huanxi Liu
- Kun Hu
- Jiaqi Liao
- Qiang Wang
- Pengfei Qian
- YuanZhao Zhai
- Dawei Feng
- Bo Ding
- Huaimin Wang
topics:
- software-foundation-model
- code-intelligence
- agent-network
- multi-agent-software-engineering
- human-ai-interaction
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# MCPEvol-Bench: Benchmarking LLM Agent Performance Across Dynamic Evolutions of MCP Servers

## Summary
MCPEvol-Bench evaluates whether LLM agents can preserve task performance when MCP tool interfaces and functions evolve. Across 12 models, evolved servers caused substantial degradation, showing that static tool-use benchmarks overestimate agent reliability in changing environments.

## Problem
- Existing MCP and tool-use benchmarks evaluate agents against largely static toolsets, so they do not measure adaptation to changed tools, parameters, descriptions, or server functionality.
- This matters because MCP servers evolve in practice: remote-server availability fell from 72.7% to 52.0% over 12 weeks, and 54.6% of analyzed initial tools were modified or deprecated.

## Approach
- The benchmark contains 123 MCP servers, 1,272 tools, and 201 multi-tool tasks across nine domains; each task is tested on original servers and versions evolved after three and five mutation rounds.
- The authors derive 11 mutation operators from observed MCP evolution, covering tool, parameter, and description changes such as additions, replacements, deletions, constraint mutations, and description updates.
- An LLM-driven pipeline uses AST-based code anchoring, applies mutations to source repositories, validates syntax and functionality, and deploys the resulting multi-version MCP servers.
- Agents are evaluated with 1–10 Task Fulfillment and Planning Effectiveness scores, plus an Evolutionary Competency Score that rewards high performance and low cross-version variance.

## Results
- GPT-5.4's task-fulfillment performance declined by 13.7% and Claude-Sonnet-4-6's declined by 14.4% on evolved MCP servers; the study evaluated 12 LLMs across 201 tasks.
- Server evolution increased planning errors by 34.1% and reasoning errors by 35.6% in analyzed agent trajectories.
- Tool additions and modifications caused the strongest performance losses, while removing redundant tools or parameters had negligible effects on original workflow execution.
- The benchmark's simulated evolutions showed high semantic similarity to real-world version updates and strong agreement with human evaluations, although the excerpt does not provide the corresponding similarity or agreement values.
- Adding reflection, planning, and memory modules improved agent adaptability, but the excerpt does not report their quantitative gains or a complete model-by-model baseline table.

## Link
- [https://arxiv.org/abs/2607.14642v1](https://arxiv.org/abs/2607.14642v1)
