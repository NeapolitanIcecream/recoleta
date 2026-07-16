---
kind: ideas
granularity: day
period_start: '2026-05-24T00:00:00'
period_end: '2026-05-25T00:00:00'
run_id: f4d60be8-002e-44a7-a834-d55624705ca0
status: succeeded
topics:
- coding agents
- software factories
- formal verification
- agent guardrails
- enterprise AI
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-factories
- topic/formal-verification
- topic/agent-guardrails
- topic/enterprise-ai
language_code: en
pass_output_id: 189
pass_kind: trend_ideas
upstream_pass_output_id: 188
upstream_pass_kind: trend_synthesis
---

# Coding Agent Control Gates

## Summary
Coding-agent adoption now points to three concrete controls: scoped maintenance jobs with external validation, formal proof gates for small high-risk code paths, and pull request checks that keep generated repository noise out of future agent context.

## Dependency update and CVE fix factory station
Platform and security teams can package one repetitive maintenance class as a factory station before widening agent use. A good starting point is dependency updates or CVE fixes across a known repo set. Each job should include the advisory or ticket, target repos, allowed commands, non-goals, reproduction steps, validation checks, no-op rules, required evidence, and a fixed output state such as `PR_READY`, `NO_OP`, `ESCALATE`, or `RETRYABLE_FAILURE`.

The useful build is the wrapper around the coding agent: intake, classification, isolated workspace setup, implementation, tests, evidence capture, retry limit, and review queue. The first pilot can run on 10 repos and count how many jobs produce reviewable PRs, justified no-ops, or escalations. The safety check should live in tests, logs, screenshots, traces, ADR checks, or other reviewer-visible evidence, since the agent’s explanation is not enough for maintenance work that touches production code.

### Sources
- [How to build your own software factory](../Inbox/2026-05-24--how-to-build-your-own-software-factory.md): Defines task packets, external validation, terminal states, no-op rules, retry limits, and a dependency-update example across repos.
- [Don't Fear the Dark Factory](../Inbox/2026-05-24--don-t-fear-the-dark-factory.md): Describes bounded maintenance automation through a validation harness, with candidate tasks including dependency upgrades and security vulnerability mitigation.

## Dafny and Z3 proof gate for small AI-written critical functions
Teams using coding agents for authorization, payment, policy, or data-access logic can add a proof gate for small functions before treating generated code as ready for review. The practical version starts with a narrow interface, writes Dafny-style preconditions and postconditions, runs Z3 to check the specification, generates or edits the implementation, and stores the verification result with the pull request.

This is best tested on code where the correctness property is compact: balance cannot go negative, an authorization rule denies by default, a policy update preserves an invariant, or an input parser rejects undefined cases. The evidence supports a constrained pilot, not a broad claim that natural-language requirements can already produce verified production systems end to end. The gap to watch is specification generation: the current vericoding results are strongest when the formal spec already exists or when a human can review the generated spec before code generation.

### Sources
- [Vericoding: The End of "Trust Me Bro, The AI Wrote It"](../Inbox/2026-05-24--vericoding-the-end-of-trust-me-bro-the-ai-wrote-it.md): Describes the proposed pipeline from natural-language intent to Dafny-style specs, Z3 checks, verified code, and proof artifacts, while noting no new end-to-end quantitative evaluation.
- [Vericoding: The End of "Trust Me Bro, The AI Wrote It"](../Inbox/2026-05-24--vericoding-the-end-of-trust-me-bro-the-ai-wrote-it.md): Cites a vericoding benchmark with 12,504 formal specifications and up to 82% success in Dafny using off-the-shelf LLMs.

## Pull request check for generated-file and log context growth
Repositories that rely on coding agents should add a PR check for changes that increase future agent context cost. Generated clients, coverage output, build artifacts, logs, snapshots, vendored files, lockfile churn, and agent instruction dumps can pass normal tests while making later agent sessions slower, more expensive, and noisier.

ContextLevy is a concrete implementation pattern: scan the GitHub pull request diff, estimate context weight, classify risky files, and post a focused comment when thresholds are exceeded. It can run as a GitHub Action or npm CLI, and it does not call an LLM or upload code. A low-risk rollout is to comment only for two weeks, tune ignored paths and thresholds, then make the check blocking for file classes the team already agrees should not enter the repo.

### Sources
- [Built a small PR guardrail for token bloat, worth maintaining?](../Inbox/2026-05-24--built-a-small-pr-guardrail-for-token-bloat-worth-maintaining.md): Explains ContextLevy’s target failure mode: PRs that add low-signal files and create persistent overhead for AI coding agents.
- [Built a small PR guardrail for token bloat, worth maintaining?](../Inbox/2026-05-24--built-a-small-pr-guardrail-for-token-bloat-worth-maintaining.md): Shows the GitHub Action setup, required permissions, and behavior of reading PR diffs and commenting when thresholds are exceeded.
