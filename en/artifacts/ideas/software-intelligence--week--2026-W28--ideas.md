---
kind: ideas
granularity: week
period_start: '2026-07-06T00:00:00'
period_end: '2026-07-13T00:00:00'
run_id: 3d21636f-4222-4a17-b775-92bc877b0fbc
status: succeeded
topics:
- coding agents
- agent harnesses
- software verification
- long-horizon evaluation
- repository workflows
- context engineering
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-harnesses
- topic/software-verification
- topic/long-horizon-evaluation
- topic/repository-workflows
- topic/context-engineering
language_code: en
pass_output_id: 323
pass_kind: trend_ideas
upstream_pass_output_id: 322
upstream_pass_kind: trend_synthesis
---

# Executable Feedback for Coding-Agent Workflows

## Summary
Coding-agent teams can improve repository work by requiring executable bug reproductions, testing harness changes against held-out tasks, and supervising test generation with live coverage signals. Each change can be piloted with a fixed model and measured against the current workflow.

## Fail-to-pass reproduction tests at issue intake
Maintainers using repair agents should add a reproduction stage before patch generation. The stage would localize the suspected bug, retrieve repository context, generate a test, and execute it on the affected revision. ReProAgent reproduced 58.43% of SWT-bench-lite issues and 70.30% of SWT-bench-verified issues at an average cost of $0.14 per case; its tests also improved downstream repair performance.

A practical pilot can use 50 closed issues with known fixes. Accept a generated test only when it fails on the pre-fix commit and passes after the recorded fix, then compare patch success, maintainer review time, and false reproductions with the existing repair-agent workflow. Teams that clear this check can require an executable reproduction artifact in the issue before an autonomous repair run begins.

### Evidence
- [ReProAgent: Tool-Augmented Multi-Stage Agentic Generation of Bug Reproduction Tests from Issue Reports](../Inbox/2026-07-10--reproagent-tool-augmented-multi-stage-agentic-generation-of-bug-reproduction-tests-from-issue-reports.md): Reports ReProAgent's reproduction rates, runtime validation, average cost, and downstream repair benefit.
- [ReProAgent: Tool-Augmented Multi-Stage Agentic Generation of Bug Reproduction Tests from Issue Reports](../Inbox/2026-07-10--reproagent-tool-augmented-multi-stage-agentic-generation-of-bug-reproduction-tests-from-issue-reports.md): Defines fail-to-pass tests as executable specifications that fail on buggy code and pass after the reference fix.

## Trace-driven harness trials with held-out repository checks
Teams operating coding agents should version the executable harness separately from the model and test proposed harness edits in a shadow runner. Each trial can replay recent execution traces, vary context construction, tool-use rules, verification steps, or recovery logic, and promote a candidate only after it passes held-out repository tasks and cost limits.

TTHE showed the size of this opportunity with frozen model weights: on DeepSeek-V4-Flash, SWE-bench Verified rose from 20.0% to 35.0%. Its documented selection regret and judge errors also show why deployment needs held-out checks. Long-Horizon-Terminal-Bench adds a useful evaluation design: grade executable subtasks throughout the run and record timeouts, since 79% of unresolved runs timed out. A low-cost trial would compare two harness versions on the same model, task set, token budget, and wall-clock limit, tracking final completion, checkpoint progress, regressions, and cost.

### Evidence
- [TTHE: Test-Time Harness Evolution](../Inbox/2026-07-09--tthe-test-time-harness-evolution.md): Describes executable harness adaptation, fixed-model gains, and failures caused by imperfect proxy-based selection.
- [Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Horizon Terminal Tasks with Dense Reward-Based Grading](../Inbox/2026-07-09--long-horizon-terminal-bench-testing-the-limits-of-agents-on-long-horizon-terminal-tasks-with-dense-reward-based-grading.md): Reports dense subtask grading, low long-horizon completion, resource use, and timeout prevalence.

## Coverage-aware supervision for agent-generated unit tests
Java teams using coding agents for unit-test generation can add a supervisor that reads current line coverage, branch coverage, missed complexity, and token cost after each iteration. The supervisor chooses whether the agent should continue normally, receive program-analysis output for uncovered paths, or stop. This targets premature completion on easy paths and limits repeated calls that add no coverage.

Scate used this pattern with a contextual bandit and an MCP program-analysis tool. Against unsupervised agent baselines, it reported 32.3% higher line coverage and 30.9% higher branch coverage with Gemini CLI, plus gains of 6.0% and 5.9% with Claude Code. A repository pilot should hold the model and token budget constant, then compare branch coverage, mutation score, generated-test maintenance failures, and cost per accepted test. The paper does not report absolute final coverage or statistical significance, so those checks should precede wider adoption.

### Evidence
- [SCATE: Learning to Supervise Coding Agents for Cost-Effective Test Generation](../Inbox/2026-07-09--scate-learning-to-supervise-coding-agents-for-cost-effective-test-generation.md): Details the coverage-aware supervisor, its action choices, and relative coverage improvements across two coding agents.
- [SCATE: Learning to Supervise Coding Agents for Cost-Effective Test Generation](../Inbox/2026-07-09--scate-learning-to-supervise-coding-agents-for-cost-effective-test-generation.md): Documents premature agent termination on complex branches and the human monitoring burden the supervisor addresses.
