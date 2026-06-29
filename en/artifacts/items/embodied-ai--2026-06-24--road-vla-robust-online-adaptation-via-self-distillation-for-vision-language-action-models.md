---
source: arxiv
url: https://arxiv.org/abs/2606.25800v1
published_at: '2026-06-24T13:17:59'
authors:
- Kejing Wang
- Toan Nguyen
- Minh Hoang Nguyen
- Simon Khan
- Flora D. Salim
topics:
- vision-language-action
- online-adaptation
- robot-foundation-model
- self-distillation
- reinforcement-learning
- manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# ROAD-VLA: Robust Online Adaptation via Self-Distillation for Vision-Language-Action Models

## Summary
ROAD-VLA adapts OpenVLA-style robot policies online by turning sparse rewards into token-level action supervision. It builds a teacher from the current policy by shifting action-token logits with calibrated advantage estimates, then distills the policy toward that teacher.

## Problem
- VLA policies need online adaptation because robots face new backgrounds, object layouts, sensor noise, and execution errors after pretraining.
- PPO uses each advantage estimate as a scalar weight on a sampled action, which gives weak supervision for high-dimensional autoregressive action tokens.
- Text-based privileged teachers using demonstrations, retrieved experience, or plans did not give reliable low-level action guidance in the authors' tests.

## Approach
- ROAD-VLA runs on-policy rollouts with OpenVLA and estimates step-wise advantages from sparse task rewards.
- It mixes an intrinsic advantage estimate with a frozen PPO-critic estimate after matching batch statistics, and uses the reference only when both estimates have the same sign.
- It standardizes and clips the mixed advantage, then shifts the sampled action-token logit up or down by that signed weight.
- The shifted logits define a nearby teacher distribution in action-token space. The student trains with teacher-to-student KL over every timestep and every action token.
- The paper proves a policy-improvement lower bound when the advantage estimates are calibrated and the student matches the teacher closely.

## Results
- The evaluation covers 7 manipulation environments across 3 shift types: 3 visual robustness tasks, 2 compositional reasoning tasks, and 2 execution robustness tasks.
- The base model is OpenVLA-7B. Both ROAD-VLA and PPO start from the same warm-up checkpoint fine-tuned on 140 expert trajectories.
- OpenVLA actions use 7 discrete action tokens, with each action dimension discretized into 256 bins; ROAD-VLA applies distillation at this token level.
- The authors claim ROAD-VLA outperforms PPO in nearly all in-distribution and out-of-distribution settings, but the provided excerpt does not include success rates, confidence intervals, or per-task tables.
- Fixed method settings reported in the excerpt include advantage mixing coefficient alpha = 0.5, clipping c = 2.0, and logit perturbation strength eta = 1.0.

## Link
- [https://arxiv.org/abs/2606.25800v1](https://arxiv.org/abs/2606.25800v1)
