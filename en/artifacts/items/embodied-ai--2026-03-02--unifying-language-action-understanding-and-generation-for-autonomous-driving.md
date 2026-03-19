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
- language-action-alignment
- shared-tokenization
- coarse-to-fine-decoding
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Unifying Language-Action Understanding and Generation for Autonomous Driving

## Summary
LinkVLA is a vision-language-action model for autonomous driving that aims to solve two key problems at once: the mismatch between language instructions and actual trajectories, and the slowness of autoregressive action generation. By sharing a discrete language/action vocabulary, adding a reverse action-to-text understanding task, and using two-stage coarse-to-fine decoding, it improves both closed-loop driving and instruction following.

## Problem
- Existing autonomous-driving VLA models often exhibit **language-action misalignment**: the model may "understand" the instruction correctly in words, but the generated driving trajectory does not actually carry it out, directly affecting safety, controllability, and user trust.
- Common action generation relies on **step-by-step autoregressive decoding**. Long trajectories require multiple serial forward passes, resulting in high inference latency and making real-world deployment difficult.
- Relying only on data augmentation, post-hoc reinforcement learning, or implicit latent-space alignment often fails to directly embed the bidirectional connection between language and action into the core supervised-learning backbone.

## Approach
- **Unify language tokens and action tokens into a shared discrete codebook**: quantize continuous trajectories into action tokens on a BEV grid and merge them with the text vocabulary, allowing a single multimodal model to handle understanding and generation in the same token space.
- Add two refinement designs for action discretization: a **log-coordinate transform** to improve near-field control resolution, and **spatial soft labels** that replace hard one-hot labels with a Gaussian distribution, explicitly leveraging spatial adjacency in the action grid.
- Beyond the standard generation objective from “language/vision to action,” add an **action-understanding objective**: given visual input and an action sequence, generate a language description in reverse, effectively teaching the model to learn “what this trajectory is doing,” thereby creating a bidirectional language-action binding.
- Replace point-by-point autoregression with **coarse-to-fine (C2F) two-step decoding**: first predict the endpoint in one shot, then obtain a coarse trajectory by linear interpolation, and finally refine all waypoints in parallel to reduce latency.

## Results
- On the **Bench2Drive** closed-loop benchmark, LinkVLA achieves **DS 91.01** and **SR 74.55%**, outperforming **SimLingo** at **DS 85.07 / SR 67.27%** and **Orion** at **DS 77.74 / SR 54.62%**.
- Its Bench2Drive Multi-Ability Mean reaches **73.40%**, higher than **SimLingo 67.28%**, **Orion 54.72%**, and **DriveTransformer 38.60%**. By category, LinkVLA performs particularly well on **Merging 60.00%**, **Overtake 80.00%**, **Brake 93.33%**, and **Traffic-Sign 83.68%**.
- In the latency comparison, the authors’ pure autoregressive version runs at **361ms/step**, while switching to **C2F reduces this to 48ms/step**, equivalent to saving about **86% of inference time**; meanwhile, the driving score also increases slightly from **90.66** to **91.01**.
- Compared with other methods, the C2F version has latency close to **SimLingo’s 34ms** but a higher driving score (**91.01 vs 85.07**); it is also faster than **Orion’s 65ms** while delivering better performance (**91.01 vs 77.74**).
- The abstract also claims consistent improvements in **instruction-following accuracy** and overall driving performance, but the provided excerpt does not include specific numbers for Action Dreaming or VQA/commentary.

## Link
- [http://arxiv.org/abs/2603.01441v1](http://arxiv.org/abs/2603.01441v1)
