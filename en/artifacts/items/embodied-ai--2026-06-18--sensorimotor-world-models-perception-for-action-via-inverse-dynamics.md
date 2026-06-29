---
source: arxiv
url: https://arxiv.org/abs/2606.20104v1
published_at: '2026-06-18T11:25:16'
authors:
- Petr Ivashkov
- Randall Balestriero
- "Bernhard Sch\xF6lkopf"
topics:
- latent-world-models
- inverse-dynamics
- representation-learning
- offline-robot-data
- model-predictive-control
- controllable-state
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Sensorimotor World Models: Perception for Action via Inverse Dynamics

## Summary
SMWM trains a latent world model from pixels and continuous actions using inverse dynamics as the only anti-collapse regularizer. The method aims to learn compact states that keep action-relevant variables and drop uncontrollable distractors.

## Problem
- JEPA-style latent world models can collapse when the encoder and dynamics model are trained only to predict the next embedding; a constant embedding can give zero forward loss.
- Pixel reconstruction pushes models to preserve visual details that may not help control, such as backgrounds or random distractors.
- This matters for offline, reward-free control data because the learned state must support planning without task labels, rewards, frozen encoders, or pretrained vision models.

## Approach
- The model uses an encoder \(f_\theta\) to map observations to embeddings, a forward model \(g_\phi\) to predict \(z_{t+1}\) from \(z_t\) and action \(a_t\), and an inverse model \(h_\psi\) to predict \(a_t\) from \((z_t,z_{t+1})\).
- Training minimizes \(\mathcal{L}=\mathcal{L}_{\text{fwd}}+\lambda\mathcal{L}_{\text{inv}}\), where both losses update the encoder.
- The inverse loss blocks full collapse because a constant embedding pair can only predict a constant action; lower inverse loss requires the embeddings to preserve action-predictive information.
- The learned representation is biased toward controllable state changes, since those changes help recover actions and help the forward model predict future embeddings.
- For control, the paper freezes the encoder and forward model, then uses CEM with receding-horizon MPC to optimize action sequences toward a goal embedding.

## Results
- In the dot-world testbed, observations are \(64\times64\) RGB images, the latent size is \(d=64\), and PCA shows that 2 principal components carry the useful variance for a true 2D state; the other 62 directions are effectively collapsed.
- A 5-step latent rollout tracks encoded ground-truth embeddings in the dot-world example, supporting the claim that actions act roughly as translations in latent space.
- Across four dot-world variants, the effective latent dimension matches the controllable dimension: Independent = 4, Coupled = 2, Distractor = 2, Combined = 6.
- In the distractor setting, the encoder ignores a randomly moving uncontrolled dot even though it is visible in the observation.
- The planning evaluation covers 4 environments: TwoRoom, Reacher, Push-T, and OGBench-Cube, with SIGReg, forward-only, and random-action baselines.
- The provided excerpt does not include quantitative planning metrics such as success rate or return; it claims competitive planning performance against SIGReg in 2D and 3D control tasks.

## Link
- [https://arxiv.org/abs/2606.20104v1](https://arxiv.org/abs/2606.20104v1)
