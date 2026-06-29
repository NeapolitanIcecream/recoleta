---
source: arxiv
url: https://arxiv.org/abs/2606.10366v1
published_at: '2026-06-09T03:25:02'
authors:
- Shuo Wang
- Hanyuan Xu
- Yingdong Hu
- Fanqi Lin
- Yang Gao
topics:
- vision-language-action
- sim2real
- robot-evaluation
- robot-foundation-models
- policy-ranking
- simulator-finetuning
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# A Practical Recipe Towards Improving Sim-and-Real Correlation for VLA Evaluation

## Summary
This paper studies when simulation gives the same VLA policy evaluation decisions as real robot tests. It finds that REALM tracks real-world rankings best among three simulators, and that limited simulator fine-tuning improves sim-real alignment.

## Problem
- Real-world VLA evaluation is expensive: the study reports 1,115 physical rollouts versus 11,800 simulated rollouts.
- Existing simulators can look realistic while still giving wrong policy rankings or wrong failure patterns.
- Policy developers need simulation to support model selection and diagnosis under vision, layout, language, and behavior changes.

## Approach
- The authors align 9 tabletop manipulation tasks between simulation and a DROID real-robot setup.
- They evaluate 5 VLA policies: π0, π0-FAST, π0.5, GR00T N1.6, and GR00T N1.7.
- They compare VLA-Arena, SIMPLER, and REALM using Spearman rank correlation, Pearson correlation, and Mean Maximum Rank Violation against real-world results.
- They measure perturbation sensitivity by normalizing each policy’s success-rate drop across vision, layout, language, and behavior perturbations.
- They test REALM-based fine-tuning with different amounts of simulator data to see how adaptation changes sim-real alignment.

## Results
- REALM gives the strongest average policy-ranking correlation: Spearman 0.700, Pearson 0.785, MMRV 0.030; VLA-Arena gets 0.575/0.725/0.060, and SIMPLER gets 0.400/0.402/0.128.
- REALM matches the real-world perturbation severity order across all 4 dimensions: behavior is highest sensitivity at 1.000, layout is mid-level at 0.644 versus 0.679 real, and vision is lowest at 0.000 versus 0.008 real.
- Simulator post-training in REALM raises proxy Spearman correlation from 0.700 to 0.875 and Pearson correlation from 0.785 to 0.878.
- Post-training cuts proxy MMRV from 0.030 to 0.015 and sensitivity MAE from 0.110 to 0.041.
- The data-scaling result is non-monotonic: Tune-5 improves several metrics, Tune-10 gives the best overall alignment, and Tune-20 reduces perturbation-sensitivity alignment below the untuned REALM setting.
- Object replacement in REALM changes absolute success rates on the banana task but keeps the same policy ordering across 5 replacement objects: corn, zucchini, hotdog, carrot, and cucumber.

## Link
- [https://arxiv.org/abs/2606.10366v1](https://arxiv.org/abs/2606.10366v1)
