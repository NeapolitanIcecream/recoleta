---
source: arxiv
url: https://arxiv.org/abs/2605.10485v1
published_at: '2026-05-11T12:44:26'
authors:
- Hao Wang
- Xiaobao Wei
- Jingyang He
- Chengyu Bai
- Chun-Kai Fan
- Jiajun Cao
- Jintao Chen
- Ying Li
- Shanyu Rong
- Ming Lu
- Xiaozhu Ju
- Jian Tang
- Shanghang Zhang
topics:
- vision-language-action
- spatial-grounding
- robot-manipulation
- feature-alignment
- 3d-visual-representations
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# VEGA: Visual Encoder Grounding Alignment for Spatially-Aware Vision-Language-Action Models

## Summary
VEGA improves OpenVLA-OFT by adding 3D-aware visual feature alignment during training, then removing the extra teacher and projector at inference.

## Problem
- VLA visual encoders are trained mainly on 2D image data, so they can miss depth, relative position, object height, and viewpoint cues needed for precise manipulation.
- Existing implicit spatial grounding methods align LLM-level visual tokens and require layer search; the alignment target depends on the task and mixes geometry with language context.

## Approach
- Use frozen DINOv2-FiT3D as a spatial teacher. FiT3D is DINOv2 tuned with multi-view 3D Gaussian Splatting supervision.
- Align OpenVLA-OFT's DINOv2 visual encoder output to DINOv2-FiT3D patch features through a LayerNorm plus two-layer MLP projector.
- Train with standard action prediction loss plus cosine feature alignment loss, with λ = 0.1 in the main experiments.
- Discard the teacher and projector at inference, so runtime is the same as the base VLA.

## Results
- On RoboTwin 2.0, across 6 bimanual tasks and 100 trials per task, VEGA reports 67.5% average success on Easy and 30.7% on Hard.
- It beats OFT + Spatial Forcing by 3.3 percentage points on Easy (67.5% vs 64.2%) and 2.9 points on Hard (30.7% vs 27.8%).
- Compared with OpenVLA-OFT, VEGA improves the average from 56.0% to 67.5% on Easy and from 22.7% to 30.7% on Hard.
- Task-level gains include Move Card Away Hard at 43% vs 34% for OpenVLA-OFT, Click Bell Hard at 53% vs 46%, and Place Shoe Hard at 25% vs 9%.
- Training efficiency claim: on Move Playingcard Away Easy, VEGA at 10k steps reaches about the same success rate as OpenVLA-OFT at 60k steps.
- Data efficiency claim: with 25% of demonstrations on Move Playingcard Away Easy, VEGA is 10 percentage points above OpenVLA-OFT.

## Link
- [https://arxiv.org/abs/2605.10485v1](https://arxiv.org/abs/2605.10485v1)
