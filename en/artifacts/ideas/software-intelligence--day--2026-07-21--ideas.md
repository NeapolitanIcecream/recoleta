---
kind: ideas
granularity: day
period_start: '2026-07-21T00:00:00'
period_end: '2026-07-22T00:00:00'
run_id: c8f5fa01-360f-4795-b8d7-66a13cdc9488
status: succeeded
topics:
- coding agents
- repository intelligence
- execution feedback
- software testing
- code benchmarks
tags:
- recoleta/ideas
- topic/coding-agents
- topic/repository-intelligence
- topic/execution-feedback
- topic/software-testing
- topic/code-benchmarks
language_code: en
pass_output_id: 343
pass_kind: trend_ideas
upstream_pass_output_id: 342
upstream_pass_kind: trend_synthesis
---

# Repository-aware editing, recovery, and evaluation for coding agents

## Summary
Coding-agent controls can move closer to the semantics of the work: requirement links can constrain cross-file edits, invariant violations can improve recovery decisions, and controlled code transformations can reveal when repository retrieval actually saves effort. The evidence supports targeted evaluations rather than broad production claims.

## Requirement-linked semantic operations for cross-file changes
Teams automating repository-wide changes should bind each semantic edit operation to the requirements and design elements it is expected to satisfy. TraceDev shows how a traceability graph can expose missing links among requirements, designs, and files, while SCAS applies deterministic operations such as renaming a symbol or adding a parameter across affected locations. Combined, these mechanisms could prevent an operation that is structurally complete but implements the wrong requirement—or a requirement-aligned plan that leaves dispersed edits unfinished.

A practical implementation would require every operation to declare the traceability nodes it affects, update the graph after execution, and block completion when a required node has no implementation or test evidence. The cheapest useful check is a set of multi-file API changes with seeded omissions: compare text patches, unconstrained semantic operations, and requirement-linked operations on token use, missed call sites, and unmet acceptance criteria. TraceDev does not isolate the graph’s causal contribution, and SCAS reports only a preliminary synthetic rename probe, so this combination needs direct ablation before production use.

### Sources
- [TraceDev: A Traceability-Driven Multi-agent Framework for Requirement-to-Code Development](../Inbox/2026-07-21--tracedev-a-traceability-driven-multi-agent-framework-for-requirement-to-code-development.md): TraceDev reports 53.63% and 56.82% success on 125 use cases while using a graph that links requirements, designs, and code.
- [Beyond Text Editing: Algebraic Manipulation of Source Code](../Inbox/2026-07-21--beyond-text-editing-algebraic-manipulation-of-source-code.md): The SCAS feasibility probe reports higher success and one to two orders of magnitude fewer tokens for a non-local cross-file change, but the evaluation is preliminary.

## Invariant-aware recovery routing for library maintenance agents
Maintainers using agents on C/C++ libraries could route failed attempts using invariant violations as well as compiler output, stderr, and ordinary test verdicts. CodeRescue demonstrates that reflection, replanning, and escalation have complementary cost-success profiles, but its router is described around conventional execution feedback. LISA produces documentation-grounded invariant checks for non-crashing functional defects, where a program can execute normally and still violate API semantics.

The router should receive the violated invariant, its provenance, and whether the failure was reproduced across valid API sequences. A likely workflow is to reflect on a localized, documentation-backed violation; replan when several independent invariants indicate a flawed approach; and escalate ambiguous candidates that still require developer confirmation. Evaluate this by replaying reintroduced library bugs and measuring confirmed fixes, false recovery cycles, escalation rate, and cost. This test matters because LISA’s candidates are not proofs of bugs, while CodeRescue’s formal guarantee controls expected cost rather than solve rate.

### Sources
- [CodeRescue: Budget-Calibrated Recovery Routing for Coding Agents](../Inbox/2026-07-21--coderescue-budget-calibrated-recovery-routing-for-coding-agents.md): A calibrated CodeRescue operating point exceeded always-escalate solve rate while using 35% of its mean recovery cost.
- [LLM-Based Invariant Testing for Software Functional Bugs](../Inbox/2026-07-21--llm-based-invariant-testing-for-software-functional-bugs.md): LISA generates API sequences and invariants and reports findings as candidates requiring developer confirmation.

## Controlled evaluation of semantic repository retrieval under code messiness
Engineering teams buying semantic repository retrieval should test whether it reduces incidental navigation work or compensates for genuinely harder program logic. JetBrains Context reports large maximum reductions in turns, latency, and execution cost, but the published excerpt does not separate task scale from repository presentation. Spaghetti Architect independently controls intrinsic problem size and incidental code messiness while preserving executable semantics, providing the missing experimental design.

Construct paired repositories from the same generated programs at several messiness levels, then run identical agent tasks with and without semantic indexing. Measure success, retrieved-file precision, turns, latency, and cost while holding intrinsic scale fixed; repeat by increasing intrinsic scale at fixed presentation. If retrieval gains appear mainly on messy variants, teams can target indexing at legacy codebases rather than treating it as a general capability upgrade. The result should remain scoped to synthetic repositories until repeated on production code, because Spaghetti Architect has not established that its messiness axis changes model accuracy and JetBrains’ figures are author-reported maxima.

### Sources
- [JetBrains Context: Repository Intelligence for Coding Agents](../Inbox/2026-07-21--jetbrains-context-repository-intelligence-for-coding-agents.md): JetBrains reports reductions of up to 68% in agent turns, 59% in latency, and 48% in execution cost across its evaluations.
- [Spaghetti Architect: A Contamination-Resistant, By-Construction-Labelled, Multi-Language Code Dataset Generator](../Inbox/2026-07-21--spaghetti-architect-a-contamination-resistant-by-construction-labelled-multi-language-code-dataset-generator.md): Spaghetti Architect generates oracle-checked programs in five languages with independently controlled intrinsic size and incidental messiness.
