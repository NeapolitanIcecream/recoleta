---
source: hn
url: https://brooker.co.za/blog/2026/05/18/whats-easy-whats-hard.html
published_at: '2026-06-01T23:05:07'
authors:
- pgedge_postgres
topics:
- coding-agents
- software-engineering
- llm-agents
- developer-tools
- formal-methods
- feedback-loops
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# What's Easy Now? What's Hard Now? How AI Is Changing Software Development

## Summary
The article argues that coding agents improve most on software tasks with fast, accurate feedback, such as compiler errors, tests, benchmarks, and formal checks. It predicts that well-specified systems work may become easier for agents than human-judged UI or product work.

## Problem
- Coding-agent capability is often judged by open-loop model quality, which misses how agents improve through build, test, and repair cycles.
- Software tasks differ in the quality of feedback they provide. Clear machine-checkable feedback helps agents; vague human preference slows them down.
- This matters because tool design, specification practice, and engineering workflows will shape what agents can build reliably.

## Approach
- The core mechanism is feedback: an LLM writes or edits code, observes errors or test results, then tries again.
- The article compares open-loop AI autocomplete with coding agents that keep build, test, and iteration inside the agent loop.
- It uses examples where feedback is strong, including Rust compiler messages, performance benchmarks, property-based tests, TLA+, P, Verus, Hydro, simulators, mocks, and spec analysis.
- It contrasts those with tasks where feedback is weak or human-dependent, such as architecture choices, UI quality, and concurrent programs with hidden runtime failures.

## Results
- The excerpt reports no benchmark, dataset, baseline, or measured accuracy result.
- It claims developer tooling has shifted over roughly the last 2 years from open-loop autocomplete toward agents that run feedback loops.
- It claims computer systems have had superhuman abilities for at least 85 years, and coding agents will likely follow the same pattern: strong on some tasks and weak on others.
- It predicts tasks with explicit specifications, safety properties, liveness properties, tests, or benchmarks will become easier for agents.
- It predicts SaaS and UI work may stay hard for agents when success depends on slow and inconsistent human feedback, while system software may become easier when specifications are machine-checkable.

## Link
- [https://brooker.co.za/blog/2026/05/18/whats-easy-whats-hard.html](https://brooker.co.za/blog/2026/05/18/whats-easy-whats-hard.html)
