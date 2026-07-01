---
kind: ideas
granularity: day
period_start: '2026-06-30T00:00:00'
period_end: '2026-07-01T00:00:00'
run_id: 65a2ce97-03e2-4b7f-a0b2-e40baed0bfa6
status: succeeded
topics:
- coding agents
- software maintenance
- performance engineering
- C-to-Rust migration
- agent governance
- benchmarking
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-maintenance
- topic/performance-engineering
- topic/c-to-rust-migration
- topic/agent-governance
- topic/benchmarking
language_code: en
pass_output_id: 295
pass_kind: trend_ideas
upstream_pass_output_id: 294
upstream_pass_kind: trend_synthesis
---

# Auditable Code Change Automation

## Summary
Coding-agent adoption is most concrete where the agent works against artifacts a reviewer already trusts: feature-to-code maps, profiler traces, compiler diagnostics, reproducible timing runs, and staged approval records. The clearest work to try is in maintenance and performance workflows where teams can measure localization quality, patch acceptance, build success, or timing improvement without changing the whole development process.

## Profiler-derived static checks for C/C++ memory patch queues
Performance teams can turn one-off memory investigations into a repeatable agent workflow: load profiler traces, ask the agent to write anti-pattern reports with source examples, generate Clang Static Analyzer checks, and open patch batches with syntax checks and rollback points. MOA reports this pattern on OpenHarmony 5.0, where three profiled services produced 13 validated anti-patterns, then synthesized checkers found 10,067 inefficiency instances across seven services. The system generated 769 optimization patches with 92.5% expert acceptance, plus reported average heap and binary-size reductions.

The practical build is a patch queue tied to profiler evidence, not a free-form optimization bot. Each proposed change should carry the trace symptom, the static checker rule that found the instance, the affected symbols, and the validation result. A small pilot can start with one high-memory service and one recurring allocation or copying pattern, then measure how many generated patches a senior performance engineer accepts without rewriting.

### Evidence
- [MOA: A Profiling-Guided LLM Framework for Memory-Optimization Automation at Codebase Scale](../Inbox/2026-06-30--moa-a-profiling-guided-llm-framework-for-memory-optimization-automation-at-codebase-scale.md): MOA summary gives the profiler-to-anti-pattern-to-checker-to-patch workflow, OpenHarmony scale, detected inefficiencies, generated patches, acceptance rate, and memory-size results.
- [MOA: A Profiling-Guided LLM Framework for Memory-Optimization Automation at Codebase Scale](../Inbox/2026-06-30--moa-a-profiling-guided-llm-framework-for-memory-optimization-automation-at-codebase-scale.md): The paper abstract states the three-agent design and reports 13 anti-patterns, over 10,000 inefficiencies, 769 patches, 92.5% expert acceptance, and heap reduction.

## Feature-to-code maps before repository-level agent edits
Teams maintaining unfamiliar Java repositories can add a feature map as the first artifact in an agent edit flow. FeatX extracts an epic-feature hierarchy, links features to classes, methods, or files, and asks the user to edit the feature list before the agent plans and generates line-level diffs. Its UI also separates feature editing, mapped code inspection, agent planning, and patch review.

This is most useful for product-facing maintenance work where the hard part is finding the code affected by a feature change. In FeatX’s study, workload fell from 12.5 to 7.4 on NASA-TLX against ChatGPT, and function-level modification localization reached 0.385 F1 across 38 feature-editing commits. A team can test the workflow by replaying recent feature commits, checking whether the map points reviewers to the functions they actually changed, then requiring every agent diff to cite the feature nodes and code entities it touched.

### Evidence
- [FeatX: Editing Software by Editing Features for Repository-Level Code Evolution](../Inbox/2026-06-30--featx-editing-software-by-editing-features-for-repository-level-code-evolution.md): FeatX summary describes feature hierarchy extraction, feature-to-code mappings, the multi-panel workflow, workload results, and localization metrics.
- [FeatX: Editing Software by Editing Features for Repository-Level Code Evolution](../Inbox/2026-06-30--featx-editing-software-by-editing-features-for-repository-level-code-evolution.md): The paper text explains the gap caused by missing feature lists and feature-to-code mappings, then describes FeatX’s hierarchy and three-stage Evolution Agent.

## Compiler-error repair templates for C-to-Rust migration pilots
C-to-Rust migration agents should keep a repair table keyed to Rust compiler diagnostics. AdaTrans maps error codes to repair templates and Rust documentation snippets, then runs `cargo build`, tests the translated Rust, and compares output behavior with the original C program. The repair loop also treats syntax, ownership, behavior, and ambiguous failures differently, including different sampling settings by error type.

The near-term fit is file-level migration of self-contained C modules with clear input and output behavior. AdaTrans reports a 95.51% mean compilation pass rate, 81.09% mean solve rate under fuzz-based tests, and 1.19% unsafe file rate on 104 algorithmic problems. A migration team can start by logging every compiler error, chosen repair template, build result, test result, and `unsafe` use for a small module set. That log gives reviewers a concrete reason to accept, reject, or improve each automated repair.

### Evidence
- [AdaTrans: Automated C to Rust Transformation via Error-Adaptive Repair](../Inbox/2026-06-30--adatrans-automated-c-to-rust-transformation-via-error-adaptive-repair.md): AdaTrans summary describes the generate-verify-repair loop, compiler-error-to-template RAG, validation pipeline, error categories, and reported pass, solve, and unsafe rates.
- [AdaTrans: Automated C to Rust Transformation via Error-Adaptive Repair](../Inbox/2026-06-30--adatrans-automated-c-to-rust-transformation-via-error-adaptive-repair.md): The abstract reports the controlled file-level setting, multi-stage validation pipeline, 104-problem evaluation, compilation pass rate, solve rate, and unsafe file rate.
