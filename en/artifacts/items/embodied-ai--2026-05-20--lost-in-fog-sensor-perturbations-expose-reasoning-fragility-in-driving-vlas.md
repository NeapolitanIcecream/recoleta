---
source: arxiv
url: https://arxiv.org/abs/2605.21446v1
published_at: '2026-05-20T17:34:02'
authors:
- Abhinaw Priyadershi
- Jelena Frtunikj
topics:
- vision-language-action
- autonomous-driving
- sensor-corruption
- chain-of-causation
- runtime-monitoring
- planning-safety
relevance_score: 0.62
run_id: materialize-outputs
language_code: en
---

# Lost in Fog: Sensor Perturbations Expose Reasoning Fragility in Driving VLAs

## Summary
This paper tests Alpamayo R1, a 10B driving VLA, under camera noise, lighting shifts, and fog. It claims that changes in the model's chain-of-causation explanation are a strong warning signal for large trajectory shifts.

## Problem
- Driving VLAs can explain their plans, but those explanations may change when cameras degrade in fog, glare, darkness, or sensor noise.
- This matters because a planner can output plausible text while its predicted path drifts, which is a safety issue for autonomous driving validation.

## Approach
- The authors evaluate Alpamayo R1 on 1,996 PhysicalAI autonomous-driving validation scenarios.
- They apply 8 synchronized multi-camera perturbations: Gaussian noise at σ=10,30,50,70, brightness 0.4× and 1.6×, and fog α=0.3 and 0.7.
- They run about 18,000 inference trials and compare clean versus perturbed outputs using ADE, ADE increase, L2 trajectory deviation, and exact-match CoC change rate.
- They also run a CoC-suppression ablation with the same checkpoint and decoding settings except for token budget, so the causal claim is limited.

## Results
- On clean inputs, Alpamayo R1 reaches 2.00 m ADE versus 6.32 m for a constant-velocity baseline, a 68.3% reduction with p<10^-257 on 1,996 samples.
- When the CoC explanation changes after perturbation, mean L2 trajectory deviation is 21.82 m versus 4.13 m when it stays unchanged, a 5.3× gap; median deviation is 15.39 m versus 2.16 m, a 7.1× gap.
- Across all 15,968 attacked sample pairs, CoC change has point-biserial r=0.53 with trajectory deviation, Cohen's d=1.12, and p<10^-100; across 8 attack types the aggregate correlation is r=0.99.
- Noise degradation rises nearly linearly over σ=10,30,50,70 with R²=0.957 and slope 0.0048 m ADE per σ unit; the >5 m trajectory-shift rate rises from 18.8% at σ=10 to 70.6% at σ=70.
- Heavy noise σ=70 is the largest tested corruption: ADE rises to 2.30 m, ΔADE is +0.30 m, CoC changes in 52.7% of samples, and p=2×10^-17.
- The CoC ablation reports 11.8% average ADE improvement when CoC generation is enabled across tested conditions, with p<0.0001; standard preprocessing defenses give only small, statistically weak relief.

## Link
- [https://arxiv.org/abs/2605.21446v1](https://arxiv.org/abs/2605.21446v1)
