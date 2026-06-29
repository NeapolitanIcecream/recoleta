---
kind: trend
trend_doc_id: 104
granularity: day
period_start: '2026-04-02T00:00:00'
period_end: '2026-04-03T00:00:00'
topics:
- coding-agents
- benchmarks
- tool-use
- software-testing
- api-testing
run_id: materialize-outputs
aliases:
- recoleta-trend-104
tags:
- recoleta/trend
- topic/coding-agents
- topic/benchmarks
- topic/tool-use
- topic/software-testing
- topic/api-testing
language_code: en
pass_output_id: 10
pass_kind: trend_synthesis
---

# Software-agent research is getting more executable, replayable, and production-bound

## Overview
Today’s research is strongest where software work can be checked by execution. The main emphasis is stricter evaluation for coding agents, plus better test generation for code and APIs. ProdCodeBench and ToolMisuseBench both narrow the gap between benchmark scores and deployment conditions. The result is a more practical picture of where agents hold up and where they still break.

## Clusters

### Production evaluation for coding agents
The strongest work today tries to grade coding agents on signals that can survive real engineering conditions. ProdCodeBench builds tasks from actual developer-assistant sessions in an industrial monorepo, keeps the original prompts, backs out the landed diff, and scores agents with stable fail-to-pass and pass-to-pass tests. That gives offline evaluation more of the constraints teams face in practice. ClickHouse adds a field report from the deployment side: agents are useful when they can read code, run tools, and stay inside a review-and-test loop. The numbers there are operational, not benchmark-grade, but they show why production teams care about grounded evaluation at all.

#### Evidence
- [ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents](../Inbox/2026-04-02--prodcodebench-a-production-derived-benchmark-for-evaluating-ai-coding-agents.md): Production-derived benchmark design and core results.
- [Agentic Coding at ClickHouse](../Inbox/2026-04-02--agentic-coding-at-clickhouse.md): Concrete deployment report with review-and-testing workflow and operational outcomes.

### Reliability is about behavior under constraints
Several papers focus on what happens after a model makes a plausible first move. Beyond Resolution Rates finds that many failures are not search failures in the narrow sense. Agents often locate the right file and still miss the fix because architectural judgment is wrong. ToolMisuseBench looks at a different layer of reliability: tool calls under schema drift, timeouts, rate limits, and authorization errors. Its baselines recover on some timeout and schema faults, but overall success stays at 0.250 and budgeted success is flat. The common message is that agent quality now depends on validation behavior, recovery policy, and action discipline, not just answer quality.

#### Evidence
- [Beyond Resolution Rates: Behavioral Drivers of Coding Agent Success and Failure](../Inbox/2026-04-02--beyond-resolution-rates-behavioral-drivers-of-coding-agent-success-and-failure.md): Trajectory analysis of coding-agent failures and the role of architectural judgment.
- [ToolMisuseBench: An Offline Deterministic Benchmark for Tool Misuse and Recovery in Agentic Systems](../Inbox/2026-04-02--toolmisusebench-an-offline-deterministic-benchmark-for-tool-misuse-and-recovery-in-agentic-systems.md): Deterministic benchmark for tool misuse, recovery, and budgeted reliability.

### LLMs are being pushed into executable testing work
Testing is becoming a first-class generation target, not just a post hoc check. TestDecision treats test-suite construction as a sequential optimization problem and reports large gains in branch coverage, execution pass rate, and bug finding over base open models. APITestGenie applies the same execution-minded attitude to APIs: it starts from business requirements plus OpenAPI specs, generates runnable Jest and Axios tests, and reaches at least one valid script for 22 of 25 requirements. Together these papers make testing more executable, more requirement-aware, and more useful as a direct product of the model pipeline.

#### Evidence
- [TestDecision: Sequential Test Suite Generation via Greedy Optimization and Reinforcement Learning](../Inbox/2026-04-02--testdecision-sequential-test-suite-generation-via-greedy-optimization-and-reinforcement-learning.md): Sequential test-suite generation with reported coverage and bug-finding gains.
- [APITestGenie: Generating Web API Tests from Requirements and API Specifications with LLMs](../Inbox/2026-04-02--apitestgenie-generating-web-api-tests-from-requirements-and-api-specifications-with-llms.md): Requirement-driven API test generation with executable validation rates.
