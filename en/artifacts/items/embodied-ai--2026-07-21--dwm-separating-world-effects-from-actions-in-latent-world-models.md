---
source: arxiv
url: https://arxiv.org/abs/2607.18715v1
published_at: '2026-07-21T05:13:26'
authors:
- Yi-Ge Zhang
- Tianqi Du
- Qi Zhang
- Yisen Wang
topics:
- latent-world-models
- model-based-control
- world-action-disentanglement
- cem-planning
- persistent-dynamics
- robotics
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# DWM: Separating World Effects from Actions in Latent World Models

## Summary
DWM trains latent world models to separate action-invariant environmental motion from action-driven changes. On benchmarks with persistent gravity or drift, it improves CEM planning while leaving inference-time architecture unchanged.

## Problem
- Standard action-conditioned latent world models supervise a single next-latent target, mixing agent-caused motion with changes that would occur under a null action.
- This matters because persistent effects such as gravity, inertia, contact rebound, and drift can produce inaccurate multi-step rollouts and poor planning decisions.

## Approach
- DWM adds a training-only world head to the existing predictor; the head is trained to produce the same representation when the current action is replaced by a different action for the same state.
- A normalized InfoNCE world-contrastive loss encourages action invariance while retaining state discrimination, and an orthogonality loss separates the world-head output from the residual action-driven component.
- The original prediction head still predicts the complete next latent and is the only head used during inference, so the planning pipeline remains unchanged.
- Evaluation uses PushT-W, Reacher-W, and TwoRoom-W, which add gravity-driven sliding, vertical-plane gravity, and constant environmental drift to standard tasks, plus Ball-in-Cup.

## Results
- Across PushT-W, Reacher-W, and TwoRoom-W, DWM improves CEM planning success by 12.0%, 10.7%, and 16.7%, respectively, for a mean absolute improvement of 13.1%.
- On Ball-in-Cup, DWM improves performance by 6.0%.
- On the standard PushT benchmark, the single-head LeWM baseline reaches 94.0% CEM success, whereas on PushT-W it reaches 32%; adding 30% zero-action training data does not help, yielding 30% success.
- DWM remains comparable to the single-head baseline on flat tasks without substantial world effects, while diagnostics and ablations associate its gains with greater action invariance and more accurate multi-step latent rollouts.
- The reported evaluation is based primarily on controlled simulated benchmark variants; the excerpt does not establish performance on physical robots or broad real-world datasets.

## Link
- [https://arxiv.org/abs/2607.18715v1](https://arxiv.org/abs/2607.18715v1)
