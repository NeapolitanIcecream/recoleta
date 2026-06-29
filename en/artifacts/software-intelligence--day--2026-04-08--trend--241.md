---
kind: trend
trend_doc_id: 241
granularity: day
period_start: '2026-04-08T00:00:00'
period_end: '2026-04-09T00:00:00'
topics:
- software-agents
- repository-engineering
- evaluation
- code-generation
- agent-infrastructure
run_id: materialize-outputs
aliases:
- recoleta-trend-241
tags:
- recoleta/trend
- topic/software-agents
- topic/repository-engineering
- topic/evaluation
- topic/code-generation
- topic/agent-infrastructure
language_code: en
pass_output_id: 42
pass_kind: trend_synthesis
---

# Software-agent work is getting more explicit about specs, checks, and whole-repository tasks

## Overview
The day’s strongest evidence favors software agents that write down the task, act at repository scale, and pass concrete checks. ReCodeAgent and REAgent post measurable gains by adding planning or requirements before generation. CLI-Tool-Bench and SWD-Bench tighten evaluation around end-to-end behavior, repository understanding, and downstream usefulness.

## Clusters

### Specification and verification sit inside the agent loop
Repository-scale coding work has stronger evidence when the system carries its own plan and checks its own output. ReCodeAgent splits translation into analysis, planning, translation, and validation, then reports 99.4% compilation success and 86.5% test pass rate across 118 projects and four language pairs. REAgent uses the same broad pattern for issue fixing: build a structured requirement first, score it with generated tests, then refine it until the requirement is good enough to drive a patch. The reported gain is 9.17% to 24.83% in resolved issues over baselines. The common point is simple: repository agents improve when specification and verification are first-class steps inside the loop, not cleanup added at the end.

#### Evidence
- [ReCodeAgent: A Multi-Agent Workflow for Language-agnostic Translation and Validation of Large-scale Repositories](../Inbox/2026-04-08--recodeagent-a-multi-agent-workflow-for-language-agnostic-translation-and-validation-of-large-scale-repositories.md): Multi-agent planning and validation deliver strong repository-level translation results.
- [REAgent: Requirement-Driven LLM Agents for Software Issue Resolution](../Inbox/2026-04-08--reagent-requirement-driven-llm-agents-for-software-issue-resolution.md): Requirement generation and assessment improve issue-resolution outcomes.

### Benchmarks are testing full repository tasks, not just code fragments
Benchmark design is getting closer to what developers actually ask agents to do. CLI-Tool-Bench starts from an empty workspace and grades complete CLI tools by command behavior, output, and file-system effects. Even the best models stay below 43% overall success. SWD-Bench scores documentation by whether it helps answer development questions, locate feature files, and recover implementation details across a repository. It also reports a downstream 20% improvement in SWE-Agent issue solving when better documentation is used. The period’s evaluation work is less interested in polished local outputs and more interested in whether an agent can complete a repository task that another system can verify.

#### Evidence
- [Evaluating LLM-Based 0-to-1 Software Generation in End-to-End CLI Tool Scenarios](../Inbox/2026-04-08--evaluating-llm-based-0-to-1-software-generation-in-end-to-end-cli-tool-scenarios.md): 0-to-1 CLI benchmark measures end-to-end repository construction and finds low success rates.
- [Evaluating Repository-level Software Documentation via Question Answering and Feature-Driven Development](../Inbox/2026-04-08--evaluating-repository-level-software-documentation-via-question-answering-and-feature-driven-development.md): Documentation benchmark ties quality to repository QA tasks and downstream agent performance.

### Agent infrastructure is becoming a product surface
Product work is packaging the agent runtime itself as the deliverable. Claude Managed Agents exposes a hosted loop with tools, code execution, web access, persistent sessions, and server-side event history. That puts runtime control, steering, and environment setup on the platform side instead of the application team. The evidence here is product documentation, not benchmark data, so the claim is narrower than the research papers. Still, it fits the day’s theme: teams want agent behavior that arrives with execution, state, and control surfaces already wired in.

#### Evidence
- [Claude Managed Agents Overview](../Inbox/2026-04-08--claude-managed-agents-overview.md): Managed runtime product bundles execution, tools, state, and steering for autonomous agents.
