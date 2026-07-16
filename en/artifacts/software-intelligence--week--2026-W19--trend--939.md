---
kind: trend
trend_doc_id: 939
granularity: week
period_start: '2026-05-04T00:00:00'
period_end: '2026-05-11T00:00:00'
topics:
- coding agents
- software engineering benchmarks
- executable evaluation
- formal verification
- agent security
- tool use
run_id: materialize-outputs
aliases:
- recoleta-trend-939
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/executable-evaluation
- topic/formal-verification
- topic/agent-security
- topic/tool-use
language_code: en
pass_output_id: 144
pass_kind: trend_synthesis
---

# Coding agents face a harder trust test: execution traces, repository discipline, and pre-action checks

## Overview
This week’s research treats large language model (LLM) coding agents as systems that need proof before trust. The strongest work checks generated code through execution, repository tasks, formal proofs, tool contracts, and adversarial security tests. SWE Atlas, VeriContest, and RubricRefine show the same practical standard: useful agents must leave inspectable evidence, handle normal engineering work, and avoid unsafe actions.

## Findings

### Executable evidence for generated code
Execution is the main filter for code-generation claims. Semantic Voting shows that running candidates on generated inputs gives a much stronger selection signal than text-level voting: execution-based selectors beat output-pattern majority voting by 19 to 52 percentage points across 18 HumanEval+ and MBPP+ settings. Sketch-and-Verify makes a related point for weaker code models. It asks the model to try distinct algorithmic sketches, then checks candidates by execution fingerprints. On 19 hard HumanEval+ cases for Gemini 3.1 Flash Lite, the smaller sketch setting solved 11 of 19 problems, compared with 5 of 19 for flat sampling at the same candidate count.

The same execution standard appears in testing work. ConCovUp targets concurrent C/C++ behavior that ordinary unit tests miss. It combines static shared-memory analysis, LLM-guided path reasoning, and run feedback, raising average shared-memory access pair coverage from 36.6% with a Claude Code baseline to 68.1% on nine real libraries.

#### Sources
- [Semantic Voting: Execution-Grounded Consensus for LLM Code Generation](../Inbox/2026-05-09--semantic-voting-execution-grounded-consensus-for-llm-code-generation.md): Semantic Voting reports large gains for execution-based candidate selection over output-pattern voting.
- [Sketch-and-Verify: Structured Inference-Time Scaling via Program Sketching](../Inbox/2026-05-09--sketch-and-verify-structured-inference-time-scaling-via-program-sketching.md): Sketch-and-Verify reports matched-budget gains from structured algorithmic sketches plus execution checks.
- [ConCovUp: Effective Agent-Based Test Driver Generation for Concurrency Testing](../Inbox/2026-05-10--concovup-effective-agent-based-test-driver-generation-for-concurrency-testing.md): ConCovUp reports execution-grounded concurrency test generation and coverage gains on real C/C++ libraries.

### Repository-grade benchmarks and abstention
Repository work is being measured beyond issue fixing. SWE Atlas covers 284 tasks across codebase Q&A, test writing, and refactoring in 18 active open-source repositories. Its evaluations combine program checks with rubrics for coverage, maintainability, conventions, cleanup, and code hygiene. The reported gap between regression-test pass rates and rubric pass rates in refactoring, about 15 to 40 points, shows why passing tests alone is an incomplete signal for engineering quality.

FixedBench adds a sharper maintenance requirement: the agent must know when to make no executable-code change. On already-fixed SWE-bench Verified issues, agents still made unwanted executable edits in 35% to 65% of cases under the main setting. Prompts that rewarded abstention improved no-change behavior, but caused harmful over-abstention when a partial fix still needed work.

#### Sources
- [SWE Atlas: Benchmarking Coding Agents Beyond Issue Resolution](../Inbox/2026-05-08--swe-atlas-benchmarking-coding-agents-beyond-issue-resolution.md): SWE Atlas defines repository Q&A, test-writing, and refactoring tasks with programmatic and rubric checks.
- [Coding Agents Don't Know When to Act](../Inbox/2026-05-08--coding-agents-don-t-know-when-to-act.md): FixedBench measures abstention on already-fixed tasks and reports unwanted edit rates plus prompt tradeoffs.

### Formal and high-stakes correctness checks
Formal verification remains a hard boundary for current models. VeriContest contains 946 Rust/Verus competitive-programming tasks with natural-language prompts, expert specifications, accepted Rust code, checked proofs, and positive and negative tests. GPT-5.5 reaches 92.18% pass@1 on natural-language-to-code generation, yet only 5.29% end-to-end verified generation. All evaluated models stay below 6% end-to-end.

SmartEval covers another high-stakes domain: Solidity smart contracts generated from natural-language specifications. The benchmark evaluates 9,000 generated contracts against a five-metric rubric for functional completeness, variable fidelity, state-machine correctness, business logic, and code quality. The weakest metric is business-logic fidelity, and lower-performing contracts are dominated by logic omissions and state-transition errors.

#### Sources
- [VeriContest: A Competitive-Programming Benchmark for Verifiable Code Generation](../Inbox/2026-05-08--vericontest-a-competitive-programming-benchmark-for-verifiable-code-generation.md): VeriContest reports the gap between ordinary code generation and end-to-end verified Rust/Verus programs.
- [SmartEval: A Benchmark for Evaluating LLM-Generated Smart Contracts from Natural Language Specifications](../Inbox/2026-05-10--smarteval-a-benchmark-for-evaluating-llm-generated-smart-contracts-from-natural-language-specifications.md): SmartEval evaluates generated Solidity contracts and reports business-logic and state-transition failure modes.

### Tool contracts and adversarial security tests
Tool-using agents need checks before their first live action. RubricRefine inspects code-mode tool calls against task-specific contracts for tool choice, output shape, call signatures, ordering, and data provenance. On M3ToolEval it averages 0.86 success across seven models, compared with 0.62 for single-pass CodeAct, without executing the candidate action during refinement.

Security evaluation also gets more concrete. MOSAIC-Bench shows that ordinary-looking staged tickets can compose into exploitable code. Across nine production coding agents, staged attack chains reached 53.3% to 85.9% end-to-end attack success with only two refusals. MonitoringBench tests monitors with 2,644 successful BashArena attack trajectories and shows that stronger red-teaming can cut apparent monitor catch rates sharply, including a drop from 94.9% to 60.3% for an Opus 4.5 full-trajectory monitor on refined attacks.

#### Sources
- [RubricRefine: Improving Tool-Use Agent Reliability with Training-Free Pre-Execution Refinement](../Inbox/2026-05-10--rubricrefine-improving-tool-use-agent-reliability-with-training-free-pre-execution-refinement.md): RubricRefine reports pre-execution contract checks and success gains on multi-tool tasks.
- [MOSAIC-Bench: Measuring Compositional Vulnerability Induction in Coding Agents](../Inbox/2026-05-05--mosaic-bench-measuring-compositional-vulnerability-induction-in-coding-agents.md): MOSAIC-Bench reports staged vulnerability induction rates and executable proof-of-concept oracles.
- [MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring](../Inbox/2026-05-10--monitoringbench-semi-automated-red-teaming-for-agent-monitoring.md): MonitoringBench reports a large benchmark of sabotage trajectories and reduced monitor catch rates under stronger attacks.
