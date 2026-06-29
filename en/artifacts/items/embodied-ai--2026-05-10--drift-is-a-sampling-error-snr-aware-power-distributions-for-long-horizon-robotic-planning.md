---
source: arxiv
url: https://arxiv.org/abs/2605.09537v1
published_at: '2026-05-10T13:49:56'
authors:
- Kewei Chen
- Yayu Long
- Mingsheng Shang
topics:
- vision-language-action
- robot-planning
- inference-time-scaling
- mcmc-sampling
- long-horizon-control
- robot-foundation-models
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# Drift is a Sampling Error: SNR-Aware Power Distributions for Long-Horizon Robotic Planning

## Summary
CAPS is a training-free inference-time method for VLA robot policies that reduces long-horizon instruction drift by searching over future action chunks when model uncertainty rises. It reports higher success rates than π0, π0.5, TACO, and several VLA baselines on RoboTwin and Simpler-WindowX.

## Problem
- Long-horizon VLA policies can choose locally likely actions that lose the original task goal after many steps.
- This matters because one wrong action in bimanual or sequential manipulation can make the task unrecoverable.
- Existing prompt and reranking methods depend on the sampled candidate set and do not iteratively repair a single trajectory.

## Approach
- CAPS treats drift as a sampling error in the policy's trajectory distribution.
- It samples from a power distribution, π(τ) ∝ pθ(τ|I,Ht)^α, which gives more weight to trajectories the base model scores as consistent with the instruction and history.
- It computes contextual SNR using KL divergence from the uniform action distribution; since SNR = log|A| - entropy, high entropy means low SNR.
- When entropy passes a threshold γ, CAPS runs Metropolis-Hastings search over action chunks: keep a prefix, resample a suffix, then accept or reject the candidate with a power-distribution likelihood ratio.
- When entropy stays below γ, it uses greedy execution to save inference cost.

## Results
- RoboTwin 1.0 with π0: CAPS reached 47.4% average success, compared with 32.2% for π0 and 41.3% for π0 + TACO; gains were +15.2 points over π0 and +6.1 points over TACO.
- RoboTwin “Dual Bottles Pick Hard”: success rose from 48.0% with π0 to 61.0% with CAPS; TACO reached 52.0%.
- Simpler-WindowX: CAPS reached 60.5% average success, compared with 48.0% for π0, 55.5% for π0 + TACO, 42.7% for SpatialVLA, 31.3% for RoboVLM, 16.0% for Octo, and 1.1% for RT-1-X.
- Simpler-WindowX “Carrot on Plate”: CAPS scored 61.0%, compared with 42.0% for π0 and 52.0% for π0 + TACO.
- The theory section claims that with α = 2 and single-step drift ε = 0.1, ideal power-distribution sampling gives a 10× effective-horizon extension; with finite MCMC steps, the bound includes a residual O(ρ^N) sampling-bias term.
- The excerpt says CAPS was also tested on Libero-long, but it does not provide aggregate Libero-long numbers in the visible text.

## Link
- [https://arxiv.org/abs/2605.09537v1](https://arxiv.org/abs/2605.09537v1)
