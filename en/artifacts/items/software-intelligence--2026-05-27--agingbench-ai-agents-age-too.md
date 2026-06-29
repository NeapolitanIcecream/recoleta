---
source: hn
url: https://agingbench.github.io
published_at: '2026-05-27T23:10:09'
authors:
- zfancy
topics:
- ai-agents
- agent-reliability
- memory-systems
- benchmarking
- longitudinal-evaluation
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# AgingBench: AI Agents Age Too

## Summary
AgingBench tests whether long-lived AI agents stay reliable as their memory and state change after deployment. A frozen base model can still fail when the agent harness compresses, retrieves, revises, or maintains state over time.

## Problem
- Day-one benchmarks evaluate freshly initialized agents and miss failures that appear after many sessions.
- Persistent agents accumulate summaries, memories, revised facts, and maintenance events, so reliability depends on the full memory pipeline.
- Operators need to know whether a failure comes from writing, retrieval, or utilization so repair targets the right component.

## Approach
- AgingBench defines four aging mechanisms: compression aging, interference aging, revision aging, and maintenance aging.
- It runs longitudinal agent scenarios across repeated sessions, then checks how reliability changes over time.
- It uses temporal dependency graphs to track which stored facts and derived states should affect later answers.
- It uses paired counterfactual probes to diagnose failures at the write, retrieval, and utilization stages of the memory pipeline.
- It tests runner-controlled and autonomous agents across multiple models and memory policies.

## Results
- The paper reports 7 scenarios, 14 models, multiple memory policies, and over ~400 runs spanning 8 to 200 sessions.
- The benchmark covers both runner-controlled and autonomous agents.
- Behavioral tests can stay clean while factual precision decays; the excerpt provides no exact precision scores.
- Derived-state tracking can collapse sharply within a single model; the excerpt gives no per-model numeric collapse rate.
- The same wrong answer can require different repairs depending on whether the diagnostic profile points to write, retrieval, or utilization failure.

## Link
- [https://agingbench.github.io](https://agingbench.github.io)
