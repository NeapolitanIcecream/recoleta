---
source: arxiv
url: https://arxiv.org/abs/2605.09241v1
published_at: '2026-05-10T00:51:47'
authors:
- Kai Zhao
- Dongliang Nie
- Yuchen Lin
- Zhehan Luo
- Yixiao Gu
- Deng-Ping Fan
- Dan Zeng
topics:
- world-model
- jepa
- latent-dynamics
- gaussian-regularization
- continuous-control
- robot-manipulation
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Sub-JEPA: Subspace Gaussian Regularization for Stable End-to-End World Models

## Summary
Sub-JEPA is a JEPA-style latent world model that reduces collapse while avoiding an overly strict full-space Gaussian prior. It reports higher planning success than LeWorldModel on four pixel-based continuous-control tasks.

## Problem
- JEPA world models can collapse during end-to-end training because the encoder can map different observations to similar latent vectors.
- LeWorldModel prevents collapse with an isotropic Gaussian regularizer over the full latent space, but this can force low-dimensional control dynamics into a high-rank shape.
- The issue matters for planning: distorted latent geometry can make model predictive control less accurate over long rollouts.

## Approach
- The model keeps the LeWorldModel setup: an encoder maps RGB observations to latent vectors, and a predictor learns the next latent state from the current latent and action.
- Sub-JEPA replaces full-space Gaussian regularization with Gaussian tests inside multiple low-dimensional projected subspaces.
- Each projection matrix is sampled once, made row-orthonormal with QR decomposition, and frozen during training.
- For each subspace, the method samples random 1D directions and applies the Epps-Pulley normality statistic, then averages the loss across directions and subspaces.
- The main training loss is latent prediction error plus the subspace Gaussian regularizer; experiments use latent dimension D=192, K=32 for most tasks, and K=16 for PushT.

## Results
- Against LeWorldModel, Sub-JEPA improves planning success on all four tasks: Two-Room 84.33±4.23% to 95.00±2.76%, Reacher 82.67±4.42% to 84.00±4.00%, PushT 84.67±6.53% to 89.00±5.33%, and OGB-Cube 67.33±5.01% to 76.33±5.99%.
- Compared with PLDM, Sub-JEPA is lower on Two-Room by 2.00 points, higher on Reacher by 6.00 points, higher on PushT by 11.00 points, and higher on OGB-Cube by 11.33 points.
- Compared with DINO-WM without proprioception, Sub-JEPA is lower on Two-Room by 5.00 points and lower on OGB-Cube by 9.67 points, but higher on Reacher by 5.00 points and PushT by 15.00 points.
- The projection ablation shows frozen orthogonal projections perform best: 95.00±2.76% on Two-Room, 84.00±4.00% on Reacher, 89.00±5.33% on PushT, and 76.33±5.99% on OGB-Cube. Random frozen projections drop to 53.00±8.44%, 68.00±5.29%, 13.33±5.61%, and 61.00±5.55%.
- The paper reports that Sub-JEPA lowers effective rank more than LeWorldModel and that larger rank reductions align with larger planning gains, but the excerpt does not provide exact effective-rank values.

## Link
- [https://arxiv.org/abs/2605.09241v1](https://arxiv.org/abs/2605.09241v1)
