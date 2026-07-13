---
source: hn
url: https://www.iroh.computer/blog/mesh-llm
published_at: '2026-07-11T22:38:57'
authors:
- tionis
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- agent-network
- multi-agent-software-engineering
- human-ai-interaction
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Mesh LLM: distributed AI computing on iroh

## Summary
Mesh LLM pools GPUs across trusted iroh-connected machines and exposes them through one OpenAI-compatible local API. It can run models locally, route requests to peers, or pipeline models that exceed a single machine's memory.

## Problem
- Hosted LLMs limit control over model versions, data location, hardware, privacy, and operating cost.
- Many teams own separate GPUs that cannot run larger models together as one system.

## Approach
- Each machine runs an iroh endpoint identified by a public key, using authenticated QUIC connections with NAT traversal and relay fallback.
- A gossip layer manages peer admission, trust, version compatibility, model discovery, and routing.
- Requests run locally, route to a peer with the model loaded, or split a model by layer ranges across pipeline stages on multiple machines.
- A plugin runtime exposes model and service capabilities through MCP, HTTP, inference, and mesh events while presenting a standard API at `http://localhost:9337/v1`.

## Results
- The catalog includes more than 40 models, ranging from 0.5B-parameter models that fit on laptops to a 235B-parameter mixture-of-experts model.
- The software package is about 18 MB and supports public or private mesh deployments.
- Two iroh relays in different regions provide fallback connectivity when direct peer connections fail.
- No latency, throughput, cost, reliability, or model-quality benchmark results are provided in the excerpt.
- The strongest demonstrated claim is functional: several modest machines can pipeline a model that no single machine can hold, while standard OpenAI clients continue using the local API.

## Link
- [https://www.iroh.computer/blog/mesh-llm](https://www.iroh.computer/blog/mesh-llm)
