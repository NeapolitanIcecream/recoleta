---
source: arxiv
url: https://arxiv.org/abs/2606.03034v1
published_at: '2026-06-02T02:17:30'
authors:
- Gaurav Naresh Mittal
topics:
- agent-networks
- trust-reputation
- capability-advertising
- multi-agent-systems
- mcp-a2a
- llm-reliability
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Capability Advertisement as a Market for Lemons: A Trust Layer for Heterogeneous Agent Networks

## Summary
The paper argues that MCP, A2A, and function-calling style agent advertisements let unreliable agents look identical to reliable ones. It proposes a Trust Layer that adds reliability claims, tests, attestations, reputation, and drift checks above existing agent protocols.

## Problem
- Current agent ads describe how to call a tool or skill, but they do not state how often it works, when it fails, what evidence backs the claim, or when the claim expires.
- In open agent networks, a caller sees the advertised capability, not the true reliability. This creates a lemons market where cheap overclaiming can drive out investment in reliable agents.
- The target failure is “confident-wrong”: an agent returns a fluent, well-formed, false answer with no error signal. Classical crash, timeout, and Byzantine handling do not fit this probabilistic and correlated failure pattern well.

## Approach
- The core mechanism is simple: replace boolean capability claims with evidence-backed reliability claims, then test and track those claims over time.
- Probabilistic capability descriptors add fields such as estimated reliability, benchmark name, sample size, evaluation date, input limits, backend version, and expiry time.
- Screening uses caller challenges, canary tasks, and third-party attestations. Attestations should include signed, reproducible evaluation records and can be posted to append-only logs.
- Reputation records update after checked outcomes, challenges, contradictions, or downstream validation. Version changes and expired descriptors trigger re-checks to catch drift.
- The paper models the system with signaling, screening, and repeated-game reputation. A separating equilibrium exists when the cost of sustaining an overclaim, c, exceeds the one-shot gain from overclaiming, g.

## Results
- The paper reports no live deployment measurements and no new LLM benchmark results. Its claims are analytical plus an illustrative Python simulation.
- Delegation reliability compounds: a 3-hop chain with per-hop reliability of 85% has end-to-end reliability of about 61% under an independence assumption.
- In the simulation, low and high true reliabilities are set to rL = 0.55 and rH = 0.92, giving an overclaim gain g = 0.37.
- Under faith-based advertising, simulated realized reliability falls to rL = 0.55 and the share of providers investing in genuine reliability drops near 0 across 24 random seeds.
- Under the Trust Layer with c = 1.5g, simulated reliability stays near rH = 0.92 and the invested share settles at 0.58, close to the predicted 0.583.
- A screening-cost sweep claims a sharp transition at c = g: when c exceeds g, overclaiming is no longer profitable in the model and honest capability signals can separate reliable and unreliable providers.

## Link
- [https://arxiv.org/abs/2606.03034v1](https://arxiv.org/abs/2606.03034v1)
