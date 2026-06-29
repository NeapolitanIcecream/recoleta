---
source: arxiv
url: https://arxiv.org/abs/2605.21414v1
published_at: '2026-05-20T17:10:31'
authors:
- Shizhe Chen
- Paul Pacaud
- Cordelia Schmid
topics:
- vision-language-action
- robot-manipulation
- point-clouds
- 3d-vla
- action-decoding
- spatial-reasoning
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# PointACT: Vision-Language-Action Models with Multi-Scale Point-Action Interaction

## Summary
PointACT is a 3D-aware vision-language-action policy for robot manipulation that feeds point-cloud geometry into the action decoder. Its main claim is that action tokens need direct, repeated contact with multi-scale point features to predict precise 3D actions.

## Problem
- Existing VLAs mostly use 2D image tokens, which weakens 3D pose, contact, and spatial reasoning for manipulation.
- Prior 3D-aware VLAs often add depth or point features at a high level, so fine geometry has limited effect on the final action output.
- The problem matters because RGB-D sensing is common, and many robot tasks depend on exact geometry rather than object labels alone.

## Approach
- PointACT uses a frozen Qwen2.5-VL backbone for image and language features, plus a separate trainable action expert for control.
- A Point Transformer v3 encoder processes colored point clouds and outputs hierarchical point features at multiple scales.
- During decoding, action tokens are broadcast into spatial point windows and attend with local point tokens through bottleneck window self-attention.
- The action tokens then average information across windows and cross-attend to the VLM features, so geometry and language both condition action prediction.
- The model supports regression for delta end-effector actions and point-anchored classification for keypoint pose prediction.

## Results
- On LIBERO, PointACT reports a 96.0% average success rate across 4 suites: Spatial 97.4%, Object 99.6%, Goal 96.2%, and Long 90.6%.
- On the same LIBERO table, PointACT beats SpatialVLA by 17.9 points on average: 96.0% vs 78.1%.
- Against the reproduced EO1 baseline on LIBERO, PointACT improves average success by 2.9 points: 96.0% vs 93.1%.
- The paper reports a 10% success-rate gain on the challenging RLBench-10Tasks suite over pretrained VLA baselines, but the excerpt does not include the full RLBench table.
- The trainable PointACT module has about 300M parameters, uses up to 4096 point-cloud points after 1 cm voxelization, and trains for 20K to 50K steps with batch size 128 on 2 NVIDIA H100 GPUs.

## Link
- [https://arxiv.org/abs/2605.21414v1](https://arxiv.org/abs/2605.21414v1)
