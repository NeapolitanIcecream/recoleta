---
source: arxiv
url: https://arxiv.org/abs/2604.26848v2
published_at: '2026-04-29T16:13:39'
authors:
- Yuxuan Tian
- Yurun Jin
- Bin Yu
- Yukun Shi
- Hao Wu
- Chi Harold Liu
- Kai Chen
- Cong Huang
topics:
- vision-language-action
- robot-world-model
- diffusion-policy
- geometric-attention
- bimanual-manipulation
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# STARRY: Spatial-Temporal Action-Centric World Modeling for Robotic Manipulation

## Summary
STARRY is a VLA robot policy that couples future world prediction with action generation for manipulation. It reports higher success on RoboTwin 2.0 and real bimanual tasks by adding 3D geometry-guided attention to a joint diffusion policy.

## Problem
- Reactive VLA policies often map current RGB-D observations and language directly to actions, which hurts tasks that need future contact, timing, and object-geometry reasoning.
- Prior world-model policies can predict future video or latent states, but those predictions may ignore action-critical regions such as handles, openings, contact surfaces, and the space near the end effector.
- The paper targets failures in spatially constrained manipulation, where small 3D alignment errors can cause collisions, unstable grasps, or failed placement.

## Approach
- STARRY jointly denoises future spatial-temporal latents and future action sequences over the same horizon with a diffusion policy.
- Its Spatial-Temporal World Model builds inputs from multi-view RGB, depth, projected 3D end-effector trajectories, and historical actions, then predicts future latent states used by the action branch.
- A Geometry Expert predicts future depth maps and end-effector positions during diffusion.
- GASAM unprojects predicted depth into 3D, computes each visual token’s distance to the predicted end effector, converts those distances into token weights, and biases action-to-video attention toward nearby geometry-relevant regions.
- Training uses staged pretraining, action and geometry learning, and joint finetuning, with initialization from Wan for video diffusion and Qwen-VL for visual-language understanding.

## Results
- On RoboTwin 2.0 across 50 bimanual tasks, STARRY reports 93.82% Clean and 93.30% Randomized average success. Baselines: LingBot-VA 92.93% / 91.55%, Motus 88.66% / 87.02%, X-VLA 72.80% / 72.84%, and pi-0.5 62.86% / 60.30%.
- On Handover Mic, STARRY reaches 100% / 99%, compared with Motus at 78% / 63% and pi-0.5 at 63% / 57.5%.
- On Hanging Mug, STARRY reaches 69% / 72%, compared with LingBot-VA at 40% / 28%, Motus at 38% / 38%, X-VLA at 23% / 27%, and pi-0.5 at 10.5% / 10%.
- On Press Stapler, STARRY reaches 100% / 100%, compared with LingBot-VA at 85% / 82%, Motus at 93% / 98%, X-VLA at 92% / 98%, and pi-0.5 at 83.5% / 76.5%.
- In real-world experiments on three ARX R5 bimanual tasks, the paper reports average success improving from 42.5% with pi-0.5 to 70.8% with STARRY, using 50 demonstrations per task and 20 evaluation rollouts per method.

## Link
- [https://arxiv.org/abs/2604.26848v2](https://arxiv.org/abs/2604.26848v2)
