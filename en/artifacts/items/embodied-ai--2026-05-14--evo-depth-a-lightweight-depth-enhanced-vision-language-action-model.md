---
source: arxiv
url: https://arxiv.org/abs/2605.14950v1
published_at: '2026-05-14T15:21:36'
authors:
- Tao Lin
- Yuxin Du
- Jiting Liu
- Nuobei Zhu
- Yunhe Li
- Yuqian Fu
- Yinxinyu Chen
- Hongyi Cai
- Zewei Ye
- Bing Cheng
- Kai Ye
- Yiran Mao
- Yilei Zhong
- MingKang Dong
- Junchi Yan
- Gen Li
- Bo Zhao
topics:
- vision-language-action
- robot-manipulation
- implicit-depth
- multi-view-rgb
- generalist-robot-policy
- depth-enhanced-vla
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Evo-Depth: A Lightweight Depth-Enhanced Vision-Language-Action Model

## Summary
Evo-Depth is a 0.9B-parameter VLA model that adds RGB-derived depth cues to improve robot manipulation that needs accurate spatial control. It claims higher simulation and real-world success than larger VLA baselines, with lower memory use and faster inference.

## Problem
- 2D-only VLA policies lose accuracy on grasping, placement, and object-object interaction tasks that need depth and relative position.
- Depth cameras, point clouds, and heavy geometry models add hardware, latency, memory cost, and noise sensitivity.
- The paper targets deployable manipulation policies that get spatial cues from existing multi-view RGB cameras.

## Approach
- IDEM reads multi-view RGB images and extracts compact latent depth features using a 0.13B plain Vision Transformer initialized from an any-view depth encoder.
- Early IDEM layers attend within each camera view; later layers mix within-view and cross-view attention so the model can relate objects across views.
- A pretrained InternVL3-1B vision-language backbone encodes images and the instruction; the paper keeps the first 14 language layers for control.
- SEM turns IDEM depth features into FiLM-style scale and shift terms, then modulates the vision-language tokens instead of concatenating large 3D features.
- A flow-matching Diffusion Transformer action expert predicts future actions, trained with three stages: SEM/action expert, then IDEM alignment, then end-to-end tuning.

## Results
- Meta-World: Evo-Depth reaches 84.4% average success with 0.9B parameters; Evo-1 reports 80.6% at 0.8B, and RoboTron Mani reports 77.7% at 4B.
- VLA-Arena: Evo-Depth reaches 41.1% total success; OpenVLA-OFT reports 39.9% at 7B, OpenVLA reports 39.6% at 7B, and UniVLA reports 38.7% at 7B.
- LIBERO: Evo-Depth reaches 95.4% average success with no robotic-data pretraining; UniVLA reports 95.2% at 7B, and DepthVLA reports 94.9% at 4.1B.
- LIBERO-Plus: Evo-Depth reaches 69.6% average success; the next listed baseline, π0-Fast, reports 53.6%.
- Real-world tests: Evo-Depth reports 90% average success across three tasks, 3.2 GB GPU memory use, and 12.3 Hz inference, with the smallest model size among compared methods.

## Link
- [https://arxiv.org/abs/2605.14950v1](https://arxiv.org/abs/2605.14950v1)
