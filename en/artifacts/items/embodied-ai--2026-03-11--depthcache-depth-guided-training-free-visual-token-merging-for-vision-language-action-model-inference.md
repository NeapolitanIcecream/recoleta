---
source: arxiv
url: http://arxiv.org/abs/2603.10469v1
published_at: '2026-03-11T06:40:44'
authors:
- Yuquan Li
- Lianjie Ma
- Han Ding
- Lijun Zhu
topics:
- vision-language-action
- token-merging
- depth-guided
- training-free
- robot-inference
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# DepthCache: Depth-Guided Training-Free Visual Token Merging for Vision-Language-Action Model Inference

## Summary
DepthCache is a training-free visual token compression method for accelerating inference in Vision-Language-Action (VLA) models. It uses depth information to preferentially preserve the near-field manipulation area and critical boundaries, reducing inference latency while minimizing harm to robotic manipulation success rates.

## Problem
- VLA models are highly promising for robotic manipulation, but the large number of visual tokens and heavy language backbone lead to high inference latency, making real-time closed-loop control difficult.
- Existing token pruning or uniform-ratio merging methods damage spatial relationships, especially hurting tasks such as grasping and alignment that depend on fine-grained geometric reasoning.
- Existing merging methods often require modifications to the vision encoder, lack cross-architecture portability, and do not exploit the naturally available depth-structure prior in robotic scenes.

## Approach
- Use depth maps to partition unprotected image patches by distance: merge less in the near-field workspace and more in the distant background; protected tokens are not compressed.
- Use a “dual protection” mechanism to preserve critical tokens: one portion comes from cross-attention in the language model, indicating semantic importance; the other comes from depth edges, indicating geometric boundary importance.
- Instead of completing merging all at once within a single frame, distribute the merging across multiple consecutive frames to exploit temporal redundancy, maintain stable representations, and reduce computation at each step.
- Monitor depth changes; if a region becomes dynamic, restore it to full resolution. For the wrist camera, add a state machine based on end-effector motion to dynamically decide whether to apply aggressive compression.
- The entire method runs outside the vision encoder, requiring no model changes or retraining, and can be directly applied to different VLA architectures.

## Results
- On the LIBERO benchmark across 3 different VLA models, DepthCache achieves **1.07×–1.28×** inference speedup while reducing average success rate by **less than 1%**.
- For **OpenVLA**: baseline average success rate is **76.7%**; DepthCache reaches **75.7% (-1.0)** with **1.21×** speed and **78.9%** token retention. In comparison, FastV achieves **64.0% (-12.7) / 1.39×**, and SP-VLA **71.9% (-4.8) / 1.50×**.
- For **π0.5**: baseline is **97.9%**; DepthCache achieves **97.6% (-0.3) / 1.28×** with **68.2%** token retention. FastV reaches **77.6% (-20.3) / 1.30×**, and ToSA **73.8% (-24.1) / 0.94×**.
- For **GR00T**: baseline is **93.1%**; DepthCache achieves **92.9% (-0.2) / 1.07×** with **87.5%** token retention.
- Under steady-state conditions, the total patch tokens from two cameras drop from **512** to about **300**.
- On 3 core real-robot tasks (based on **π0.5**), the total number of successes changes from **55/60** to **52/60**, and average latency drops from **191 ms** to **143 ms**, achieving **1.33×** speedup.

## Link
- [http://arxiv.org/abs/2603.10469v1](http://arxiv.org/abs/2603.10469v1)
