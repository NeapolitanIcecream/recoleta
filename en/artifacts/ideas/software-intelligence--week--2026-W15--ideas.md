---
kind: ideas
granularity: week
period_start: '2026-04-06T00:00:00'
period_end: '2026-04-13T00:00:00'
run_id: ead7a913-d224-4dbe-aa9c-41958ae9d654
status: succeeded
topics:
- coding-agents
- verification
- benchmarks
- security
- repo-scale-evaluation
tags:
- recoleta/ideas
- topic/coding-agents
- topic/verification
- topic/benchmarks
- topic/security
- topic/repo-scale-evaluation
language_code: en
pass_output_id: 53
pass_kind: trend_ideas
upstream_pass_output_id: 52
upstream_pass_kind: trend_synthesis
---

# Verification gates for agent-written code

## Summary
The clearest near-term builds put verification in the action loop. One path is an external policy layer that rejects agent edits unless they satisfy traceability and test obligations. Another is a repository migration workflow that treats translated tests and repair reports as first-class artifacts. The third is a security gate for AI-written code that proves exploitability on selected diffs instead of relying on prompts or conventional static scanners.

## External policy and proof checks in the coding-agent write path
A governance file that an agent must satisfy before it can save code is becoming a practical product shape for teams that need traceability, architecture rules, and test evidence on every change. Nidus pushes this furthest: requirements, architecture, workflows, traces, and proof obligations live in one artifact, and every mutation is checked before persistence with structural checks and Z3. The concrete user is an engineering team in a regulated or high-assurance environment that already has CI, reviews, and policy documents but still loses context when agent work crosses tickets, docs, and code. The build is an external policy and verification layer that sits in the write path for coding agents, rejects changes with machine-readable violations, and keeps a durable record of why a change passed.

A cheap validation step is to apply this to one narrow workflow such as adding a feature that must include updated tests, linked requirements, and an approved architecture note. If the tool can reject incomplete agent edits and return actionable failure signals that help the next attempt succeed, teams will use it. If it only produces another static checklist, it will stall. The case is credible now because the paper reports a self-hosting deployment on a 100,000-line system with proof obligations checked on every commit, including a concrete rejected delivery that passed only after the agent added a missing test file.

### Evidence
- [Nidus: Externalized Reasoning for AI-Assisted Engineering](../Inbox/2026-04-06--nidus-externalized-reasoning-for-ai-assisted-engineering.md): Describes a governance runtime with solver-checked mutations, proof obligations on every commit, and a concrete rejected change that passed after adding a missing test.
- [Nidus: Externalized Reasoning for AI-Assisted Engineering](../Inbox/2026-04-06--nidus-externalized-reasoning-for-ai-assisted-engineering.md): The abstract states the self-hosting deployment and externalized enforcement model in direct terms.

## Repository migration workflow with translated tests and repair reports
Repository migration agents need a dedicated validation loop that translates tests, measures coverage gaps, and sends repair reports back before code is accepted. ReCodeAgent gives a concrete template for this workflow. Its Analyzer and Planning stages map repository structure and dependencies first, then the Validator runs translated tests, generates extra tests for uncovered functions, and feeds failures back to the Translator. That is a buildable product for platform teams handling language migrations, SDK rewrites, or framework upgrades across large internal codebases.

The useful scope is narrower than full autonomous translation across every language pair. Start with one migration class where teams already know the target stack and care about preserving behavior more than perfect style. The early product can expose the plan, name mappings, translated tests, uncovered functions, and repair loop as reviewable artifacts. The evidence supports this as a workflow change, not just a benchmark trick: removing the Validator cut test pass rate by 30.3 percentage points, and the full system reached 99.4% compilation success and 86.5% test pass rate across 118 real-world projects.

### Evidence
- [ReCodeAgent: A Multi-Agent Workflow for Language-agnostic Translation and Validation of Large-scale Repositories](../Inbox/2026-04-08--recodeagent-a-multi-agent-workflow-for-language-agnostic-translation-and-validation-of-large-scale-repositories.md): Provides the multi-agent workflow, including translated tests, coverage-gap checks, and repair reports, plus the ablation showing the Validator’s effect.
- [ReCodeAgent: A Multi-Agent Workflow for Language-agnostic Translation and Validation of Large-scale Repositories](../Inbox/2026-04-08--recodeagent-a-multi-agent-workflow-for-language-agnostic-translation-and-validation-of-large-scale-repositories.md): The abstract confirms repository-level autonomous translation and validation for large-scale projects.

## Exploitability gates for security-sensitive AI code changes
Security review for AI-written code needs an exploitability check layer, not just prompt hardening and static scanning. Broken by Default is concrete on the gap: across 3,500 generated programs, 55.8% contained at least one vulnerability found by COBALT, with 1,055 Z3-proven findings, while six industry tools together missed 97.8% of the formally proven cases in the subset test. Secure prompts reduced the mean vulnerability rate by only 4 points. For teams using coding agents on parsers, auth flows, memory management, or input handling, the practical build is a gate that selects security-sensitive diffs, generates proof obligations or witness inputs for likely weakness classes, and blocks merge when exploitability is demonstrated.

This fits first in narrow surfaces where the weakness classes are known and the cost of missed bugs is high: C and C++ memory code, auth handlers, SQL-facing request code, archive extraction, and similar paths. The first product does not need whole-program proof. It needs to prove or falsify exploitability for a small set of common failure modes and attach the witness to the review. The paper’s self-review result also gives a workflow clue: models spotted their own vulnerable outputs 78.7% of the time in review mode, so a paired generation-plus-proof-review path is easier to justify than trusting generation alone.

### Evidence
- [Broken by Default: A Formal Verification Study of Security Vulnerabilities in AI-Generated Code](../Inbox/2026-04-07--broken-by-default-a-formal-verification-study-of-security-vulnerabilities-in-ai-generated-code.md): Reports the core vulnerability rates, Z3-proven findings, secure-prompt ablation, industry-tool miss rate, and self-review asymmetry.
- [Broken by Default: A Formal Verification Study of Security Vulnerabilities in AI-Generated Code](../Inbox/2026-04-07--broken-by-default-a-formal-verification-study-of-security-vulnerabilities-in-ai-generated-code.md): The paper abstract states the formal verification framing and headline exploitability numbers.
