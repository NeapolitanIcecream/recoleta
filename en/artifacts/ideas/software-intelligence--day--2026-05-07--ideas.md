---
kind: ideas
granularity: day
period_start: '2026-05-07T00:00:00'
period_end: '2026-05-08T00:00:00'
run_id: ece68aa0-fdbb-4456-ade7-de513c8e0dda
status: succeeded
topics:
- coding agents
- software engineering benchmarks
- repository evaluation
- test evolution
- agent control
- maintainability
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering-benchmarks
- topic/repository-evaluation
- topic/test-evolution
- topic/agent-control
- topic/maintainability
language_code: en
pass_output_id: 135
pass_kind: trend_ideas
upstream_pass_output_id: 134
upstream_pass_kind: trend_synthesis
---

# Repository Safeguards for Agent-Written Code

## Summary
Coding-agent adoption needs repository checks that catch missed tests, structural backend violations, and unsafe maintenance edits before generated code reaches reviewers. The concrete work is small enough to add around current agents: affected-test search for production commits, CI verifiers for backend structure and migration behavior, and a code-smell triage loop that limits broad refactors.

## Affected-test search before agent-written test patches
Teams using agents to update tests after production changes should add a separate affected-test discovery step before allowing the agent to edit the suite. The step should ask for three lists: tests expected to fail, tests that still pass but need semantic updates, and behavior that needs new tests. Reviewers can compare the list with dependency traces, recent coverage, changed public APIs, and repository search results before accepting a generated patch.

TEBench shows why this belongs before patch generation. Across seven configurations using Claude Code, Codex CLI, and OpenCode, affected-test identification F1 stayed between 45.7% and 49.4%. Stale tests were hardest, with average F1 around 36%, because agents followed execution failures and missed passing tests that no longer checked the changed behavior. ProCodeBench adds a related signal: repository context improves intent prediction from real VS Code traces, while simulated traces overstate performance. A cheap internal check is to sample recent production commits, ask the agent for the affected-test inventory, and have maintainers grade missed stale and missing-test cases before measuring generated patch quality.

### Evidence
- [Breaking, Stale, or Missing? Benchmarking Coding Agents on Project-Level Test Evolution](../Inbox/2026-05-07--breaking-stale-or-missing-benchmarking-coding-agents-on-project-level-test-evolution.md): TEBench reports low affected-test identification F1 and identifies stale tests as the hardest category.
- [An Empirical Study of Proactive Coding Assistants in Real-World Software Development](../Inbox/2026-05-07--an-empirical-study-of-proactive-coding-assistants-in-real-world-software-development.md): ProCodeBench reports that repository context helps intent prediction and that real developer traces are harder than simulated traces.

## Backend-generation CI gates for architecture, database, and ORM requirements
Backend teams should encode structural requirements as executable checks alongside API tests when accepting agent-generated services or feature patches. A practical gate would run the usual HTTP behavioral suite, then verify allowed layers, database choice, migrations or schema setup, and ORM usage. The database checks deserve explicit fixtures for PostgreSQL or SQLite because data-layer defects are a repeated failure source.

Constraint Decay fixed one OpenAPI contract across 80 backend-generation tasks and found that capable agent configurations lost about 30 percentage points in assertion pass rate when Clean Architecture, database, and ORM constraints were added. Database requirements caused the largest marginal losses: PostgreSQL cost 19.3 ± 2.5 assertion-pass points and SQLite cost 14.3 ± 2.5. ScarfBench points to the same adoption blocker in enterprise Java migration: agents often reached compile or deploy stages without preserving behavior, and only 1 of 204 directed migrations was fully behaviorally equivalent. A useful first test is to run the gate on agent-created backend pull requests that already pass API tests and count how often structure or data-layer checks would have blocked review.

### Evidence
- [Constraint Decay: The Fragility of LLM Agents in Backend Code Generation](../Inbox/2026-05-07--constraint-decay-the-fragility-of-llm-agents-in-backend-code-generation.md): Constraint Decay quantifies assertion-pass losses under architecture, database, and ORM constraints, with database requirements causing the largest losses.
- [ScarfBench: A Benchmark for Cross-Framework Application Migration in Enterprise Java](../Inbox/2026-05-07--scarfbench-a-benchmark-for-cross-framework-application-migration-in-enterprise-java.md): ScarfBench shows low behavior-preserving success for cross-framework enterprise Java migration even when compile or deploy success improves.

## Code-smell triage with false-positive labels and net-new-smell checks
Architectural smell repair should start as a triage workflow, with agent edits held until the smell is labeled as true positive, false positive, or partially valid. The agent can still help by gathering affected modules, explaining dependency paths, proposing a small patch, and reporting the smell delta after the patch. Reviewers should see both removed smells and newly introduced smells before approving any cross-module refactor.

SmellBench gives the reason for this control point. Expert review found 41 false positives among 65 hard static detections in scikit-learn, a 63.1% false-positive rate. The best agent resolved 47.7% of cases, but the most aggressive repair setting introduced 140 new smells. The first implementation can be a pull-request bot around an existing smell detector: require a triage label, run the detector before and after the proposed change, and block broad agent edits when net smells increase or the affected-module list is larger than the review budget.

### Evidence
- [SmellBench: Evaluating LLM Agents on Architectural Code Smell Repair](../Inbox/2026-05-07--smellbench-evaluating-llm-agents-on-architectural-code-smell-repair.md): SmellBench reports high false-positive rates for hard architectural smells, limited resolution rates, and 140 new smells from the most aggressive agent setting.
