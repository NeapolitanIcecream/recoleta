---
source: arxiv
url: http://arxiv.org/abs/2604.02375v1
published_at: '2026-03-31T21:38:28'
authors:
- Cormac Guerin
- Frank Guerin
topics:
- llm-agents
- tool-use
- agent-execution
- security-gating
- parallel-planning
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# KAIJU: An Executive Kernel for Intent-Gated Execution of LLM Agents

## Summary
KAIJU is an execution-layer architecture for LLM agents that separates planning from tool execution and adds an external intent gate for tool authorization. The paper argues that this cuts context growth, enables parallel execution, and blocks some failure and safety modes that ReAct-style agents cannot prevent with prompts alone.

## Problem
- ReAct-style tool agents accumulate full history across turns, giving quadratic token growth: the paper states total cost is $O(n^{2}k)$, with about 63K tokens for a 7-tool task and about 250K for an 18-tool task.
- The model keeps control of tool use at each turn, so after tool failures or partial results it can stop early, fall back to parametric knowledge, or ask the user instead of finishing the task.
- Safety rules usually live in prompts or model-side defenses, which the paper says are weak against hallucination, prompt injection, context overflow, and adaptive attacks.

## Approach
- KAIJU splits the agent into a reasoning layer and an execution layer. The LLM plans a dependency graph up front, then an executive kernel handles scheduling, dependency resolution, tool dispatch, failure recovery, and final result flow.
- The main security mechanism is Intent-Gated Execution (IGX). Each tool call is checked against four variables: scope, intent, impact, and clearance from an external authority.
- The execution layer runs tools in parallel when dependencies allow it, and uses `param_refs` to inject outputs from earlier nodes into later tool arguments without forcing a full sequential reasoning loop.
- The system adapts during execution through three modes: Reflect at dependency-wave boundaries, nReflect after every N completed nodes, and Orchestrator with per-node observers.
- Failed tool calls trigger a scoped micro-planner that adds replacement nodes such as retries with new parameters, alternate tools, or skips, while keeping failed nodes immutable for auditability.

## Results
- In the paper's running example, a ReAct baseline with parallel function calling took 9 LLM calls, 14 tool executions, and 64.5 seconds.
- On the same query, KAIJU in Reflect mode took 4 LLM calls, 10 tool executions, and 41.8 seconds, about 1.54x faster than the ReAct run in wall-clock time.
- The paper claims a latency penalty on simple queries because of planning overhead, convergence at moderate complexity, and a structural advantage on computational queries that benefit from parallel data gathering.
- The paper states token complexity improves from $O(n^{2}k)$ in ReAct to $O(nkd)$ in Reflect mode and to $O(nk)$ in Orchestrator mode, where $d$ is dependency depth.
- Relative to prior DAG execution work, the paper says LLM Compiler reported up to 3.7x speedup over sequential ReAct, while the authors observed similar gains on simple cases, about 7x on complex queries, and up to 18x on highly complex queries against sequential ReAct. The excerpt does not provide a benchmark table or dataset details for these numbers.
- Several claims are structural rather than benchmarked: the model does not observe gate denials, blocked tools are hidden behind the execution layer, and authorization is enforced in compiled code rather than by prompt instructions.

## Link
- [http://arxiv.org/abs/2604.02375v1](http://arxiv.org/abs/2604.02375v1)
