---
kind: ideas
granularity: day
period_start: '2026-06-13T00:00:00'
period_end: '2026-06-14T00:00:00'
run_id: fad86bcd-72a0-4150-a802-94902a2ead13
status: succeeded
topics:
- coding agents
- software factories
- local AI
- data privacy
- Rails
- database correctness
- LLM inference
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-factories
- topic/local-ai
- topic/data-privacy
- topic/rails
- topic/database-correctness
- topic/llm-inference
language_code: en
pass_output_id: 255
pass_kind: trend_ideas
upstream_pass_output_id: 254
upstream_pass_kind: trend_synthesis
---

# Controlled agentic engineering workflows

## Summary
Engineering teams can move agentic development into narrower production workflows by adding explicit controls around context, spend, validation, and data invariants. The clearest near-term changes are spend-capped Claude Code sub-agent chains, agent-readable project contracts with agent-run test gates, and Rails change reviews that require a named database invariant before locks are added.

## Spend-capped Claude Code sub-agent chains for debugging workflows
Teams using Claude Code for incident triage or code-quality sweeps should treat nested sub-agents as a configured workflow with a budget, an allowlist, and a depth rule. Claude Code v2.1.172 allows sub-agents to spawn sub-agents up to five levels deep, with each frame carrying its own prompt, model choice, and 200K-token context. That is useful for noisy jobs such as log search, where the parent session only needs a short verdict.

A practical setup is a project-level `.claude/agents/<name>.md` chain for one debugging path: an Opus triage agent, Sonnet repro agents, and Haiku leaf agents for grep, test generation, or log summarization. Each agent definition should use `Agent()` to name the only child agents it may spawn. Add a per-session spend cap before using the chain on production incidents. The article’s reported failures are large enough to justify this control: about 7x token overhead per branch per level, one user reaching 887,000 tokens per minute, and a reported $47,000 invoice after 23 sub-agents ran for three days.

The cheap test is one real incident replay. Measure tokens, wall time, number of spawned agents, and whether the parent session receives enough evidence to make a decision without raw log dumps.

### Evidence
- [Claude Code v2.1.172: Sub-Agents Can Now Spawn Sub-Agents](../Inbox/2026-06-13--claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents.md): Summarizes Claude Code nested sub-agents, five-level depth, separate contexts, model routing, token overhead, and reported cost incidents.
- [Claude Code v2.1.172: Sub-Agents Can Now Spawn Sub-Agents](../Inbox/2026-06-13--claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents.md): Shows the need for spend limits and the `Agent()` allowlist in sub-agent definitions.
- [Claude Code v2.1.172: Sub-Agents Can Now Spawn Sub-Agents](../Inbox/2026-06-13--claude-code-v2-1-172-sub-agents-can-now-spawn-sub-agents.md): Describes tiered routing and circular spawning risks.

## Agent-readable project contracts and isolated test gates for coding-agent pull requests
Teams asking coding agents to move beyond small edits need a project contract that the agent can read before it writes code. The concrete artifact can be an `AGENTS.md` file or a small set of markdown files that state architecture boundaries, validation commands, coding rules, and release expectations. Pair that with a tiered gate the agent can run on its own: linting, type checks, unit tests, security scans, integration tests, UI tests, and rollout checks where the system supports them.

The operational pressure is shared validation capacity. The software-factory writeup says concurrent agent work stalls when requests share one staging environment, one branch, or one deploy slot. A useful first build is an agent-run verification script that can create or reset its own test environment, run the required checks, and attach the trace to the pull request. Human review then focuses on failures, risky diffs, and product judgment. Reviewer comments, incidents, and metrics should be fed back into the contract so repeated mistakes become explicit instructions.

Start with one service and one common request type. The pilot is successful if an agent can take a ticket, produce a pull request, run the agreed checks without a developer babysitting the environment, and leave enough evidence for a reviewer to approve or reject quickly.

### Evidence
- [Designing Software for Software Factories](../Inbox/2026-06-13--designing-software-for-software-factories.md): Lists project contracts, tiered validation, agent-run test loops, isolated environments, and feedback capture as requirements for agentic development loops.
- [Designing Software for Software Factories](../Inbox/2026-06-13--designing-software-for-software-factories.md): Describes concurrent request handling and the bottleneck created by shared staging, branches, or deploy slots.
- [Designing Software for Software Factories](../Inbox/2026-06-13--designing-software-for-software-factories.md): States that software-factory workflows need patterns, contracts, and scaffolding.

## Rails invariant review before adding locks to AI-generated changes
Rails teams that accept AI-generated backend changes should add an invariant review to pull requests that touch money, reservations, quotas, roles, or inventory. The reviewer should require one sentence naming the data rule being protected, then check whether the database enforces it with the smallest suitable mechanism: a unique index, `CHECK`, `SERIALIZABLE`, a locked parent row, an advisory lock, or ordered locking.

This catches a common failure mode in generated Rails code. `lock`, `lock!`, and `with_lock` look simple, but their behavior depends on transaction scope, isolation level, adapter behavior, and query shape. A row lock can fix a single-row lost update. It cannot protect a rule over multiple rows, missing rows, or a predicate such as “no more than 100 reservations per event.” The article also notes that `Seat.lock.find(id)` without a surrounding transaction releases the lock immediately.

A lightweight adoption step is a pull request checklist and two concurrency tests for each risky path: one test for simultaneous writes to the same row, and one test for the broader invariant. If the second test fails, the fix belongs in the database rule or transaction design, not in another application-level guard.

### Evidence
- [Rails: The Sharp Parts. Lock Is Not a Mutex](../Inbox/2026-06-13--rails-the-sharp-parts-lock-is-not-a-mutex.md): Summarizes why Rails locks are easy to misuse and recommends starting from the invariant and choosing the smallest database mechanism.
- [Rails: The Sharp Parts. Lock Is Not a Mutex](../Inbox/2026-06-13--rails-the-sharp-parts-lock-is-not-a-mutex.md): Explains that Rails pessimistic locking depends on transaction boundaries, isolation levels, database behavior, and query shape, and that row locks do not cover multi-row invariants.
- [Rails: The Sharp Parts. Lock Is Not a Mutex](../Inbox/2026-06-13--rails-the-sharp-parts-lock-is-not-a-mutex.md): Lists the invariant questions reviewers should ask before reaching for a lock.
