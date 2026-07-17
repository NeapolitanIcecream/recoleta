---
source: arxiv
url: https://arxiv.org/abs/2607.14890v1
published_at: '2026-07-16T12:06:21'
authors:
- Jek Huang
- Jeffery Hsia
- Jiayi Sun
- Freddie Shi
- Wei Huang
- Ian H. White
topics:
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
- human-ai-interaction
- verifiable-evidence
- software-lifecycle
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Proof-or-Stop: Don't Trust the Agent, Trust the Evidence -- Loop Engineering for Verifiable Evidence-Gated Lifecycle Control

## Summary
Proof-or-Stop is a model-agnostic control layer that advances autonomous software lifecycle states only when fresh, authenticated, source-state-bound evidence passes a defined gate. Its evaluation supports reliable claim blocking and reduced propagation of visible-pass/hidden-fail artifacts within one model family and a self-hosted implementation, but not semantic correctness or broad generalization.

## Problem
- Autonomous coding agents can claim that work is reviewed, tested, done, or ready to merge without producing evidence that is current, complete, authorized, and tied to the exact source state.
- Stale logs, self-reports, visible-test overfitting, or reviewer prose can cause downstream automation to advance defective work.
- This matters because lifecycle transitions such as merge and done can become irreversible operational decisions based on unsupported claims.

## Approach
- Treat every consequential agent or workflow output as a claim rather than lifecycle state; a gate admits the claim only when its evidence is acceptable.
- Bind structured evidence to the current tracked source using material, commit, and story-file hashes, plus policy and command-set hashes.
- Verify freshness, completeness, integrity, producer authorization, execution receipts, claim support, and accepted outcomes; reject missing, stale, tampered, unauthorized, or reconfigured evidence.
- On failed gates, use bounded repair or reflection, honest degradation, escalation, or stop instead of advancing the lifecycle.
- Implement the method in the open-source Proof-or-Stop system and evaluate its engine contract, receipt verifier, control-policy ablation, recovery behavior, and self-application corpus.

## Results
- The unattended-loop engine passed 10/10 tested scenarios with false-done = 0; its local-key receipt verifier rejected 18 tamper classes with zero false accepts and zero false rejects in the tested suite.
- In a powered 9,240-cell ablation across 24 tasks, visible-pass/hidden-fail amplification fell from 31/1,800 injected cells under a compute-budgeted naive loop to 2/1,800 under the gated loop, a +1.6 percentage-point not-amplified gain with a 95% CI of [0.8, 2.5].
- The near-compute comparison reported 14/1,800 amplified cells for a reviewer-added control versus 2/1,800 for the gated loop, indicating that enforcing review as a lifecycle gate contributed beyond merely adding a reviewer; the effect was concentrated in a trap-active task.
- The self-application corpus contained 565 stories and 1,007 review findings, with 94.8% resolved; 26/28 curated deep-set findings were filed while author tests were green.
- A refreshed cross-vendor exhibit contained 68 high/critical findings across 26 stories, all resolved, but it was observational rather than a controlled marginal-rate estimate.
- The evidence is limited to one model family, 24 ablation tasks, and a self-hosted corpus; the paper does not establish semantic program correctness, multi-model or external-benchmark generalization, or a strong independent-host quorum.

## Link
- [https://arxiv.org/abs/2607.14890v1](https://arxiv.org/abs/2607.14890v1)
