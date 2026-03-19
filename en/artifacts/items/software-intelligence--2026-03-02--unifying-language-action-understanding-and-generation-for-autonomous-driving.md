---
source: arxiv
url: http://arxiv.org/abs/2603.01441v1
published_at: '2026-03-02T04:41:10'
authors:
- Xinyang Wang
- Qian Liu
- Wenjie Ding
- Zhao Yang
- Wei Li
- Chang Liu
- Bailin Li
- Kun Zhan
- Xianpeng Lang
- Wei Chen
topics:
- autonomous-driving
- vision-language-action
- instruction-following
- multimodal-alignment
- coarse-to-fine-decoding
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Unifying Language-Action Understanding and Generation for Autonomous Driving

## Summary
LinkVLA proposes an autonomous driving VLA framework that unifies natural language instructions and driving actions into the same discrete token space, improving both instruction–action alignment and inference efficiency. It also adds an understanding task that "infers language from trajectories" and replaces point-by-point auto-regressive generation with a two-stage coarse-to-fine decoding process.

## Problem
- Existing autonomous driving VLA models often exhibit **inconsistency between language understanding and actual actions**: for example, they may say "change lanes to the left" but generate a "keep lane" trajectory, which directly affects safety, controllability, and user trust.
- Typical **auto-regressive action generation is too slow**: long trajectories must be decoded step by step, causing noticeable inference latency in deployment.
- Methods focused on data augmentation, posterior RL correction, or implicit latent-space alignment often fail to establish a **verifiable bidirectional language–action link** during supervised learning.

## Approach
- **Unified token space**: language tokens and trajectory tokens are merged into a shared discrete codebook; continuous trajectories are first quantized into action tokens, then processed by a single multimodal model, structurally narrowing the modality gap.
- **Better action tokenization**: a logarithmic transform is applied to trajectory coordinates to improve precision in near-vehicle regions; then spatial soft labels (Gaussian neighborhoods) are used for training instead of hard one-hot labels, so nearby actions are also treated as "similar" during learning.
- **Bidirectional semantic alignment**: in addition to the standard objective of "generate actions from images + instructions," an auxiliary objective of "generate instruction descriptions from images + actions" is added, forcing the model to infer linguistic meaning from trajectories and form bidirectional consistency.
- **Coarse-to-fine generation (C2F)**: the trajectory endpoint is first predicted in a single forward pass, then a coarse trajectory is obtained through linear interpolation, and finally all waypoints are refined in parallel, replacing point-by-point auto-regressive decoding.

## Results
- On the **Bench2Drive closed-loop evaluation**, LinkVLA achieves **DS 91.01**, **SR 74.55%**, **Efficiency 255.84**, and **Comfort 34.62**. Compared with the strongest listed instruction-following baseline, **SimLingo** (**85.07 DS** / **67.27% SR** / **259.23 Efficiency** / **33.67 Comfort**), this corresponds to **+5.94 DS**, **+7.28 SR**, **-3.39 Efficiency**, and **+0.95 Comfort**.
- On the **Multi-Ability average score**, LinkVLA reaches **73.40%**, exceeding **SimLingo 67.28%** and **Orion 54.72%**. Category scores include: Merging **60.00**, Overtake **80.00**, Brake **93.33**, Give-Way **50.00**, and Traffic-Sign **83.68**.
- In the **latency comparison**, the auto-regressive version of LinkVLA takes **361 ms**, while the C2F version drops to **48 ms**, equivalent to saving about **86.7%** of inference time; meanwhile, the driving score improves from **90.66** to **91.01**.
- Compared with other methods, the C2F version of LinkVLA has **48 ms** latency, faster than **Orion 65 ms** and close to **SimLingo 34 ms**, but with a higher driving score (LinkVLA **91.01** vs Orion **77.74** vs SimLingo **85.07**).
- The paper also claims **state-of-the-art** performance in closed-loop driving and instruction-following ability, with the core evidence coming from the leading scores in the main Bench2Drive table and the latency table.

## Link
- [http://arxiv.org/abs/2603.01441v1](http://arxiv.org/abs/2603.01441v1)
