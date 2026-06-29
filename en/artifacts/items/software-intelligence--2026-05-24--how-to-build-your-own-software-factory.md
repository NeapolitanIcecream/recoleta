---
source: hn
url: https://web.navan.dev/posts/2026-05-06-how-to-build-your-own-software-factory.html
published_at: '2026-05-24T22:57:00'
authors:
- _doctor_love
topics:
- software-factory
- coding-agents
- code-intelligence
- agent-orchestration
- software-validation
- human-ai-interaction
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# How to build your own software factory

## Summary
This article gives a practical design for a software factory: a system around coding agents that turns repeatable engineering work into validated, auditable jobs. Its main claim is that teams should automate bounded product lines first, such as dependency updates, CVE fixes, flaky-test triage, or repo migrations.

## Problem
- Teams often treat the coding agent as the whole factory, then get code changes without enough validation, evidence, or stopping rules.
- Brownfield software work depends on hidden context: logs, runbooks, CI behavior, customer paths, known flaky tests, and senior-engineer judgment.
- Agent runs fail when the input task is vague, when the agent cannot return a no-op, or when success depends only on the agent's own claim.

## Approach
- Pick 1 narrow product line before scaling automation, such as dependency updates across a fixed set of repos.
- Define a seed for each job: the ticket, advisory, logs, migration spec, repo list, failure history, or other input that starts the run.
- Convert prompts into task packets with intent, source, scope, non-goals, reproduction steps, allowed tools, validation, no-op rules, required evidence, and output format.
- Wrap the coding-agent loop with an outer factory loop: ingest, classify, reproduce, plan, implement, validate, collect evidence, decide the terminal state, and feed failures back into the system.
- Validate behavior outside the agent when possible, using tests, scenarios, logs, screenshots, traces, digital twins, or other evidence that a reviewer can inspect.

## Results
- The article gives no quantitative benchmark results, accuracy scores, cost data, or measured productivity gains.
- It defines 4 terminal states for a factory station: PR_READY, NO_OP, ESCALATE, and RETRYABLE_FAILURE.
- It gives a concrete bounded example: dependency update tickets across 10 repos should open a PR only when the update applies, builds, passes tests, and preserves public behavior.
- It describes fleet scale as a different class of work: 1 dependency update across 500 repos requires repo selection, isolated workspaces, central tracking, retries, cost limits, review queues, and audit logs.
- It recommends retrying validation revisions only 1 or 2 times before stopping, rather than letting an agent loop without a clear terminal state.

## Link
- [https://web.navan.dev/posts/2026-05-06-how-to-build-your-own-software-factory.html](https://web.navan.dev/posts/2026-05-06-how-to-build-your-own-software-factory.html)
