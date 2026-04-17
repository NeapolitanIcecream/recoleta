---
source: arxiv
url: http://arxiv.org/abs/2604.05656v1
published_at: '2026-04-07T09:56:03'
authors:
- Wuyang Luan
- Junhui Li
- Weiguang Zhao
- Wenjian Zhang
- Tieru Wu
- Rui Ma
topics:
- vision-language-action
- flow-matching
- robot-inference-acceleration
- self-distillation
- generalist-robot-policy
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# SnapFlow: One-Step Action Generation for Flow-Matching VLAs via Progressive Self-Distillation

## Summary
SnapFlow cuts flow-matching VLA action generation from 10 denoising steps to 1 step with a self-distillation recipe that keeps or slightly improves task success. The paper targets inference latency in large robot policies such as \(\pi\)0.5 and SmolVLA.

## Problem
- Flow-matching VLAs generate actions with iterative denoising, usually 10 Euler steps, and this dominates inference time. For \(\pi\)0.5, denoising takes about 241 ms out of 274 ms end to end, or 80% of latency.
- Naively dropping to 1 step is unreliable because the model was trained to predict local velocities for multi-step integration, not a single large jump from noise to action.
- This matters for robot control because edge and real-time settings have tight control-cycle budgets; the paper gives 3 Hz control as an example, where 330 ms must cover both perception and action generation.

## Approach
- SnapFlow trains the same flow-matching VLA to do two jobs: standard flow matching for local velocity prediction and a consistency-style shortcut objective for direct 1-step action generation.
- The shortcut target is a two-step Euler estimate built from the model’s own marginal velocity predictions at time 1 and 0.5, instead of using conditional velocities that the paper argues cause trajectory drift.
- Training mixes the original flow-matching loss and the shortcut loss, so the model keeps its velocity estimator while learning accurate one-step jumps.
- A zero-initialized target-time embedding tells the network whether it should act like the original local denoiser or the new one-step generator, without changing the main architecture.
- The method is plug-and-play for existing flow-matching VLAs, needs no external teacher, and trains only the action expert plus the new target-time embedding; the paper reports about 30k steps and about 12 hours on one A800.

## Results
- On \(\pi\)0.5 (3B) over 4 LIBERO suites, 40 tasks, and 400 episodes, SnapFlow at 1 step reaches **98.75%** average success versus the 10-step baseline at **97.75%** and naive 1-step at **96.75%**.
- For \(\pi\)0.5 latency on A800, end-to-end time drops from **274 ms** to **83 ms**, a **3.3x** end-to-end speedup; denoising speedup is reported as **9.6x**.
- On \(\pi\)0.5 offline LIBERO metrics, MSE improves from **0.01169** to **0.00773** (**-33.9%**), standard deviation from **0.05412** to **0.02964** (**-45.2%**), P95 MSE from **0.02357** to **0.01664** (**-29.4%**), and cosine similarity from **0.9885** to **0.9916**.
- Per-suite \(\pi\)0.5 LIBERO success changes are: Spatial **98.0% -> 99.0%**, Object **100.0% -> 100.0%**, Goal **96.0% -> 99.0%**, Long-10 **97.0% -> 97.0%**.
- On SmolVLA (500M), SnapFlow lowers PushT MSE from **0.468** to **0.429** (**-8.3%**), raises cosine similarity from **0.765** to **0.818** (**+6.9%**), and gives **3.56x** end-to-end acceleration.
- In an action-step sweep on long-horizon tasks, SnapFlow keeps an advantage across execution horizons; the abstract reports **93%** success at **n_act = 5** versus **90%** for the baseline.

## Link
- [http://arxiv.org/abs/2604.05656v1](http://arxiv.org/abs/2604.05656v1)
