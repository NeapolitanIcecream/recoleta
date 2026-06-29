---
source: arxiv
url: https://arxiv.org/abs/2606.06324v1
published_at: '2026-06-04T15:58:30'
authors:
- Mengzhuo Chen
- Junjie Wang
- Zhe Liu
- Yawen Wang
- Qing Wang
topics:
- llm-agents
- agent-harnesses
- trace-diagnosis
- automated-repair
- software-engineering-agents
- multi-agent-systems
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# From Failed Trajectories to Reliable LLM Agents: Diagnosing and Repairing Harness Flaws

## Summary
HarnessFix repairs LLM agent harnesses by tracing failed executions to specific runtime steps and harness layers, then generating scoped patches. The paper claims 15.2%–50.0% held-out performance gains over initial harnesses across SWE-Bench Verified, Terminal-Bench 2.0 Verified, GAIA, and AppWorld.

## Problem
- LLM agents fail for reasons outside the base model, including tool schemas, context assembly, orchestration, logging, validation, sandboxing, and policy checks.
- Existing self-improvement methods often optimize prompts or workflows from final scores, so they can change the wrong part of the agent harness or make broad edits.
- Reliable repair matters because long-horizon software, terminal, research, and app-automation agents depend on external tools and state changes, where small harness flaws can cause bad final submissions.

## Approach
- HarnessFix converts raw traces and harness code into HTIR, a step-level representation with request/response messages, roles, execution status, artifact or state effects, provenance links, and control-flow links.
- A diagnosis agent uses HTIR to locate the responsible TraceStep or steps, map them to ETCLOVG layers, and write diagnosis records.
- Similar diagnosis records are grouped into recurring flaw records before any edit is made.
- A repair agent maps each flaw record to scoped repair operators, such as argument validation, context refresh, verification-gated finalization, or state-delta logging.
- A validation agent checks that a patch stays within scope, reduces the target flaw, and avoids unacceptable regressions.

## Results
- On 4 benchmarks, SWE-Bench Verified, Terminal-Bench 2.0 Verified, GAIA, and AppWorld, HarnessFix improves held-out test performance over the initial harnesses by 15.2%–50.0%.
- The paper says HarnessFix beats human-designed harnesses and self-evolution baselines, but the excerpt does not provide exact baseline scores.
- The method uses 4 cooperating LLM agents: trace abstraction, diagnosis, repair, and validation.
- The analysis covers 7 harness layers in the ETCLOVG taxonomy: Execution, Tooling, Context, Lifecycle, Observability, Verification, and Governance.
- Ablations test prompt-only repair, trace-grounded diagnosis, scoped repair operators, and regression-aware acceptance; the excerpt says every component helps, without giving ablation numbers.

## Link
- [https://arxiv.org/abs/2606.06324v1](https://arxiv.org/abs/2606.06324v1)
