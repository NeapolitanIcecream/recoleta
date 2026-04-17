---
kind: ideas
granularity: day
period_start: '2026-04-08T00:00:00'
period_end: '2026-04-09T00:00:00'
run_id: ead7a913-d224-4dbe-aa9c-41958ae9d654
status: succeeded
topics:
- software-agents
- repository-engineering
- evaluation
- code-generation
- agent-infrastructure
tags:
- recoleta/ideas
- topic/software-agents
- topic/repository-engineering
- topic/evaluation
- topic/code-generation
- topic/agent-infrastructure
language_code: en
pass_output_id: 43
pass_kind: trend_ideas
upstream_pass_output_id: 42
upstream_pass_kind: trend_synthesis
---

# Repository Task Validation

## Summary
The clearest near-term work is adding explicit specification and verification steps around repository agents, then testing them with end-to-end repository tasks instead of local code checks. The evidence supports three concrete moves: draft structured requirements before issue fixing, package repository migration around planning and validation checkpoints, and evaluate 0-to-1 code generation with black-box CLI behavior tests from an empty workspace.

## Structured issue requirements before repository patch generation
Repository issue agents need a requirement-writing step before they attempt a patch. REAgent gives a concrete pattern: turn the issue and repository context into a structured requirement with background, reproduction steps, expected behavior, root cause, modification location, and success criteria; generate tests from that requirement; then refine the requirement when the tests expose conflict, omission, or ambiguity. The reported gain is large enough to justify building this as a separate product layer for teams already using SWE-bench-style issue agents: 9.17% to 24.83% more resolved issues across three benchmarks, with average improvement of 17.40%.

A practical build is a repo-connected triage tool that opens every incoming bug or feature request by drafting the requirement record first, showing missing fields to the developer, and only then handing the task to the patch agent. The first users are teams with high issue volume and uneven ticket quality, where missing reproduction steps and unclear success criteria waste agent runs. A cheap check is simple: take a sample of your own unresolved issues, add the requirement record and test-generation loop, and compare patch acceptance and rerun count against the current flow.

### Evidence
- [REAgent: Requirement-Driven LLM Agents for Software Issue Resolution](../Inbox/2026-04-08--reagent-requirement-driven-llm-agents-for-software-issue-resolution.md): REAgent reports requirement generation, requirement scoring with generated tests, iterative refinement, and 9.17% to 24.83% gains in resolved issues.
- [REAgent: Requirement-Driven LLM Agents for Software Issue Resolution](../Inbox/2026-04-08--reagent-requirement-driven-llm-agents-for-software-issue-resolution.md): The paper states that repository-level issue resolution remains far below function-level performance, which supports demand for a requirements layer.

## Repository migration workflow with explicit planning and validation
Repository migration tools can now be sold as planned translation plus validation, not just code conversion. ReCodeAgent shows that whole-repository translation improves when analysis, planning, translation, and validation are split into distinct steps and tied to repository-aware checks. The validator does more than run existing tests: it looks for coverage gaps, generates extra tests for uncovered functions, and sends repair reports back into the loop. On 118 projects across four language pairs, the system reports 99.4% compilation success and 86.5% test pass rate, with large drops when Analyzer, Planning, or Validator are removed.

That supports a concrete service for teams moving codebases across languages: ingest the source repository, produce a target-project design and dependency-aware implementation plan, then keep a visible validation ledger for compile status, translated-test status, and newly generated test coverage. Migration buyers care about auditability and rollback points more than raw code output. A useful first trial is a narrow migration queue inside one engineering org, measured by compile success, human rework hours, and the share of translated modules that pass repository tests without manual repair.

### Evidence
- [ReCodeAgent: A Multi-Agent Workflow for Language-agnostic Translation and Validation of Large-scale Repositories](../Inbox/2026-04-08--recodeagent-a-multi-agent-workflow-for-language-agnostic-translation-and-validation-of-large-scale-repositories.md): ReCodeAgent describes the four-agent workflow and reports 99.4% compilation success and 86.5% test pass rate across 118 projects.

## Black-box CLI generation harness for empty-workspace agent evals
Teams evaluating coding agents need a black-box repository test harness that checks command behavior and file-system effects from an empty workspace. CLI-Tool-Bench is useful here because it measures a real user-facing task: can the agent build a complete CLI tool from a natural-language spec, with no scaffold, and produce the right outputs and files when commands run. Current top models stay below 43% overall success, and the paper reports common failure patterns such as monolithic repositories and infinite generation loops.

This points to an internal eval product for agent teams shipping code generation features. Start each run in a blank container, feed in a requirement, the `--help` interface, and one verified example per command class, then compare return code, stdout, and file-system side effects against an oracle implementation. The same harness can also catch regressions in planning quality, repo layout, and termination behavior that unit tests miss. If a team already generates small apps or CLIs from prompts, this is a low-cost way to find where the agent still breaks before users do.

### Evidence
- [Evaluating LLM-Based 0-to-1 Software Generation in End-to-End CLI Tool Scenarios](../Inbox/2026-04-08--evaluating-llm-based-0-to-1-software-generation-in-end-to-end-cli-tool-scenarios.md): CLI-Tool-Bench defines empty-workspace CLI generation and black-box evaluation over return code, stdout, and file-system side effects, with top models below 43% success.
- [Evaluating LLM-Based 0-to-1 Software Generation in End-to-End CLI Tool Scenarios](../Inbox/2026-04-08--evaluating-llm-based-0-to-1-software-generation-in-end-to-end-cli-tool-scenarios.md): The paper reports monolithic code structures and infinite generation loops as observed failure modes, which a black-box harness can surface.
