---
source: hn
url: https://blog.bastion.computer/what-does-software-development-look-like-when-agents-write-100-of-the-code/
published_at: '2026-06-16T23:34:17'
authors:
- almostlit
topics:
- agentic-coding
- multi-agent-software-engineering
- automated-software-production
- code-verification
- human-ai-interaction
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# What does software development look like when agents write 100% of the code?

## Summary
The post argues that software development should shift to isolated, long-running coding agents that write production code under human-written specs and verification. Engineers spend less time editing generated code and more time defining work, context, tests, and release checks.

## Problem
- Parallel coding agents can interfere with a developer’s local machine through shared ports, processes, state, dependencies, and shell access.
- Long-running agent tasks need compute that stays online and remains isolated when the developer is offline.
- Human micromanagement of many agent sessions becomes the bottleneck, so output quality depends on better upfront specs and verification.

## Approach
- Run each coding agent on its own isolated computer, separate from the developer’s machine.
- Give agents detailed product specs, architecture decisions, and task breakdowns before they start coding.
- Close the feedback loop with unit tests, integration tests, end-to-end tests, linting, type checks, observability, and task-specific tools such as agent-browser and agentmail.
- Move human review toward specs, context, and verification processes, with PR review as a final check before merge.

## Results
- The post gives no benchmark, dataset, controlled experiment, or measured accuracy result.
- It claims agentic coding moved in 2 years from toy autocomplete to generating an overwhelming share of production code, but it gives no percentage or study.
- It claims implementation time can shrink from weeks to hours when agents have clear specs and closed-loop verification.
- It claims isolated agent computers reduce collisions across ports, processes, local state, and dependencies during parallel work.
- It claims red/green TDD and comprehensive tests let agents iterate toward a PR with less human steering.

## Link
- [https://blog.bastion.computer/what-does-software-development-look-like-when-agents-write-100-of-the-code/](https://blog.bastion.computer/what-does-software-development-look-like-when-agents-write-100-of-the-code/)
