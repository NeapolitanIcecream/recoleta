---
source: arxiv
url: https://arxiv.org/abs/2605.01567v1
published_at: '2026-05-02T18:37:36'
authors:
- Mehmet Iscan
topics:
- coding-agents
- developer-memory
- reinforcement-learning
- model-context-protocol
- contextual-bandits
- off-policy-evaluation
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Feedback-Normalized Developer Memory for Reinforcement-Learning Coding Agents: A Safety-Gated MCP Architecture

## Summary
RL Developer Memory is a local MCP memory-control layer for RL coding agents that logs retrieval decisions, normalizes developer feedback, and blocks learned reranking unless offline evidence clears safety gates. It targets RL code fixes where a wrong memory can change training targets, terminal masks, gradient flow, or validation claims.

## Problem
- Coding agents need persistent repository memory across long sessions, but generic vector retrieval can return plausible records that are unsafe for RL code.
- RL implementation bugs often depend on small details such as Bellman targets, target-network detach, PPO clipping, SAC entropy signs, and terminal masks, so false-positive memory retrieval can produce invalid patches or invalid claims.
- Developer feedback arrives in mixed labels and delayed resolutions; without logging and normalization, the system cannot learn which retrieved memory helped.

## Approach
- The system runs as a local-first Model Context Protocol server with tools named issue_match, issue_feedback, and issue_record_resolution.
- issue_match normalizes the query, retrieves candidates, ranks them with a deterministic weighted scorer, and returns match, ambiguous, or abstain based on score, margin, and specificity checks.
- issue_feedback maps raw labels into canonical feedback types with bounded rewards in [-1, 1], while neutral labels do not update learning state.
- issue_record_resolution links later verified fixes back to earlier retrieval events using explicit IDs or session, repository, and query compatibility.
- A diagonal contextual-bandit residual policy runs in shadow mode, logs propensities, and can only enter active canary through conservative OPE gates; RL/control memories also need theory-to-code metadata, validation tiers, and review gates.

## Results
- On a deterministic 200-case RL developer-memory benchmark, the deterministic control path reached 80.0% expected-decision accuracy.
- The full shadow/OPE configuration also reached 80.0% expected-decision accuracy, so the paper reports no demonstrated accuracy gain over the same-commit deterministic control.
- Both configurations reached 100.0% hard-negative suppression.
- Static validation passed 11/11 checks, and dynamic integration passed 10/10 cases.
- Patch-replay audits showed favorable raw deltas in offline pass rate and recall-delta metrics, but the paper does not claim method superiority from those deltas.
- Reported limits include no active learned-policy deployment, no official-client MCP interoperability, p95 latency regression in the live full configuration, and 40 residual failures in non-RL path, scope, and alias compatibility cases.

## Link
- [https://arxiv.org/abs/2605.01567v1](https://arxiv.org/abs/2605.01567v1)
