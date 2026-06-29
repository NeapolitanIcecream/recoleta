---
source: arxiv
url: http://arxiv.org/abs/2604.04198v1
published_at: '2026-04-05T17:43:16'
authors:
- Mengmeng Liu
- Diankun Zhang
- Jiuming Liu
- Jianfeng Cui
- Hongwei Xie
- Guang Chen
- Hangjun Ye
- Michael Ying Yang
- Francesco Nex
- Hao Cheng
topics:
- autonomous-driving
- world-model
- video-action-model
- zero-shot-generalization
- diffusion-transformer
relevance_score: 0.63
run_id: materialize-outputs
language_code: en
---

# DriveVA: Video Action Models are Zero-Shot Drivers

## Summary
DriveVA is a driving world model that generates future video and the ego trajectory together, using a pretrained video generator as the base. The paper claims this joint video-action setup improves closed-loop driving and transfers better across datasets and domains without target-domain fine-tuning.

## Problem
- Autonomous driving models often fail under unseen roads, traffic patterns, sensor setups, and domain shifts, which blocks real deployment.
- Prior world-model planners usually predict future visuals and future actions in separate or weakly connected modules, so the planned trajectory can drift away from the imagined scene.
- Vision-language pretraining on static image-text data gives semantic knowledge, but weaker motion and causal priors for planning over time.

## Approach
- DriveVA conditions on recent camera history, ego velocity, and a language command, then predicts a short future rollout of both video latents and action tokens in one shared generative process.
- The model uses a pretrained Wan2.2 video VAE and text encoder, then a single DiT decoder jointly generates future video latents and trajectory tokens with conditional flow matching.
- Actions are 3D tokens for future ego pose `(x, y, yaw)`, trained together with future video tokens so the trajectory stays aligned with the generated scene evolution.
- A video continuation strategy rolls out short clips recurrently from a history buffer, which is meant to keep longer-horizon predictions consistent.
- The paper reports that dense video supervision is a main source of planning gain: adding video supervision raises NAVSIMv1 PDMS from 71.4 to 90.9, a gain of 19.5 points over action-only optimization.

## Results
- On NAVSIM v1, DriveVA reaches **90.9 PDMS** in closed-loop evaluation. In the shown table, this is above DiffusionDrive at **88.1**, ReCogDrive-IL at **86.5**, Epona at **86.2**, and LAW at **84.6**.
- In zero-shot cross-dataset transfer from NAVSIM training to **nuScenes**, DriveVA reduces **average L2 error by 78.9%** and **collision rate by 83.3%** relative to the stated state-of-the-art world-model planner.
- In zero-shot real-to-sim transfer from NAVSIM to **Bench2Drive / CARLA v2**, it reduces **average L2 error by 52.5%** and **collision rate by 52.4%** against the same class of baseline.
- The model is generative, but the paper states that **2 sampling steps** already give near-optimal closed-loop performance.
- The paper’s strongest claim is that joint video-action generation, rather than action prediction alone, is what drives the planning improvement and the zero-shot transfer gains.

## Link
- [http://arxiv.org/abs/2604.04198v1](http://arxiv.org/abs/2604.04198v1)
