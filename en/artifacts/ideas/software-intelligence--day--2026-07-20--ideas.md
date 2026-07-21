---
kind: ideas
granularity: day
period_start: '2026-07-20T00:00:00'
period_end: '2026-07-21T00:00:00'
run_id: 2235a8e7-5004-4de7-ac96-d6857d8a5bad
status: succeeded
topics:
- coding agents
- software quality
- test coverage
- context management
- verification
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-quality
- topic/test-coverage
- topic/context-management
- topic/verification
language_code: en
pass_output_id: 341
pass_kind: trend_ideas
upstream_pass_output_id: 340
upstream_pass_kind: trend_synthesis
---

# Verification-aware cleanup of coding-agent work

## Summary
Coding-agent cleanup should preserve the evidence needed to merge a change, not merely its passing status. The most useful changes are to make patch minimization coverage-aware, protect explicit obligations during context pruning, and reuse abandoned repair hypotheses to target tests before discarding the associated code.

## Coverage-preserving minimization of agent-authored pull requests
Maintainers reviewing agent-authored pull requests could run trajectory-guided minimization only under a broader acceptance check: a removal must keep the test suite green, preserve or improve diff coverage, and retain links between stated requirements and executable evidence. TRIM currently accepts a smaller patch when execution tests still pass, but field data show that existing tests exercise only 61.5% of changed Java lines and 27.0% of changed Python lines. A passing suite can therefore authorize deletion without showing that the remaining change is adequately tested. VNVSpec supplies a practical representation for the missing condition by linking requirements, tests, and verdicts in CI.

The cheapest check is an offline replay on completed agent pull requests: compare ordinary TRIM with the expanded acceptance rule and inspect disagreements, especially removals involving tests, error handling, or requirement-linked files. This would establish whether stronger evidence checks materially change the minimized patch before adding another merge gate.

### Sources
- [TRIM: Reducing AI-Generated CodeSlop via Agent Trajectory Minimization](../Inbox/2026-07-20--trim-reducing-ai-generated-codeslop-via-agent-trajectory-minimization.md): TRIM removes 17.8%–32.9% of redundant patch content by accepting smaller candidates whose execution tests still pass.
- [Test Coverage Analysis of Agentic Pull Requests](../Inbox/2026-07-20--test-coverage-analysis-of-agentic-pull-requests.md): Existing tests covered 61.5% of changed Java lines and 27.0% of changed Python lines across the analyzed agent-generated pull requests.
- [Integrating High-Level Requirements to Low-Level Tests with Machine-Readable V&V Specifications](../Inbox/2026-07-20--integrating-high-level-requirements-to-low-level-tests-with-machine-readable-v-v-specifications.md): VNVSpec represents requirements, test links, and verification evidence in a machine-readable traceability graph that runs in CI.

## Protected requirement lines in coding-agent context pruning
Teams running coding agents from detailed repository instructions should mark requirement statements, acceptance criteria, and checker failures as non-prunable context. SWE-Pruner Pro shows that line-level removal of tool output can cut token use substantially, but its relevance signal is learned from the model’s hidden states. The white-box audit study shows why a second constraint is needed: a few omitted requirements invalidated otherwise nearly complete artifacts, while an explicit 24-item checklist passed 10 of 10 runs compared with 5 of 10 for a generic self-check. A pruner should therefore optimize token reduction only after preserving lines tied to an external checklist or machine-readable requirement identifier.

Evaluate the change by adding protected-line masks to a pruning replay and reporting both token savings and requirement-level completion, rather than benchmark success alone. The audit task’s fixed checks offer a small initial test, although its context-length result was limited to one model-task pair and should not be treated as universal.

### Sources
- [SWE-Pruner Pro: The Coder LLM Already Knows What to Prune](../Inbox/2026-07-20--swe-pruner-pro-the-coder-llm-already-knows-what-to-prune.md): SWE-Pruner Pro derives line-level pruning decisions from backbone hidden states and reports token reductions of up to 39.4% while largely preserving benchmark quality.
- [How Agent Skills Fail under Long Contexts: A White-Box Study in Code Auditing](../Inbox/2026-07-20--how-agent-skills-fail-under-long-contexts-a-white-box-study-in-code-auditing.md): A detailed 24-check list passed 10/10 audit runs versus 5/10 for a generic self-check; the study cautions that the observed long-context failure was task-dependent.
- [Integrating High-Level Requirements to Low-Level Tests with Machine-Readable V&V Specifications](../Inbox/2026-07-20--integrating-high-level-requirements-to-low-level-tests-with-machine-readable-v-v-specifications.md): VNVSpec assigns explicit metrics and acceptance criteria to requirements and connects them to tests and evidence.

## Trajectory-derived tests for discarded repair hypotheses
Coding-agent maintainers could use the repair trajectory twice: first to identify speculative edits and abandoned hypotheses, then to generate focused tests before those edits are removed from the final patch. TRIM finds that exploratory changes often survive after the correct repair is reached. Separately, pull-request analysis finds that error-handling additions are especially poorly exercised, with try/catch miss rates of 86.0% in Java and 81.0% in Python. Tool failures, temporary exception handling, and reverted conditions in the trajectory may expose precisely the boundary cases that the final patch’s tests omit.

A post-run step could extract touched branches, exception types, and failed commands from edits later classified as removable; generate tests against the minimized patch; and retain only tests that increase diff or mutation coverage. Replaying this on recorded trajectories would show whether discarded hypotheses yield more useful tests than tests generated from the final diff alone.

### Sources
- [TRIM: Reducing AI-Generated CodeSlop via Agent Trajectory Minimization](../Inbox/2026-07-20--trim-reducing-ai-generated-codeslop-via-agent-trajectory-minimization.md): Observed repair trajectories retain speculative edits, abandoned hypotheses, and temporary changes after the successful fix is found.
- [Test Coverage Analysis of Agentic Pull Requests](../Inbox/2026-07-20--test-coverage-analysis-of-agentic-pull-requests.md): Error-handling constructs had high test miss rates: try/catch lines reached 86.0% in Java and 81.0% in Python.
