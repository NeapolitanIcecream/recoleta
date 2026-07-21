---
source: arxiv
url: https://arxiv.org/abs/2607.17786v1
published_at: '2026-07-20T10:20:32'
authors:
- Tuan Duong Trinh
- Naveed Akhtar
- Basim Azam
topics:
- robot-foundation-model
- vision-language-action
- robot-robustness
- adversarial-attacks
- latent-reasoning
- robot-safety
relevance_score: 0.98
run_id: materialize-outputs
language_code: en
---

# Reasoning as a Double-Edged Sword: Architecture and Cross-Stage Robustness in Vision-Language-Action Models

## Summary
The paper tests whether explicit reasoning makes vision-language-action (VLA) policies more robust and finds that robustness depends on the reasoning architecture. In the reported LIBERO and SimplerEnv experiments, latent iterative reasoning is especially fragile, while runtime reasoning monitors fail under adaptive attacks.

## Problem
- It addresses whether adding a reasoning stage helps VLA models absorb perturbations or instead amplifies them, which matters for deploying generalist robot policies under sensor, computation, or command errors.
- It also tests whether an exposed reasoning trace can support runtime safety monitoring rather than merely improve task performance.

## Approach
- The authors compare three LIBERO-fine-tuned VLAs: OpenVLA-OFT with no reasoning, DeepThinkVLA with text chain-of-thought, and RD-VLA with a 12-step latent iterative loop.
- They inject stochastic and adversarial perturbations separately at the vision, reasoning, and action stages, using Gaussian noise, FGSM, PGD-10, Square Attack, and text entity swaps across LIBERO and SimplerEnv.
- They vary RD-VLA's inference recurrence depth from K=4 to K=12 to test whether its fragility grows multiplicatively with reasoning steps.
- They evaluate a plan-action consistency monitor and an action-anomaly monitor under adaptive attack and matched false-positive-rate calibration.

## Results
- On LIBERO with Gaussian vision noise at sigma=0.2, success rate was 92.7% for DeepThinkVLA, 89.0% for OpenVLA-OFT, and 14.8% for RD-VLA; RD-VLA lost 74.3 percentage points from its clean performance.
- Under white-box PGD-10 at epsilon=8/255, success rate was 49.8% for DeepThinkVLA, 18.2% for OpenVLA-OFT, and 0.0% for RD-VLA, establishing the reported ordering DeepThinkVLA > OpenVLA-OFT >> RD-VLA at that operating point.
- RD-VLA's amplification was nearly unchanged between K=8 and K=12: rho(12)/rho(8)=1.005, compared with a multiplicative prediction of 2.0. The authors therefore attribute the observed fragility to a structural property of the encoder and recurrent fixed-point output rather than accumulation across iterations, while noting that the K=4 condition is out of distribution.
- The plan-action consistency probe's detection AUC fell from 0.996 under naive corruption to 0.493 under adaptive attack, approximately chance performance.
- Combining the consistency and action-anomaly probes did not raise defended task success above undefended success on any PGD-10 cell under matched-FPR calibration.
- The conclusions are limited to the tested architectures, simulated manipulation benchmarks, perturbation classes, and output-level monitors; the provided excerpt is truncated and does not establish physical-world transfer or a general impossibility result for defenses.

## Link
- [https://arxiv.org/abs/2607.17786v1](https://arxiv.org/abs/2607.17786v1)
