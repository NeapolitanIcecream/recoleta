---
source: arxiv
url: https://arxiv.org/abs/2606.06155v1
published_at: '2026-06-04T13:28:51'
authors:
- Qize Yu
- Jiadi You
- Yuran Wang
- Jiaqi Liang
- Bowen Ping
- Yang Tian
- Yue Chen
- Minghong Cai
- Zeying Gong
- Ruihai Wu
- Yinchuan Li
- Junwei Liang
- Yingcong Chen
topics:
- vision-language-action
- robot-foundation-model
- affordance-learning
- generalist-robot-policy
- dexterous-manipulation
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# AffordanceVLA: A Vision-Language-Action Model Empowering Action Generation through Affordance-Aware Understanding

## Summary
AffordanceVLA adds affordance prediction to a vision-language-action robot policy so the model predicts what object to use, where to touch it, and how its 3D shape should guide action.

## Problem
- Direct VLA policies map images and language to robot actions, but VLM features are semantic while robot actions need 3D spatial control.
- Dense video prediction can add redundant pixels and slow inference, while coarse rationales often miss contact locations and geometry.
- The problem matters because manipulation fails when the policy attends to the wrong object, wrong contact region, or wrong spatial layout.

## Approach
- The model uses three transformer experts: an Understanding Expert for image-language features, an Affordance Generation Expert for task-relevant physical cues, and an Action Expert for action chunks.
- Which2Act predicts a latent for the target object crop, which pushes the model to focus on the object named by the instruction.
- Where2Act predicts a 2D affordance map, which gives the policy an explicit interaction region.
- How2Act predicts 3D shape and a 10-DoF layout vector for rotation, scale, and translation.
- Training uses 3 stages: affordance grounding pre-training, affordance-augmented robot co-training, and target-task post-training for LIBERO, CALVIN, and real-world deployment.

## Results
- The provided excerpt does not include the LIBERO or CALVIN success-rate tables, so benchmark percentages and baseline gaps are unavailable here.
- The paper claims strong simulation performance on LIBERO and CALVIN and real-world gains, but the excerpt only states this qualitatively.
- The data pipeline produces over 100,000 affordance annotations using keyframe extraction, Claude Opus 4.5, Qwen3-VL, RexOmni, SAM, and SAM-3D.
- Stage I uses affordance loss weights of 0.1 for Which2Act, Where2Act, and shape, and 0.04 for layout.
- Stage II trains with action loss weight 1.0 and affordance loss weight 0.5; Stage III lowers the affordance weight to 0.15 for task adaptation.

## Link
- [https://arxiv.org/abs/2606.06155v1](https://arxiv.org/abs/2606.06155v1)
