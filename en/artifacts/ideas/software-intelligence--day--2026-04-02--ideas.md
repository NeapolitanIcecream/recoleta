---
kind: ideas
granularity: day
period_start: '2026-04-02T00:00:00'
period_end: '2026-04-03T00:00:00'
run_id: e30d1f13-3c1f-4ef7-8316-e547eaa9439c
status: succeeded
topics:
- coding-agents
- benchmarks
- tool-use
- software-testing
- api-testing
tags:
- recoleta/ideas
- topic/coding-agents
- topic/benchmarks
- topic/tool-use
- topic/software-testing
- topic/api-testing
language_code: en
pass_output_id: 11
pass_kind: trend_ideas
upstream_pass_output_id: 10
upstream_pass_kind: trend_synthesis
---

# Operational Agent Validation

## Summary
Production-facing software-agent work is getting concrete in three places: private replay benchmarks for coding agents, deterministic testing for tool-call failure and recovery, and requirement-driven API test generation that emits runnable scripts. Each one maps to a build teams can pilot with their own repos, tool contracts, or OpenAPI-backed services.

## Private replay benchmark for agent-assisted code changes
A practical next step for teams already using coding agents is an internal benchmark built from real accepted agent sessions, with the original prompt, the landed diff backed out of the repo, and a stable test set scored as fail-to-pass and pass-to-pass. ProdCodeBench shows this can be done in a changing monorepo and still produce repeatable offline evaluation across model and harness changes. That matters for teams choosing between agent configurations, tool wiring, and model upgrades, because online A/B tests take weeks and expose real developers to bad runs.

The useful build here is not a public leaderboard. It is a rolling private eval pipeline tied to your own repository and prompt distribution. Start with merged agent-assisted changes from one team, exclude requests that cannot be checked by execution, and add repeated pre-change and post-change test runs to filter unstable tests. Use it for release gating on agent updates and for regression checks after prompt, retrieval, or tool changes. A cheap validation step is to replay the last few dozen accepted sessions and see whether score changes line up with reviewer preference and CI outcomes better than your current benchmark mix.

### Evidence
- [ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents](../Inbox/2026-04-02--prodcodebench-a-production-derived-benchmark-for-evaluating-ai-coding-agents.md): ProdCodeBench describes a production-derived benchmark that preserves verbatim prompts, backs out landed diffs, and grades agents with stable F2P and P2P tests in a monorepo.
- [ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents](../Inbox/2026-04-02--prodcodebench-a-production-derived-benchmark-for-evaluating-ai-coding-agents.md): The paper states that organizations need fast offline signals for model and harness changes because online A/B testing is slow and costly.

## Replay harness for tool-call failure and recovery policy
Teams deploying tool-using agents need a replay harness for schema drift, timeouts, rate limits, and authorization failures before they expand production access. ToolMisuseBench is a clear sign that generic capability tests miss this layer. In its released setting, all three baselines finish with the same overall success rate of 0.250, and authorization and rate-limit subsets stay at 0.000 success. Recovery logic helps on timeouts and schema drift, but the budgeted success curve stays flat.

That points to a concrete support layer: an internal fault-injection test bed for every agent tool contract. Record representative tasks, freeze tool schemas and success checks, then replay the same episodes with injected faults and strict limits on retries, calls, and steps. Score invalid calls, policy violations, recovery success, and completion under budget. The first users are platform teams responsible for agent runtime safety and API owners who are seeing plausible tool plans fall apart under normal production errors. A cheap check is to take your top ten agent actions and simulate expired auth, one schema rename, and a 429 policy. If success collapses, the blocker is operational recovery policy, not prompt quality.

### Evidence
- [ToolMisuseBench: An Offline Deterministic Benchmark for Tool Misuse and Recovery in Agentic Systems](../Inbox/2026-04-02--toolmisusebench-an-offline-deterministic-benchmark-for-tool-misuse-and-recovery-in-agentic-systems.md): ToolMisuseBench isolates tool misuse and recovery with deterministic fault injection and explicit step, call, and retry budgets.

## Requirement-to-Jest API acceptance test generation
Requirement-linked API test generation is ready for a pilot in teams that already maintain OpenAPI specs and write acceptance tests by hand. APITestGenie takes a business requirement plus the OpenAPI document and emits runnable Jest and Axios tests. Across 25 requirements, it produced at least one valid script for 22 within three attempts, including large industrial APIs. Some generated tests exposed API defects, including cross-endpoint issues. The reported average cost was €0.37 per generation and the average generation time was 126 seconds.

The workflow change is straightforward: let product, QA, or integration engineers submit requirement text at ticket or story level, retrieve the relevant OpenAPI sections, generate two or three candidate tests, run them in CI, and keep only scripts that execute and match the intended behavior. This is useful where test coverage breaks at the boundary between endpoint correctness and business flow correctness. A cheap pilot is one service with a decent OpenAPI spec and a backlog of manually written acceptance tests. Measure valid-script rate, reviewer edit time, and defect yield on multi-endpoint scenarios.

### Evidence
- [APITestGenie: Generating Web API Tests from Requirements and API Specifications with LLMs](../Inbox/2026-04-02--apitestgenie-generating-web-api-tests-from-requirements-and-api-specifications-with-llms.md): APITestGenie generates executable API tests from business requirements plus OpenAPI specs and reports high requirement-level success on real-world APIs.
