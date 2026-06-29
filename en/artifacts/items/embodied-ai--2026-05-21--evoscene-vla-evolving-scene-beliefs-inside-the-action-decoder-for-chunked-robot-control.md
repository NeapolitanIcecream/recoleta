---
source: arxiv
url: https://arxiv.org/abs/2605.21862v1
published_at: '2026-05-21T01:19:17'
authors:
- Chushan Zhang
- Ruihan Lu
- Jinguang Tong
- Xuesong Li
- Yikai Wang
- Hongdong Li
topics:
- vision-language-action
- generalist-robot-policy
- world-model
- robot-data-scaling
- sim2real
- embodied-foundation-model
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# EvoScene-VLA: Evolving Scene Beliefs Inside the Action Decoder for Chunked Robot Control

## Summary
EvoScene-VLA is a chunked robot VLA policy that carries an action-updated scene state across control calls. It improves RoboTwin average success over a depth-supervised LingBot-VLA baseline by +1.9 points in fixed scenes and +2.4 points with randomized layouts.

## Problem
- Chunked VLA policies predict many robot actions from one visual update, so contact, occlusion, and moved objects can make later actions use stale scene geometry.
- Spatial VLAs improve single-frame geometry, and temporal VLAs store past observations, but the policy still lacks a compact scene state updated by its own recent actions.
- This matters for manipulation tasks where the robot changes the scene during a chunk, such as opening a microwave, stacking blocks, or placing objects into cabinets.

## Approach
- The method adds a recurrent scene prefix to the VLM input: observation slots read current multi-view images, and prior slots carry the scene state from the previous chunk.
- The VLM corrects the carried prior using the new observation, then the action decoder predicts both the next action chunk and future scene tokens in one flow-matching denoising pass.
- The final predicted scene token becomes the prior for the next control call, so inference needs no separate scene predictor or memory module.
- Training uses a Local Anchor with masked depth reconstruction from a frozen monocular depth teacher, plus a Global Anchor that matches frozen 3D foundation model features.
- A training-only Scene Predictor maps current scene tokens and actions to future scene-token targets, which are distilled into the action decoder through a scene flow-matching loss.

## Results
- On 31 RoboTwin tasks, EvoScene-VLA raises average success from 87.2% to 89.1% under fixed evaluation, a +1.9 point gain over the depth-supervised LingBot-VLA baseline.
- Under randomized initial positions and orientations on the same 31 RoboTwin tasks, average success rises from 86.1% to 88.5%, a +2.4 point gain.
- Against the original LingBot-VLA baseline, the reported averages improve from 85.3% to 89.1% in fixed scenes and from 84.1% to 88.5% in randomized scenes.
- Against π0.5, the reported averages improve from 81.2% to 89.1% in fixed scenes and from 75.9% to 88.5% in randomized scenes.
- Example task gains over the depth-supervised LingBot-VLA baseline include Open Microwave fixed success from 70% to 82%, Place Dual Shoes fixed success from 75% to 91%, and Stack Blocks Three randomized success from 88% to 95%.
- The excerpt says Galaxea R1-Lite real-robot trials outperform all baselines, but it does not provide the numeric real-robot table.

## Link
- [https://arxiv.org/abs/2605.21862v1](https://arxiv.org/abs/2605.21862v1)
