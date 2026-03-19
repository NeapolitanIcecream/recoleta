---
source: hn
url: https://choosejoy.com.au
published_at: '2026-03-14T23:38:44'
authors:
- savvyllm
topics:
- ai-agents
- trust-network
- agent-discovery
- mcp
- decentralized-systems
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Show HN: Joy – Trust Network for AI Agents to Verify Each Other

## Summary
Joy is a decentralized discovery and trust network for AI agents and MCP servers, allowing agents to register, search, and vouch for one another. Its core goal is to provide a simple, verifiable trust layer for the agent ecosystem to improve discovery quality and collaboration safety.

## Problem
- AI agents and MCP servers lack a unified decentralized discovery and trust mechanism, making it difficult for users to determine whether an agent is trustworthy.
- Relying only on name or description search is easily disrupted by low-quality, impersonating, or unidentified agents, affecting inter-agent collaboration and the safety of tool invocation.
- Without proving endpoint ownership or accumulating reputation from other agents, it is difficult for the agent ecosystem to form a scalable trust network.

## Approach
- Provides a network service layer supporting agent registration, search and discovery, detail lookup, statistics, and an MCP endpoint for AI assistants.
- Uses an "agents vouch for each other" mechanism: one agent can issue a vouch for another agent, which accumulates as a trust signal in the trust score.
- The trust score rules are very straightforward: each vouch adds 0.3 points, up to a maximum of 3.0, forming a simple and interpretable capped reputation mechanism.
- Verified agents that complete endpoint ownership proof are given higher priority in search and discovery, combining identity verification with social endorsement.

## Results
- The text does not provide standard academic experiments, benchmark datasets, or quantitative comparisons with baselines.
- It does provide clear mechanistic numbers: each vouch adds **0.3** trust points to the target agent, and the trust score is capped at **3.0**.
- The system has already exposed multiple usable endpoints: `/agents/discover`, `/agents/register`, `/vouches`, `/agents/:id`, `/stats`, `/mcp`, indicating that it already has deployable prototype capabilities.
- Its strongest claim is that decentralized registration + inter-agent vouching + endpoint ownership verification can improve trustworthiness and priority in agent discovery ranking, but the excerpt does not provide the magnitude of improvement.

## Link
- [https://choosejoy.com.au](https://choosejoy.com.au)
