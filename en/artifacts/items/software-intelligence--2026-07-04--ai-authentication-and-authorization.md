---
source: hn
url: https://fusionauth.io/articles/ai/ai-authentication-authorization
published_at: '2026-07-04T23:10:55'
authors:
- mooreds
topics:
- ai-authentication
- authorization
- rag-security
- mcp
- agent-security
- identity-management
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# AI Authentication and Authorization

## Summary
The article argues that AI systems should inherit authority from a human identity and enforce access with deterministic checks. It covers RAG, tool access through MCP or APIs, and multi-agent workflows in a banking support example.

## Problem
- RAG systems can leak restricted documents if retrieval sends unauthorized chunks to the model before access checks run.
- AI tools and agents can update records, read files, call external services, and schedule meetings, so each action needs a clear user, agent identity, permission, and audit record.
- Prompt-only controls are unsafe for access control because the model may hallucinate or improvise while the identity layer must return a fixed yes-or-no decision.

## Approach
- Authenticate the human user through an identity provider, then carry user claims into RAG, tool, and agent requests.
- For RAG, store access metadata on document chunks, run vector retrieval, filter results through fine-grained authorization, and send only authorized chunks to the LLM.
- For tools, use MCP with OAuth 2.1 authorization code flow, or use existing APIs with access tokens, API keys, and gateway controls.
- For agents, give each agent its own identity, split work across limited-scope sub-agents, and use signed JWTs with delegation claims to preserve the human-to-agent chain of identity.
- Use audit logs, short-lived credentials, entity grants, and cleanup of workflow-specific agent entities to reduce stale access.

## Results
- The article provides no benchmark evaluation, accuracy metric, latency number, security test result, or production incident comparison.
- It organizes the guidance around 3 AI use cases: RAG, tool use through MCP or APIs, and agentic systems.
- The agent example splits a banking workflow into 4 agents: a coordinator, document agent, business service agent, and calendar agent.
- The JWT example uses a 300-second token lifetime and an `act` claim aligned with OAuth Token Exchange semantics in RFC 8693.
- The audit log example records a concrete action where a document agent gathered 4 documents from a folder, with actor, delegator, human user, role, and scope fields.

## Link
- [https://fusionauth.io/articles/ai/ai-authentication-authorization](https://fusionauth.io/articles/ai/ai-authentication-authorization)
