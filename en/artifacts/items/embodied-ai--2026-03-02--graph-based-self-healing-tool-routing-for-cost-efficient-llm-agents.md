---
source: arxiv
url: http://arxiv.org/abs/2603.01548v1
published_at: '2026-03-02T07:21:15'
authors:
- Neeraj Bholani
topics:
- llm-agents
- tool-routing
- fault-tolerance
- graph-search
- workflow-orchestration
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Graph-Based Self-Healing Tool Routing for Cost-Efficient LLM Agents

## Summary
This paper proposes a **self-healing graph router** for tool-using LLM Agents: it shifts most control-flow decisions from “having the LLM think at every step” to “recomputing shortest paths on a tool graph.” The goal is to substantially reduce LLM invocation costs while preserving correctness, and to avoid the silent failures that static workflows suffer under compound failures.

## Problem
- Existing tool-using Agents often swing between two extremes: **sending every decision to the LLM**, which is correct but expensive and high-latency; or using **pre-coded workflow graphs**, which are cheap but brittle when multiple tools fail at once.
- Covering compound failures with static state machines leads to **combinatorial explosion**: the paper notes that for a system with N tools and K failure modes per tool, one would need to cover roughly **K^N** combinations, otherwise **silent failure** becomes likely.
- This matters because production Agents often depend on external tools for payments, notifications, bookings, reviews, and more; once failure recovery is unreliable, it leads to incorrect execution, higher costs, and lack of observability.

## Approach
- The core mechanism is simple: represent tools and fallback paths as a **weighted graph**, and treat “which tool chain to take” as a **cheapest feasible path search** rather than open-ended reasoning.
- The system first runs **parallel health monitors** (such as intent, risk, tool health, progress, etc.), each outputting a priority score; the highest-scoring signal determines what the system should focus on most at that moment.
- The routing layer uses **Dijkstra shortest path**: under normal conditions it chooses the lowest-cost primary path; if a tool fails during execution, it sets the weights of edges connected to that tool to **infinity**, then **reruns Dijkstra** to automatically detour to a backup path.
- The LLM is invoked only when **no feasible path exists** in the graph, at which point it performs “goal demotion/escalation” reasoning, such as deciding what to do when a refund cannot be completed.
- The author also proposes production-oriented extensions: combining edge weights from real-time telemetry (cost, latency, reliability, rate limits, availability), and integrating a circuit breaker; however, the paper explicitly states that this portion is **an architectural suggestion and was not experimentally validated**.

## Results
- Across **19 scenarios and 3 graph topologies** (linear pipeline, dependency DAG, parallel fan-out), Self-Healing Router achieved **19/19 correctness**, matching **ReAct’s 19/19**, while reducing control-plane **LLM reasoning calls from 123 to 9, a 93% reduction**.
- By contrast, the carefully engineered static-workflow baseline **LangGraph** achieved **16/19 correctness** and exhibited **3 silent failures**; Self-Healing Router had **0** silent failures.
- In the aggregate results table (totals across 19 scenarios): Self-Healing Router **Tools=66, Recovery=13, Silent Fail=0**; ReAct **Tools=93, Recovery=0**; LangGraph **Tools=87, Recovery=24, Silent Fail=3**.
- In the customer service domain (7 scenarios), under S6 “both notification channels fail” and S7 “triple failure,” the static workflow showed **Yes silent fail**; by contrast, Self-Healing Router maintained correctness in these scenarios through rerouting or LLM escalation. Examples in this domain also show that SH used **0 LLM calls** in S1/S2/S5, whereas ReAct required **4/5/5** respectively.
- In the travel booking domain (6 scenarios), Self-Healing Router handled cascading reroutes: for example, T2/T3/T6 recovered with **0 LLM calls**, whereas ReAct required **6/7/8**; in T5, when “both lodging and rental car were unavailable,” it used **1 LLM call** for goal demotion.
- The paper claims that recovery complexity is **insensitive to the number of simultaneous failures K**: Self-Healing Router is **O((V+E) log V)** under both single failures and K simultaneous failures, whereas ReAct/Agent SDKs increase approximately linearly with the number of failures, and static workflows fail when compound failures are not explicitly encoded. It is important to note that the experiments validate **control flow and call counts**, not end-to-end semantic robustness based on real tool outputs.

## Link
- [http://arxiv.org/abs/2603.01548v1](http://arxiv.org/abs/2603.01548v1)
