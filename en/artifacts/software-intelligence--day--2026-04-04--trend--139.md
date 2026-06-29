---
kind: trend
trend_doc_id: 139
granularity: day
period_start: '2026-04-04T00:00:00'
period_end: '2026-04-05T00:00:00'
topics:
- coding-agents
- repository-level-generation
- program-repair
- runtime-debugging
- agent-safety
- context-pruning
run_id: materialize-outputs
aliases:
- recoleta-trend-139
tags:
- recoleta/trend
- topic/coding-agents
- topic/repository-level-generation
- topic/program-repair
- topic/runtime-debugging
- topic/agent-safety
- topic/context-pruning
language_code: en
pass_output_id: 14
pass_kind: trend_synthesis
---

# Coding-agent research is getting judged by execution loops, runtime evidence, and real action control

## Overview
This day’s strongest papers make coding-agent claims more executable and more inspectable. The emphasis is concrete control over what agents read, remember, run, and are allowed to change. EnvGraph and LiveCoder tie repository generation to runtime validation and repeated-attempt evidence. DebugHarness pushes repair into live debugging. Squeez and AmPermBench narrow two operational bottlenecks: context bloat and permission coverage.

## Clusters

### Executable repositories and multi-attempt memory
Repository-level code generation is getting judged by whether the whole project installs, links, runs, and survives repeated attempts. EnvGraph treats runtime failure diagnosis as a structured attribution problem across external packages and internal references, and reports gains of 5.72 to 5.87 points in functional correctness and 4.58 to 8.66 points in non-functional quality on RAL-Bench and NL2Repo-Bench. LiveCoder attacks the same bottleneck from another angle: it keeps success notes, failure notes, and the best repository artifact across attempts. On RAL-Bench it reports up to +22.94 functional points, up to 81.58% repository reuse, and up to 53.63% cost reduction. The shared message is practical: execution feedback is now part of the method, not just the scorecard.

#### Evidence
- [Toward Executable Repository-Level Code Generation via Environment Alignment](../Inbox/2026-04-04--toward-executable-repository-level-code-generation-via-environment-alignment.md): EnvGraph summary with approach and benchmark gains.
- [Persistent Cross-Attempt State Optimization for Repository-Level Code Generation](../Inbox/2026-04-04--persistent-cross-attempt-state-optimization-for-repository-level-code-generation.md): LiveCoder summary with persistent cross-attempt state and reported improvements.

### Pruning agent observations into evidence blocks
Tool-use efficiency is getting its own benchmarkable subproblem. Squeez focuses on a small step inside coding-agent loops: keep only the verbatim lines needed from one tool output for the next action. Its dataset has 11,477 examples across 27 tool types, and the LoRA-tuned Qwen 3.5 2B model reaches 0.80 F1 at 0.92 compression on a 618-example reviewed test set. That result matters because it makes agent context management measurable at line level, with direct evidence-preservation metrics instead of broad claims about prompt compression. The paper does not show end-to-end task gains, so the current evidence supports a strong component result, not a full agent win.

#### Evidence
- [Squeez: Task-Conditioned Tool-Output Pruning for Coding Agents](../Inbox/2026-04-04--squeez-task-conditioned-tool-output-pruning-for-coding-agents.md): Summary gives task definition, dataset scale, and line-level results under heavy compression.

### Repair agents are reading runtime state, not just code
Program repair work is becoming more tied to live state. DebugHarness uses GDB, pwndbg, and rr record/replay to inspect runtime memory, trace faults backward, test hypotheses, and then validate patches in a loop. On SEC-bench, which covers 200 real-world vulnerabilities across 29 C/C++ projects, it reports about 90% resolution, above PatchAgent at 57.5% and VulnResolver at 67.5%. The concrete value here is not just a higher patch rate. The method treats runtime inspection as the main source of bug evidence for memory-safety failures where the crash site and root cause are far apart.

#### Evidence
- [DebugHarness: Emulating Human Dynamic Debugging for Autonomous Program Repair](../Inbox/2026-04-04--debugharness-emulating-human-dynamic-debugging-for-autonomous-program-repair.md): Summary covers dynamic debugging workflow and SEC-bench results.

### Permission gating still misses many real agent actions
Agent safety evaluation is getting more specific about where permission systems fail. The Claude Code auto-mode study builds AmPermBench for ambiguous DevOps requests and scores decisions at the individual action level. Across 253 state-changing actions, the reported false negative rate is 81.0%. A large part of the problem is architectural: 36.8% of actions pass through Tier 2 file edits that the classifier never checks, yielding 51 false negatives there alone. Even when the gate does inspect actions, Tier 3-only performance remains weak at 70.3% false negatives and 31.9% false positives. This gives the period a concrete risk theme: guardrails need coverage over equivalent state-changing paths, not only shell commands.

#### Evidence
- [Measuring the Permission Gate: A Stress-Test Evaluation of Claude Code's Auto Mode](../Inbox/2026-04-04--measuring-the-permission-gate-a-stress-test-evaluation-of-claude-code-s-auto-mode.md): Summary provides benchmark design, tiered architecture, and action-level error rates.
