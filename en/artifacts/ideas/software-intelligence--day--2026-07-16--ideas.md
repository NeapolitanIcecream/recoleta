---
kind: ideas
granularity: day
period_start: '2026-07-16T00:00:00'
period_end: '2026-07-17T00:00:00'
run_id: 9d46ea63-5d8b-4b80-8ed0-226063df495c
status: succeeded
topics:
- agent reliability
- evidence gating
- coding agents
- dynamic tools
- domain evaluation
tags:
- recoleta/ideas
- topic/agent-reliability
- topic/evidence-gating
- topic/coding-agents
- topic/dynamic-tools
- topic/domain-evaluation
language_code: en
pass_output_id: 331
pass_kind: trend_ideas
upstream_pass_output_id: 330
upstream_pass_kind: trend_synthesis
---

# Execution evidence tied to changing dependencies, tools, and artifacts

## Summary
Agent controls should bind successful execution to the external state that made it possible: package origin and version, tool schema, domain workflow, and non-code artifacts. The most useful near-term changes are narrow release and completion gates that replay real workflows and invalidate evidence when those inputs change.

## Version-bound release gates for tool-using agent workflows
Agent-platform release engineers should make a successful workflow receipt identify not only the source commit, but also every package source and version and the exact MCP server schema used during execution. Package-install experiments found that agents commonly accepted untrusted registries, while MCPEvol-Bench measured 13.7% and 14.4% task-performance declines for two frontier models after tool evolution. Proof-or-Stop shows how lifecycle evidence can be rejected when it is stale or detached from tracked state, but its current evaluation does not establish coverage of changing external tools.

A release gate could replay a small set of high-value workflows against both pinned and candidate dependency/tool versions, run deterministic package provenance checks before installation, and issue a receipt over the code commit, registry identity, dependency lock, MCP schema, and test outputs. Any change to those inputs would invalidate the prior receipt. The cheapest useful check is to mutate one registry URL and one MCP parameter in an existing release suite and verify that the gate blocks reuse of the old evidence and localizes the failed step.

### Sources
- [Setup Complete, Now You Are Compromised: Weaponizing Setup Instructions Against AI Coding Agents](../Inbox/2026-07-16--setup-complete-now-you-are-compromised-weaponizing-setup-instructions-against-ai-coding-agents.md): Source-based package attacks were missed across ecosystems; a deterministic check of package names, sources, and versions closed most of the observed gap.
- [MCPEvol-Bench: Benchmarking LLM Agent Performance Across Dynamic Evolutions of MCP Servers](../Inbox/2026-07-16--mcpevol-bench-benchmarking-llm-agent-performance-across-dynamic-evolutions-of-mcp-servers.md): GPT-5.4 and Claude-Sonnet-4-6 lost 13.7% and 14.4% task performance on evolved MCP servers.
- [Proof-or-Stop: Don't Trust the Agent, Trust the Evidence -- Loop Engineering for Verifiable Evidence-Gated Lifecycle Control](../Inbox/2026-07-16--proof-or-stop-don-t-trust-the-agent-trust-the-evidence-loop-engineering-for-verifiable-evidence-gated-lifecycle-control.md): The tested lifecycle gate produced zero false-done outcomes in 10 scenarios and rejected 18 receipt-tampering classes, with evaluation limited to one model family and a self-hosted corpus.

## Artifact-complete closure checks for AI/ML maintenance issues
Maintainers of AI/ML repositories should prevent an issue from being marked resolved until the workflow records which prompts, datasets, model settings, dependencies, runtime configuration, and source files were inspected or changed, then attaches verification appropriate to each affected artifact. In a study of four AI/ML projects, 28 of 64 AI/ML issues required changes outside production code. StructureClaw separately found that requiring a linked, executable chain of models, validation records, solver outputs, checks, and reports raised mean workflow success from 56.8% to 88.6% in its structural-engineering benchmark.

The practical change is an issue template and closure gate that builds an artifact-impact manifest during diagnosis, carries artifact hashes and execution conditions into repeated or statistical tests, and refuses closure when an affected artifact has no current verification record. This extends executable evidence chains to maintenance work where a passing code test can coexist with an unchanged prompt, dataset, or runtime configuration. A low-cost pilot can apply the manifest retrospectively to recently closed model-behavior issues and measure how often the recorded fix omits an artifact later identified in the pull request or reproduction steps.

### Sources
- [Rethinking Issue Resolution for AI/ML Systems](../Inbox/2026-07-16--rethinking-issue-resolution-for-ai-ml-systems.md): The qualitative study found cross-stage experimentation and coordinated changes across datasets, prompts, and model configurations in 100 issues from four projects.
- [StructureClaw: Traceable LLM Agents and an Executable Benchmark for Structural Engineering Workflows](../Inbox/2026-07-16--structureclaw-traceable-llm-agents-and-an-executable-benchmark-for-structural-engineering-workflows.md): Mean success increased from 56.8% to 88.6% when the benchmark required the governed, artifact-centered workflow.
- [Proof-or-Stop: Don't Trust the Agent, Trust the Evidence -- Loop Engineering for Verifiable Evidence-Gated Lifecycle Control](../Inbox/2026-07-16--proof-or-stop-don-t-trust-the-agent-trust-the-evidence-loop-engineering-for-verifiable-evidence-gated-lifecycle-control.md): Proof-or-Stop binds lifecycle transitions to fresh evidence over exact tracked source state, while explicitly not claiming semantic correctness.

## Payment integration regression suites across API and tool evolution
Payment SDK teams supplying coding-agent skills should release each skill with executable regression cases for signature verification, asynchronous notifications, idempotency, refunds, and business-state consistency, then rerun those cases across old and candidate API or MCP tool versions. Alipay-PIBench found that an official integration skill improved mean rubric pass rate by 10.31 percentage points, but MCPEvol-Bench shows that tool additions and modifications can disrupt previously successful agent plans. A skill can therefore improve initial implementation while silently becoming unsafe as the connected interface evolves.

The build change is to version the skill, tool schema, and domain rubric together. Deterministic end-to-end checks should control release decisions; any LLM-judged properties, such as product fit or semantic state consistency, should be calibrated against fresh human labels for the changed integration rather than inherited from the prior version. Kaleidoscope’s pilot is too small to validate this design broadly, but it provides a concrete calibration method and warns that combining several rubric dimensions in one judge prompt degrades performance.

### Sources
- [Alipay-PIBench: A Realistic Payment Integration Benchmark for Coding Agents](../Inbox/2026-07-16--alipay-pibench-a-realistic-payment-integration-benchmark-for-coding-agents.md): Across six models and 18 tasks, the official skill improved mean rubric pass rate by 10.31 percentage points; advanced checks covered idempotency, abnormal transactions, refund safeguards, and fund safety.
- [MCPEvol-Bench: Benchmarking LLM Agent Performance Across Dynamic Evolutions of MCP Servers](../Inbox/2026-07-16--mcpevol-bench-benchmarking-llm-agent-performance-across-dynamic-evolutions-of-mcp-servers.md): Tool evolution increased planning and reasoning failures, with additions and modifications producing the largest losses.
- [Project Kaleidoscope: Contextual, Human-Aligned Evaluation for Real-World AI Applications](../Inbox/2026-07-16--project-kaleidoscope-contextual-human-aligned-evaluation-for-real-world-ai-applications.md): Kaleidoscope calibrates application-specific automated judges against human-reviewed labels; its evidence is an early three-week pilot across four use cases.
