---
kind: ideas
granularity: day
period_start: '2026-06-16T00:00:00'
period_end: '2026-06-17T00:00:00'
run_id: 3ccf3c66-3d3f-4166-8c9b-13e262313b09
status: succeeded
topics:
- AI coding agents
- software engineering evaluation
- program repair
- test oracles
- agent harnesses
- efficient inference
tags:
- recoleta/ideas
- topic/ai-coding-agents
- topic/software-engineering-evaluation
- topic/program-repair
- topic/test-oracles
- topic/agent-harnesses
- topic/efficient-inference
language_code: en
pass_output_id: 263
pass_kind: trend_ideas
upstream_pass_output_id: 262
upstream_pass_kind: trend_synthesis
---

# Coding Agent Verification Controls

## Summary
Agent-authored code needs quality gates that inspect what tests assert, repair loops that pass targeted execution evidence back to the model, and evaluation reports that separate model, harness, environment, verifier, and skill effects. The common operational problem is false confidence: a PR can contain tests with weak assertions, a repair agent can see only pass/fail feedback, and a leaderboard score can hide harness choices that move results by double-digit margins.

## Oracle-strength checks for agent-authored test files
Teams accepting pull requests from coding agents can add a CI or review bot that classifies new and modified test files by oracle strength before review. The first useful version can flag tests with no assertions, non-null checks, boolean-only checks, mock-only checks, and snapshot-only checks, then require a reviewer note or stronger assertion for risky changes.

The case is concrete because agent tests often create a verification illusion. All Smoke, No Alarm studied 86,156 test-file patches from 33,596 agent-authored PRs and found that 80.2% had weak or no explicit oracle signals. The same study found that stronger multi-signal oracles were associated with higher merge likelihood after controlling for agent, PR size, repository stars, task type, and language.

A cheap pilot is to run the classifier only on agent-labeled PRs for two weeks and report three numbers: share of changed test files with no behavior check, share with value or error assertions, and reviewer override rate. The tool does not need to block every weak test. It gives reviewers a targeted warning when a patch adds test files that execute code without checking expected behavior.

### Evidence
- [All Smoke, No Alarm: Oracle Signals in Agent-Authored Test Code](../Inbox/2026-06-16--all-smoke-no-alarm-oracle-signals-in-agent-authored-test-code.md): The study defines oracle-signal categories, analyzes 86,156 agent-authored test-file patches, and reports that 80.2% contain weak or no explicit oracle signals.
- [All Smoke, No Alarm: Oracle Signals in Agent-Authored Test Code](../Inbox/2026-06-16--all-smoke-no-alarm-oracle-signals-in-agent-authored-test-code.md): The abstract states that tests lacking explicit assertions execute code without verifying behavior and that test-file presence can overestimate verification strength.

## Execution-evidence bundles for automated program repair loops
Code-repair agents should capture a small evidence bundle for each failing run: failing test name, compiler or runtime error, relevant input and expected output, executed statements in the suspected function, in-scope variable values, branch outcomes, and a trace diff after each attempted patch. The agent can then revise a named repair hypothesis after each failed candidate patch.

PracRepair shows the fuller version of this workflow for Java APR. It combines static context from a Code Property Graph with failing-test traces, variable values, branch outcomes, validation diagnostics, and trace-level behavior changes. With GPT-4o, it reports 162 correct fixes on Defects4J V1.2 and 171 on V2.0, plus 93 unique correct fixes compared with ReInFix. A simpler code-correction study supports the same operational pattern: generate code, run it, return compiler errors or failed test details, and ask the model to revise.

The adoption path can start inside an existing test runner. Store the evidence bundle as a JSON artifact beside each failed agent attempt, cap refinement at a small number of rounds, and compare fixes with and without trace fields on recurring bug classes. Syntax and runtime failures are the easiest early targets; logic and algorithm errors need richer examples and stronger tests.

### Evidence
- [PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices](../Inbox/2026-06-16--pracrepair-llm-empowered-automated-program-repair-inspired-by-human-like-debugging-practices.md): PracRepair records static and dynamic context, exposes evidence through tool calls, uses validation diagnostics and trace diffs, and reports Defects4J fix counts.
- [PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices](../Inbox/2026-06-16--pracrepair-llm-empowered-automated-program-repair-inspired-by-human-like-debugging-practices.md): The paper abstract states that PracRepair uses on-demand static-dynamic context, question-driven failure diagnosis, repair hypotheses, and validation trace behavior changes.
- [Unlocking LLM Code Correction with Iterative Feedback Loops](../Inbox/2026-06-16--unlocking-llm-code-correction-with-iterative-feedback-loops.md): The code-correction study evaluates iterative repair using compiler errors, runtime errors, failed test cases, and resource-limit feedback across repeated attempts.

## Component-level reports for coding-agent evaluations
Internal coding-agent evaluations should publish a run card for each score with the model, harness, tool set, environment image, task source, verifier, prompt or skill pack version, retry policy, and cost. The same task set should also include a small ablation table: fixed model with different harnesses, fixed harness with different models, and skill enabled versus disabled when skills encode project rules.

The need is visible in benchmark results. One position paper reports that Terminal-Bench success for fixed Claude Opus 4.6 ranges from 79.8% ± 1.6 with ForgeCode to 58.0% ± 2.9 with Claude Code, a 21.8-point spread tied to harness choice. It also cites SWE-Bench+ leakage and insufficient-test findings, plus cases where resolved SWE-Bench-style patches fail developer-written tests or diverge from gold-patch runtime behavior.

The skill-evaluation work gives a practical measurement pattern for teams that encode repository rules, API patterns, or workflow preferences as agent skills. It generated tasks and hidden rubrics from each skill, then ran agents with and without the skill. Across about 500 skills, 1,000 tasks, 19 agent-model configurations, and 38,000 valid trajectories, relevant skills added 5.5 to 22 points depending on the model. A team can copy the paired-run design for its own skills before rolling them into default agent workstations.

### Evidence
- [Position: Coding Benchmarks Are Misaligned with Agentic Software Engineering](../Inbox/2026-06-16--position-coding-benchmarks-are-misaligned-with-agentic-software-engineering.md): The position paper separates model, harness, tools, environment, task setup, and verifier, and reports a 21.8-point Terminal-Bench spread across harnesses with a fixed model.
- [Position: Coding Benchmarks Are Misaligned with Agentic Software Engineering](../Inbox/2026-06-16--position-coding-benchmarks-are-misaligned-with-agentic-software-engineering.md): The paper argues that end-to-end scores combine model, harness, environment, context, and feedback signals, limiting component-level diagnosis.
- [A Framework for Evaluating Agentic Skills at Scale](../Inbox/2026-06-16--a-framework-for-evaluating-agentic-skills-at-scale.md): The skill-evaluation study compares agent runs with and without relevant skills across about 500 skills, 1,000 tasks, 19 configurations, and about 38,000 valid trajectories.
