---
kind: ideas
granularity: day
period_start: '2026-05-01T00:00:00'
period_end: '2026-05-02T00:00:00'
run_id: ae19bbc9-e6b7-48b5-8bbb-d50eef5dbc9e
status: succeeded
topics:
- AI coding agents
- software engineering
- reward models
- agent orchestration
- reproducibility
- GPU serving
- developer tooling
tags:
- recoleta/ideas
- topic/ai-coding-agents
- topic/software-engineering
- topic/reward-models
- topic/agent-orchestration
- topic/reproducibility
- topic/gpu-serving
- topic/developer-tooling
language_code: en
pass_output_id: 123
pass_kind: trend_ideas
upstream_pass_output_id: 122
upstream_pass_kind: trend_synthesis
---

# Agent Workload Visibility

## Summary
AI coding agents now have enough local evidence to justify three concrete changes: recording prompt-to-edit traces during real development, testing scientific agents with claim-level reproduction tasks, and measuring agent serving by full task completion time. Each change targets a place where normal code metrics hide the cost of agent work.

## VS Code prompt-to-edit replay for AI-assisted code review
Engineering teams adopting Copilot, Cursor, Claude Code, or similar tools should add a lightweight trace layer to pilot projects: capture chat prompts, fine-grained edits, file saves, and shadow commits, then replay them alongside diffs during review or retro. The review pain is provenance. A pull request can show the final patch, but it usually cannot show which prompt caused a risky edit, which AI suggestion was discarded, or whether a developer spent a long session cycling through the same error.

RECAP gives a concrete implementation path. Its VS Code extension records Copilot chat JSON and shadow git changes, links text edit groups to diffs within a five-minute window, and labels edits as Copilot, human, partial match, unmatched, or likely external source. In a course deployment, it captured 2,034 prompts and 8,239 shadow-git commits across 406 work sessions. The useful first test for a software team is small: run this kind of capture on one AI-assisted project for two weeks, then inspect repeated error loops, AI edit share by session, and review comments tied to generated code.

### Sources
- [RECAP: An End-to-End Platform for Capturing, Replaying, and Analyzing AI-Assisted Programming Interactions](../Inbox/2026-05-01--recap-an-end-to-end-platform-for-capturing-replaying-and-analyzing-ai-assisted-programming-interactions.md): RECAP records Copilot chat, shadow git commits, prompt-to-edit links, replay timelines, AI edit share, and a course deployment with 2,034 prompts and 8,239 commits.
- [The Productivity-Reliability Paradox: Specification-Driven Governance for AI-Augmented Software Development](../Inbox/2026-05-01--the-productivity-reliability-paradox-specification-driven-governance-for-ai-augmented-software-development.md): The specification-governance paper identifies review load, churn, context limits, and reliability risk as adoption blockers for AI-generated code.

## Claim-level reproduction harnesses for scientific coding agents
Computational science groups should test coding agents on reproduced claims before using them as research assistants. A practical harness would package a paper claim, metadata, optional artifacts, required domain tools, and hidden expert reproduction steps. The agent would submit traces, logs, files, and a short report, with evaluation focused on whether the evidence supports the claim.

AutoMat shows why this check matters. Across 85 computational materials-science claims, the best tested setting reached a 54.1% success rate. Reproduction from paper text alone had near-zero success across systems, while artifact-based reproduction was easier. The failure mode is operational: incomplete procedures, method deviations, fragile execution, and missing domain choices. A lab can start with 10 recent internal claims, require agents to run in the same container or HPC environment used by researchers, and compare outputs with expert reproduction notes before trusting agent-generated scripts or post-processing.

### Sources
- [Can Coding Agents Reproduce Findings in Computational Materials Science?](../Inbox/2026-05-01--can-coding-agents-reproduce-findings-in-computational-materials-science.md): AutoMat evaluates 85 materials-science claims, keeps hidden expert reproduction steps, scores traces/logs/files/reports, and reports 54.1% best success with near-zero paper-only reproduction.
- [Can Coding Agents Reproduce Findings in Computational Materials Science?](../Inbox/2026-05-01--can-coding-agents-reproduce-findings-in-computational-materials-science.md): The paper reports low overall success and identifies incomplete procedures, methodological deviations, and execution fragility as main failure sources.

## Workflow-level latency measurement for coding-agent serving
Teams serving coding or browser agents on shared GPUs should measure cost and latency at the task level: one issue fix, one SWE-bench run, one browser task, or one full tool-using session. Per-request metrics such as time-to-first-token miss the idle gaps, tool calls, and KV-cache regeneration that users experience as waiting time.

SAGA gives a concrete systems test. Agent tasks often make 10 to 100 chained LLM calls separated by tool calls. In a SWE-bench measurement, 38% of execution time went to KV-cache regeneration, average GPU memory use was 42%, and end-to-end latency was 6.0x the inference-only baseline. SAGA keeps reusable KV cache through tool-call gaps and routes later steps back to the same worker. On 64 A100 GPUs, it cut task completion time by 1.73x on SWE-bench and 1.55x on WebArena versus vLLM with Automatic Prefix Caching, with about 30% lower peak throughput. The practical adoption check is an A/B run on the team’s own agent traces, comparing full task completion time, SLO attainment, GPU memory use, and throughput loss.

### Sources
- [SAGA: Workflow-Atomic Scheduling for AI Agent Inference on GPU Clusters](../Inbox/2026-05-01--saga-workflow-atomic-scheduling-for-ai-agent-inference-on-gpu-clusters.md): SAGA reports agent tasks with 10–100 chained calls, KV-cache regeneration costs, task-level scheduling, and completion-time gains on SWE-bench and WebArena.
- [SAGA: Workflow-Atomic Scheduling for AI Agent Inference on GPU Clusters](../Inbox/2026-05-01--saga-workflow-atomic-scheduling-for-ai-agent-inference-on-gpu-clusters.md): The paper explains why KV cache continuity across agent steps can consume gigabytes and why discarding cache adds latency overhead.
