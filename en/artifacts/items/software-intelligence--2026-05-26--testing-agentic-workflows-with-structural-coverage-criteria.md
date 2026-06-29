---
source: arxiv
url: https://arxiv.org/abs/2605.26521v1
published_at: '2026-05-26T04:07:55'
authors:
- Nafiseh Kahani
- Mojtaba Bagherzadeh
topics:
- multi-agent-testing
- agent-workflows
- structural-coverage
- code-intelligence
- software-agents
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Testing Agentic Workflows with Structural Coverage Criteria

## Summary
The paper proposes structural coverage tests for multi-agent workflows, so a test suite can show whether declared agents, tools, restrictions, and handoffs were exercised.

## Problem
- End-to-end task success can pass while some agents, tool permissions, restricted calls, or delegation paths never run.
- Workflow edits can change tool access or handoff structure without causing a benchmark failure, which makes structural regressions hard to see.
- This matters for agent systems with policy, safety, or compliance constraints, where teams need traceable evidence that restrictions and routing rules were tested.

## Approach
- The method converts an agent workflow into a typed coordination graph with agent nodes, tool nodes, allowed tool edges, restricted tool edges, and delegation edges.
- It derives four coverage criteria: reachable agents, allowed tool calls, restricted tool attempts, and delegation edges.
- For each graph obligation, it builds a witness objective such as reaching an agent, using a tool, probing a restricted tool, or triggering a handoff.
- DSPy turns each objective into a natural-language test scenario; runtime traces then decide whether the intended structural event occurred.
- The prototype targets OpenAI Agents SDK-style workflows and extracts manifests from Python agent entry points.

## Results
- The evaluation covers 10 SDK-derived workflows with 49 reachable agents, 47 tools, and 403 structural obligations.
- Generated scenarios witnessed 54 of 75 allowed-tool obligations, or 72%, within the stated refinement budget.
- Generated scenarios witnessed 36 of 48 delegation obligations, or 75%, within the same bounded process.
- Restricted-tool probing produced 23 restricted-call violations out of 248 restricted-tool obligations, identifying concrete misrouting failures.
- The running oai_customer_service example contains 3 reachable agents, 2 tools, 2 allowed tool edges, 4 restricted tool edges, and 4 delegation edges, giving 13 structural obligations.

## Link
- [https://arxiv.org/abs/2605.26521v1](https://arxiv.org/abs/2605.26521v1)
