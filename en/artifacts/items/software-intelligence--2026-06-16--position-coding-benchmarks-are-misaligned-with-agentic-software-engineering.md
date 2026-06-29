---
source: arxiv
url: https://arxiv.org/abs/2606.17799v1
published_at: '2026-06-16T11:21:01'
authors:
- Maria I. Gorinova
- Macey Baker
- Amy Heineike
- Maksim Shaposhnikov
- Rob Willoughby
- Dru Knox
topics:
- coding-benchmarks
- agentic-software-engineering
- coding-agents
- swe-bench
- harness-evaluation
- code-intelligence
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Position: Coding Benchmarks Are Misaligned with Agentic Software Engineering

## Summary
The paper argues that current coding benchmarks give misleading signals for agentic software engineering. They often score a whole agent setup as if it were a model score, and they grade against narrow reference solutions instead of behavior and code-quality requirements.

## Problem
- Current leaderboards often attribute a score to the LLM even though the measured object includes the model, agent harness, tools, environment, task setup, and verifier.
- Single-reference grading can reject valid alternative implementations and miss code quality problems such as poor abstractions, broken project conventions, or weak tests.
- End-to-end scores give little guidance for improving agent systems because they do not show whether failures came from context, tools, task decomposition, verifiers, or the model.

## Approach
- The paper describes a coding agent as part of a system harness made of tasks, one or more agent harnesses, environment, context, and feedback signals.
- It separates feedback into inner-loop signals such as tests and type checks, middle-loop signals such as reviewer requests and simulation, and outer-loop signals such as PR acceptance, reverts, incidents, and customer feedback.
- It analyzes three benchmark failures: model-harness conflation, single-reference anchoring, and lack of component-level signal.
- It proposes three fixes: require metadata for model, harness, environment, and dataset versions; replace single-reference tests with behavioral verifiers that allow multiple valid solution shapes; and add component-level evaluation next to end-to-end scores.

## Results
- This is a position paper, so it does not introduce a new benchmark or report a new controlled experimental result.
- On Terminal-Bench with fixed Claude Opus 4.6, reported success varies from 79.8% ± 1.6 for ForgeCode to 58.0% ± 2.9 for Claude Code, a 21.8 percentage-point gap across harnesses using the same model.
- The paper cites practitioner reports of 4–10 percentage-point swings for Claude Opus 4.5 on SWE-Bench Verified when changing scaffolds, and an OpenHands result of 77.6% with comparable models under a different harness.
- It cites AI21 results from more than 200,000 SWE-Bench runs showing that orchestration choices, container allocations, and evaluation seeds can move pass rates at fixed model and fixed harness.
- It cites SWE-Bench+ findings of 32.67% solution leakage in issue text and 31.08% passes under insufficient tests.
- It cites differential testing showing that 7.8% of resolved SWE-Bench-style patches fail developer-written tests and 29.6% diverge from the gold patch’s runtime behavior; it also cites AIDev data from 456k agent-authored PRs in 61k repositories with real-world acceptance rates of 35–64%, below headline SWE-Bench Verified figures above 70%.

## Link
- [https://arxiv.org/abs/2606.17799v1](https://arxiv.org/abs/2606.17799v1)
