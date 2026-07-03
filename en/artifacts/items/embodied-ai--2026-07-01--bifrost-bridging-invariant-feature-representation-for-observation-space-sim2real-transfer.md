---
source: arxiv
url: https://arxiv.org/abs/2607.01410v1
published_at: '2026-07-01T19:15:17'
authors:
- Yunfu Deng
- Josiah P. Hanna
topics:
- sim2real
- robot-policy
- latent-representation
- bisimulation
- visual-navigation
- cross-domain-transfer
relevance_score: 0.79
run_id: materialize-outputs
language_code: en
---

# BIFROST: Bridging Invariant Feature Representation for Observation-space Sim2Real Transfer

## Summary
BIFROST trains a shared latent history encoder so a robot policy trained in simulation can run in the target domain without online adaptation. The supplied excerpt shows clear sim2sim gains under visual and dynamics gaps, while sim2real results are claimed but not numerically shown in the provided text.

## Problem
- Sim2real robot policies often fail because simulated images differ from camera images and simulated physics differs from real contact, friction, and actuation.
- Existing methods usually handle perception and dynamics gaps with separate modules, which can break when both gaps appear together.
- The problem matters because real robot data is costly and risky, while simulation data is cheap enough for policy training.

## Approach
- BIFROST collects paired target-source trajectory segments by replaying target-domain action sequences in simulation from matched observable configurations.
- A GRU history encoder maps observation-action histories from both domains into one latent state space.
- Training uses three losses: target reward prediction, latent next-state prediction, and cross-domain successor alignment.
- The alignment loss approximates a Wasserstein-1 distance between predicted latent successor distributions, following cross-domain bisimulation: histories with similar rewards and future behavior should map near each other.
- After encoder training, the encoder is frozen; SAC trains a policy in simulation on latent states, then the same encoder and policy run in the target domain with no further adaptation.

## Results
- In top-down sim2sim navigation, BIFROST reaches a 0.68 ± 0.08 success rate over 10 seeds, compared with Direct Transfer 0.19 ± 0.04, Target-Only 0.46 ± 0.09, BDA 0.67 ± 0.05, Co-Training BC 0.59 ± 0.08, and Co-Training Offline RL 0.63 ± 0.08.
- In egocentric sim2sim navigation, BIFROST reaches 0.50 ± 0.08 success rate, compared with Direct Transfer 0.03 ± 0.02, Target-Only 0.16 ± 0.07, BDA 0.34 ± 0.05, Co-Training BC 0.37 ± 0.07, and Co-Training Offline RL 0.17 ± 0.14.
- The navigation target data budget is 200 trajectories, about 4,600 paired segments with average length 32.
- The excerpt claims sim2real evidence on contact-rich manipulation and visual servoing, but the supplied text does not include the quantitative sim2real tables or metrics.

## Link
- [https://arxiv.org/abs/2607.01410v1](https://arxiv.org/abs/2607.01410v1)
