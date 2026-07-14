---
source: arxiv
url: https://arxiv.org/abs/2607.11098v1
published_at: '2026-07-13T05:14:12'
authors:
- Aritra Mazumder
- Nusrat jahan Lia
topics:
- llm-agents
- mcp-security
- fault-injection
- agent-evaluation
- tool-use-reliability
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# AgentCheck: A Reproduce-Intervene-Mitigate Workbench for LLM Agents over MCP

## Summary
AgentCheck is an open-source MCP workbench for reproducing tool failures in LLM agents, testing mitigations, and confirming whether the same failure is fixed. It exposes silent misuse of stale, incorrect, failed, or poisoned tool responses before deployment.

## Problem
- Most agent evaluations assume that tools return valid responses, so they miss failures caused by timeouts, stale data, schema changes, false results, and poisoned instructions.
- These failures matter because agents often act confidently on incorrect tool output or execute unsafe instructions without crashing.

## Approach
- AgentCheck runs an agent once with real tools and caches every tool response.
- It replays the same task while changing one selected response with an injector covering 12 fault types across tool execution, data quality, and security.
- It compares clean and faulted trajectories, identifies the first divergence, and applies deterministic fault-specific pass/fail checks plus LLM-based diagnostic labels.
- A mitigation can be rerun against the identical cached fault, producing a fix-confirmed verdict when the failed checks pass.
- The workbench includes 120 scenarios across five domains and can connect to a developer's own MCP server and agent harness.

## Results
- Across five agent configurations, the strongest agent passed 105/120 scenarios and the weakest passed 77/120.
- The evaluation found that failures were usually silent acceptance or propagation of incorrect tool outputs rather than agent crashes.
- For the weakest agent, a retry mitigation improved timeout-fault success from as low as 30% to 100% of cases.
- Stale-data faults remained difficult: success stayed near 3-4 out of 10 cases across mitigations.
- The scenario suite contains 120 cases, with 10 cases for each of 12 fault types, and the scoring checks were validated against human annotations.

## Link
- [https://arxiv.org/abs/2607.11098v1](https://arxiv.org/abs/2607.11098v1)
