---
source: hn
url: https://www.custodianlabs.io
published_at: '2026-07-19T22:57:48'
authors:
- sherryf123
topics:
- ai-agents
- code-intelligence
- automated-software-production
- privacy-preserving-ai
- retrieval-augmented-generation
- model-agnostic-infrastructure
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Show HN: Deploy AI agent in 5 lines of code

## Summary
Custodian Labs is a platform for deploying production AI agents with built-in PII controls, retrieval, model switching, and managed infrastructure. Its main value is reducing setup work while keeping sensitive data under application control.

## Problem
- Deploying an agent typically requires hosting, databases, vector search, model-provider integration, retry logic, and streaming support before application logic is written.
- Sending raw PII to an external model creates privacy and compliance risks, while removing PII can reduce context and response quality.

## Approach
- The platform reduces deployment to an SDK and API-key workflow, claiming that an agent can be running in production in under 10 minutes and in five lines of code.
- Its Guardian Layer detects configured PII entities, reports confidence scores, and supports three policies: transform PII into synthetic equivalents, mask it with typed labels, or detect it without changing the text.
- A one-line knowledge-base configuration provides retrieval-augmented generation and persistent document memory without direct embedding or vector-database setup.
- The agent logic remains unchanged when switching among OpenAI, Anthropic, Mistral, and local models; Custodian also abstracts hosting and database infrastructure.

## Results
- The excerpt reports no independent benchmarks, accuracy measurements, latency results, or baseline comparisons.
- The product claims deployment in under 10 minutes and implementation in five lines of code, but provides no reproducible test conditions.
- The documented starter tier includes 100,000 tokens and 1,000 requests; the higher starter tier includes 1 million tokens and 10,000 requests.
- The strongest concrete product claim is that PII can be handled before it reaches a model while preserving context through synthetic replacement, masking, or detection-only modes.
- The platform states that its foundations were commercialised with AUT Ventures and New Zealand Government funding, but the excerpt gives no details about the underlying academic research.

## Link
- [https://www.custodianlabs.io](https://www.custodianlabs.io)
