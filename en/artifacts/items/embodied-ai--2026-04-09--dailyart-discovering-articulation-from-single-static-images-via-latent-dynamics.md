---
source: arxiv
url: http://arxiv.org/abs/2604.07758v1
published_at: '2026-04-09T03:24:07'
authors:
- Hang Zhang
- Qijian Tian
- Jingyu Gong
- Daoguo Dong
- Xuhong Wang
- Yuan Xie
- Xin Tan
topics:
- articulated-object-understanding
- single-image-reconstruction
- kinematic-joint-estimation
- novel-view-synthesis
- embodied-ai
relevance_score: 0.81
run_id: materialize-outputs
language_code: en
---

# DailyArt: Discovering Articulation from Single Static Images via Latent Dynamics

## Summary
DailyArt estimates articulated joints from one static image by first generating an opened version of the object, then reading joint structure from the difference between the closed and opened states. The paper targets image-only inference with no part masks, no CAD retrieval, and no manual joint hints at test time.

## Problem
- The task is to recover an articulated object's joint type, axis, pivot, and motion range from a single closed-state image.
- This matters for embodied AI and world models because robots need explicit kinematic structure to predict and manipulate objects, and a closed image often hides the motion cues needed to infer that structure.
- Prior work usually needs extra inputs at test time, such as multiple states, videos, masks, part graphs, retrieval candidates, or object templates.

## Approach
- DailyArt turns single-image articulation inference into a two-state reasoning problem by synthesizing a maximally opened view of the same object under the same camera view.
- Stage I uses a frozen DINOv2 image encoder and a learned VAE-style decoder. A scalar state variable `t` is injected with AdaLN so the model can generate the opened state from the closed image.
- Stage II lifts both the input image and the synthesized opened image into dense 3D point maps with VGGT, computes cross-state 3D motion seeds, filters them with confidence and displacement heuristics, and predicts all joints at once with a set-prediction transformer.
- Joint prediction uses Hungarian matching during training and outputs joint type, pivot origin, axis direction, and motion range, with up to `K=16` joint slots.
- Stage III feeds the estimated joints back into the synthesis model so it can generate part-level novel states conditioned on a chosen joint and a target motion value `t'`.

## Results
- The excerpt says DailyArt achieves strong performance on articulated joint estimation and supports part-level novel state synthesis, but it does not provide benchmark tables, dataset names, or final quantitative scores.
- The method claims image-only inference at test time without object-specific templates, multi-view inputs, explicit part annotations, masks, graphs, prompts, or declared part counts.
- The model predicts a full joint set in one forward pass, including joint type, pivot origin, axis direction, and motion limits in object-centered world coordinates.
- Stage II uses a confidence threshold of `0.85` for 3D point filtering, removes the shortest `15%` and longest `20%` of displacement seeds, and sets the joint-slot upper bound to `16`.
- Motion ranges are normalized to `[0,2]` during training, with revolute values mapped from `[-360°, 360°]` for evaluation.

## Link
- [http://arxiv.org/abs/2604.07758v1](http://arxiv.org/abs/2604.07758v1)
