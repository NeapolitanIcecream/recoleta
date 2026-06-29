---
kind: ideas
granularity: day
period_start: '2026-04-18T00:00:00'
period_end: '2026-04-19T00:00:00'
run_id: 2c820f02-ea9f-4551-985d-436f1ebff98d
status: succeeded
topics:
- agent-ops
- evaluation
- runtime-security
- developer-tooling
tags:
- recoleta/ideas
- topic/agent-ops
- topic/evaluation
- topic/runtime-security
- topic/developer-tooling
language_code: en
pass_output_id: 79
pass_kind: trend_ideas
upstream_pass_output_id: 78
upstream_pass_kind: trend_synthesis
---

# Agent Reliability Controls

## Summary
The clearest near-term work is adding control layers around coding agents and their evaluation. The evidence supports three concrete moves: put shared-agent traffic behind a scheduling proxy, add prompt-perturbation checks to any LLM judge used for software decisions, and scan repositories for missing agent-facing documentation and safeguards before rolling out heavier AI workflows.

## HTTP scheduling proxy for parallel coding agents
A local proxy for coding agents is now a practical build, not a research sketch. HiveMind puts scheduling and retry between existing agents and the model API, with no agent-side code changes, and reports failure rates falling from 72%–100% under contention to 0%–18% across seven scenarios. In the replayed 11-agent case, full HiveMind reached 0% failure; removing retry pushed failure back to 63.6%. That points to a concrete product surface for teams already running parallel code generation, repair, or test-writing jobs on shared model quotas: admission control, retry with jitter, backpressure, token budgets, and per-job priority in one proxy. The first users are platform and developer-experience teams that already see agents die on 429s, 502s, and connection resets. A cheap validation check is simple: replay one busy internal workflow through a proxy and compare completion rate, dead-agent token waste, and wall-clock time against direct API access.

### Evidence
- [HiveMind: OS-Inspired Scheduling for Concurrent LLM Agent Workloads](../Inbox/2026-04-18--hivemind-os-inspired-scheduling-for-concurrent-llm-agent-workloads.md): Quantifies failure reductions under contention and identifies retry as the most important primitive.
- [HiveMind: OS-Inspired Scheduling for Concurrent LLM Agent Workloads](../Inbox/2026-04-18--hivemind-os-inspired-scheduling-for-concurrent-llm-agent-workloads.md): Confirms zero agent-code changes and frames the proxy as a transparent insertion point.

## Prompt-perturbation harness for LLM code judges
Teams that use LLM judges for patch ranking or candidate selection need a perturbation test before they trust the scores. The audit in Bias in the Loop keeps the code fixed and changes only the judge prompt, then shows large verdict swings from superficial prompt cues. The clearest number is on unit test generation, where distraction drops a GPT-based judge from 77.46% to 62.51% accuracy. The paper also recommends concrete controls such as A/B order swapping and controlled prompt perturbations. That supports a small evaluation harness for software teams and benchmark authors: run the same judged comparisons across prompt variants, record sensitivity and test-retest consistency, and fail any judge setup that changes rankings too easily. The first adopters are groups using judge models to filter expensive executions, rank repair candidates, or report leaderboard results. A low-cost check is to rerun one internal benchmark with order swaps and a few prompt perturbations, then measure how often the winner changes.

### Evidence
- [Bias in the Loop: Auditing LLM-as-a-Judge for Software Engineering](../Inbox/2026-04-18--bias-in-the-loop-auditing-llm-as-a-judge-for-software-engineering.md): Reports prompt-induced accuracy swings and recommends bias sensitivity reporting with explicit controls.
- [Bias in the Loop: Auditing LLM-as-a-Judge for Software Engineering](../Inbox/2026-04-18--bias-in-the-loop-auditing-llm-as-a-judge-for-software-engineering.md): Shows the mechanism: prompt artifacts can alter rankings even when the code is unchanged.

## Repository readiness scanner with draft pull requests
Repository preparation for coding agents is concrete enough to turn into a scanner plus draft-PR workflow. Workstream scores repositories across agent configuration, documentation, CI/CD quality, code structure, and security, then generates missing files and suggested fixes. Its strongest measured result is repository readiness improvement: the authors report a score increase from 48 to 98 on their own repository and from 41.6 to 73.7 on an external repository after applying recommendations. The fixes are plain engineering artifacts such as AGENTS.md, CLAUDE.md, GEMINI.md, ARCHITECTURE.md, CONTRIBUTING.md, SECURITY.md, pre-commit hooks, Dependabot, and more test coverage. This is useful for teams whose agents fail because repositories do not expose enough operating context or guardrails. A sensible first deployment is a read-only scanner in CI that opens a draft PR with missing agent-facing files and setup changes, then tracks whether agent task completion or review quality improves after the patch lands.

### Evidence
- [Workstream: A Local-First Developer Command Center for the AI-Augmented Engineering Workflow](../Inbox/2026-04-18--workstream-a-local-first-developer-command-center-for-the-ai-augmented-engineering-workflow.md): Describes the readiness scanner, categories, and measured repository score improvements.
- [Workstream: A Local-First Developer Command Center for the AI-Augmented Engineering Workflow](../Inbox/2026-04-18--workstream-a-local-first-developer-command-center-for-the-ai-augmented-engineering-workflow.md): Confirms automated gap-filling and draft PR generation as part of the workflow.
