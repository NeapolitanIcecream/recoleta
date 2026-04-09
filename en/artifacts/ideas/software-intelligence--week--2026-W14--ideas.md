---
kind: ideas
granularity: week
period_start: '2026-03-30T00:00:00'
period_end: '2026-04-06T00:00:00'
run_id: e30d1f13-3c1f-4ef7-8316-e547eaa9439c
status: succeeded
topics:
- coding-agents
- evaluation
- runtime-verification
- context-control
- software-engineering
tags:
- recoleta/ideas
- topic/coding-agents
- topic/evaluation
- topic/runtime-verification
- topic/context-control
- topic/software-engineering
language_code: en
pass_output_id: 19
pass_kind: trend_ideas
upstream_pass_output_id: 18
upstream_pass_kind: trend_synthesis
---

# Executable agent workflow benchmarks

## Summary
This week points to three practical workflow changes around coding agents: build offline replay benches from real production sessions, insert tool-output pruning into agent loops to cut repeated context load, and evaluate agents across dependent PR sequences instead of one task at a time. All three directions rely on executable checks such as stable tests, preserved repository state, and measurable token or latency effects.

## Internal replay benchmark for coding-agent changes in monorepos
Teams evaluating coding agents on production repositories can build an internal replay bench from real assistant sessions, landed diffs, and stable test subsets. ProdCodeBench shows the recipe in enough detail to copy: keep the original developer prompt, back out the landed change from current repo state, then grade candidate agents against repeated fail-to-pass and pass-to-pass test runs. The useful part is not only realism. It is speed. The paper positions this as a faster offline check for model swaps, harness changes, and infrastructure updates that would otherwise wait on slow A/B tests. A practical first version is narrow: one service, one language-heavy area of the monorepo, and only prompts that already have stable relevant tests. If that slice can reproduce relative model rankings across three reruns without heavy manual triage, it becomes a routine gate for agent releases.

### Evidence
- [ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents](../Inbox/2026-04-02--prodcodebench-a-production-derived-benchmark-for-evaluating-ai-coding-agents.md): Production-derived benchmark built from real developer-agent sessions, with backed-out diffs and stable execution-based grading.
- [ProdCodeBench: A Production-Derived Benchmark for Evaluating AI Coding Agents](../Inbox/2026-04-02--prodcodebench-a-production-derived-benchmark-for-evaluating-ai-coding-agents.md): Explains why offline replay is useful for model and harness decisions when online A/B testing is slow and expensive.

## Tool-output pruning filter for coding-agent loops
Coding-agent teams can add a tool-output pruning step between shell or repository tools and the main model. Squeez gives a concrete target for that filter: keep only the smallest verbatim spans that answer the current subtask, and return nothing when the observation has no useful evidence. The reported numbers are good enough to justify a cheap deployment test. On a manually reviewed test set, the fine-tuned 2B model keeps recall at 0.86 and F1 at 0.80 while removing 92% of tokens, and it handles negative cases much better than a larger zero-shot model. This is useful in loops that reread logs, grep hits, stack traces, and file contents. A practical rollout is a sidecar CLI on piped tool output, with logging for how often the filter drops lines that later prove necessary. The paper does not show end-to-end task completion gains, so the first check should be token savings and step latency on debugging runs before claiming accuracy gains.

### Evidence
- [Squeez: Task-Conditioned Tool-Output Pruning for Coding Agents](../Inbox/2026-04-04--squeez-task-conditioned-tool-output-pruning-for-coding-agents.md): Defines task-conditioned tool-output pruning and reports strong line-level evidence retention under heavy compression.
- [Squeez: Task-Conditioned Tool-Output Pruning for Coding Agents](../Inbox/2026-04-04--squeez-task-conditioned-tool-output-pruning-for-coding-agents.md): States that the model can be inserted as a CLI filter on piped tool output in existing coding-agent stacks with minimal loop changes.

## Sequence-level evaluation for dependent pull-request chains
Teams using coding agents for multi-PR work can add a sequence-level acceptance check that runs after a chain of related changes, not only after each pull request. SWE-STEPS gives a direct reason: isolated evaluation overstates success by up to 20 percentage points, and agents that clear single-PR checks can still leave behind higher cognitive complexity and more technical debt. The immediate workflow change is to group dependent tasks, preserve repository state across the run, and score both new-function tests and regression tests at the sequence level. A small pilot does not need a new benchmark release. A team can mine a few chains of related merged PRs from one repository, replay them with the agent in order, and compare isolated pass rates against continuous-run outcomes. If the gap looks like the paper's reported 15% to 25% drop, the team has a concrete case for changing evaluation and rollout policy.

### Evidence
- [Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution](../Inbox/2026-04-03--beyond-isolated-tasks-a-framework-for-evaluating-coding-agents-on-sequential-software-evolution.md): Introduces sequential multi-PR evaluation with repository-health metrics and shows why isolated PR tests miss cumulative damage.
- [Beyond Isolated Tasks: A Framework for Evaluating Coding Agents on Sequential Software Evolution](../Inbox/2026-04-03--beyond-isolated-tasks-a-framework-for-evaluating-coding-agents-on-sequential-software-evolution.md): Reports up to 20-point performance inflation under isolated evaluation and repository-health degradation in continuous settings.
