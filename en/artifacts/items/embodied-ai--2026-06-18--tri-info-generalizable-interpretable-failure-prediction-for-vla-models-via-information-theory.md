---
source: arxiv
url: https://arxiv.org/abs/2606.19998v1
published_at: '2026-06-18T09:34:22'
authors:
- Jinghan Yang
- Yunchao Zhang
- Wang Yuan
- Haolun Wan
- Jiaming Zhang
- Zhengyang Hu
- Yanchao Yang
topics:
- vision-language-action
- failure-prediction
- robot-safety
- information-theory
- sim2real
- generalist-robot-policy
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Tri-Info: Generalizable, Interpretable Failure Prediction for VLA Models via Information Theory

## Summary
Tri-Info predicts failures in VLA robot rollouts using entropy and mutual information computed over recent state and action embeddings. It aims to transfer across models and sim-to-real without retraining while giving a concrete reason for the alarm.

## Problem
- VLA policies can fail under new objects, lighting, tasks, models, or physical settings, and robot failures can damage objects or create safety risks before a human can react.
- Existing failure detectors often depend on one model's internal embedding space, so they need retraining when the VLA architecture changes.
- A useful detector must warn early and show whether the policy is freezing, drifting, or acting out of sync with the observed state.

## Approach
- The paper treats VLA control as a closed-loop sequence of state embeddings, action embeddings, next states, and next actions.
- It derives eight entropy and mutual-information signals, then reduces them to three Tri-Info signals: action entropy H(A_t), temporal action mutual information I(A_t; A_t+1), and state-transition/action mutual information I(S_t, S_t+1; A_t).
- These three signals map to simple failure cues: too little or too much action diversity, weak action consistency over time, and weak coupling between actions and state changes.
- The method estimates each signal in a sliding window with k-NN mutual-information and entropy estimators, then z-normalizes the values.
- It trains one GRU per signal, averages the three failure probabilities, and uses Functional Conformal Prediction to set a time-varying alarm threshold.

## Results
- The evaluation covers six VLA models and three benchmark settings: LIBERO-10, CALVIN, and ALOHA, including simulated and real robot tasks.
- In the abstract, Tri-Info reaches 83% accuracy on real-world tasks under sim-to-real transfer, while prior detectors fall to chance-level performance.
- Single-metric logistic regression shows that the information signals carry direct failure signal: pooled in-domain AUC is at least 0.701 for all eight metrics, and I(A_t; A_t+1) reaches 0.895 pooled AUC.
- Adding temporal GRU modeling raises pooled single-metric AUCs to 0.973-0.982 across the eight metrics; H(A_t) reaches 0.982 pooled AUC and I(A_t; A_t+1) reaches 0.976.
- On in-domain LIBERO, Tri-Info reports balanced accuracy of 0.91 by mid-trajectory for PI0 and 0.85 by 10% progress for PI0.5, with PI0.5 peaking at 0.92.
- Baseline comparison claims Tri-Info matches the strongest in-domain baselines and transfers across architectures, environments, and sim-to-real without retraining; SAFE peaks at 0.96 on PI0 and 0.91 on PI0.5, while STAC reaches 0.89 and 0.93 later in the rollout.

## Link
- [https://arxiv.org/abs/2606.19998v1](https://arxiv.org/abs/2606.19998v1)
