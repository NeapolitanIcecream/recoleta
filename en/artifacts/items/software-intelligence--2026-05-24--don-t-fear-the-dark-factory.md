---
source: hn
url: https://mattwynne.net/dont-fear-the-dark-factory
published_at: '2026-05-24T22:24:57'
authors:
- _doctor_love
topics:
- agentic-coding
- software-automation
- code-validation
- multi-agent-workflows
- human-ai-interaction
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Don't Fear the Dark Factory

## Summary
The article argues that dark factories can automate bounded software tasks when agents run in a validation loop. The main claim is practical: use agents for work with clear checks, not blind trust.

## Problem
- Agent-written code can feel unsafe when humans do not read it, especially to teams that value internal design quality.
- Many software chores, such as dependency upgrades, security fixes, architectural drift checks, and mutation-test triage, still need human time even when the desired outcome can be checked.
- The risk is poorly specified agent work; the article says the missing piece is a validation harness that defines acceptable output.

## Approach
- A dark factory is described as a loop of agent sessions that receive a seed input, make changes, and keep running until validation passes.
- The validation harness contains the tests, heuristics, architectural records, or other checks that judge whether the output is good enough.
- In the yaks example, one agent compares code against ADRs and produces recommendations; another agent implements the top recommendation; tests and unresolved recommendations keep the loop going.
- The author suggests starting with small maintenance tasks before giving agents feature work.

## Results
- The excerpt reports no benchmark, accuracy score, throughput measure, dataset result, or baseline comparison.
- One concrete claim is that the yaks architectural review loop can run for 1 hour or more with little human action.
- The claimed result is improved code integrity against ADR-based design heuristics after the loop resolves all recommendations and passes automated tests.
- The article gives 4 candidate task types for dark factories: security vulnerability mitigation, dependency upgrades, mutation-test triage, and production feature implementation.
- The author also reports building a daily-use tool in a language they had never read or written, without reading the generated code.

## Link
- [https://mattwynne.net/dont-fear-the-dark-factory](https://mattwynne.net/dont-fear-the-dark-factory)
