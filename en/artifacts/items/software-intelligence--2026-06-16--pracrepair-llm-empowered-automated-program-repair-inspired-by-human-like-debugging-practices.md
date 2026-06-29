---
source: arxiv
url: https://arxiv.org/abs/2606.17612v1
published_at: '2026-06-16T07:18:37'
authors:
- Yu Cheng
- Zhongxin Liu
- Zhenchang Xing
- Chao Ni
- Qing Huang
- Xiaoxue Ren
topics:
- automated-program-repair
- llm-code-repair
- execution-traces
- debugging-agents
- code-intelligence
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices

## Summary
PRACREPAIR is an LLM-based automated program repair method that adds execution traces and validation trace diffs to the repair loop. It reports higher fix counts than prior APR baselines on Defects4J and claims the best RWB results across several foundation models.

## Problem
- Existing LLM-based APR methods often rely on static code, retrieved context, error messages, and pass/fail test feedback, so they miss runtime causes of bugs.
- This matters because developers spend about 35% to 50% of their time and 50% to 75% of project budgets on testing, verification, and debugging, with reported yearly costs above $100 billion.
- Raw traces are too large to hand to an LLM directly, and pass/fail validation gives little guidance when an attempted patch changes behavior but still fails.

## Approach
- PRACREPAIR builds static context with a Code Property Graph using Joern, covering AST, CFG, calls, and definition-use relations.
- It records dynamic context from failing Java tests with JavaAgent and ASM bytecode instrumentation: executed statements, in-scope variable values, and branch outcomes inside the buggy function.
- The LLM accesses this evidence through tool calls rather than receiving the whole project and full trace at once.
- The method asks diagnostic questions about what happened, why it failed, and how the faulty logic should change, then turns the answers into an explicit repair hypothesis.
- Failed candidate patches are analyzed with validation diagnostics, code diffs, and trace diffs, then the repair hypothesis is updated for up to 3 refinement rounds; diagnosis has a budget of up to 10 rounds.

## Results
- On Defects4J V1.2/V2.0 with GPT-3.5, PRACREPAIR correctly fixes 139 and 136 bugs, respectively.
- On Defects4J V1.2/V2.0 with GPT-4o, it correctly fixes 162 and 171 bugs, respectively.
- Compared with ReInFix, PRACREPAIR reports 75 unique correct fixes with GPT-3.5 and 93 unique correct fixes with GPT-4o.
- The paper states that PRACREPAIR outperforms baselines including ChatRepair, ThinkRepair, RepairAgent, and ReInFix on Defects4J, but the excerpt does not provide each baseline's fix count.
- On RWB V1.0/V2.0, the excerpt gives no exact fix counts; it claims the best performance across multiple foundation models.

## Link
- [https://arxiv.org/abs/2606.17612v1](https://arxiv.org/abs/2606.17612v1)
