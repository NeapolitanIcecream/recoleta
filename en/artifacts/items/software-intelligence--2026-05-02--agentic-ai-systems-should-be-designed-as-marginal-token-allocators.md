---
source: arxiv
url: https://arxiv.org/abs/2605.01214v1
published_at: '2026-05-02T03:06:02'
authors:
- Siqi Zhu
topics:
- agentic-ai
- token-allocation
- coding-agents
- llm-routing
- serving-systems
- rl-training
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Agentic AI Systems Should Be Designed as Marginal Token Allocators

## Summary
The paper argues that agentic AI systems should allocate each added token by expected quality gain minus compute, latency, and risk costs. It uses a coding-agent request to show how routing, agent actions, serving, and training fit one allocation rule.

## Problem
- Flat per-token accounting treats model selection, planning, verification, KV cache use, and RL rollouts as the same kind of cost, even though they change quality, latency, and risk in different ways.
- Local optimization can waste tokens: a cheap router choice can force extra agent verification, create serving congestion, and produce lower-quality training traces.
- This matters for coding agents and other action-taking systems because token cuts can raise the cost of wrong commits, missed tests, stale caches, and slow service.

## Approach
- The paper defines each possible token use as an option: cheap model, frontier model, retrieval, planning, tool call, verifier, prefill, decode, KV transfer, RL rollout, reward computation, or gradient update.
- The core rule is simple: spend the next token where `task value × marginal quality gain - compute cost - latency cost - risk cost` is highest.
- It maps the same rule to 4 layers: routing as model screening, agent policy as plan-act-verify allocation, serving as prefill/decode/KV production, and training as investment in future capability.
- It proposes shared shadow prices for compute, latency, and risk so upstream choices can account for downstream cost.
- It turns common failures into pricing errors: over-routing, over-delegation, under-verification, serving congestion, stale rollouts, and cache misuse.

## Results
- This is a position paper and reports no empirical benchmark gains, ablations, or production measurements.
- It gives a worked routing example: cheap model quality `0.7` at cost `1` versus frontier model quality `0.9` at cost `5`; the frontier model becomes preferred when task value exceeds `20` without risk.
- In the same example, adding wrong-action probabilities `0.05` for the cheap model and `0.01` for the frontier model with risk price `50` shifts the crossover to about `10`.
- It claims one first-order condition covers `4` system layers: demand, action, supply, and capital.
- It identifies `6` recurring failure modes explained by mispriced marginal tokens: over-routing, over-delegation, under-verification, congestion, stale rollouts, and cache misuse.
- It recommends concrete artifacts for evaluation and operation: regret-based router evaluation, autonomy schedules by action class, and logged shadow prices for prefill, decode, and KV resources.

## Link
- [https://arxiv.org/abs/2605.01214v1](https://arxiv.org/abs/2605.01214v1)
