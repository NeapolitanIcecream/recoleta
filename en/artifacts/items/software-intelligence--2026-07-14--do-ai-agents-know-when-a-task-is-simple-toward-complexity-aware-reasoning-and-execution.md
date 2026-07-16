---
source: arxiv
url: https://arxiv.org/abs/2607.13034v1
published_at: '2026-07-14T17:59:31'
authors:
- Junjie Yin
- Xinyu Feng
topics:
- software-agents
- code-intelligence
- adaptive-computation
- tool-use
- execution-efficiency
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Do AI Agents Know When a Task Is Simple? Toward Complexity-Aware Reasoning and Execution

## Summary
E3 helps software agents estimate a task's required execution scope, start with the smallest viable path, and expand only when verification fails. In a controlled benchmark, it preserves success while sharply reducing cost, token use, and file inspection.

## Problem
- LLM agents often use a maximum-context-first strategy, rereading files and dependencies even for localized edits; this matters because unnecessary context increases latency, tokens, tool calls, and engineering cost without improving correctness.
- The paper addresses the missing ability to estimate task difficulty, required information, and the shortest reliable execution path before acting.

## Approach
- E3 (Estimate, Execute, Expand) first predicts difficulty, scope, risk, and confidence from the task and at most one cheap environment probe.
- It executes a minimum viable path: localized edits for simple tasks, broader file inspection or dependency tracing only for larger estimated scopes.
- It verifies the result and expands scope incrementally when verification fails or confidence is low, reusing cached search results rather than restarting.
- The paper formalizes minimum-sufficient execution and the Agent Cognitive Redundancy Ratio (ACRR), which measures realized cost relative to an oracle-defined minimum.

## Results
- On MSE-Bench, a deterministic benchmark with 121 edits, E3 matches the strongest baseline at 100% success while reducing total cost by 85%, tokens by 91%, and inspected files by 92%.
- E3 also outperforms a strong adaptive retrieval baseline by 16% on cost at comparable success, indicating that the gains are not limited to comparison with a maximum-context-first policy.
- Under held-out instruction wording, E3 retains 100% success and remains the cheapest fully successful policy under essentially every tested cost weighting.
- In the LLM-Case real-model harness, a live gpt-4o agent editing an open-source library showed milder but measurable over-reading; E3 was the leanest and fastest policy at comparable task success, with its only reported shortfall caused by a provider rate limit rather than an incorrect edit.
- The evidence is strongest for the capability-controlled simulator and the reported harness cases; it does not establish performance for deployed agents generally.

## Link
- [https://arxiv.org/abs/2607.13034v1](https://arxiv.org/abs/2607.13034v1)
