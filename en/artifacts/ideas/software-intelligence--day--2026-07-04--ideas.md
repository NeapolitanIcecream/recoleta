---
kind: ideas
granularity: day
period_start: '2026-07-04T00:00:00'
period_end: '2026-07-05T00:00:00'
run_id: 2e196e0c-dcc5-45f0-928c-3f3f6d838479
status: succeeded
topics:
- AI agents
- agent security
- LLM budgets
- browser testing
- local inference
- agentic desktops
tags:
- recoleta/ideas
- topic/ai-agents
- topic/agent-security
- topic/llm-budgets
- topic/browser-testing
- topic/local-inference
- topic/agentic-desktops
language_code: en
pass_output_id: 303
pass_kind: trend_ideas
upstream_pass_output_id: 302
upstream_pass_kind: trend_synthesis
---

# Agent Execution Boundaries

## Summary
Agent teams can add concrete operating controls at the places where failures become expensive: pre-call cost reservations for LLM requests, deterministic authorization before RAG chunks or tool calls reach a model, and a narrow Windows benchmark for out-of-core local inference on consumer GPU hardware.

## Pre-call LLM spend reservations for autonomous agent runs
Platform engineers running LLM gateways can add a budget decision before every provider request in an agent run. The practical shape is a gateway hook, sidecar, or SDK middleware that estimates worst-case cost from current input tokens, the effective output cap, and a versioned price table, then reserves that amount atomically across scopes such as run, user, and key. After the call, it commits actual usage and releases the unused reserve.

This targets the cost pattern that ordinary monthly or per-key budgets miss: an agent loop that resends accumulated context and can cross 50K input tokens by step 20. The agent also needs machine-readable budget state. Headers and RFC 9457 problem-detail errors can tell the agent when to choose a cheaper model, cut context, or stop cleanly. A useful first test is to replay real agent traces with parallel branches, missing price metadata, and growing context, then measure added latency, blocked calls, and dollars reserved versus dollars spent.

### Sources
- [RFC: Stopping runaway AI agent spend with atomic budget reservations](../Inbox/2026-07-04--rfc-stopping-runaway-ai-agent-spend-with-atomic-budget-reservations.md): Summarizes the RFC design: pre-call estimated spend, atomic reservation, scopes, budget-state headers, and lack of evaluation results.
- [RFC: Stopping runaway AI agent spend with atomic budget reservations](../Inbox/2026-07-04--rfc-stopping-runaway-ai-agent-spend-with-atomic-budget-reservations.md): Describes the agent loop cost mechanism, including accumulated context and a 50K-token call by step 20.
- [RFC: Stopping runaway AI agent spend with atomic budget reservations](../Inbox/2026-07-04--rfc-stopping-runaway-ai-agent-spend-with-atomic-budget-reservations.md): Lists the budget authority behavior: reserve before provider calls, fail closed on unknown prices, and expose budget state for agent adaptation.

## Human-to-agent authorization records for RAG and tool workflows
Teams adding RAG and tool use to support workflows can build the identity path as a required part of every request. The retriever should attach access metadata to chunks, authenticate the user, filter retrieved chunks through fine-grained authorization, and send only authorized text to the model. Tool calls need the same treatment through MCP with OAuth 2.1 or through ordinary APIs with tokens and gateway controls.

Agent workflows need separate records for the human user, the agent actor, the delegated scope, and the action taken. A support desk flow can split work across limited sub-agents, issue short-lived signed JWTs with delegation claims, and log the actor, delegator, human user, role, and scope for each operation. A small validation set should include restricted documents, expired credentials, and a delegated agent trying to call a tool outside its scope.

### Sources
- [AI Authentication and Authorization](../Inbox/2026-07-04--ai-authentication-and-authorization.md): Summarizes the article’s pattern for RAG filtering, MCP or API tool access, separate agent identities, short-lived credentials, and audit logs.
- [AI Authentication and Authorization](../Inbox/2026-07-04--ai-authentication-and-authorization.md): Explains the need to maintain a chain of identity from the authorizing human through every agent action.
- [AI Authentication and Authorization](../Inbox/2026-07-04--ai-authentication-and-authorization.md): States that RAG should filter documents before they reach the model.
- [AI Authentication and Authorization](../Inbox/2026-07-04--ai-authentication-and-authorization.md): Gives the concrete RAG implementation pattern: chunk access metadata, user claims, and filtering through fine-grained authorization.

## Windows benchmark lane for out-of-core 70B local inference
Developers evaluating local inference on consumer GPUs can add a dedicated benchmark lane for Kortex on Windows 11 before selecting a runtime for oversized GGUF models. The relevant test is narrow: a machine with a 20 GB GPU, enough RAM, one or two NVMe drives, and a 70B quantized model that exceeds VRAM. Compare Kortex with llama.cpp partial offload on the same prompt, context size, and decoding settings, then record tokens per second, output match, drive layout, and GPU residency plan.

Kortex reports Llama-3.3-70B Q4_K_M at 1.95 tokens per second on a Radeon RX 7900 XT 20 GB system, compared with 0.21 tokens per second for llama.cpp b9860 Vulkan with 30 of 80 layers offloaded on the same hardware. The current adoption boundary is clear: the streaming path is Windows-only, there is no HTTP server or multi-turn REPL, and Linux streaming has not been tested. That points to an evaluation and batch-inference path first, with service integration left for a later build.

### Sources
- [Out-of-core LLM inference engine written from scratch in Rust](../Inbox/2026-07-04--out-of-core-llm-inference-engine-written-from-scratch-in-rust.md): Summarizes Kortex’s out-of-core design, reported 70B result, llama.cpp comparison, correctness checks, and current limits.
- [Out-of-core LLM inference engine written from scratch in Rust](../Inbox/2026-07-04--out-of-core-llm-inference-engine-written-from-scratch-in-rust.md): States the Windows-only streaming path and the reported 70B performance on a 20 GB consumer GPU.
- [Out-of-core LLM inference engine written from scratch in Rust](../Inbox/2026-07-04--out-of-core-llm-inference-engine-written-from-scratch-in-rust.md): Explains the measured 1.95 tok/s result, the llama.cpp partial-offload bottleneck, and Kortex’s GPU-only compute with streamed weights.
