---
source: arxiv
url: https://arxiv.org/abs/2607.02092v1
published_at: '2026-07-02T12:30:50'
authors:
- Liuhaichen Yang
- Zhuang Jiang
- Chenchao Sheng
- Zezhi Tang
topics:
- vision-language-action
- flow-matching
- q-guided-inference
- robot-manipulation
- critic-guidance
- libero
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Guided Action Flow: Q-Guided Inference for Flow-Matching Vision-Language-Action Policies

## Summary
Guided Action Flow adds test-time Q-guidance to a frozen SmolVLA flow-matching VLA policy. A learned action-chunk critic steers the sampler during inference and improves LIBERO success in single-task and validation settings, with only a small held-out gain.

## Problem
- Frozen VLA robot policies can fail after distribution shifts, early action errors, or locally plausible action chunks that do not finish the task.
- Full VLA fine-tuning can be costly and hard to validate when only small task-local rollout data is available.
- The paper asks whether a small critic trained from success and failure rollouts can improve a frozen flow-matching VLA without changing its weights.

## Approach
- The base policy is the official SmolVLA LIBERO checkpoint, kept frozen throughout all QGF experiments.
- The method trains an MLP critic on rollout chunks. The critic takes policy-side observation features, a candidate action chunk, and optional task-description features, then predicts sparse success-to-go.
- During reverse-time SmolVLA sampling, the method estimates the clean action chunk as `a_hat = x_t - t v_t`, computes the critic gradient with respect to that action chunk, clips it, gates it with critic-ensemble disagreement, and adjusts the flow velocity.
- A 3-critic ensemble supplies uncertainty through value disagreement. High disagreement reduces guidance, while a minimum gate keeps a small guidance signal active.
- The strongest critic variant conditions on frozen SmolVLA VLM hidden-state task features, using the base policy language pathway without training a new text encoder.

## Results
- Frozen SmolVLA baseline anchors: LIBERO vanilla reached 65/100 success (65.0%), LIBERO-Plus spatial subset reached 39/50 (78.0%), and LIBERO-PRO zero-shot reached 1/100 (1.0%).
- Single-task QGF improved one LIBERO spatial task from 34/50 (68.0%) to 41/50 (82.0%) on seed window 3000, a +14.0 percentage point gain.
- On seed window 4000 for the same single-task setting, QGF improved success from 41/50 (82.0%) to 43/50 (86.0%), a +4.0 point gain.
- A spatial-only transfer critic failed to transfer: validation success was at most 31/60 (51.7%) versus a 32/60 (53.3%) baseline, a regression of at least -1.7 points.
- The multi-family task-description critic improved validation success from 23/50 (46.0%) to 28/50 (56.0%), a +10.0 point gain.
- On the locked held-out test, the multi-family task-description critic improved from 26/40 (65.0%) to 27/40 (67.5%), a +2.5 point gain, showing positive but limited generalization.

## Link
- [https://arxiv.org/abs/2607.02092v1](https://arxiv.org/abs/2607.02092v1)
