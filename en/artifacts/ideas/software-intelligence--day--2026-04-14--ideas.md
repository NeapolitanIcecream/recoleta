---
kind: ideas
granularity: day
period_start: '2026-04-14T00:00:00'
period_end: '2026-04-15T00:00:00'
run_id: 2c820f02-ea9f-4551-985d-436f1ebff98d
status: succeeded
topics:
- coding-agents
- evaluation
- repository-context
- multi-agent-workflows
- code-editing
tags:
- recoleta/ideas
- topic/coding-agents
- topic/evaluation
- topic/repository-context
- topic/multi-agent-workflows
- topic/code-editing
language_code: en
pass_output_id: 71
pass_kind: trend_ideas
upstream_pass_output_id: 70
upstream_pass_kind: trend_synthesis
---

# Repository-grounded code review

## Summary
Current coding-agent work points to three concrete changes: add executable specification checks to pull-request review, add repository-context reasoning traces to evaluation, and route cross-file follow-up edits through IDE and language-server tools before broad model search. The common pattern is simple: repository evidence exposes failures that final patch scoring and local editing flows still miss.

## Pull request checks for executable preconditions and postconditions
Teams evaluating coding agents can add executable specification checks to their review path for repository tasks. CodeSpecBench shows why this matters: function-level spec generation reaches 47.0% pass rate, but repository-level performance on 500 SWE-bench Verified issues falls to 20.2% for the best model. The gap points to a concrete failure mode in production code review: an agent may produce a plausible patch without capturing the intended input constraints, state assumptions, or output guarantees.

A practical build is a CI step that asks the model for preconditions and postconditions on the functions touched by a pull request, runs them against existing and generated tests, and flags mismatches for reviewer inspection. This fits teams already using agent-written patches in Python services or libraries, because the output is executable and can be checked with the same test harnesses they trust today. A cheap pilot is a one-week trial on bug-fix PRs in one repository: track how often generated specs fail while the patch still looks acceptable in review, and whether those failures surface hidden semantic regressions earlier than existing tests.

### Evidence
- [CodeSpecBench: Benchmarking LLMs for Executable Behavioral Specification Generation](../Inbox/2026-04-14--codespecbench-benchmarking-llms-for-executable-behavioral-specification-generation.md): CodeSpecBench provides the repository-level spec-generation results, execution-based evaluation design, and the 20.2% repo pass-rate ceiling that supports adding spec checks to PR review.

## Repository-context input and output prediction suites for coding-agent evaluation
Repository benchmarks can stop relying on final patch success alone and add input and output prediction tasks built from live code paths. R²Eval shows how large the blind spot is when evaluation stays on short standalone snippets: average input-prediction accuracy drops from 81.23% on CRUXEval to 16.91% on real repository problems, and output prediction drops from 80.37% to 28.15%. The benchmark also keeps complex runtime objects intact by serializing compound and custom types, then deserializing predictions back into objects for test-based scoring.

That supports a concrete workflow change for model vendors, internal eval teams, and enterprises buying coding agents: add a small repository-context reasoning suite before expanding deployment. The suite does not need to be large. A few dozen traced methods from one production service, with serialized inputs and expected outputs, will show whether the model can follow project state, dependencies, and object-heavy APIs. The cheap check is to sample methods from recent incidents or flaky fixes and compare scores on those traces against current snippet-heavy evals. If the same model still looks strong only on the simple set, the deployment risk is already visible.

### Evidence
- [Evaluating LLMs Code Reasoning Under Real-World Context](../Inbox/2026-04-14--evaluating-llms-code-reasoning-under-real-world-context.md): R²Eval provides the real-repository input/output prediction setup, object serialization method, and the measured collapse from snippet benchmarks to repository-context reasoning.

## Tool-routed follow-up edits for cross-file changes
Cross-file editing assistants can improve acceptance by routing obvious structural edits through IDE and language-server tools before asking the model to search the codebase. TRACE gives a concrete pattern: detect whether the current change looks like a rename, signature update, clone update, or diagnose-fix case, call tools such as rename and def-use analysis to gather edit locations, then use the model for the remaining semantic edits. On 38K commits across 678 projects, this raises edit-location precision by 43.76%, recall by 9.96%, and edit-generation accuracy by 11.16% over prior systems. In interactive simulation it also reports 27.71% suggestion acceptance with lower time cost.

This is a build target for IDE teams and code-review automation vendors working on follow-up edits after an initial patch lands. The immediate product surface is narrow: a "propagate change" action after a developer edits one file, with tool-backed candidate locations shown before the model writes patches. A cheap validation run is to replay recent refactors and bug-fix commits from one repository and measure accepted suggestions on the second and third files touched in each change.

### Evidence
- [Learning Project-wise Subsequent Code Edits via Interleaving Neural-based Induction and Tool-based Deduction](../Inbox/2026-04-14--learning-project-wise-subsequent-code-edits-via-interleaving-neural-based-induction-and-tool-based-deduction.md): TRACE provides the tool-routing design, the specific structural edit cases, and the cross-project gains in location precision, generation accuracy, time cost, and suggestion acceptance.
