---
kind: trend
trend_doc_id: 1537
granularity: day
period_start: '2026-06-16T00:00:00'
period_end: '2026-06-17T00:00:00'
topics:
- AI coding agents
- software engineering evaluation
- program repair
- test oracles
- agent harnesses
- efficient inference
run_id: materialize-outputs
aliases:
- recoleta-trend-1537
tags:
- recoleta/trend
- topic/ai-coding-agents
- topic/software-engineering-evaluation
- topic/program-repair
- topic/test-oracles
- topic/agent-harnesses
- topic/efficient-inference
language_code: en
pass_output_id: 262
pass_kind: trend_synthesis
---

# Coding-agent research is centering on evidence, harnesses, and bounded compute

## Overview
The day’s research treats AI coding agents as systems that need runtime evidence, meaningful tests, and harness-aware scoring. PracRepair and LoopCoder-v2 show gains when repair evidence and latent compute are measured carefully; evaluation papers add pressure for component-level results.

## Findings

### Runtime feedback for code repair
Automated program repair (APR) work is using execution evidence as first-class input. PracRepair combines static code context with failing-test traces, variable values, branch outcomes, validation diagnostics, and trace diffs. With GPT-4o, it reports 162 correct fixes on Defects4J V1.2 and 171 on V2.0, plus many fixes not found by ReInFix.

A separate code-correction study tests the same idea in a simpler loop: generate code, run it, return compiler errors or failing test details, and revise. GPT-o4-mini leads pass@1 on the 450-problem core set, while the study finds that syntax and runtime failures are easier to repair than logic and algorithm errors.

Test generation remains a weak point. In 86,156 agent-authored test-file patches, 80.2% contain weak or no explicit oracle signals. The finding matters because a test file can execute code and still check no expected behavior.

#### Sources
- [PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices](../Inbox/2026-06-16--pracrepair-llm-empowered-automated-program-repair-inspired-by-human-like-debugging-practices.md): PracRepair method and Defects4J repair counts.
- [Unlocking LLM Code Correction with Iterative Feedback Loops](../Inbox/2026-06-16--unlocking-llm-code-correction-with-iterative-feedback-loops.md): Iterative code-correction setup, models, and pass@1 results.
- [All Smoke, No Alarm: Oracle Signals in Agent-Authored Test Code](../Inbox/2026-06-16--all-smoke-no-alarm-oracle-signals-in-agent-authored-test-code.md): Large-scale evidence on weak oracle signals in agent-authored tests.

### Harness-aware agent evaluation
Benchmarking work is naming the measured object more carefully. One position paper argues that coding-agent scores include the model, harness, tools, environment, task setup, and verifier. Its cited Terminal-Bench example shows a fixed Claude Opus 4.6 scoring 79.8% ± 1.6 with ForgeCode and 58.0% ± 2.9 with Claude Code, a 21.8-point spread across harnesses.

The agent-skills evaluation paper turns that concern into a measurement procedure. It generates tasks and hidden rubrics from each skill, runs agents with and without the skill, and scores instruction following and goal completion. Across about 500 skills, 1,000 tasks, 19 agent-model configurations, and 38,000 valid trajectories, relevant skills add 5.5 to 22 points depending on the model.

#### Sources
- [Position: Coding Benchmarks Are Misaligned with Agentic Software Engineering](../Inbox/2026-06-16--position-coding-benchmarks-are-misaligned-with-agentic-software-engineering.md): Benchmark critique, harness components, and Terminal-Bench harness spread.
- [A Framework for Evaluating Agentic Skills at Scale](../Inbox/2026-06-16--a-framework-for-evaluating-agentic-skills-at-scale.md): Skill evaluation method, scale, and reported score gains.

### Bounded compute for coding models and agents
LoopCoder-v2 gives a concrete compute-scaling result for code models. The 7B Parallel Loop Transformer reuses shared blocks across loops and keeps cache cost down with shared-key-value attention. In the reported suite, two loops improve the average score from 38.0 to 46.5. On SWE-bench Verified, the score rises from 43.0 to 64.4, while three and four loops fall sharply.

Operational writing in the corpus applies a similar bounded-systems view to agent workstations. Long-running agents need isolated computers, separate ports, state, dependencies, and shell access. The practical claim is that quality depends on specs, tests, type checks, linting, observability, and final pull-request review, not on continuous human editing of generated code.

#### Sources
- [LoopCoder-v2: Only Loop Once for Efficient Test-Time Computation Scaling](../Inbox/2026-06-16--loopcoder-v2-only-loop-once-for-efficient-test-time-computation-scaling.md): LoopCoder-v2 architecture, training setup, and two-loop benchmark gains.
- [What does software development look like when agents write 100% of the code?](../Inbox/2026-06-16--what-does-software-development-look-like-when-agents-write-100-of-the-code.md): Agent isolation, long-running execution, and verification workflow claims.
