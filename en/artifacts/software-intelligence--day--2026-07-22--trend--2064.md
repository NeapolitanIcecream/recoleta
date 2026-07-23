---
kind: trend
trend_doc_id: 2064
granularity: day
period_start: '2026-07-22T00:00:00'
period_end: '2026-07-23T00:00:00'
topics:
- coding agents
- program repair
- code optimization
- test generation
- repository context
run_id: materialize-outputs
aliases:
- recoleta-trend-2064
tags:
- recoleta/trend
- topic/coding-agents
- topic/program-repair
- topic/code-optimization
- topic/test-generation
- topic/repository-context
language_code: en
pass_output_id: 344
pass_kind: trend_synthesis
---

# Executable feedback is outperforming prompt-only coding workflows

## Overview
The recent run of work on coding-agent controls continues, but today’s evidence makes the control signals more task-specific. Profilers, mutation patches, static analysis, and repository context guide generation and verify outcomes inside the loop. Reported gains are substantial, though they come from separate benchmarks and do not establish one generally superior architecture.

## Findings

### Performance optimization
Repository-level optimization improves when agents receive measured runtime evidence rather than broad instructions. PerfAgent identifies hotspots with a sampling profiler, validates each patch, and feeds speedup results back for up to five rounds. With GPT-5.1, expert-matching patches rose from 19.6% to 39.2% on GSO and from 26% to 74% on SWE-efficiency-Lite.

MoST supplies a complementary form of executable guidance. It converts optimization knowledge from commits and technical documents into validated Semgrep rules, including strategies transferred across languages and architectures. On 351 historical tasks, it produced 24.44%–180.00% more exact developer-matching patches than SemOpt. Together, the studies support task-specific measurement and validated rules as stronger optimization signals than unguided generation.

#### Sources
- [PerfAgent: Profiler-Guided Iterative Refinement for Repository-Level Code Optimization](../Inbox/2026-07-22--perfagent-profiler-guided-iterative-refinement-for-repository-level-code-optimization.md): Reports profiler-guided iteration, correctness validation, and expert-matching patch rates on GSO and SWE-efficiency-Lite.
- [Multi-Source and Cross-Scenario Strategy-Guided Code Optimization](../Inbox/2026-07-22--multi-source-and-cross-scenario-strategy-guided-code-optimization.md): Describes cross-source strategy extraction, Semgrep rule validation, and developer-patch matching results across 351 tasks.

### Tests as discriminating verifiers
Test generation is being judged by whether it separates correct patches from plausible failures, not merely whether a test runs. CoHarden challenges generated bug-reproduction tests with semantic mutations. Rigorous tests raised repair resolution by 8.5 points, while lax tests produced no gain and misaligned tests reduced resolution by 3.6 points.

CATGen addresses an earlier reliability boundary: generated unit tests must compile in dependency-heavy projects before coverage matters. It retrieves project and framework context, creates scaffolding deterministically, and applies static-analysis repairs. Across eight industrial projects, compilation success improved by 24.72%–38.05%, while token use fell by 66.83%–83.86%. The shared result is that test artifacts become more useful when deterministic checks surround model generation.

#### Sources
- [Beyond Fail-to-Pass: Iterative Hardening of Co-Generated Bug Reproduction Tests and Fixes](../Inbox/2026-07-22--beyond-fail-to-pass-iterative-hardening-of-co-generated-bug-reproduction-tests-and-fixes.md): Distinguishes rigorous, lax, and misaligned reproduction tests and measures their different effects on downstream repair.
- [Context Matters: Improving the Practical Reliability of LLM-Based Unit Test Generation](../Inbox/2026-07-22--context-matters-improving-the-practical-reliability-of-llm-based-unit-test-generation.md): Reports compilation, coverage, generation-time, and token-use gains from explicit context and deterministic repair.

### Repository context before generation
Two systems narrow generation by assembling the surrounding software context first. AutoGlue interprets each behavior-driven development step within its scenario, then retrieves related specifications and project APIs. It improved API F1 by 58.7% over few-shot prompting, although only 46.1% of outputs were directly usable.

CATGen similarly retrieves class structure, external calls, and testing frameworks before asking the model to complete a fixed test skeleton. Its industrial results show that this division of labor can improve compilation while reducing repair loops. The evidence is limited to Java-oriented testing and glue-code tasks, so broader repository editing remains unproven.

#### Sources
- [Bridging Behavior and Implementation: Automated Java Glue Code Generation for Behavior-Driven Development](../Inbox/2026-07-22--bridging-behavior-and-implementation-automated-java-glue-code-generation-for-behavior-driven-development.md): Evaluates scenario interpretation and project-aware retrieval on 1,307 Java behavior-step pairs.
- [Context Matters: Improving the Practical Reliability of LLM-Based Unit Test Generation](../Inbox/2026-07-22--context-matters-improving-the-practical-reliability-of-llm-based-unit-test-generation.md): Uses five types of project context and deterministic scaffolding across proprietary Java projects and Defects4J.
