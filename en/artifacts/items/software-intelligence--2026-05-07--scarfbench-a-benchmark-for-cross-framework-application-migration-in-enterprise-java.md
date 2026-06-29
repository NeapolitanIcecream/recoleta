---
source: arxiv
url: https://arxiv.org/abs/2605.06754v2
published_at: '2026-05-07T16:05:35'
authors:
- Advait Pavuluri
- Bridget McGinn
- Ashita Saxena
- George Safta
- Srikanth Tamilselvam
- Raju Pavuluri
- Michele Merler
- Baishakhi Ray
- Rahul Krishna
topics:
- cross-framework-migration
- enterprise-java
- coding-agents
- software-benchmarks
- behavior-preserving-refactoring
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# ScarfBench: A Benchmark for Cross-Framework Application Migration in Enterprise Java

## Summary
ScarfBench is a benchmark for testing whether coding agents can migrate enterprise Java applications across Spring, Jakarta EE, and Quarkus while preserving behavior. Current agents rarely complete these migrations, even when their code compiles and deploys.

## Problem
- Enterprise Java framework migration requires coordinated edits to build files, dependency injection, persistence, HTTP handling, deployment, and runtime configuration.
- Existing coding benchmarks mostly test bug fixing, feature work, version upgrades, or same-stack modernization, so they miss cross-framework application refactoring.
- The problem matters because long-lived Java systems often need migration to newer runtimes, and broken migrations can fail at compile time, startup, or user-visible behavior.

## Approach
- ScarfBench contains 34 application families implemented by Java experts in Spring, Jakarta EE, and Quarkus, giving 102 framework-specific variants and 204 directed migration tasks.
- Each task gives an agent a working source application and a target framework; the agent must create a behavior-equivalent target implementation without seeing the expert target.
- The benchmark has 29 focused single-layer applications and 5 whole applications, totaling about 151K lines of paired Java across 1,946 source and test files.
- Evaluation rebuilds the candidate, deploys it in the target container or Docker Compose stack, and runs application-specific behavioral tests over the observable interface.
- The paper also derives 13 failure categories across build, deploy, and test stages, with LLM annotation and expert adjudication.

## Results
- The strongest focused-layer score is 15.3% aggregate behavioral test pass; the strongest whole-application score is 12.2%.
- Only 1 of 204 directed migration tasks produces a fully behaviorally equivalent target implementation.
- With skills enabled, Claude Code with Opus-4.6 has the best whole-application run: 87% compile, 40% deploy, and 12% test success.
- On focused applications with skills, Claude Code reaches 93% compile success, while Gemini CLI with Gemini-3.1-Pro reaches 61% deploy and 15% test success.
- Migration target matters: Jakarta EE target migrations pass behavioral tests only 2% of the time, compared with 12% for Spring targets and 14% for Quarkus targets; 57% of Jakarta-targeted attempts fail at compile time.
- Skills help runnability more than behavior: for Gemini focused tasks, deploy success rises from 7% without skills to 61% with skills, while test success rises from 2% to 15%.

## Link
- [https://arxiv.org/abs/2605.06754v2](https://arxiv.org/abs/2605.06754v2)
