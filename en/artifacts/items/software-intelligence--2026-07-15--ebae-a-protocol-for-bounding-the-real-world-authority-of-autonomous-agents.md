---
source: hn
url: https://zenodo.org/records/21385239
published_at: '2026-07-15T23:26:46'
authors:
- Akumaskills
topics:
- autonomous-agents
- agent-security
- access-control
- attested-execution
- cryptographic-protocols
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# EBAE: A protocol for bounding the real-world authority of autonomous agents

## Summary
EBAE is a protocol for limiting the real-world authority of autonomous agents by separating action proposals from protected execution. It releases an action only when its intent, authorization, policy state, freshness, and anti-rollback state agree within the same epoch.

## Problem
- Autonomous agents may propose valid-looking actions while holding too much authority to execute them directly.
- Without binding authorization to a specific action and current security state, systems may permit replayed, stale, or rolled-back commands.
- The excerpt does not provide experimental history or benchmark results, so the protocol's practical effectiveness remains unquantified.

## Approach
- Separate the agent that proposes an action from a protected executor that can release it.
- Organize authority into epochs, which provide bounded periods of valid authorization.
- Require the active manifest, a one-use certificate for the exact intent, the cryptographic profile, policy, freshness state, and anti-rollback state to match the same epoch and action.
- Represent this agreement as an Authorization Closure Digest; the working reference implementation is intended to reject actions that do not satisfy the closure conditions.

## Results
- The paper reports a working reference implementation, but the provided excerpt contains no quantitative evaluation, dataset, latency measurement, or baseline comparison.
- The strongest concrete claim is that execution is blocked unless all required authorization inputs agree on the same action and epoch.
- The record identifies the work as a July 16, 2026, version 1 preprint; the excerpt is truncated before the implementation's detailed replay-blocking results can be assessed.

## Link
- [https://zenodo.org/records/21385239](https://zenodo.org/records/21385239)
