---
source: arxiv
url: https://arxiv.org/abs/2606.19135v1
published_at: '2026-06-17T14:45:20'
authors:
- Linus Sander
- Habtom Kahsay Gidey
- Alexander Lenz
- Alois Knoll
topics:
- llm-agents
- agent-communication
- multi-agent-systems
- protocol-taxonomy
- interoperability
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# A Technical Taxonomy of LLM Agent Communication Protocols

## Summary
The paper classifies LLM agent communication protocols so developers and researchers can compare them by concrete technical choices. Its main claim is that current protocols are fragmented and will likely evolve into a federated, layered stack rather than one universal standard.

## Problem
- LLM multi-agent systems need common communication protocols so heterogeneous agents, tools, and data services can connect without hard-coded integrations.
- The protocol space is fragmented, with overlapping systems that are often not interoperable.
- This matters because distributed agent networks depend on reliable discovery, message structure, state handling, and schema agreement.

## Approach
- The authors build a taxonomy using the iterative method from Nickerson et al.
- They select 9 actively maintained open-source protocols with public implementations and visible adoption.
- They run 5 taxonomy-building iterations: 3 empirical-to-conceptual and 2 conceptual-to-empirical.
- The final taxonomy has 5 dimensions: counterparty, payload, interaction state, discovery mechanism, and schema flexibility.
- They use the taxonomy to classify the sampled protocols and identify recurring protocol design patterns.

## Results
- The taxonomy contains 5 technical dimensions for classifying LLM agent communication protocols.
- The study analyzes 9 protocols that are open source, actively maintained, and have demonstrable adoption.
- All sampled agent-to-agent protocols combine hybrid payloads with session-state persistence.
- Most sampled protocols support multiple predefined schemas.
- 2 protocols negotiate schemas at runtime, which the authors treat as evidence of movement toward greater schema flexibility.
- Decentralized discovery is rare in the sample, and the authors identify privacy and policy enforcement as open research gaps.

## Link
- [https://arxiv.org/abs/2606.19135v1](https://arxiv.org/abs/2606.19135v1)
