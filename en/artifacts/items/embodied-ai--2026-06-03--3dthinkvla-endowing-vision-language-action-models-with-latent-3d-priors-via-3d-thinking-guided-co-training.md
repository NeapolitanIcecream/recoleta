---
source: arxiv
url: https://arxiv.org/abs/2606.04436v1
published_at: '2026-06-03T04:34:07'
authors:
- Jiaxin Shi
- Xidong Zhang
- Fucai Zhu
- Zhe Li
- Siyu Zhu
- Weihao Yuan
topics:
- vision-language-action
- robot-foundation-model
- 3d-spatial-reasoning
- latent-distillation
- robot-manipulation
- 2d-to-3d
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# 3DThinkVLA: Endowing Vision-Language-Action Models with Latent 3D Priors via 3D-Thinking-Guided Co-training

## Summary
3DThinkVLA is a VLA training method that injects latent 3D geometry and spatial reasoning into action prediction while keeping inference to 2D images. It reports top or near-top success rates on LIBERO and LIBERO-PLUS using Qwen3-VL-2B with an OFT-style action head.

## Problem
- Standard VLA models predict robot actions from 2D images, so they often miss 3D relations such as object position, distance, and orientation.
- Direct 3D inputs such as point clouds or depth maps add sensor and model requirements, and direct feature alignment can damage the pretrained VLM’s vision-language alignment.
- Co-training on action data and 3D reasoning data can still fail because action prompts can cause the model to skip spatial reasoning and learn action shortcuts.

## Approach
- The model co-trains on VLA action data and 3D VLM question-answer data built around real-world images.
- A geometry adapter maps intermediate Qwen3-VL visual features into a latent space and aligns them with VGGT 3D foundation-model features using cosine similarity.
- A shared reasoning-anchor token carries spatial information. A teacher branch sees explicit 3D reasoning prompts, while a student branch sees normal action prompts.
- A reasoning adapter trains the student anchor to match the teacher anchor in latent space, so action prediction can use spatial reasoning without generating chain-of-thought text.
- The action head receives the normal action-query features plus projected geometry and reasoning features through additive fusion; at inference the VGGT teacher path is removed.

## Results
- On LIBERO, 3DThinkVLA reaches 98.7% average success, compared with 98.5% for SpatialForcing, 98.1% for 3D-CAVLA, 97.7% for GeoVLA, and 97.1% for OpenVLA-OFT.
- LIBERO suite scores are 100.0% on Spatial, 100.0% on Object, 98.8% on Goal, and 95.8% on Long.
- On LIBERO-PLUS, it reaches 81.0% average success, compared with 80.5% for ABot-M0, 75.0% for Qwen3-VL-OFT, and 69.9% for OpenVLA-OFT.
- LIBERO-PLUS perturbation scores are 73.8% Camera, 64.5% Robot, 78.0% Language, 98.4% Light, 94.8% Background, 84.7% Noise, and 81.5% Layout.
- The excerpt also claims state-of-the-art performance on SimplerEnv and real-world manipulation tasks, but it does not provide those numeric results in the supplied text.

## Link
- [https://arxiv.org/abs/2606.04436v1](https://arxiv.org/abs/2606.04436v1)
