---
source: hn
url: https://avriz.io/eng/paper
published_at: '2026-07-12T22:39:40'
authors:
- rezat
topics:
- llm-routing
- contextual-bandits
- code-agents
- production-ml
- cost-optimization
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# We taught our platform to learn its own pricing decisions

## Summary
Avriz describes a production system that learns which language-model tier should handle each coding-agent turn while keeping new routing decisions out of user traffic until they pass data and safety gates. It combines content-free features, ledger-based rewards, per-model linear learners, shadow evaluation, and bounded on-policy testing.

## Problem
- Each turn must balance answer quality against model cost. Output-token prices differ by 12×, while many simple requests can use the cheapest model.
- Hand-tuned routing rules become stale as model behavior, prices, and usage change.
- Training from historical traffic is difficult because the platform observes the reward only for the model it actually served, and storing message text would create privacy and data-collection costs.

## Approach
- Treat model selection as a contextual bandit. A turn is represented by 11 scaled, content-free features such as code markers, traceback signals, hard verbs, message length, current rung, and tenant escalation rate.
- Build rewards from existing billing records: usable completion, failure, cost in cents, and mid-turn escalation. The system stores no message text and uses one 11-weight ridge-regression model per model rung.
- Start with a deterministic hand-set difficulty scorer as the prior. The learned policy stays in shadow mode until each arm clears a coverage threshold.
- Detect model, endpoint, or price changes with a per-rung economics fingerprint. When a fingerprint changes, the affected arm's weights and sample count reset.
- Graduate the policy through an administrator-controlled traffic percentage and maximum rung ceiling. Bandit-served turns provide measured on-policy rewards for comparison with judge-served turns.

## Results
- The model ladder has a 12× spread in wholesale output-token cost, creating a direct economic incentive for accurate routing.
- The implementation uses 11 features, 11 readable weights per arm, and 55 linear parameters across five rungs.
- Rewards are backfilled over a 600-second turn window after a 120-second settling delay; follow-up calls reuse the routing decision for 10 minutes.
- Constant-step-size SGD gives the learner an effective memory of about 20 samples per arm when the learning rate is approximately 0.05, allowing it to track price changes.
- The report provides no aggregate accuracy, cost-reduction, or user-quality uplift against a baseline. Its strongest concrete claim is a zero-risk deployment path: shadow operation, a data bar, a configurable traffic slice, and a rung ceiling before learned routing can affect users.

## Link
- [https://avriz.io/eng/paper](https://avriz.io/eng/paper)
