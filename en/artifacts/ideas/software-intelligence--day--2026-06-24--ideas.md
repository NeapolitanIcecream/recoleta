---
kind: ideas
granularity: day
period_start: '2026-06-24T00:00:00'
period_end: '2026-06-25T00:00:00'
run_id: 3b4b5a17-cd1c-4d94-ae11-d44f2b7c16ce
status: succeeded
topics:
- coding agents
- software engineering
- agent harnesses
- tool reliability
- code benchmarks
- test migration
- agent governance
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/agent-harnesses
- topic/tool-reliability
- topic/code-benchmarks
- topic/test-migration
- topic/agent-governance
language_code: en
pass_output_id: 281
pass_kind: trend_ideas
upstream_pass_output_id: 280
upstream_pass_kind: trend_synthesis
---

# Coding Agent Reliability Harnesses

## Summary
Coding-agent adoption is ready for narrower harness work: separated bug-fix roles, recovery tests around unreliable tools, and intent-based test migration for teams with overlapping library behavior. The evidence is strongest where the papers report executable evaluations, measured regressions, or working pipelines with real defects found.

## Separated explorer, patch editor, and validator workflow for GitHub issue fixes
Teams using coding agents on repository issues can split the fix loop into three roles: an Explorer that finds files, functions, and call chains; a Patch Editor that changes code; and a Validator that writes and runs reproduction and regression tests. The useful control is the boundary between patching and validation. i cat-agent hides test code and assertions from the Patch Editor, while the agents pass structured events such as pass/fail results and suspicious statements.

This is a practical build for teams seeing agents pass weak self-written tests or lose track of long issue threads. Start with a small issue-quality gate: if a ticket names the file, function, fix strategy, and reproduction steps, send it directly to patching and validation; if it lacks those details, run exploration first. On SWE-bench Pro, i cat-agent with GPT-5.4-xhigh solved 67.4% of tasks, 8.3 percentage points above mini-SWE-agent with the same model, and the paper reports lower average per-instance cost than Claude Code on that benchmark.

### Sources
- [Unlocking Model Potentials Through Adaptive Multi-Agent Scaffolding for Efficient Issue Resolution](../Inbox/2026-06-24--unlocking-model-potentials-through-adaptive-multi-agent-scaffolding-for-efficient-issue-resolution.md): Summarizes i cat-agent's Explorer, Patch Editor, Validator roles, hidden validator assertions, issue-quality gate, and SWE-bench results.
- [Unlocking Model Potentials Through Adaptive Multi-Agent Scaffolding for Efficient Issue Resolution](../Inbox/2026-06-24--unlocking-model-potentials-through-adaptive-multi-agent-scaffolding-for-efficient-issue-resolution.md): Reports the 67.4% SWE-bench Pro result and cost comparison context.
- [Unlocking Model Potentials Through Adaptive Multi-Agent Scaffolding for Efficient Issue Resolution](../Inbox/2026-06-24--unlocking-model-potentials-through-adaptive-multi-agent-scaffolding-for-efficient-issue-resolution.md): Describes test overfitting and patch overfitting as failure modes in single-agent trajectories.

## Recoverable tool-failure tests for coding-agent tool calls
Agent teams should add a local fault-injection test set for the tools their coding agents call: repository search, package managers, CI logs, issue trackers, internal APIs, and MCP servers. Each case should keep a valid recovery path, such as retrying after a timeout, using a fallback command, normalizing changed output, checking a second source, or resolving conflicting evidence.

ToolBench-X gives a concrete template. It injects Specification Drift, Invocation Error, Execution Failure, Output Drift, and Cross-source Conflict across executable multi-step tasks. No evaluated model reached 0.60 overall accuracy, and the best score was 0.513. After a failed tool response, agents often retried the same tool, but retry frequency did not track task accuracy. The useful metric is whether the agent diagnoses the hazard and chooses the right recovery action. A small internal version can run in CI against recorded tool traces and block agent rollout when recovery accuracy falls on common hazards.

### Sources
- [Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability](../Inbox/2026-06-24--beyond-function-calling-benchmarking-tool-using-agents-under-tool-environment-unreliability.md): Summarizes ToolBench-X task design, hazard types, model accuracy, retry behavior, and targeted recovery hint results.
- [Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability](../Inbox/2026-06-24--beyond-function-calling-benchmarking-tool-using-agents-under-tool-environment-unreliability.md): Defines ToolBench-X as executable multi-step tasks with five recoverable reliability hazards and valid recovery paths.
- [Beyond Function Calling: Benchmarking Tool-Using Agents under Tool-Environment Unreliability](../Inbox/2026-06-24--beyond-function-calling-benchmarking-tool-using-agents-under-tool-environment-unreliability.md): Explains real tool failures such as stale documentation, renamed fields, timeouts, incomplete returns, and conflicting evidence.

## Intent-based unit test migration across similar libraries
Maintainers porting behavior across similar libraries can use an intent-level migration pipeline for unit tests. The workflow is concrete: split source tests into smaller sub-tests, convert each one into a Test Description Language record, map the intent onto a target repository graph, gather constructors and dependencies, generate the target test, then run a verification pass.

This is most useful for libraries with overlapping domains and different APIs or languages, such as JSON, HTML, and Time libraries. IntentTester evaluated nine open-source projects in Java and Python. From 2,058 source tests, it produced 5,536 sub-tests and kept 3,257 after filtering. It generated 2,776 syntactically correct tests with 85% correctness, compared with 51% for MUT and 43% for METALLICUS. The generated tests exposed 25 real defects, including stack overflow and null dereference bugs. A team can trial the method on one source library and one target library, then measure executable migrated tests and newly failing behavior checks.

### Sources
- [IntentTester: Intent-Driven Multi-agent Framework for Cross-Library Test Migration](../Inbox/2026-06-24--intenttester-intent-driven-multi-agent-framework-for-cross-library-test-migration.md): Summarizes IntentTester's TDL conversion, repository graph mapping, verification loop, evaluation scale, correctness rates, and defects found.
- [IntentTester: Intent-Driven Multi-agent Framework for Cross-Library Test Migration](../Inbox/2026-06-24--intenttester-intent-driven-multi-agent-framework-for-cross-library-test-migration.md): States the cross-library and cross-language migration approach using language-agnostic Test Description Language and repository graph context.
- [IntentTester: Intent-Driven Multi-agent Framework for Cross-Library Test Migration](../Inbox/2026-06-24--intenttester-intent-driven-multi-agent-framework-for-cross-library-test-migration.md): Reports generated test counts, 85% correctness, 74% effectiveness, and previously unknown defects.
