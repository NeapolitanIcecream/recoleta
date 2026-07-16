---
kind: trend
trend_doc_id: 956
granularity: day
period_start: '2026-05-11T00:00:00'
period_end: '2026-05-12T00:00:00'
topics:
- coding agents
- agent runtimes
- tool-use evaluation
- workflow security
- context compression
- CAD automation
run_id: materialize-outputs
aliases:
- recoleta-trend-956
tags:
- recoleta/trend
- topic/coding-agents
- topic/agent-runtimes
- topic/tool-use-evaluation
- topic/workflow-security
- topic/context-compression
- topic/cad-automation
language_code: en
pass_output_id: 146
pass_kind: trend_synthesis
---

# Agent systems need inspectable execution before they can carry more responsibility

## Overview
The strongest signal is that agents need inspectable execution and stricter task evidence. DuST uses execution-labeled candidate code as training data, Shepherd records live agent state for branching, and ComplexMCP shows tool agents still lag humans on stateful software work.

## Findings

### Execution feedback as training signal
DuST treats generated code samples as a source of pairwise supervision. The base model samples 64 candidate programs per problem, a sandbox labels each candidate as passing or failing, and mixed groups train the same model to rank correct programs above incorrect ones using Group Relative Policy Optimization (GRPO). The reward only scores ranking quality, yet generation improves.

On LiveCodeBench v6, Qwen3-30B-Thinking rises from 65.4% to 68.5% pass@1. Its judgment score rises from 70.1 to 76.3 NDCG, and Best-of-4 accuracy rises from 68.7% to 72.6%. The result gives a concrete recipe for reusing test-time scaling data after inference.

#### Sources
- [Primal Generation, Dual Judgment: Self-Training from Test-Time Scaling](../Inbox/2026-05-11--primal-generation-dual-judgment-self-training-from-test-time-scaling.md): Summary gives DuST data construction, GRPO ranking objective, and LiveCodeBench gains.

### Traceable runtime state for meta-agents
Shepherd makes an agent execution a typed object that another agent can inspect, fork, replay, and modify. Every model call, tool call, file write, and environment action becomes an event in a Git-like trace. Forking uses copy-on-write isolation for the process and filesystem, so alternative continuations can start from the same past state.

The reported systems numbers are practical enough to matter for agent search. On Terminal-Bench 2.0 images up to 5.8 GB, Shepherd forks in 134–143 ms. Full filesystem copy reaches 53,462 ms on the largest image. Replay also reaches about a 95% prompt-cache hit rate on Claude Haiku 4.5 across eight tasks.

#### Sources
- [Shepherd: A Runtime Substrate Empowering Meta-Agents with a Formalized Execution Trace](../Inbox/2026-05-11--shepherd-a-runtime-substrate-empowering-meta-agents-with-a-formalized-execution-trace.md): Summary describes Shepherd's typed trace, fork/replay operations, and performance results.

### Stateful tool and CAD benchmarks expose narrow competence
ComplexMCP tests agents through the Model Context Protocol (MCP) with more than 300 tools and seven stateful sandboxes. The best reported model, Gemini-3-Flash, reaches 55.31% success across 47 tasks. Human users reach 93.61% through the same interface. The failures include tool retrieval saturation, skipped environment checks, and poor recovery after errors.

BenchCAD applies a similar pressure to multimodal design work. It contains 17,900 execution-verified CadQuery programs across 106 industrial part families. The benchmark separates image-to-code generation, visual question answering, code question answering, and edit tasks. Models read CAD code better than they infer the same details from renders: top Code QA is about 0.838, while Vision QA peaks at 0.587.

#### Sources
- [ComplexMCP: Evaluation of LLM Agents in Dynamic, Interdependent, and Large-Scale Tool Sandbox](../Inbox/2026-05-11--complexmcp-evaluation-of-llm-agents-in-dynamic-interdependent-and-large-scale-tool-sandbox.md): Summary reports MCP tool scale, stateful sandboxes, human and model success rates, and failure modes.
- [BenchCAD: A Comprehensive, Industry-Standard Benchmark for Programmatic CAD](../Inbox/2026-05-11--benchcad-a-comprehensive-industry-standard-benchmark-for-programmatic-cad.md): Summary reports BenchCAD dataset size, tasks, and QA results.

### Workflow context and compressed memory need stronger checks
JAW shows that agent workflows can be hijacked when attacker-controlled content enters prompts connected to tokens, tools, or secrets. It combines workflow path analysis, prompt-provenance tracing, capability checks, and payload evolution. The paper reports 4,174 hijackable GitHub workflows and eight hijackable n8n templates, with impacts including credential leakage and command execution.

The context problem also appears inside coding agents. An In-Context Autoencoder (ICAE) compresses observations into continuous memory tokens and lets agents run longer trajectories, but detail loss hurts real issue resolution. On SWE-bench Verified, the compressed system solves 7 of 500 issues, below the uncompressed Qwen3-8B baseline at 19 and far below the supervised fine-tuned model at 86.

#### Sources
- [Comment and Control: Hijacking Agentic Workflows via Context-Grounded Evolution](../Inbox/2026-05-11--comment-and-control-hijacking-agentic-workflows-via-context-grounded-evolution.md): Summary gives JAW method, affected workflow types, counts, and reported impacts.
- [On Problems of Implicit Context Compression for Software Engineering Agents](../Inbox/2026-05-11--on-problems-of-implicit-context-compression-for-software-engineering-agents.md): Summary reports ICAE setup and SWE-bench Verified resolution drop.
