---
source: hn
url: https://sebastianhanke.substack.com/p/stigmergy-for-capability-selection
published_at: '2026-06-03T23:06:36'
authors:
- pssah4
topics:
- llm-agents
- tool-selection
- mcp
- stigmergy
- code-intelligence
- prompt-caching
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Stigmergy for capability selection in LLM agent loops (skills, tools, MCP)

## Summary
The paper proposes a local stigmergy layer for LLM agents that learns which tools, MCP tools, and skills tend to work in sequence. It aims to cut repeated failed tool exploration while keeping cached tool definitions stable.

## Problem
- LLM agents carry capability descriptions in context on each step; Anthropic reports 58 tools at about 55,000 tokens and another setup above 140,000 tokens, so large catalogues can consume much of the prompt before work starts.
- Tool choice gets worse as catalogues grow, and wrong choices cost extra calls, retries, loaded skill text, and error messages.
- Current retrieval, deferred loading, routers, and skill disclosure do not feed past outcomes into the next choice, so the same bad paths can repeat.

## Approach
- The method stores capabilities as nodes in a local directed graph and stores transitions between capabilities as edges.
- Each edge has a pheromone value, decayed success and failure evidence, timestamps, and optional user pins.
- At each step it scores candidate next capabilities with decayed pheromone for the previous-to-current transition and semantic similarity between the task and capability description.
- Edges that lead to accepted outcomes get reinforced; unused or stale edges decay, which lets old paths fade as codebases and workflows change.
- Prompt caching changes the default optimization: the paper keeps the full tool block stable when possible and adds a small learned path hint after the cache breakpoint, rather than rewriting the visible tool list each turn.

## Results
- The paper does not report a completed controlled empirical study for the proposed method; it defines the protocol and says the central token-reduction test remains to be run.
- It reports 1 preliminary self-run mechanism check with large token reduction and a cold-start success regression, but the excerpt gives no exact token or success-rate numbers for that run.
- The motivation uses published platform numbers: 58 tools can occupy about 55,000 tokens, Anthropic reported 134,000 tool-definition tokens before optimization, and a community MCP setup reported about 144,800 tokens.
- It cites Anthropic tool-search results where selection accuracy improved from 49% to 74% on one model and from 79.5% to 88.1% on another when search replaced loading all tools.
- The claimed technical result is an implemented local design with deterministic seeded selection, no network egress, bounded pheromone values [τ_min, τ_max], lazy exponential decay, and explicit evaluation pivot conditions.

## Link
- [https://sebastianhanke.substack.com/p/stigmergy-for-capability-selection](https://sebastianhanke.substack.com/p/stigmergy-for-capability-selection)
