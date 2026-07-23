---
kind: ideas
granularity: day
period_start: '2026-07-22T00:00:00'
period_end: '2026-07-23T00:00:00'
run_id: f50b9860-2370-482a-b6f9-4e5c11417056
status: succeeded
topics:
- coding agents
- program repair
- code optimization
- test generation
- repository context
tags:
- recoleta/ideas
- topic/coding-agents
- topic/program-repair
- topic/code-optimization
- topic/test-generation
- topic/repository-context
language_code: en
pass_output_id: 345
pass_kind: trend_ideas
upstream_pass_output_id: 344
upstream_pass_kind: trend_synthesis
---

# Executable controls for code optimization and generated tests

## Summary
Performance and test-generation workflows can make model output more dependable by combining complementary executable signals: runtime profiles to prioritize static optimization matches, semantic mutations to challenge acceptance tests, and deterministic project scaffolding before behavior-level validation.

## Profiler-weighted ranking of static optimization matches
Performance engineers could run MoST-style validated Semgrep rules across a repository, then rank the matches by the runtime share and call context reported by a sampling profiler. MoST supplies reusable candidate transformations across languages and architectures, but a static match does not show whether a location matters for the deployed workload; PerfAgent shows that profiler feedback helps agents cross abstraction boundaries and reach expert-level speedups more often. The concrete change is to give the coding agent only the highest-impact rule matches, re-profile every correct patch, and retain the fastest result rather than the last one. A low-cost check is to compare profiler-ranked and unranked rule matches on the same optimization tasks, measuring successful speedup per attempted edit and validation cost.

### Sources
- [PerfAgent: Profiler-Guided Iterative Refinement for Repository-Level Code Optimization](../Inbox/2026-07-22--perfagent-profiler-guided-iterative-refinement-for-repository-level-code-optimization.md): PerfAgent increased expert-matching patches from 19.6% to 39.2% on GSO and from 26% to 74% on SWE-fficiency-Lite using profiler-guided iterative validation.
- [Multi-Source and Cross-Scenario Strategy-Guided Code Optimization](../Inbox/2026-07-22--multi-source-and-cross-scenario-strategy-guided-code-optimization.md): MoST converts multi-source optimization strategies into validated Semgrep rules and reported 24.44%–180.00% more exact developer-matching patches than SemOpt.

## Mutation-hardened acceptance tests for performance patches
Maintainers accepting agent-generated optimizations should challenge the affected-test set with plausible incorrect performance patches before labeling the fastest candidate correct. PerfAgent efficiently selects the fastest patch that passes targeted tests, but its own failure analysis notes that narrow testing can miss edge cases. CoHarden shows why a passing test is not necessarily discriminating: rigorous reproduction tests improved repair resolution by 8.5 points, lax tests produced no gain, and misaligned tests reduced it. An optimization loop could generate semantic mutants such as removed bounds checks, altered fallback paths, or unsafe cache reuse, then expand the selective test set until it rejects those mutants. Replaying previously accepted patches with and without this hardening would reveal whether the extra mutation step catches regressions that selective dependency-based testing misses.

### Sources
- [PerfAgent: Profiler-Guided Iterative Refinement for Repository-Level Code Optimization](../Inbox/2026-07-22--perfagent-profiler-guided-iterative-refinement-for-repository-level-code-optimization.md): PerfAgent identifies insufficiently narrow testing as a source of fast patches that silently break edge cases or downstream paths.
- [Beyond Fail-to-Pass: Iterative Hardening of Co-Generated Bug Reproduction Tests and Fixes](../Inbox/2026-07-22--beyond-fail-to-pass-iterative-hardening-of-co-generated-bug-reproduction-tests-and-fixes.md): Rigorous tests raised Resolved by 8.5 points; lax tests added no benefit and misaligned tests reduced Resolved by 3.6 points.

## Compilation and mutation checks for generated BDD glue code
Teams maintaining Java BDD suites could separate glue-code acceptance into three gates: deterministic framework scaffolding, compilation and static repair, then mutation-based behavior checks. AutoGlue retrieves scenario and repository context, yet only 46.1% of generated implementations were directly usable and execution validation was limited by weak step-level oracles. CATGen shows that fixed skeletons and static-analysis repairs can remove many project-integration failures cheaply; CoHarden shows that an executable test can still accept a plausible but wrong implementation. For each generated step definition, the pipeline should mutate API calls, parameters, or omitted actions and require the enclosing scenario to reject those variants. The first evaluation can compare compilation rate, direct usability, and surviving mutants against AutoGlue’s current generation workflow.

### Sources
- [Bridging Behavior and Implementation: Automated Java Glue Code Generation for Behavior-Driven Development](../Inbox/2026-07-22--bridging-behavior-and-implementation-automated-java-glue-code-generation-for-behavior-driven-development.md): AutoGlue produced directly usable code for 46.1% of 1,307 Java BDD steps, with execution validation constrained by environment dependencies and weak step-level oracles.
- [Context Matters: Improving the Practical Reliability of LLM-Based Unit Test Generation](../Inbox/2026-07-22--context-matters-improving-the-practical-reliability-of-llm-based-unit-test-generation.md): CATGen’s deterministic skeletons and static-analysis repairs improved industrial compilation success by 24.72%–38.05% while reducing token use by 66.83%–83.86%.
- [Beyond Fail-to-Pass: Iterative Hardening of Co-Generated Bug Reproduction Tests and Fixes](../Inbox/2026-07-22--beyond-fail-to-pass-iterative-hardening-of-co-generated-bug-reproduction-tests-and-fixes.md): CoHarden distinguishes rigorous tests from lax tests that satisfy fail-to-pass while still accepting plausible incorrect fixes.
