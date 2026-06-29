---
source: arxiv
url: https://arxiv.org/abs/2605.19924v1
published_at: '2026-05-19T14:47:38'
authors:
- Shuoqin Zhang
- Yixin Xiong
- Xiru Gao
- Kai Liu
- Ke Wang
- Xichuan Zhou
- Zhe Hu
topics:
- robot-rl
- human-in-the-loop
- illumination-robustness
- world-model-relighting
- offline-fine-tuning
- real-robot-manipulation
relevance_score: 0.58
run_id: materialize-outputs
language_code: en
---

# RoHIL: Robust Human-in-the-Loop Robotic Reinforcement Learning Against Illumination Variations

## Summary
RoHIL adapts a solved human-in-the-loop robot RL policy to new lighting conditions using only existing robot data. It relights recorded trajectories, mixes relit and original data during offline fine-tuning, and anchors the policy to the original model to reduce forgetting.

## Problem
- HIL-SERL can reach near-perfect success on the workstation where it was trained, then fail when lamp position, daylight, shadows, or highlights change a few meters away.
- Re-collecting demonstrations and running human-in-the-loop RL for each workstation makes deployment cost grow with the number of workstations.
- Naive offline fine-tuning on shifted-light data can damage the original workstation policy through catastrophic forgetting.

## Approach
- RoHIL starts with one source-workstation HIL-SERL run and does all adaptation offline, with no extra real-robot interaction.
- It uses Cosmos-Transfer1-DiffusionRenderer to relight recorded RGB streams under 4 HDRI target lighting conditions while keeping the real actions, rewards, and done labels unchanged.
- Illumination-Retention Replay mixes original-light policy data with relit policy and demo data; the reported best retention setting is alpha = 0.75.
- The critic adds a feature anchor against the frozen source model, and the actor adds a mean-action anchor against the frozen source policy.
- Fine-tuning uses L_Critic = L_Bellman + L_feat and L_Actor = L_SAC + L_mse, with anchor weights lambda_feat = 0.2 and beta_mse = 0.1.

## Results
- The paper evaluates 4 real-robot Franka Panda tasks: ram_insertion, usb_insertion, circuit_breaker, and table_wiping.
- Evaluation covers 10 illumination conditions, including 5 HDRI maps, 3 task-light spotlight configurations, and 2 natural-window-light shifts.
- RoHIL fine-tunes for 15,000 offline steps after source HIL-SERL training budgets of 60k steps for RAM, 30k for USB, 35k for circuit-breaker, and 95k for table wiping.
- On USB insertion with alpha = 0.75, the anchored objective reaches 1.00 source success and 1.00 shifted-light success around 15,000 steps; standard SAC fine-tuning ends much lower at 0.57 source and 0.73 shifted-light success in the reported training sweep.
- In the USB anchor ablation over 30 trajectories, no anchor gets 0.77 source and 0.67 shifted-light success; feature anchor only gets 0.57 and 0.97; action-mean anchor only gets 1.00 and 0.80; both anchors get 1.00 and 1.00 with mean successful episode times of 2.75 s source and 2.48 s shifted-light.
- DiffusionRenderer relights 8,000 transitions in 6.82 h with 26.80 GB peak VRAM, compared with UniRelight at 48.63 h and 39.88 GB for the same camera stream.

## Link
- [https://arxiv.org/abs/2605.19924v1](https://arxiv.org/abs/2605.19924v1)
