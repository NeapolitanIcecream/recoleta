---
source: arxiv
url: http://arxiv.org/abs/2604.19825v1
published_at: '2026-04-20T13:00:46'
authors:
- Woojin Lee
- Jin-Xia Huang
topics:
- llm-code-generation
- multi-agent-systems
- execution-grounding
- program-synthesis
- property-based-testing
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# SolidCoder: Bridging the Mental-Reality Gap in LLM Code Generation through Concrete Execution

## Summary
SolidCoder improves LLM code generation by replacing imagined execution checks with actual sandboxed execution and property-based tests. The paper argues that current agent pipelines fail because models miss edge cases during planning and then misjudge buggy code during verification.

## Problem
- Existing code-generation agents often rely on mental simulation to plan and debug, so they can invent execution traces and approve incorrect code.
- The paper splits this failure into two parts: a **Specification Gap** that misses edge cases early, and a **Verification Gap** that treats flawed code as correct later.
- This matters because competitive programming and similar tasks need code that passes hidden tests, where false confidence leads to wrong final submissions.

## Approach
- SolidCoder is a multi-agent pipeline built around one rule: execute code instead of trusting the model's internal trace.
- **Shift-left Planning** asks the model to surface edge cases before writing the algorithm, so the plan accounts for boundary conditions up front.
- **Oracle-based Assertions** avoid the missing-oracle problem by testing properties of outputs rather than exact answers, such as ordering, length, or permutation constraints.
- **Live Execution** runs generated code in a sandbox and uses real failures, assertion errors, and runtime errors to drive debugging.
- **Intermediate Simulation** gives a cheap first check after code generation, and **Defensive Accumulation** keeps every discovered failing test so later fixes do not reintroduce old bugs.

## Results
- On **GPT-4o**, SolidCoder reports state-of-the-art **pass@1**: **95.7% on HumanEval** vs **95.1% for CodeSIM** (**+0.6%p**), **77.0% on CodeContests** vs **72.7%** (**+4.3%p**), and **26.7% on APPS** vs **23.3%** (**+3.4%p**).
- Across all three tested models, SolidCoder matches or beats CodeSIM on all nine model-benchmark pairs. Average pass@1 rises from **97.0% to 97.2%** on HumanEval, **85.3% to 89.1%** on CodeContests, and **34.6% to 36.5%** on APPS.
- On **CodeContests**, gains are consistent across models: **GPT-4o 72.7% -> 77.0% (+4.3%p)**, **GPT-OSS-120B 87.9% -> 92.1% (+4.2%p)**, and **Grok-4.1-Fast 95.2% -> 98.2% (+3.0%p)**.
- The ablation on **CodeContests with GPT-4o** shows the largest drop when removing **Shift-left Planning**: **77.0% -> 53.3% (-23.7%p)**. Other removals also hurt: **Intermediate Simulation 64.0% (-13.0%p)**, **Oracle-based Assertions 65.4% (-11.6%p)**, **Live Execution 69.1% (-7.9%p)**, and **Defensive Accumulation 70.3% (-6.7%p)**.
- The efficiency table shows these gains cost more inference work. For **GPT-4o on APPS**, SolidCoder uses **35 API calls / 60.4K tokens** versus **26 / 49.3K** for CodeSIM. For **Grok-4.1-Fast on APPS**, it uses **47 calls / 520.9K tokens** versus **20 / 266.5K** for CodeSIM.

## Link
- [http://arxiv.org/abs/2604.19825v1](http://arxiv.org/abs/2604.19825v1)
