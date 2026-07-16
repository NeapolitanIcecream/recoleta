---
kind: trend
trend_doc_id: 1072
granularity: day
period_start: '2026-05-19T00:00:00'
period_end: '2026-05-20T00:00:00'
topics:
- agent reliability
- code generation
- runtime verification
- multi-agent systems
- code model calibration
run_id: materialize-outputs
aliases:
- recoleta-trend-1072
tags:
- recoleta/trend
- topic/agent-reliability
- topic/code-generation
- topic/runtime-verification
- topic/multi-agent-systems
- topic/code-model-calibration
language_code: en
pass_output_id: 178
pass_kind: trend_synthesis
---

# Agent reliability is an engineering control problem

## Overview
This day’s strongest signal is runtime discipline. STORM, OpenComputer, and DIFFCODEGEN point to the same requirement: agents need current state, executable checks, and cheap validation around model output before teams trust longer autonomous work.

## Findings

### State and authority controls for agents
Several items treat a large language model (LLM) agent as one part of a controlled runtime. STORM rejects writes when an agent has read stale files, then returns fresh context so the agent can retry. The production-agent architecture paper makes the same point at the tool boundary: a model proposes, deterministic code verifies, accepted actions are committed, and rejected actions get typed feedback. Capframe gives a concrete Model Context Protocol (MCP) version of this idea with scoped capability tokens and deterministic policy checks for tool calls.

The shared concern is practical. Parallel agents can overwrite each other or act on old assumptions. Tool-using agents can receive too much authority. The strongest work in this group adds version checks, commit rules, denial receipts, and audit records around the model.

#### Sources
- [Multi-agent Collaboration with State Management](../Inbox/2026-05-19--multi-agent-collaboration-with-state-management.md): STORM uses shared workspace state, file version counters, stale-write rejection, and reports gains on Commit0-Lite and PaperBench.
- [A Methodology for Selecting and Composing Runtime Architecture Patterns for Production LLM Agents](../Inbox/2026-05-19--a-methodology-for-selecting-and-composing-runtime-architecture-patterns-for-production-llm-agents.md): The runtime architecture paper defines a proposer-verifier-commit-reject contract and audits failures at the model-to-action boundary.
- [Show HN: Capframe – capability tokens for AI agent tool calls](../Inbox/2026-05-19--show-hn-capframe-capability-tokens-for-ai-agent-tool-calls.md): Capframe maps MCP tool access, issues scoped capability tokens, and enforces deterministic runtime policy on tool calls.

### Verifiable agent evaluation
OpenComputer and AgentAtlas both argue for evaluation below the final success number. OpenComputer builds 1,000 desktop tasks across 33 applications and scores them with programmatic checks tied to real application state, including browser profiles, files, databases, and saved documents. That matters because screenshot scoring can miss hidden state errors.

AgentAtlas looks at the trajectory itself. It labels control decisions such as Act, Ask, Refuse, Stop, Confirm, and Recover, then shows that prompt format and evaluation axis can change model rankings. Its audit also finds that memory, state, and efficiency receive weak coverage in existing agent benchmarks. The evidence says agent evaluation needs task results plus trace-level checks.

#### Sources
- [OpenComputer: Verifiable Software Worlds for Computer-Use Agents](../Inbox/2026-05-19--opencomputer-verifiable-software-worlds-for-computer-use-agents.md): OpenComputer provides verifier-grounded desktop tasks, 33 applications, 1,000 tasks, and state-based scoring.
- [AgentAtlas: Beyond Outcome Leaderboards for LLM Agents](../Inbox/2026-05-19--agentatlas-beyond-outcome-leaderboards-for-llm-agents.md): AgentAtlas defines control and trajectory labels, audits 15 benchmarks, and reports axis-sensitive model rankings.

### Diagnostic feedback as an optimizer
optimize_anything broadens LLM-based search into a common loop: edit a text artifact, score it, pass diagnostic side information back to the proposer, and try another candidate. The same API is applied to prompts, code, agent structures, scheduling policies, CUDA kernels, and numerical solvers. The reported gains are strongest when evaluators return useful side information such as traces, profiler data, costs, or images.

DIFFCODEGEN applies a narrower form of runtime evidence to code selection. It samples multiple candidate programs, fuzzes inputs, compares observed behavior, clusters candidates, and returns the medoid of the largest behavior group. This avoids extra LLM calls after generation and reports much lower time and token use than prior test-time selection methods that need public tests or model-based judges.

#### Sources
- [optimize_anything: A Universal API for Optimizing any Text Parameter](../Inbox/2026-05-19--optimize-anything-a-universal-api-for-optimizing-any-text-parameter.md): optimize_anything uses evaluator scores plus side_info diagnostics and reports gains across agent architecture search, scheduling, CUDA, prompts, and coding-agent skills.
- [Code Generation by Differential Test Time Scaling](../Inbox/2026-05-19--code-generation-by-differential-test-time-scaling.md): DIFFCODEGEN selects candidates using fuzzing and behavioral clustering, with reported time and token savings over prior test-time scaling methods.

### Selective code automation
Two reliability papers focus on when code models should act. The defer-and-recover paper calibrates correctness scores, accepts outputs above a threshold, and sends uncertain cases to validation or recovery steps such as compiler checks, static analysis, prompt augmentation, and task decomposition. Its results show better Brier score and expected calibration error on MBPP+ and defect prediction, but also warn that no single uncertainty metric worked across tasks.

The input-adaptation paper tests a different control point. It rewrites or adjusts inputs at inference time when a validity score is low. Early results are clearest for vulnerability detection: CodeBERT improves from 63.36% accuracy to 76.75% with latent transformation, while existing uncertainty metrics remain weak error detectors. The lesson is narrow and useful: code automation needs task-specific confidence handling, not a generic confidence number.

#### Sources
- [When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions](../Inbox/2026-05-19--when-to-answer-and-when-to-defer-a-decision-framework-for-reliable-code-predictions.md): The defer-and-recover paper reports calibrated selective prediction and recovery paths for uncertain code outputs.
- [On-the-Fly Input Adaptation for Reliable Code Intelligence](../Inbox/2026-05-19--on-the-fly-input-adaptation-for-reliable-code-intelligence.md): The input-adaptation paper reports near-chance uncertainty metrics and accuracy gains from input or latent transformations on vulnerability detection.
