---
source: hn
url: https://www.vichoiglesias.com/writing/agent-failures-dont-start-where-they-appear
published_at: '2026-03-11T23:39:33'
authors:
- vichoiglesias
topics:
- agent-debugging
- failure-analysis
- execution-traces
- state-tracking
- long-horizon-agents
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# Agent Failures Don't Start Where They Appear

## Summary
This article argues that failures in long-running agents usually do not begin at the step where the error surfaces, but are instead determined earlier at some state inflection point. The author advocates changing the debugging goal from "where did it go wrong" to "when did the system first enter an unrecoverable failure state."

## Problem
- The visible failure in long-chain agent execution is often only the result of an earlier erroneous state propagating forward, so tracing logs backward from the end is often inefficient and misleading.
- Existing agent observability tools mainly record events, prompts, tool calls, and latency, but cannot directly locate the causal boundary where the system goes from recoverable to unrecoverable.
- This matters because runs may last from tens of minutes to hours; if the earliest failure point cannot be found, engineers can only manually reconstruct the story, making debugging costly and unstable.

## Approach
- The core idea is to treat failure as a **state trajectory problem propagated over time**, rather than a problem of a single action or a single function call.
- What needs to be recorded is not just the event log, but also the system state at each step: what the agent knew at that time, how internal variables changed, and whether risk conditions had already been met.
- With a time-evolving history of states, it becomes possible to determine which step first made the failure condition true—that is, the moment when the future began to break.
- The author further proposes turning this localization process into a search problem over execution history, and claims that the failure starting point can be found in **logarithmic time**.

## Results
- The article does not provide formal experiments, datasets, or baseline comparisons, nor does it report accuracy, recall, or runtime metrics.
- The strongest concrete claim is that if execution history records state evolution, it is possible to search for the **exact step where failure first began**.
- The article explicitly claims that this search can be completed in **logarithmic time**, but does not provide algorithmic details, a complexity proof, or implementation results.
- The article illustrates the idea with examples: for instance, when an improper approval appears at step **47**, the state change that truly caused the failure may have occurred earlier at step **12** or some intermediate step, but this is only a conceptual illustration, not an experimental result."

## Link
- [https://www.vichoiglesias.com/writing/agent-failures-dont-start-where-they-appear](https://www.vichoiglesias.com/writing/agent-failures-dont-start-where-they-appear)
