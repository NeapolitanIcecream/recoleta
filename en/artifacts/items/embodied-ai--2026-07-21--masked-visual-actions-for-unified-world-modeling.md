---
source: arxiv
url: https://arxiv.org/abs/2607.19343v1
published_at: '2026-07-21T17:59:11'
authors:
- Hadi Alzayer
- Wenlong Huang
- Haonan Chen
- Christopher Luey
- Lvmin Zhang
- Maneesh Agrawala
- Gordon Wetzstein
- Li Fei-Fei
- Yilun Du
- Jiajun Wu
- Jia-Bin Huang
topics:
- robot-world-model
- masked-video-modeling
- pixel-space-actions
- embodiment-generalization
- model-based-planning
- inverse-dynamics
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Masked Visual Actions for Unified World Modeling

## Summary
Masked Visual Actions turns robot motion into partially revealed pixel-space trajectories that a pretrained video model can use to predict scene responses or infer robot behavior from desired object motion. A single checkpoint, adapted with 15 hours of real and simulated data, improves visual prediction and generalizes better to unseen robot embodiments than sparse or embodiment-specific action representations.

## Problem
- Robotic world models need to connect actions with their visual consequences and also infer actions that achieve desired outcomes.
- Existing controls such as joint commands, end-effector states, skeletons, and tracks are often sparse, embodiment-specific, or poorly aligned with the visual representations learned by video models.
- This matters because a visual, embodiment-agnostic action interface could support simulation, policy evaluation, model-based planning, and inverse control with one model.

## Approach
- Represent an action as a masked pixel-space trajectory of an entity in a video. The model receives the initial scene and the revealed trajectory, then completes the remaining entities and frames.
- Reveal robot motion to obtain a forward model that predicts object and scene responses; reveal desired object motion to obtain an inverse model that predicts compatible robot motion.
- Fine-tune Wan-Fun-Control 2.2 14B with LoRA rank 256 for about 10,000 steps using masked examples from DROID and Robocasa, totaling approximately 15 hours of data.
- Construct conditioning through robot segmentation or rendered robot meshes, enabling trajectories from different embodiments to share the same pixel-space interface.

## Results
- On DROID, Masked Visual Actions achieved LPIPS 0.0945, SSIM 0.887, and PSNR 23.74, versus Ctrl-World at 0.362, 0.708, and 18.15 respectively.
- On the unseen bimanual BEHAVIOR embodiment, it achieved LPIPS 0.123, SSIM 0.843, and PSNR 22.90, versus Ctrl-World at 0.196, 0.837, and 18.39.
- Against sparse end-effector and skeleton visualizations, it performed best on DROID, real-world data, and BEHAVIOR; on real-world data it reached LPIPS 0.148, SSIM 0.864, and PSNR 22.79, compared with skeleton visualization at 0.169, 0.866, and 21.02.
- The paper reports that imagined rollouts correlate with real execution for policy evaluation, improve candidate selection in model-based planning, and support inverse modeling, but the provided excerpt does not include their downstream task-success numbers.
- The model uses one checkpoint for forward prediction, planning, policy evaluation, and inverse motion synthesis, including zero-shot conditioning on passive object trajectories despite training masks primarily on active robotic entities.

## Link
- [https://arxiv.org/abs/2607.19343v1](https://arxiv.org/abs/2607.19343v1)
