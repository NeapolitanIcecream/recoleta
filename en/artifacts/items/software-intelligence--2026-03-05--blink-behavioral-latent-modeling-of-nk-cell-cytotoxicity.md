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
- computational-biology
- state-space-models
- world-models
- time-series-microscopy
- cell-dynamics
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# BLINK: Behavioral Latent Modeling of NK Cell Cytotoxicity

## Summary
BLINK proposes a latent dynamics model for modeling the process by which NK cells kill tumors, shifting cytotoxicity prediction from single-frame discrimination to trajectory-based temporal inference over entire sequences. It encodes microscopy time series into rollable latent states and predicts apoptotic outcomes in a monotonically accumulating manner.

## Problem
- This work addresses the question of how to estimate NK cell–induced cumulative tumor cell death from long-duration, multi-channel fluorescence microscopy sequences **at the single-cell trajectory level**, rather than performing only single-frame death detection.
- This matters because NK cell killing efficacy is determined by a **dynamic process** involving migration, contact, interaction, and apoptosis induction; frame-by-frame classification alone ignores history dependence, partial observability, and the monotonic cumulative nature of the outcome.
- Traditional bulk assays, endpoint measurements, and manual trajectory inspection are difficult to scale and also struggle to reveal different NK behavioral modes and their temporal structure.

## Approach
- The core method is a **recurrent state-space world model** inspired by DreamerV2: each frame of an NK-tumor interaction image is encoded into a latent state, and a recurrent dynamics model updates that state over time.
- The model treats the problem as a partially observable process: observations are multi-channel microscopy images, actions are the NK cell’s 2D displacement in the imaging plane, and the latent state represents interaction stages and internal cellular conditions that cannot be directly observed.
- A two-layer MLP is attached on top of the latent state. Instead of directly regressing cumulative death, it predicts a **non-negative apoptosis increment** for each frame; summing these increments yields the cumulative cytotoxic outcome, thereby naturally enforcing monotonicity.
- Training jointly optimizes three components: image reconstruction, consistency between the latent posterior and prior (KL regularization), and a Huber supervised loss on cumulative cytotoxic outcomes.
- Because the model learns latent prior transitions under missing observations, it can not only estimate current outcomes but also perform latent rollout prediction for the next 30 frames and produce interpretable behavioral-mode embeddings.

## Results
- The dataset consists of roughly **10 hours** of NK-PC3/PSMA coculture time-series microscopy data with **60 s** temporal resolution; there are **485/29/57** training/validation/test trajectories, totaling about **250,000** frames.
- For trajectory-level cumulative cytotoxicity prediction on the test set, **BLINK** achieves **MAE 0.60±0.07**, **RMSE 0.81±0.08**, **Pearson 0.77±0.05**, and **Within ±1 = 80.7%±5.2%**, outperforming **BLINK-no-action** (0.80/1.14/0.61/69.4%) and **GRU-monotone** (0.74/1.04/0.57/71.9%).
- For future prediction, BLINK reaches **F-MAE30 = 0.05±0.01**, outperforming **BLINK-no-action 0.09±0.01**, **GRU-monotone 0.22±0.04**, and **Mean 0.24±0.05**, indicating that its latent dynamics are better suited for forward-looking rollout prediction.
- Compared with non-temporal/non-monotonic baselines, **FrameAE** achieves only **MAE 0.95±0.11** and **Corr 0.32±0.07**; **GRU-regress** collapses to near-zero predictions, with **MAE 1.25±0.14, Corr 0.00**, supporting the authors’ argument for the necessity of “temporal modeling + monotonic increment constraints.”
- Unsupervised clustering in latent space identifies **4 behavioral modes**: High Cytotoxic (mean outcome **0.56**, speed **5.60**, share **12.9%**), Motile (**0.26**, **5.67**, **19.2%**), Low Cytotoxic (**0.13**, **1.55**, **43.0%**), and Quiescent (**0.09**, **1.44**, **24.9%**); test trajectories show structured transitions from highly cytotoxic states to low-activity/quiescent states.
- The authors claim this is the **first** application of a latent recurrent state-space world model to modeling NK-tumor interactions in time-series fluorescence microscopy, unifying outcome estimation, future prediction, and interpretable behavioral representations within a single framework.

## Link
- [http://arxiv.org/abs/2603.05110v1](http://arxiv.org/abs/2603.05110v1)
