---
kind: ideas
granularity: day
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-07T00:00:00'
run_id: 0c36ae2d-cf90-45a2-ae82-9abea07ab6e7
status: succeeded
topics:
- coding-agents
- reinforcement-learning
- verification
- repository-repair
- workflow-automation
tags:
- recoleta/ideas
- topic/coding-agents
- topic/reinforcement-learning
- topic/verification
- topic/repository-repair
- topic/workflow-automation
language_code: en
pass_output_id: 21
pass_kind: trend_ideas
upstream_pass_output_id: 20
upstream_pass_kind: trend_synthesis
---

# Validation loops for software agents

## Summary
The clearest near-term changes are tighter validation loops around software agents: let repair systems revise tests during search, move repeated workflows into validated deterministic code, and record design decisions as tests before agents edit the codebase. Each one addresses a specific failure mode in current agent use: frozen or incomplete oracles, runtime variance and audit gaps, and developer misunderstanding of agent-made design choices.

## Repository repair loop with editable test candidates
Repository repair agents can ship fewer brittle fixes if they are allowed to edit tests during search and are scored on the interaction between the patch and the revised tests. Agent-CoEvo gives a concrete pattern: keep a population of code candidates and a population of test candidates, run them against each other, and rank both sides from the execution matrix. That is a practical build for teams already running SWE-bench-style patch loops on internal repositories, because it does not require a new foundation model. It changes the validator from a frozen pass/fail gate into a search object.

The operational pain is familiar: an issue report points to a behavior gap, but the existing tests are incomplete, mis-specified, or missing the failure mode. A code-only agent can then optimize against the wrong oracle and still look successful in CI. Agent-CoEvo reports 41.33% resolved on SWE-bench Lite and 46.4% on SWT-bench Lite, with 56.0% ΔC on test quality. For an internal tool, the first cheap check is narrow: take a small backlog of bug reports that required humans to change both code and tests, then compare a frozen-test repair loop against a co-evolving loop on resolution rate and regression escapes.

### Evidence
- [Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints](../Inbox/2026-04-06--beyond-fixed-tests-repository-level-issue-resolution-as-coevolution-of-code-and-behavioral-constraints.md): Summary reports the coevolution method and benchmark gains on SWE-bench Lite, SWT-bench Lite, and test quality.
- [Beyond Fixed Tests: Repository-Level Issue Resolution as Coevolution of Code and Behavioral Constraints](../Inbox/2026-04-06--beyond-fixed-tests-repository-level-issue-resolution-as-coevolution-of-code-and-behavioral-constraints.md): Paper text states that behavioral constraints should be revised during repair and describes mutual evaluation of code and test candidates.

## Compiled workflow runner for repeated document and API tasks
High-volume document and function-calling workflows can move model use to build time, then run as validated deterministic code in production. Compiled AI is a concrete route for claims processing, prior authorization, invoice extraction, and other workflows where the steps are stable and operators need predictable outputs, audit logs, and lower per-transaction cost. The build pattern is small: generate a narrow business-logic function inside a fixed template, then require security scanning, syntax and type checks, sandbox tests, and golden-output checks before deployment.

The evidence is specific enough to support an adoption test. On BFCL, Compiled AI reports 96% task completion, 4.5 ms median latency, and break-even against direct runtime inference at about 17 transactions. On DocILE, its bounded Code Factory path reaches 80.4% line item recognition with lower latency than direct LLM use. A team choosing the first candidate should look for workflows with repeated schemas, a finite exception set, and existing golden cases. The cheap validation step is to compile one production workflow, run both systems side by side for a week, and measure variance, queue time, review burden, and token spend.

### Evidence
- [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](../Inbox/2026-04-06--compiled-ai-deterministic-code-generation-for-llm-based-workflow-automation.md): Summary provides the compiled-AI workflow, validation stages, latency, cost, and benchmark results.
- [Compiled AI: Deterministic Code Generation for LLM-Based Workflow Automation](../Inbox/2026-04-06--compiled-ai-deterministic-code-generation-for-llm-based-workflow-automation.md): Abstract frames deterministic compiled execution for enterprise workflows where reliability and auditability are required.

## Decision log and test generation for agent-written feature changes
Coding teams using agents for feature work can add a decision log that turns accepted design choices into executable tests before code generation. Aporia shows a usable interaction model inside VS Code: ask targeted yes/no design questions, store the answers in a persistent Decision Bank, generate tests from those answers, then let the implementer modify the code under those tests. This addresses a direct adoption blocker for agent-heavy teams: developers approve code that works locally but do not share an accurate mental model of the behavior they just accepted.

The user-study evidence is narrower than the repair and workflow papers, but it points to a concrete support layer that many coding agents still lack. In a 14-programmer within-subject study, participants using Aporia were 5x less likely to hold mental models that disagreed with the code than with Claude Code. A practical first rollout is not a full IDE replacement. Add a decision-capture step on risky feature branches, especially for policy logic, permissions, and edge-case handling, and track whether review comments shift from basic behavior clarification to actual design tradeoffs.

### Evidence
- [Decision-Oriented Programming with Aporia](../Inbox/2026-04-06--decision-oriented-programming-with-aporia.md): Summary describes the Decision Bank, questioner-planner-implementer flow, and the mental-model study result.
- [Decision-Oriented Programming with Aporia](../Inbox/2026-04-06--decision-oriented-programming-with-aporia.md): Abstract explains that decisions are explicit, structured, co-authored, and traceable to code.
