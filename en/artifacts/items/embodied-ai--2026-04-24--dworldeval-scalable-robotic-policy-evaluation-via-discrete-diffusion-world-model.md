---
source: arxiv
url: http://arxiv.org/abs/2604.22152v1
published_at: '2026-04-24T01:50:53'
authors:
- Yaxuan Li
- Zhongyi Zhou
- Yefei Chen
- Yaokai Xue
- Yichen Zhu
topics:
- robot-policy-evaluation
- world-model
- discrete-diffusion
- vision-language-action
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# dWorldEval: Scalable Robotic Policy Evaluation via Discrete Diffusion World Model

## Summary
dWorldEval is a robot policy evaluator built as a discrete diffusion world model. It predicts future observations and a task-progress token from language, images, and actions in one token sequence, with the goal of ranking robot policies without running them in every environment.

## Problem
- Evaluating robot policies at large scale is expensive with real rollouts and asset-heavy simulators, especially across many tasks and environments.
- Prior world-model evaluators often fail as proxies because they do not follow robot actions well under out-of-distribution or failed behaviors, and they drift over long horizons.
- This matters because policy ranking becomes unreliable when the model hallucinates success, misses failures, or breaks spatial and temporal consistency.

## Approach
- The model maps vision, language, and robot action chunks into one discrete token space and predicts them with a single transformer denoiser, so actions are first-class inputs rather than weak side conditions.
- It uses masked discrete diffusion to reconstruct future tokens, jointly generating the next visual state and a discrete progress token.
- A sparse keyframe memory stores low-resolution history frames with explicit frame-index tokens to reduce long-horizon drift and keep object layout consistent.
- During training, task progress is converted into discrete text-like tokens using milestone-based scoring; at inference, success is declared when the predicted progress reaches 1.
- The paper also introduces **Δ-LPIPS**, a metric that scores how well predicted state changes match ground-truth state changes under the given action sequence.

## Results
- On LIBERO action controllability, dWorldEval reports the best **Δ-LPIPS** on both expert and failure subsets: **0.315 / 0.352**, compared with **WorldEval 0.423 / 0.701**, **WorldGym 0.347 / 0.650**, and **Ctrl-World 0.334 / 0.416**. Standard LPIPS is also slightly better: **0.215** vs **0.262 / 0.218 / 0.220**.
- For long-horizon round-trip consistency, the full model beats its no-memory ablation across action horizons **H=5,10,15,20** with LPIPS **0.130, 0.145, 0.193, 0.243** versus **0.177, 0.186, 0.302, 0.411**.
- In the full consistency comparison against prior methods, dWorldEval again has the lowest round-trip LPIPS: at **H=20**, **0.243** vs **WorldEval 0.531**, **WorldGym 0.482**, **Ctrl-World 0.370**.
- As a policy-evaluation proxy, estimated success rates correlate strongly with real execution: **r=0.910** on LIBERO multi-view, **r=0.927** on RoboTwin, and **r=0.918** on real-world tasks. The introduction also states **Pearson r ≈ 0.9** overall.
- On LIBERO single-view ranking, the paper reports minimal rank violation for dWorldEval with **MMRV = 0.013**, while baselines reach **up to 0.039**.
- The experiments use **LIBERO** (5.5k expert demos plus **1k** failed rollouts), **RoboTwin** (**5.5k** trajectories across **10** tasks), and a real bimanual robot dataset with **5.2k** trajectories including **1k** failures across **5** tasks.

## Link
- [http://arxiv.org/abs/2604.22152v1](http://arxiv.org/abs/2604.22152v1)
