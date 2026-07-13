---
kind: ideas
granularity: day
period_start: '2026-07-09T00:00:00'
period_end: '2026-07-10T00:00:00'
run_id: 6f1fd830-7243-4016-b889-ab3387b57be5
status: succeeded
topics:
- agent harnesses
- test-time adaptation
- long-horizon evaluation
- repository verification
- small language models
tags:
- recoleta/ideas
- topic/agent-harnesses
- topic/test-time-adaptation
- topic/long-horizon-evaluation
- topic/repository-verification
- topic/small-language-models
language_code: en
pass_output_id: 315
pass_kind: trend_ideas
upstream_pass_output_id: 314
upstream_pass_kind: trend_synthesis
---

# Agent Workflow Optimization and Validation

## Summary
Agent teams can cut inference cost by adapting the control program to a bounded workflow, improve deployed behavior through trace-driven harness edits, and diagnose long runs with checkpoint-level grading. Each change needs an executable promotion test because proxy signals, workload diversity, and timeouts can distort headline success rates.

## Harness adaptation gate for small-model workflow migration
Teams running repetitive workflows such as budget approval should test a small language model with a task-specific harness before committing to frontier-model inference costs. The harness optimizer can inspect failed trajectories and edit instructions, tool availability, context selection, hooks, and orchestration loops. In the reported budget-approval task, an adapted Gemma-4-26B-A4B setup reached 98.3% accuracy, up from 75.0% with the default harness and above the 97.3% reported for Gemini-3.1-Pro. Across 21 task-model pairs, adaptation improved 16 and closed the measured gap on seven.

A practical adoption gate is a replay set drawn from one high-volume workflow, split by instance diversity and operational edge cases. Compare the frontier agent, the small model with its current harness, and the adapted small-model agent on task accuracy, contract violations, latency, and cost per completed case. Keep a frontier-model fallback for cases outside the validated workflow. The study found larger gains on repetitive tasks and stronger small models, so a diverse holdout is needed before using the savings estimate for capacity planning.

### Evidence
- [Better Harnesses, Smaller Models: Building 90% Cheaper Agents via Automated Harness Adaptation](../Inbox/2026-07-09--better-harnesses-smaller-models-building-90-cheaper-agents-via-automated-harness-adaptation.md): Reports the optimizer design, results across 21 task-model pairs, the budget-approval comparison, cost reduction, and limits tied to task diversity and base-model capability.
- [Better Harnesses, Smaller Models: Building 90% Cheaper Agents via Automated Harness Adaptation](../Inbox/2026-07-09--better-harnesses-smaller-models-building-90-cheaper-agents-via-automated-harness-adaptation.md): Describes the concrete budget-approval harness changes: a plan skeleton, reduced tool set, and enforced constraints through hooks.

## Shadow-mode harness updates from unlabeled execution traces
Agent operators can run candidate harness edits in shadow mode using traces already produced by SQL, coding, and data workflows. Each branch should record prompts, tool calls, outputs, runtime errors, artifacts, and recovery decisions. A proposer edits the executable harness; a selector scores candidates with execution health, round-trip consistency, or public-test results. Promotion should require a separate labeled canary set because these proxies can select a worse branch.

TTHE shows the size of the possible gain with a frozen model: on DeepSeek-V4-Flash, BIRD rose from 12.0% to 50.0% and SWE-bench Verified from 20.0% to 35.0%. The same experiments found selection regret, judge errors, limited candidate coverage, and non-monotonic returns from larger search budgets. An initial deployment can therefore cap branches and compute, retain every code diff, and promote only when both proxy scores and canary outcomes improve. Rollback remains a normal code release because the adapted state is the harness program.

### Evidence
- [TTHE: Test-Time Harness Evolution](../Inbox/2026-07-09--tthe-test-time-harness-evolution.md): Details TTHE's branching, trace collection, proxy-based selection, benchmark gains, and documented selection limitations.
- [TTHE: Test-Time Harness Evolution](../Inbox/2026-07-09--tthe-test-time-harness-evolution.md): Defines the harness as executable code for context construction, tool use, verification, and failure recovery, and describes persistent test-time updates from unlabeled traces.

## Checkpoint-level grading for long-running terminal agents
Developers evaluating terminal agents should add executable graders for meaningful intermediate states: environment setup, artifact creation, test completion, schema validity, and final verification. Record reward by checkpoint alongside elapsed time, episode count, token use, retries, and the last verified state. This separates agents that stall early, make substantial progress, or finish the work but fail final validation.

Long-Horizon-Terminal-Bench found partial reward in 433 of 690 runs, including 180 runs at or above 0.5. Seventy-three runs scored between 0.75 and 0.95, compared with 30 full passes at the 0.95 threshold. Timeouts accounted for 79% of unresolved runs, while an average run consumed 9.9 million tokens, 231 episodes, and 85.3 minutes. A cheap first check is to decompose five representative internal tasks into weighted checkpoints and rerun the current agent under the existing time limit. The resulting traces will show whether engineering effort belongs in planning, state recovery, verification, or runtime budgeting.

### Evidence
- [Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Horizon Terminal Tasks with Dense Reward-Based Grading](../Inbox/2026-07-09--long-horizon-terminal-bench-testing-the-limits-of-agents-on-long-horizon-terminal-tasks-with-dense-reward-based-grading.md): Provides the partial-reward distribution, near-completion counts, timeout share, and average token, episode, and runtime measurements.
- [Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Horizon Terminal Tasks with Dense Reward-Based Grading](../Inbox/2026-07-09--long-horizon-terminal-bench-testing-the-limits-of-agents-on-long-horizon-terminal-tasks-with-dense-reward-based-grading.md): Describes the benchmark's fine-grained graded subtasks and dense intermediate rewards for incomplete long-horizon workflows.
