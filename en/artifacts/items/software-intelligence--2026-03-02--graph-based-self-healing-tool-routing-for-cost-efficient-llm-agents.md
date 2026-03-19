---
source: arxiv
url: http://arxiv.org/abs/2603.01548v1
published_at: '2026-03-02T07:21:15'
authors:
- Neeraj Bholani
topics:
- llm-agents
- tool-routing
- graph-orchestration
- fault-tolerance
- cost-efficiency
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Graph-Based Self-Healing Tool Routing for Cost-Efficient LLM Agents

## Summary
This paper proposes Self-Healing Router, which replaces most LLM control-flow decisions with graph routing and automatically recomputes paths when tools fail, thereby reducing cost and improving observability. The core claim is that common agent decisions are more like “finding an available and inexpensive path” than requiring language reasoning at every step.

## Problem
- Existing tool-using LLM agents face a dilemma between **reliability and cost**: methods like ReAct delegate every decision to the LLM, which is correct but expensive and high-latency.
- Pure workflow/state-machine solutions are cheaper, but they are very brittle under **compound tool failures**; pre-coding branches for all combinations of simultaneous failures leads to combinatorial explosion, so real systems omit cases and produce **silent failures**.
- This matters because production agents frequently encounter API timeouts, rate limits, service outages, and risk interruptions; if the control plane is both expensive and unstable, it is hard to support large-scale automated software execution.

## Approach
- Use **parallel health monitors** instead of the LLM for routine “attention allocation”: modules such as intent classification, risk detection, and tool health checks run in parallel, each producing a priority score, and the highest-scoring signal determines what the system should focus on at the moment.
- Use a **cost-weighted tool graph** to represent executable paths: tools are nodes, dependency/switching relations are edges, and Dijkstra’s algorithm finds the currently cheapest available path.
- When a tool fails during execution, set the weights of its related edges to **infinity**, then rerun Dijkstra from the current position; if an alternative path exists, the system automatically detours, **without calling the LLM**.
- Only when **no feasible path exists anywhere in the graph** does the system call the LLM to perform “goal demotion or escalation,” for example degrading from “refund” to “escalate to human support.”
- The paper also proposes production-oriented extension ideas: combining real-time latency, reliability, rate limits, and availability into dynamic edge weights, together with a circuit breaker; however, the author explicitly notes that these are **architectural suggestions and were not validated experimentally**.

## Results
- Across **19 scenarios and 3 graph topologies** (linear pipeline, dependency DAG, parallel fan-out), Self-Healing Router achieves **19/19 correctness**, matching **ReAct’s 19/19** and outperforming the static workflow baseline at **16/19**.
- The number of control-plane LLM calls drops from **123 for ReAct** to **9**, which the paper claims is a **93% reduction**; meanwhile, the total number of tool calls is **66**, lower than ReAct’s **93** and also lower than the LangGraph baseline’s **87**.
- There were **13 recovery events** handled directly by graph rerouting, and **0 cases requiring LLM involvement for recovery**; the author claims that recovery complexity is **insensitive** to the number of simultaneous failures **K**, remaining just one Dijkstra recomputation.
- Compared with the “well-engineered” LangGraph baseline, Self-Healing Router reduces **silent failures from 3 to 0**; the baseline has **3/19** compound-failure scenarios with silent failures across the 19 scenarios.
- In the customer service domain, Self-Healing Router requires **2 LLM calls** in double/triple-failure scenarios such as **S6/S7** for escalation after no path remains, whereas ReAct requires **8/9 calls** respectively; in the travel domain, cascading failures in **T2/T3/T6** can be recovered graphically with **0 LLM calls**.
- The paper also states a clear limitation: these numbers validate **control-flow properties** (rerouting, escalation, call counts, observability), **not** the semantic correctness of real tool outputs or end-to-end robustness under malformed response conditions.

## Link
- [http://arxiv.org/abs/2603.01548v1](http://arxiv.org/abs/2603.01548v1)
