---
source: arxiv
url: https://arxiv.org/abs/2606.10211v1
published_at: '2026-06-08T22:04:51'
authors:
- Hunter Leary
- Luke Hanuska
- Chris Brown
topics:
- test-generation
- foundation-models
- code-intelligence
- software-testing
- dotnet
- evaluation-infrastructure
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# TestMap: Evidence Infrastructure for Foundation-Model-Assisted Test Generation

## Summary
TestMap is an open-source prototype that records evidence for FM-generated unit tests in real C#/.NET repositories. It checks whether each candidate builds, passes, improves coverage or mutation signals, needs repair, and looks reviewable.

## Problem
- FM-generated tests can compile and pass while still checking weak or wrong behavior, so teams need evidence before using them to validate production code.
- Existing signals such as build logs, coverage, mutation results, code metrics, and test smells sit in separate tools and are hard to tie back to a single generated test.
- This matters because test generation is entering normal developer workflows while trust remains low: Stack Overflow 2025 reports 45% of respondents distrust AI tool outputs, and Google DORA 2025 reports 30% have little or no trust in AI-generated code.

## Approach
- TestMap ingests a repository, records commit and project metadata, opens .NET solutions with Roslyn, and stores project evidence in SQLite.
- It runs static analysis, baseline tests, coverage collection, mutation testing with Stryker.NET when feasible, code metrics, and xNose-based C# test-smell detection.
- It maps generated candidates to source methods, related tests, uncovered code, survived mutants, prompts, models, generation strategy, repair budget, and execution results.
- The generation flow builds an evidence package for a target method, optionally creates a context graph, then prompts the model through staged planning and test creation.
- It keeps failed, repaired, low-impact, and evidence-positive candidates so researchers can compare models, prompts, context modes, pass@k budgets, and repair loops.

## Results
- The excerpt reports no quantitative benchmark result for generated-test quality, such as pass rate, coverage gain, mutation-score gain, or developer acceptance.
- TestMap defines 9 evidence categories: repository, target, generation, execution, testing-impact, quality, failure, repair, and strategy evidence.
- It assigns 4 pipeline outcomes: ValidationFailed, Validated, ValidatedLowImpact, and ValidatedEvidencePositive.
- The prototype targets C#/.NET repositories and uses named tools including Roslyn, TRX test results, Cobertura coverage reports, Stryker.NET mutation reports, SQLite, and xNose.
- The paper claims the main gain is candidate-level traceability across generation, validation, repair, and measurement, including failed candidates that many pipelines discard.

## Link
- [https://arxiv.org/abs/2606.10211v1](https://arxiv.org/abs/2606.10211v1)
