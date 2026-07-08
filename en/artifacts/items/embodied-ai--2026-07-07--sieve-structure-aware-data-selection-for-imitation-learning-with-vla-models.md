---
source: arxiv
url: https://arxiv.org/abs/2607.06442v1
published_at: '2026-07-07T16:10:02'
authors:
- Changti Wu
- Bin Yu
- Zhaolong Shen
- Shijie Lian
- Xiaopeng Lin
- Cong Huang
- Zhirui Zhang
- Lei Zhang
- Kai Chen
topics:
- vision-language-action
- imitation-learning
- robot-data-scaling
- data-selection
- vla-models
- robot-manipulation
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# SIEVE: Structure-Aware Data Selection for Imitation Learning with VLA Models

## Summary
SIEVE selects a smaller, cleaner subset of robot demonstrations for VLA imitation learning by keeping reusable behavior structures and central examples. On Bridge-V2 with Qwen3-VL-4B-GR00T, it beats full-data training while using 50% of the demonstrations and 50% of the training steps.

## Problem
- VLA policies are trained on large robot demonstration sets, but those sets often contain duplicate trajectories, noisy actions, poor demonstrations, and uneven task coverage.
- Existing selection methods usually score whole trajectories or individual state-action pairs, which can miss mid-level behavior units used across long-horizon tasks.
- This matters because behavior cloning can waste compute on repeated or inconsistent supervision, and smaller selected datasets can train faster if they keep the right behavior coverage.

## Approach
- SIEVE segments each trajectory at gripper or hand state flips, with a 5-frame persistence rule to avoid jitter boundaries.
- It encodes each segment with V-JEPA2, samples 8 frames per segment, concatenates start, middle, and end features, and reduces the feature to 256 dimensions with PCA.
- It clusters segment features with MiniBatch K-Means to discover reusable visuo-motor primitives, then represents each trajectory as an ordered primitive sequence.
- It allocates the selection budget across primitive-sequence buckets using a structural exposure objective that rewards coverage of reused primitives and adjacent transitions with diminishing returns.
- Within each bucket, it selects trajectories closest to the medoid, using cosine similarity over concatenated segment features, so the chosen demonstrations are central examples for behavior cloning.

## Results
- On Bridge-V2, SIEVE with a 50% selection budget, 26.5K demonstrations, and 25K training steps reaches 56.3% average success on SimplerEnv-WidowX, above full-data training at 51.8% with 50K steps.
- Under the same 50% data and 25K-step setting, SIEVE beats Random 39.6%, DemInf 43.2%, and SCIZOR 52.2% average success.
- With 50% data and 50K training steps, SIEVE reaches 59.4% average success, compared with Random 40.4%, DemInf 46.6%, and SCIZOR 55.5%.
- With a 70% selection budget, 37.1K demonstrations, and 35K training steps, SIEVE reaches 62.3% average success, compared with Random 44.6%, DemInf 55.2%, and SCIZOR 56.8%.
- With 70% data and 50K steps, SIEVE reaches 62.5% average success, above Random 46.9%, DemInf 57.1%, SCIZOR 58.1%, and full-data training at 51.8%.
- The excerpt also says experiments cover Bridge-V2, Fractal, and GR00T-X-Sim with two Qwen3-VL-4B VLA variants, but the provided quantitative table is for Bridge-V2 with Qwen3-VL-4B-GR00T.

## Link
- [https://arxiv.org/abs/2607.06442v1](https://arxiv.org/abs/2607.06442v1)
