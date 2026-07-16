---
kind: ideas
granularity: day
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-12T00:00:00'
run_id: e47f27c6-bb3f-4a68-b74f-685e04019ec2
status: succeeded
topics:
- coding agents
- agent runtimes
- tool-use evaluation
- workflow security
- context compression
- CAD automation
tags:
- recoleta/ideas
- topic/coding-agents
- topic/agent-runtimes
- topic/tool-use-evaluation
- topic/workflow-security
- topic/context-compression
- topic/cad-automation
language_code: en
pass_output_id: 147
pass_kind: trend_ideas
upstream_pass_output_id: 146
upstream_pass_kind: trend_synthesis
---

# Agent Execution Integrity

## Summary
Agent teams can move faster by adding trace, state, and provenance checks around the places where agents already fail: coding runs, MCP tool workflows, and automation workflows that mix untrusted text with secrets or shell access.

## Prompt-provenance scans for agentic GitHub Actions and n8n workflows
Security teams should add a workflow check that traces whether attacker-controlled fields, such as GitHub issue comments, can reach an agent prompt that also has secrets, shell access, API tokens, or database tools. The useful output is a small path report: trigger event, transformed prompt fields, agent call, available tools, and the action that could leak data or execute commands.

JAW gives a concrete recipe for this check. It combines workflow path analysis, runtime prompt tracing with canary-marked inputs, capability checks, and payload evolution. In real GitHub Actions and n8n templates, it found 4,174 hijackable GitHub workflows and eight hijackable n8n templates, with reported impacts including credential leakage and arbitrary command execution. A first internal version can run on pull requests that change workflow YAML, reusable actions, n8n templates, or agent permissions, then block only the cases where untrusted prompt content and privileged tools meet in the same execution path.

### Sources
- [Comment and Control: Hijacking Agentic Workflows via Context-Grounded Evolution](../Inbox/2026-05-11--comment-and-control-hijacking-agentic-workflows-via-context-grounded-evolution.md): JAW reports the workflow analysis method, the 4,174 hijackable GitHub workflows, eight n8n templates, and impacts such as credential leakage and command execution.
- [Comment and Control: Hijacking Agentic Workflows via Context-Grounded Evolution](../Inbox/2026-05-11--comment-and-control-hijacking-agentic-workflows-via-context-grounded-evolution.md): The paper describes static path-feasibility analysis, dynamic prompt-provenance analysis, and capability analysis for end-to-end exploitation.

## Branchable execution traces for coding-agent review and recovery
Coding-agent runners should record model calls, tool calls, file writes, and environment actions as a typed execution trace that a reviewer or supervising agent can inspect and fork. The practical feature is a “resume from here” control on failed or risky runs: keep the exact prior state, branch before the bad command, try a different continuation, and preserve the trace for review.

Shepherd shows that this can be fast enough for live use. On Terminal-Bench 2.0 images up to 5.8 GB, it reports 134–143 ms forks, while full filesystem copy reaches 53,462 ms on the largest image. Replay also reaches about a 95% prompt-cache hit rate on Claude Haiku 4.5 across eight tasks. The same paper reports a live supervisor raising CooperBench pair-coding pass rate from 28.8% to 54.7%. A small adoption test is to wrap one internal coding-agent runner, record every filesystem and tool effect, and measure how often reviewers can repair a failed run by branching before the first wrong state change.

### Sources
- [Shepherd: A Runtime Substrate Empowering Meta-Agents with a Formalized Execution Trace](../Inbox/2026-05-11--shepherd-a-runtime-substrate-empowering-meta-agents-with-a-formalized-execution-trace.md): Shepherd records agent execution as a typed Git-like trace and reports fork, replay, and supervision results.
- [Shepherd: A Runtime Substrate Empowering Meta-Agents with a Formalized Execution Trace](../Inbox/2026-05-11--shepherd-a-runtime-substrate-empowering-meta-agents-with-a-formalized-execution-trace.md): The abstract describes cheap forking and replay of past agent states with prompt-cache reuse.

## State-diff regression tests for MCP tool agents
Teams exposing many tools through MCP should test agents against seeded stateful sandboxes and score the final environment state, not only whether the agent produced a plausible answer. The regression suite should include changing permissions, carts, chat histories, accounts, API failures, and nested state. Each task should report completion, misbehavior, skipped checks, and recovery after tool errors.

ComplexMCP is a useful template because it tests more than 300 tools across seven stateful sandboxes and uses rule-based comparison between the agent’s final nested environment state and the ground truth. The best reported model, Gemini-3-Flash, reaches 55.31% success, while humans using the same interface reach 93.61%. The failure modes are directly actionable for product tests: tool retrieval saturation, skipped environment checks, and failure rationalization after errors. A cheap check is to convert ten high-value customer workflows into seeded MCP tasks and fail releases when a model changes the wrong state or stops after a recoverable tool error.

### Sources
- [ComplexMCP: Evaluation of LLM Agents in Dynamic, Interdependent, and Large-Scale Tool Sandbox](../Inbox/2026-05-11--complexmcp-evaluation-of-llm-agents-in-dynamic-interdependent-and-large-scale-tool-sandbox.md): ComplexMCP reports the MCP sandbox design, success rates for Gemini-3-Flash and humans, final-state evaluation, and failure modes.
- [ComplexMCP: Evaluation of LLM Agents in Dynamic, Interdependent, and Large-Scale Tool Sandbox](../Inbox/2026-05-11--complexmcp-evaluation-of-llm-agents-in-dynamic-interdependent-and-large-scale-tool-sandbox.md): The abstract describes over 300 tools, seven stateful sandboxes, dynamic environment states, and unpredictable API failures.
