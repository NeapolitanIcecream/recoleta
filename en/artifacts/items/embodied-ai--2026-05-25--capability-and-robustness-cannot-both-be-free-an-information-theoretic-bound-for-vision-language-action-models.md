---
source: arxiv
url: https://arxiv.org/abs/2605.25889v3
published_at: '2026-05-25T14:16:57'
authors:
- Jianwei Tai
topics:
- vision-language-action
- robot-policy-robustness
- information-theory
- adversarial-attacks
- openvla
- libero
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Capability and Robustness Cannot Both Be Free: An Information-Theoretic Bound for Vision-Language-Action Models

## Summary
The paper claims a general information-theoretic upper bound on the sum of VLA policy capability and adversarial robustness. It targets robot action policies such as OpenVLA, including tokenized, continuous, multi-step, and encoder-based variants.

## Problem
- VLA models can perform well on clean robot benchmarks while failing under small image perturbations; the excerpt cites OpenVLA-7B dropping from above 95% LIBERO success to under 5% under a 16/255 PGD attack.
- Existing VLA attack and defense work reports empirical trade-offs, but it has not shown whether clean capability and attack robustness can both increase without a limit.
- The issue matters because a VLA output is a physical robot action, so visual fragility can produce unsafe behavior instead of a wrong label.

## Approach
- The core bound is: capability plus robustness is at most task entropy plus attack channel capacity: `I(A*; A_pi) + I(A_pi; A_tilde_pi) - I(A_pi; delta) <= H(A*) + I(X; X_tilde)`.
- Capability means the mutual information between the policy action and the oracle action.
- Robustness means how much information the clean action and attacked action share, with a debit for attack signal that leaks through the action output.
- The proof uses two applications of the Data Processing Inequality: actions come from observations, and attacked actions come from perturbed observations, so the action channel cannot carry more information than the observation channel.
- The paper extends the bound to quantized continuous actions, multi-step rollouts up to horizon `T`, and encoder-specific budgets using `I(phi(X); phi(X_tilde))`.

## Results
- The bound has zero reported violations across 320 validation cells covering Gaussian VLA proxies, OpenVLA-7B with PGD and Square attacks, all 4 LIBERO suites, horizons up to `T=10`, and both continuous-`L1` regression and flow-matching action heads.
- In the closed-form Gaussian proxy, analytical slack and MINE-estimated slack are non-negative in 252/252 cells; after grouping, 52/84 configurations show significant positive slack at `alpha=0.05` after Holm-Bonferroni correction.
- For OpenVLA on LIBERO, the excerpt reports `H(A*) ≈ 26` nats and pixel/PCA `I(X; X_tilde) ≈ 5,000` nats at `epsilon=4/255`.
- The encoder-specific bound is reported as 28x to 68x tighter than the pixel-PCA bound across `epsilon in {2,4,8,16}/255` on the 4 LIBERO suites.
- At `epsilon=8/255`, the encoder-specific budget is reported as 86 to 142 nats on vanilla OpenVLA, with discretized capability around 7.5 nats and slack reduced from about `3.7-4.3e3` nats to 79 to 134 nats.
- The paper claims three practical diagnostics computable from at most 200 samples: a roughly 5-minute pre-flight encoder ceiling, a defense-forensics shift signature, and a head-agnostic robustness ratio `Rob_disc/Cap_disc`.

## Link
- [https://arxiv.org/abs/2605.25889v3](https://arxiv.org/abs/2605.25889v3)
