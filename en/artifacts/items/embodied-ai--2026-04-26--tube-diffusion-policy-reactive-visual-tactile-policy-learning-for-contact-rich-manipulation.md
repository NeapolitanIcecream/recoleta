---
source: arxiv
url: http://arxiv.org/abs/2604.23609v1
published_at: '2026-04-26T08:48:26'
authors:
- Teng Xue
- Alberto Rigo
- Bingjian Huang
- Jiayi Shen
- Zhengtong Xu
- Nick Colonnese
- Amirhossein H. Memar
topics:
- contact-rich-manipulation
- visual-tactile-learning
- diffusion-policy
- reactive-control
- dexterous-manipulation
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Tube Diffusion Policy: Reactive Visual-Tactile Policy Learning for Contact-rich Manipulation

## Summary
Tube Diffusion Policy (TDP) learns a reactive visual-tactile manipulation policy for contact-rich tasks. It combines diffusion for chunk-start action generation with a learned streaming feedback flow so the robot can adjust actions at each step instead of running an open-loop action chunk.

## Problem
- Existing imitation learning methods for manipulation often generate multi-step action chunks and execute them with limited feedback inside the chunk.
- This hurts contact-rich manipulation because object geometry, friction, and contact events are uncertain, while tactile sensing arrives at high frequency and needs fast action updates.
- Slow diffusion inference also makes per-timestep replanning hard, which reduces robustness to disturbances and model mismatch.

## Approach
- TDP replaces a fixed **action chunk** with an **action tube**: a nominal action initialization plus local feedback corrections during execution.
- At the start of each chunk horizon, a diffusion model denoises to produce an initial action that accounts for nonlinear contact dynamics.
- During execution, a learned observation-conditioned velocity field streams later actions from fresh visual and tactile observations, giving step-wise corrections inside the chunk.
- The method uses a dual-time design: diffusion time for denoising and trajectory time for real-time action evolution.
- The control view is inspired by tube MPC, but TDP learns the feedback flow directly from demonstrations and does not require an explicit dynamics model.

## Results
- The paper claims TDP **consistently outperforms state-of-the-art imitation learning baselines** on the Push-T benchmark and **three additional** visual-tactile dexterous manipulation tasks.
- It reports **two real-world experiments** showing stronger reactivity under contact uncertainty and external disturbances.
- The paper states that the action-tube step-wise correction **reduces the required denoising steps**, which improves suitability for **real-time, high-frequency** feedback control.
- The provided excerpt does **not include quantitative numbers** such as success rates, error metrics, denoising-step counts, or exact baseline margins.

## Link
- [http://arxiv.org/abs/2604.23609v1](http://arxiv.org/abs/2604.23609v1)
