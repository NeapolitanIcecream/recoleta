---
source: arxiv
url: https://arxiv.org/abs/2606.27355v1
published_at: '2026-06-25T17:56:33'
authors:
- Xingyu Ren
- Chugang Yi
- Ge Ma
- Youran Sun
topics:
- vision-language-action
- generalist-robot-policy
- robot-policy-routing
- robot-data-scaling
- robot-evaluation
- sim2real
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# RouterVLA: Turning Smoke Tests into Supervision for Heterogeneous VLA Selection

## Summary
RouterVLA shows that pre-deployment robot smoke tests can choose among frozen VLA experts better than a single global policy. On LIBERO-Plus, a simple probe-success router beats Global Best by 14.64 percentage points under trial-disjoint evaluation.

## Problem
- Robot teams test candidate VLA policies before deployment, then often choose one average-best checkpoint for all target conditions.
- Expert strengths vary by task and perturbation, so a global average loses condition-specific evidence needed for expert selection.
- If the same rollout is used to build the profile and score the selected expert, measured routing gains can be inflated.

## Approach
- For each known task-and-perturbation variant, RouterVLA runs 3 probes per available frozen expert and scores the selected expert on a separate held-out trial.
- It builds a 14-feature profile per expert with probe success, Beta summaries, rollout length, duration, termination behavior, training-suite priors, probe count, and missing-statistic masks.
- It compares transparent rules based on probe success against learned scorers: logistic regression, GBDT, and a small MLP.
- The main protocol uses 3-to-1 trial-disjoint cross-fitting over 4 trial IDs, with leave-one-suite-out training for learned scorers.

## Results
- The study uses 34,752 valid LIBERO-Plus rollout records, 398 task-and-perturbation variants, 28 frozen expert IDs, and 1,592 variant-trial evaluation rows.
- Global Best reaches 0.4686 held-out success; the transparent probe-success rule reaches 0.6149, a +14.64 percentage-point gain with 95% CI [+11.37,+17.96].
- Learned scorers do not clearly beat the simple rule: logistic regression reaches 0.6168, GBDT 0.6187, and MLP 0.6144. GBDT exceeds the probe-success rule by +0.38 pp with 95% CI [-0.88,+1.57].
- The realized hindsight upper bound is 0.7393, showing remaining complementarity in the expert pool, though this bound is unavailable at deployment time.
- Same-trial reuse raises an MLP diagnostic from 0.6132 to 0.7393 and inflates the measured gain by 1.87× with 95% CI [1.63,2.24].
- Probe cost is large under exhaustive testing: with mean 21.8 candidates and B=3, commissioning uses 65.5 probe executions on average; a shortlist with M=12,B=3 reaches 0.6185 with 36 probes.

## Link
- [https://arxiv.org/abs/2606.27355v1](https://arxiv.org/abs/2606.27355v1)
