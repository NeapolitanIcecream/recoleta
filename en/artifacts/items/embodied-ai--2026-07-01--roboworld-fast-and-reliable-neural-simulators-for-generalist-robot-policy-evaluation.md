---
source: arxiv
url: https://arxiv.org/abs/2607.01060v1
published_at: '2026-07-01T15:22:41'
authors:
- Byeongguk Jeon
- Seonghyeon Ye
- JaeHyeok Doo
- Sungdong Kim
- Minjoon Seo
- Hyungmok Son
- Kimin Lee
topics:
- robot-policy-evaluation
- video-world-models
- vision-language-action
- generalist-robot-policy
- neural-simulation
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# RoboWorld: Fast and Reliable Neural Simulators for Generalist Robot Policy Evaluation

## Summary
RoboWorld evaluates generalist robot policies by running them inside a fast action-conditioned video world model and scoring generated rollouts with a task-progress VLM rubric. It reports close agreement with real RoboArena policy rankings without physical rollouts.

## Problem
- Generalist robot policies need many trials across tasks, objects, and environments, which makes real-robot evaluation slow and costly.
- Hand-built simulators need asset and environment engineering, and their sim-to-real gaps can change policy rankings.
- Video world models can generate policy rollouts, but long-horizon artifacts, slow denoising, and binary VLM scoring can turn model errors into false policy failures.

## Approach
- The system trains an autoregressive video world model on DROID, initialized from Wan2.1-T2V-1.3B, with causal attention, action cross-attention, and per-frame noise schedules.
- Step Forcing trains the model with the same few-step denoising schedule used at inference, so 4-step rollout conditions match training more closely.
- Step Forcing creates one-step self-forwarded priors, which expose the model to its own imperfect contexts during training without running full sequential rollouts.
- Anchor steps mix in noisy ground-truth contexts, keeping action-observation dynamics tied to data instead of model-induced states.
- RoboWorld runs policies in closed loop: policy action, generated next multi-view observation, policy action again. A VLM judge, GPT-4o by default, assigns a 0-5 task-progress score and uses the wrist view to detect world-model artifacts.

## Results
- On RoboArena, RoboWorld evaluated 8 open-sourced policies with 4,186 generated rollouts and matched the real-world leaderboard with Pearson r=0.989 and Spearman rho=0.970.
- The full RoboArena-style neural evaluation took 100 H100 GPU hours, including policy action generation and world-model rollout.
- The task-progress VLM rubric reached Spearman rho=0.970 against the RoboArena ranking; replacing it with binary success scoring dropped rho to 0.922.
- On BAIR Robot Pushing, Step Forcing with 4 denoising steps reached SSIM 0.8063 ID and 0.7374 OOD, and LPIPS 0.0525 ID and 0.0768 OOD. Teacher Forcing with 8 steps had SSIM 0.7942 ID and 0.7118 OOD, and LPIPS 0.0554 ID and 0.1058 OOD.
- On 300-frame, 20-second RoboArena video generation, autoregressive Step Forcing ran at 15.31 FPS; 4-step bidirectional baselines ran at 5.70 FPS. The paper reports the best LPIPS overall and the best SSIM and FVD among 4-step methods.
- On DROID wrist-view ablations, the full method had FVD 231.0. Removing the self-forwarded prior raised FVD to 258.5, and removing anchor steps raised FVD to 294.0.

## Link
- [https://arxiv.org/abs/2607.01060v1](https://arxiv.org/abs/2607.01060v1)
