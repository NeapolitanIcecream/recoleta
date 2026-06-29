---
source: arxiv
url: https://arxiv.org/abs/2605.06481v1
published_at: '2026-05-07T16:06:08'
authors:
- Yushan Liu
- Peibo Sun
- Shoujie Li
- Yifan Xie
- Lingfeng Zhang
- Xintao Chao
- Shiyuan Dong
- Fang Chen
- Xiao-Ping Zhang
- Wenbo Ding
topics:
- vision-language-action
- world-action-model
- object-centric-slots
- robot-manipulation
- libero-plus
- flow-matching-actions
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# OA-WAM: Object-Addressable World Action Model for Robust Robot Manipulation

## Summary
OA-WAM makes a world-action robot policy address objects directly by splitting each object slot into a fixed identity address and a changing content state. It reports top or near-top manipulation success on LIBERO, SimplerEnv, and LIBERO-Plus scene-shift tests tied to target binding.

## Problem
- Existing World Action Models predict future scenes as images, token streams, or global latents, so target identity can get mixed with background, pose, and distractors.
- This matters because robot policies can score high on standard benchmarks while failing when camera view, layout, robot start pose, lighting, language, or sensor noise changes.
- The paper focuses on instructions that name objects, such as choosing the red mug rather than a nearby distractor.

## Approach
- Each frame is converted into N+1 slots: one robot slot and up to 16 object slots.
- Each object slot has a 32-dimensional fixed address from the language label and initial DINOv3 feature, plus a 256-dimensional content vector updated each frame from SAM 3 and DINOv3, plus time and role embeddings.
- A Chameleon-style 7B transformer processes text, image VQ tokens, proprioception, past actions, slots, and an action query in a block-causal sequence.
- Cross-slot attention keys read only the fixed address slice, and every transformer layer resets that address slice to the cached value. This keeps slot routing tied to object identity while content and pose can change.
- A world head predicts next-frame per-slot content and pose, and a flow-matching action head outputs a 16-step continuous action chunk in one pass.

## Results
- On LIBERO, OA-WAM reports 97.8% average success, above π0.5 at 96.9%, VLA-JEPA at 97.2%, and MemoryVLA at 96.5%.
- On SimplerEnv WidowX Visual Matching, it reports 79.3% average success, above CoWVLA at 76.0%, MemoryVLA at 71.9%, and InternVLA-M1 at 71.7%.
- On LIBERO-Plus, it reports 83.9% average success versus π0.5 at 85.7%; its lower overall score is mainly from Sensor Noise, where it gets 75.6% versus Cosmos-Policy at 92.7%.
- On LIBERO-Plus geometric axes, it reports Camera 80.5%, Robot init 89.6%, Layout 82.8%, and Geo Avg 84.3%, beating π0.5 Geo Avg 79.5% by 4.8 points.
- A causal slot-intervention test reports swap-binding cosine 0.87 for OA-WAM versus 0.09 or lower for eight holistic baselines.
- An ablation says removing addr-only key projection drops LIBERO-Plus Camera by 13.3 points while changing in-distribution LIBERO by 1.5 points.

## Link
- [https://arxiv.org/abs/2605.06481v1](https://arxiv.org/abs/2605.06481v1)
