---
source: arxiv
url: https://arxiv.org/abs/2605.05287v1
published_at: '2026-05-06T17:59:21'
authors:
- Francisco Javier Arceo
- Varsha Prasad Narsing
topics:
- agentic-rag
- multitenant-security
- access-control
- tool-use
- server-side-orchestration
- enterprise-ai
relevance_score: 0.64
run_id: materialize-outputs
language_code: en
---

# Securing the Agent: Vendor-Neutral, Multitenant Enterprise Retrieval and Tool Use

## Summary
The paper proposes a multitenant agentic RAG design that keeps tenant data out of prompts unless the user is authorized to see it. It implements the design in OGX, an OpenAI-compatible open-source system for server-side retrieval, tool use, and multi-turn agent execution.

## Problem
- Enterprise RAG and agent systems often rank documents by semantic or keyword relevance, so a user can retrieve another tenant’s data when that data matches the query.
- Client-side agent loops can skip retrieval filters, call unauthorized tools, or carry leaked context across turns.
- The problem matters because enterprises need shared infrastructure for cost control, but shared retrieval, tools, and model serving can expose confidential or regulated data.

## Approach
- The core mechanism is simple: tag every document chunk with tenant and access metadata at ingestion, then apply authorization checks before and during retrieval.
- Retrieval uses ABAC gating with resource-level checks before search and chunk-level metadata filters after search; backends with predicate pushdown can apply tenant filters inside vector search.
- Tool execution, conversation state, audit logging, and policy checks run on the server, so clients choose the task but cannot control the security-critical loop.
- The LLM serving layer is shared across tenants because the design isolates the retrieved context before it enters the prompt.
- OGX implements this as OpenAI-compatible APIs for responses, vector stores, search, tools, conversations, safety, telemetry, and Kubernetes deployment.

## Results
- In the paper’s reported evidence, ungated retrieval leaks cross-tenant data in 98–100% of cross-tenant probes.
- With ABAC gating, Cross-Tenant Leakage Rate and Authorization Violation Rate drop to 0% in the shown evaluation, for both client-side and server-side orchestration modes.
- The evaluation uses 6 experiments over a 2×2 matrix: client-side vs. server-side orchestration crossed with ungated vs. ABAC-gated retrieval.
- The setup includes 3 tenants, 300 documents total, 100 documents per tenant, about 512 tokens per document, 300 authorized queries, 300 cross-tenant probes, and 90 prompt-injection probes.
- The paper claims negligible overhead from ABAC gating, but the provided excerpt does not include an exact latency or throughput number.
- Shared inference reduces model endpoint cost scaling from O(N·M) to O(M), where N is tenant count and M is model endpoint count.

## Link
- [https://arxiv.org/abs/2605.05287v1](https://arxiv.org/abs/2605.05287v1)
