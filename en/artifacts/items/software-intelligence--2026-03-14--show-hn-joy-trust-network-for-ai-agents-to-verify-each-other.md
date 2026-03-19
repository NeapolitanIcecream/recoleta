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
- multi-agent-systems
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Show HN: Joy – Trust Network for AI Agents to Verify Each Other

## Summary
Joy is a decentralized discovery and trust network for AI agents and MCP servers, allowing agents to register, search for one another, and build computable trust scores through mutual vouching. It attempts to solve the infrastructure problem of “how to find trustworthy agents” in an open agent ecosystem.

## Problem
- An open AI agent ecosystem needs a mechanism to **discover** available agents and MCP services; otherwise, agent collaboration and tool invocation are difficult to scale.
- Directories or self-reported information alone are insufficient; the system also needs to determine **which agents are more trustworthy**, because low-quality or spoofed agents can undermine the safety and reliability of automated tasks.
- This matters because multi-agent software engineering, agent networks, and intelligent operating environments all depend on verifiable agent identities and rankable trust signals.

## Approach
- Joy provides a decentralized-style agent directory and API: agents can register, and other agents or clients can search for target agents by name, description, or capabilities.
- The core mechanism is very simple: agents can submit **vouches** for one another; each vouch adds **0.3** to the vouched agent’s trust score, up to a maximum of **3.0**.
- The system also supports **endpoint ownership proof**; agents that complete verification receive higher priority in discovery results.
- It exposes standardized interfaces, including `/agents/register`, `/agents/discover`, `/vouches`, `/agents/:id`, `/stats`, and the `/mcp` MCP endpoint for AI assistants.

## Results
- The text **does not provide formal experiments, benchmarks, or paper-style quantitative results**, so it is not possible to report precise improvements in performance, recall, success rate, or comparison figures against baseline methods.
- The most specific mechanistic numbers provided are: **each vouch increases trust by 0.3, up to a maximum of 3.0**, indicating that its trust calculation uses a linearly accumulated capped model.
- The system claims to enable **decentralized discovery and trust** for agents, and supports Claude Code access through MCP, but does not provide datasets, user scale, false positive rates, or latency metrics.
- Another explicit claim is that **agents that complete endpoint ownership proof receive priority in discovery ranking**, but the effect of this ranking policy is not quantified.

## Link
- [https://choosejoy.com.au](https://choosejoy.com.au)
