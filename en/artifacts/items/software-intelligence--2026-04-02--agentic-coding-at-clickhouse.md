---
source: hn
url: https://clickhouse.com/blog/agentic-coding
published_at: '2026-04-02T23:06:53'
authors:
- hodgesrm
topics:
- agentic-coding
- code-intelligence
- software-engineering
- developer-productivity
- multi-agent-systems
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Agentic Coding at ClickHouse

## Summary
This article argues that coding agents became useful for daily engineering work at ClickHouse in 2025, including large C++ codebases, when paired with strong human review and testing. It is an experience report, not a controlled study, and its evidence is a set of internal use cases with concrete productivity claims.

## Problem
- Teams need a practical view of where coding agents help in real software work, beyond benchmark scores and broad claims about AI replacing engineers.
- Large, old, safety-sensitive codebases such as ClickHouse's C++ server create hard tasks for agents: bug investigation, refactoring, CI maintenance, code review, and feature work.
- The main risk is wrong but plausible output. Without review, tests, and engineer judgment, agents can waste time or introduce bugs.

## Approach
- ClickHouse uses agentic coding mainly at the "Level 2" stage: CLI or IDE agents that read code, search logs, run tools, build and test code, and work through multi-step tasks with human guidance.
- The preferred setup is CLI agents such as Claude Code and Codex CLI, because they can plan, manage context, call tools, inspect logs, use GitHub, run builds, and iterate on feedback.
- Engineers apply agents to concrete workflows: boilerplate edits, stale pull requests, merge conflicts, code porting, code review, bug and incident investigation, flaky test repair, optimization, prototypes, and internal tools.
- Human oversight is part of the method. The article repeats a simple loop: specify the task, let the agent edit or investigate, validate with tests and CI, and review the diff or reasoning.
- ClickHouse also started limited autonomous agents for narrow tasks such as flaky-test fixing and edge-case test generation, but the article says longer autonomous loops are still less reliable.

## Results
- The strongest quantitative result is CI cleanup: in January and February, the author says agents helped produce **700 pull requests** for test and CI fixes, reducing findings from about **200 per day** to about **3 to 5 per 10,000,000** tests.
- For code porting, an agent fixed SQL dialect compatibility issues in the Polyglot project over **36 hours** with **23 hours of API time** at a cost of about **$500**, and the changes were merged and used for ClickHouse needs.
- For a complex bug, the reported final fix was a **one-line change** after about **one hour** of model reasoning, with a session cost below **$30**; the author says confirmation still requires months of further stress and fuzz testing.
- For incident investigation, one on-call engineer reports doing initial investigation in **1 day** that would otherwise take **3 to 4 days**, with the warning that the agent still produces many wrong hypotheses.
- For optimization, the article claims an agent improved ClickHouse build speed by **28%** after an overnight run on a large server; no benchmark setup or baseline details are provided in the excerpt.
- For autonomous flaky-test fixing, the Groene.AI agent reportedly produces a correct fix in about **30% to 50%** of cases before further feedback. The article also claims that in the last half year, **100%** of real bug bounty findings received by ClickHouse were found using coding agents, but it gives no raw count beyond saying real findings are on the order of **10 per year**.

## Link
- [https://clickhouse.com/blog/agentic-coding](https://clickhouse.com/blog/agentic-coding)
