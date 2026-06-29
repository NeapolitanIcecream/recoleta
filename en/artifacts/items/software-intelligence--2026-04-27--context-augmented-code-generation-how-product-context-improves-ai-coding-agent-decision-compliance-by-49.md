---
source: arxiv
url: https://arxiv.org/abs/2605.08112v1
published_at: '2026-04-27T20:38:55'
authors:
- Drew Dillon
- Kasyap Varanasi
topics:
- code-generation
- coding-agents
- product-context
- retrieval-augmented-generation
- software-engineering-benchmarks
- human-ai-interaction
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Context-Augmented Code Generation: How Product Context Improves AI Coding Agent Decision Compliance by 49%

## Summary
The paper tests whether product context helps AI coding agents follow team decisions that are absent from source code. On an 8-task benchmark, Claude Code + Brief raises weighted decision compliance from 46% to 95%, with a workflow confound that the authors acknowledge.

## Problem
- AI coding agents can produce code that compiles while missing product decisions stored in specs, wikis, audits, and product tools.
- This matters because missed decisions can create compliance failures, deprecated UI usage, wrong feature flags, or changes that need human rework.
- Existing code benchmarks such as SWE-bench focus on issue resolution and do not score whether code follows team-specific product decisions.

## Approach
- The paper defines decision compliance as a weighted pass/fail score for task-specific gotchas, such as required audit logging, approved UI components, feature flags, ORM choices, and auth wrappers.
- The benchmark uses a clean-room Next.js 14 app called Prism Analytics, with 8 realistic tasks, 41 weighted decision points, 15 seeded product decisions, 3 personas, 5 customer signals, and 3 competitor profiles.
- The baseline is Claude Code with codebase access only, using Claude Sonnet 4.6 for code generation.
- The augmented setup adds Brief, which retrieves recorded decisions, personas, customer signals, and competitive context during spec generation and mid-build consultation; Opus 4.6 handles planning and Sonnet 4.6 handles code generation.
- Scoring uses regex checks over git diffs plus human review, with 3 independent runs per task per setup, for 48 total runs.

## Results
- Decision compliance improves from 19/41 points, or 46%, for Claude Code to 39/41 points, or 95%, for Claude Code + Brief, a 49 percentage point gain.
- Claude Code + Brief reaches 100% compliance on 6/8 tasks, compared with 2/8 for Claude Code; tasks at 0% drop from 2/8 to 0/8.
- Blocking violations fall from 5 to 0, deprecated pattern use falls from 3 to 0, and `any` type count falls from 9 to 0.
- Merge-ready tasks increase from 2/8, or 25%, to 8/8, or 100%; cost per merge-ready task drops from $2.07 to $0.66, a 68% reduction, even though total cost rises from $4.13 to $5.28.
- The augmented setup writes 838 tests while the baseline writes 0; lint and typecheck pass rates are 100% for both, while test pass rate is 0% for the baseline and 100% for the augmented setup.
- The evidence is limited by the small clean-room benchmark, 16 PR pairs, one human reviewer, and a confound: Brief changes both available context and the coding workflow through specs, acceptance criteria, and mid-build guidance.

## Link
- [https://arxiv.org/abs/2605.08112v1](https://arxiv.org/abs/2605.08112v1)
