---
source: arxiv
url: https://arxiv.org/abs/2606.18955v1
published_at: '2026-06-17T11:37:59'
authors:
- Runze Xu
- Yiluo Zhang
- Jian Wang
- Yu Wang
- Jincheng Yu
topics:
- vision-language-action
- latent-action
- human-egovideo
- cross-embodiment
- robot-data-scaling
- dual-arm-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Motion-Focused Latent Action Enables Cross-Embodiment VLA Training from Human EgoVideos

## Summary
This paper proposes a VLA training method that learns motion intent from unlabeled human egocentric videos and adapts to robots with about 50 trajectories per task. Its main claim is that masked latent action tokens can transfer across human, single-arm robot, and dual-arm robot embodiments.

## Problem
- Generalist VLA models need large robot datasets with action labels, which are expensive to collect and hard to align across robot bodies.
- Human egocentric manipulation videos are abundant, but most lack hand pose or robot action labels, so standard VLA training cannot use them directly.
- Existing latent-action video methods can encode background changes, camera motion, and other visual noise as action tokens, which weakens human-to-robot transfer.

## Approach
- The method trains a hybrid disentangled VQ-VAE on adjacent video frames spaced 1 second apart, using frozen DINOv2 features and separate action and background latent branches.
- It uses physical masks from SAM2 for human hands or RoboEngine for robot arms so the action branch reconstructs foreground motion while the background branch reconstructs scene regions.
- The action and background codebooks each have size 16; each frame pair is encoded as 4 discrete latent action tokens.
- A Prismatic-7B VLM is pre-trained to predict those latent action tokens from an image and language instruction, so the VLM learns motion intent without action labels.
- During robot adaptation, LoRA updates the VLM, a flow-matching action expert predicts robot controls, and DINOv2 visual features plus proprioception provide state feedback to reduce action hallucination.

## Results
- On LIBERO simulation, the full method reaches 91.8% average success across Spatial, Object, Goal, and Long suites, above villa-x at 90.1%, UniVLA-Bridge at 88.1%, pi0-fast at 85.5%, OpenVLA at 76.5%, and Diffusion Policy at 72.4%.
- On LIBERO, it scores 95.5% Spatial, 94.0% Object, 93.5% Goal, and 84.0% Long. It beats villa-x by 2.0 points on Goal and 9.5 points on Long, while villa-x is higher on Spatial and Object.
- The LIBERO ablation without DINO state features drops from 91.8% to 85.4% average, supporting the intent-perception split.
- On RoboTwin 2.0 dual-arm simulation, the method reaches 67.7% average success across 10 tasks, compared with pi0 at 65.2%, UniVLA at 63.6%, RDT at 52.5%, ACT at 51.2%, and Diffusion Policy at 49.7%.
- On RoboTwin 2.0, removing DINO state features gives 62.8% average, and freezing the VLM during post-training gives 52.4%, compared with 67.7% for the full method.
- The downstream adaptation setting uses 50 trajectories per task on LIBERO and RoboTwin 2.0, while pre-training uses only unlabeled video data without action labels.

## Link
- [https://arxiv.org/abs/2606.18955v1](https://arxiv.org/abs/2606.18955v1)
