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
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Agent Failures Don't Start Where They Appear

## Summary
This article argues that failures in long-running agent systems usually do not begin at the step where they "appear to go wrong," but rather enter an unrecoverable state earlier. The author advocates shifting the focus of debugging from reading end-of-run logs to locating the state transition point where failure first became inevitable.

## Problem
- Traditional agent debugging usually works backward from the final error through the trace, but in long trajectories the visible error is often only a downstream result of an earlier problem.
- Observable logs such as prompts, tool calls, and model outputs can only reconstruct the process; they cannot directly indicate when the system first entered an unrecoverable failure state.
- For long-running systems, failing to identify this causal boundary makes troubleshooting slow, subjective, and prone to misjudgment, which matters for production-grade agent systems.

## Approach
- The core idea is to treat failure as a **trajectory problem that propagates over time**, rather than a single-point event; the real question should be: **At which step did the system first enter a state where failure had become inevitable?**
- To do this, the execution history needs to record the **evolution of state over time**, not just external events, but also what the agent "knew" at each step and how key internal state changed.
- Once states can be compared across time steps, it becomes possible to check when a violation condition or failure condition first became true, thereby locating the boundary where the future effectively broke.
- The author further claims that if run history is recorded in this way, the starting point of failure can be searched for in **logarithmic time**, rather than by manually reading through a long trace line by line.

## Results
- The article does not provide experimental data, benchmark datasets, or quantitative evaluation results.
- The strongest concrete claim is that by recording state evolution rather than only events, it becomes possible to locate the step where failure first became unrecoverable, instead of only seeing the final visible error.
- The author's efficiency claim is that the failure origin can be found in **logarithmic time**, but no algorithmic details, complexity proof, or experimental validation are provided.
- The article uses transaction sanctions screening as an example to illustrate the point: for instance, the incorrect approval may only appear at **step 47**, while the state change that truly caused the failure may have occurred earlier, such as at **step 12** or another intermediate step; these numbers are illustrative examples, not experimental results.

## Link
- [https://www.vichoiglesias.com/writing/agent-failures-dont-start-where-they-appear](https://www.vichoiglesias.com/writing/agent-failures-dont-start-where-they-appear)
