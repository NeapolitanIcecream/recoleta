---
kind: ideas
granularity: week
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-27T00:00:00'
run_id: f9f4ae89-06b0-46d4-b288-2d12297bfb6b
status: succeeded
topics:
- coding-agents
- evaluation
- repo-level-codegen
- execution
- agent-harness
tags:
- recoleta/ideas
- topic/coding-agents
- topic/evaluation
- topic/repo-level-codegen
- topic/execution
- topic/agent-harness
language_code: en
pass_output_id: 113
pass_kind: trend_ideas
upstream_pass_output_id: 112
upstream_pass_kind: trend_synthesis
---

# Executable Repository Readiness

## Summary
Coding-agent work this week points to three practical changes: treat repository setup as its own executable stage, evaluate repo generation with size-aware runnable tests, and put harness features under explicit benchmark control. The common pattern is that runnable proof depends on more than the base model. Environment configuration, repository size, and flag interactions each change whether an agent can complete real software tasks.

## Repository bootstrap worker with executable setup logs
A repo-level coding agent needs an environment setup stage with its own budget, telemetry, and pass criteria. The evidence this week points to setup failure as a separate operational problem, not a minor prelude to code generation. RAT reports executable setup success of 63.2% on Python, 41.3% on Java, 98.7% on Rust, and 68.7% on JS/TS across a 2,000+ repository benchmark, with large gains over SWE-agent on the same backbone. The cost is also visible: full RAT uses about 421.9K tokens and 24.3 minutes on average in one Python setting. Teams deploying coding agents on internal repos can turn this into a concrete workflow change: run environment configuration as a first-class step, log whether the repo became runnable, and stop scoring downstream patch quality when setup never succeeded.

The practical build here is a repo bootstrap worker that detects language, selects a base image, installs dependencies in a sandbox, and emits a machine-readable setup record with commands tried, files touched, test or smoke-check status, and failure class. That output can feed both evaluation and user-facing product behavior. A cheap test is to take a mixed sample of internal repositories and measure how often the worker reaches a runnable state before any code-editing agent starts. If that rate is low, patch-generation metrics are hiding the main failure mode.

### Evidence
- [RAT: RunAnyThing via Fully Automated Environment Configuration](../Inbox/2026-04-25--rat-runanything-via-fully-automated-environment-configuration.md): RAT quantifies environment setup success by language, compares against baselines, and reports token and latency cost for executable setup.
- [RAT: RunAnyThing via Fully Automated Environment Configuration](../Inbox/2026-04-25--rat-runanything-via-fully-automated-environment-configuration.md): The paper states that repository-level tasks require executable environments because otherwise code remains unverifiable and functionally invalid.

## Repo-level evaluation harness with size-bucketed scoring
Evaluation for repo-level code generation can now be built around structured design inputs and runnable repository tests, with separate tracks by repository size. RealBench gives a clear reason to change the harness: current models reach only 19.39% average Pass@1 on full-repository generation, performance stays above 40% on repositories under 500 LOC, and falls below 15% above 2000 LOC. It also reports that holistic generation works better on smaller repositories, while incremental generation works better once repositories get larger.

A concrete build for model teams and applied platform groups is an internal benchmark that starts from requirements plus package and class diagrams, then scores generated repositories by test pass, coverage, and size bucket. The key workflow change is to stop reporting a single repo-wide score. Small repos and large repos behave differently enough that one blended metric hides where a system is usable. This also creates a straightforward product gate: allow end-to-end repo generation for small, low-dependency codebases, and require file-by-file or module-by-module plans for larger ones. A cheap check is to rerun an existing coding agent on the same task set with separate scoring for repositories below 1000 LOC and above 1000 LOC and compare holistic generation against incremental generation.

### Evidence
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): RealBench reports repo-level Pass@1, performance by repository size, and the split between holistic and incremental generation strategies.
- [RealBench: A Repo-Level Code Generation Benchmark Aligned with Real-World Software Development Practices](../Inbox/2026-04-24--realbench-a-repo-level-code-generation-benchmark-aligned-with-real-world-software-development-practices.md): The paper text states that smaller repositories favor whole-repo generation while complex repositories need staged generation.

## Harness flag registry and benchmark replay for coding agents
Agent teams can justify a dedicated harness tuning loop before adding more memory, reflection, or self-evaluation features. HARBOR's manual tuning study on Terminal-Bench 2 shows how unstable these combinations are: the all-flags-off baseline passes 15 of 89 tasks, a five-flag native configuration reaches 17 of 89, adding a self-evaluation gate drops to 13 of 89, and adding ACON, Reflexion, and PASTE drops to 12 of 89. The paper also notes that harness code dominates the implementation in production-style agents, with one cited audit putting Claude Code at about 98.4% harness code.

The immediate build is a flag registry and experiment runner for harness features such as cache modes, context compression, trajectory replay, tool prediction, and self-evaluation gates. Each run should record active flags, task suite version, runtime cost, and pass count on a fixed executable benchmark. This is useful for any team that keeps adding features to a coding agent and only checks whether the latest stack feels better in demos. A cheap check is to replay the last few harness releases on one stable terminal or repo benchmark and see whether recent feature additions improved pass rate or only increased latency and context use.

### Evidence
- [HARBOR: Automated Harness Optimization](../Inbox/2026-04-22--harbor-automated-harness-optimization.md): HARBOR reports the four-round manual tuning study and shows that extra harness features can reduce task success.
- [HARBOR: Automated Harness Optimization](../Inbox/2026-04-22--harbor-automated-harness-optimization.md): The paper text says production-style agents are dominated by harness code and operational complexity.
