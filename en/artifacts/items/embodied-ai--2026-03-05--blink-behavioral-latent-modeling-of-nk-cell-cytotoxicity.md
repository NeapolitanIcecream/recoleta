---
source: arxiv
url: http://arxiv.org/abs/2603.05110v1
published_at: '2026-03-05T12:29:57'
authors:
- Iman Nematollahi
- Jose Francisco Villena-Ossa
- Alina Moter
- Kiana Farhadyar
- Gabriel Kalweit
- Abhinav Valada
- Toni Cathomen
- Evelyn Ullrich
- Maria Kalweit
topics:
- world-model
- cell-dynamics
- time-series-modeling
- fluorescence-microscopy
- latent-state-space
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# BLINK: Behavioral Latent Modeling of NK Cell Cytotoxicity

## Summary
BLINK proposes a latent dynamics model for the process by which NK cells kill tumors, shifting cytotoxicity prediction from “single-frame discrimination” to “trajectory-level state inference.” It introduces the world-model idea into time-series fluorescence microscopy to more accurately estimate and forecast cumulative apoptosis outcomes.

## Problem
- The problem it addresses is: how to estimate the **cumulative cytotoxic outcome** caused by NK cells on tumor cells from **time-resolved microscopy sequences**, rather than only detecting death events in individual frames.
- This matters because NK-cell killing is a process that **accumulates over time and depends on contact history and latent cellular states**; frame-wise classification ignores the dynamic chain from migration and contact to activation and apoptosis induction.
- Traditional manual trajectory inspection and endpoint/population-level measurements scale poorly and make it difficult to reveal behavioral heterogeneity and temporal structure at the single-cell level.

## Approach
- The core method is a **trajectory-level recurrent state-space model (RSSM)** inspired by DreamerV2: it encodes each frame of an NK-tumor interaction crop into a latent state and uses the NK cell’s 2D displacement between adjacent frames as the “action” to model latent interaction dynamics.
- The model learns both the **posterior latent variables** (the state when observing the current image) and the **prior dynamics model** (the prediction of the next state without seeing future images), so it can not only fit the past but also perform future rollout prediction in latent space.
- A two-layer MLP is attached on top of the latent state; rather than directly regressing total cytotoxicity, it predicts per-frame **non-negative apoptosis increments**, which are then accumulated into cumulative cytotoxicity, structurally ensuring that predictions are **monotonically increasing**.
- The training objective jointly includes three parts: image reconstruction, latent-variable KL regularization, and cumulative cytotoxicity supervision (Huber loss), enabling end-to-end learning.
- The authors also use the latent representation for unsupervised clustering to analyze whether interpretable behavioral modes and phase transitions emerge.

## Results
- On trajectory-level cumulative cytotoxicity prediction on the test set, **BLINK outperforms all baselines**: MAE **0.60±0.07**, RMSE **0.81±0.08**, Pearson correlation **0.77±0.05**, proportion within **±1 outcome** of **80.7%±5.2%**, and 30-frame future prediction error F-MAE30 **0.05±0.01**.
- Compared with the strongest deterministic baseline, **GRU-monotone**, BLINK improves from **MAE 0.74±0.09 → 0.60±0.07**, **RMSE 1.04±0.11 → 0.81±0.08**, **correlation 0.57±0.04 → 0.77±0.05**, **±1 outcome hit rate 71.9%±3.3% → 80.7%±5.2%**, and **F-MAE30 0.22±0.04 → 0.05±0.01**.
- Compared with **BLINK-no-action**, adding the NK motion action also improves performance: MAE **0.80±0.06 → 0.60±0.07**, RMSE **1.14±0.09 → 0.81±0.08**, correlation **0.61±0.04 → 0.77±0.05**, ±1 outcome **69.4%±7.3% → 80.7%±5.2%**, F-MAE30 **0.09±0.01 → 0.05±0.01**.
- The single-frame autoencoding baseline **FrameAE** is clearly weaker (MAE **0.95±0.11**, correlation **0.32±0.07**), supporting the authors’ claim that “**trajectory-level temporal modeling is more critical than frame-level methods**.”
- The authors claim the model also learns interpretable behavioral modes: unsupervised clustering yields four window-state classes — **High Cytotoxic** (average outcome **0.56**, speed **5.60**, share **12.9%**), **Motile** (**0.26**, **5.67**, **19.2%**), **Low Cytotoxic** (**0.13**, **1.55**, **43.0%**), and **Quiescent** (**0.09**, **1.44**, **24.9%**); test trajectories show structured transitions from high-killing states toward low-cytotoxicity/quiescent states.

## Link
- [http://arxiv.org/abs/2603.05110v1](http://arxiv.org/abs/2603.05110v1)
