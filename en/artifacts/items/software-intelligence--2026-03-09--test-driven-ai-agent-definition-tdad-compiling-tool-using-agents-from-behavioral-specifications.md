---
source: arxiv
url: http://arxiv.org/abs/2603.08806v1
published_at: '2026-03-09T14:04:54'
authors:
- Tzafrir Rehan
topics:
- llm-agents
- test-driven-development
- prompt-compilation
- behavioral-specification
- mutation-testing
- agent-evaluation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Test-Driven AI Agent Definition (TDAD): Compiling Tool-Using Agents from Behavioral Specifications

## Summary
TDAD turns “building a usable tool-using agent” into a test-driven-development-like compilation pipeline: first convert behavioral specifications into tests, then repeatedly revise the prompt until the tests pass. Its goal is to make compliance, regression safety, and test strength for production-grade agents measurable, instead of relying on manual spot checks.

## Problem
- Tool-using LLM agents in production are hard to **verify for true compliance with specifications**: small prompt changes can cause silent regressions, incorrect tool use, leakage of sensitive information, or process violations.
- Existing practice mostly relies on manual trial and error and sampling-based inspection, and **lacks executable behavioral contracts that can plug into CI/CD like in software engineering**.
- Once tests become the optimization target, **specification gaming** can emerge: the agent may learn to “pass the tests” rather than actually satisfy the requirements.

## Approach
- Treat agent development as “compilation”: the input is a YAML specification (tools, policies, decision trees, response contracts, etc.), and the output is a compiled prompt and tool descriptions.
- Use two coding agents collaboratively: **TestSmith** first converts the specification into executable tests; **PromptSmith** then repeatedly makes minimal prompt edits based on failures in the visible tests until they pass.
- To prevent “teaching to the test,” TDAD introduces three mechanisms: **visible/hidden test split** (compile using only visible tests; hidden tests are used only to evaluate generalization), **semantic mutation testing** (generate prompt variants that are intentionally wrong but seemingly reasonable, then check whether the tests catch them), and **spec evolution** (after v1→v2 requirement changes, use hidden old-version invariant tests to measure regression safety).
- Make tests as deterministic as possible: use fixed fixtures, scripted multi-turn dialogues, a structured `respond` tool, and assertions over tool-call traces, rather than relying on LLM-as-a-judge scoring.
- Evaluate on **SpecSuite-Core**, a benchmark containing 4 deeply specified scenarios: SupportOps, DataInsights, IncidentRunbook, ExpenseGuard.

## Results
- Across **24 independent trials** (4 specs × 2 versions × 3 repetitions), TDAD reports **92% v1 compilation success** and **58% v2 compilation success**.
- For successful runs, the mean **hidden pass rate (HPR)** is **97% for v1** and **78% for v2**, indicating some generalization even when only visible tests are seen, though the evolved specifications are clearly harder.
- The **mutation score (MS)** reaches **86%–100%**, suggesting that visible tests usually kill most prompt variants that “seem reasonable but behave incorrectly”; the paper also notes that **87% of mutation intents** are successfully activated across experiments, with the rest excluded as inactive mutations.
- The **spec update regression safety score (SURS)** averages **97%**, indicating that v2 largely preserves prior behavior even without directly seeing the v1 invariant tests.
- In failure cases, the authors say that **most failed runs miss only 1–2 visible tests**, implying that the pipeline often gets close to completion but can still stall under more complex evolved requirements.
- In terms of benchmark scale, the 4 specs each contain **10–14 decision nodes**; each version includes roughly **34–53 visible tests**, **42–45 hidden tests**, and **6–7 mutation intents** (median values, with about ±10–30% variation across 3 trials).

## Link
- [http://arxiv.org/abs/2603.08806v1](http://arxiv.org/abs/2603.08806v1)
