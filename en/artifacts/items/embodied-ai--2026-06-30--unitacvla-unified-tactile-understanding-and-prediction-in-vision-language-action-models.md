---
source: arxiv
url: https://arxiv.org/abs/2606.31723v1
published_at: '2026-06-30T14:24:00'
authors:
- Xidong Zhang
- Yichi Zhang
- Jiaxin Shi
- Fucai Zhu
- Siyu Zhu
- Michael Yu Wang
- Xiaojun Wu
- Weihao Yuan
topics:
- vision-language-action
- tactile-sensing
- dexterous-manipulation
- contact-rich-control
- robot-policy
- tactile-prediction
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# UniTacVLA: Unified Tactile Understanding and Prediction in Vision Language Action Models

## Summary
UniTacVLA adds tactile reasoning, future tactile prediction, and high-frequency tactile correction to a vision-language-action robot policy for contact-rich manipulation. It reports higher real-robot success rates on 8 dexterous tasks, with the largest gains under perturbations.

## Problem
- Vision-language-action policies struggle with contact events such as slipping, jamming, contact onset, and small alignment errors, especially when the contact point is occluded.
- Many tactile VLA methods feed touch signals into the policy as extra inputs, but they do not train the model to understand contact stages or predict how contact will change.
- The problem matters because insertion, wiping, adjustment, and assembly tasks fail when low-frequency action chunks cannot correct small contact errors in time.

## Approach
- UniTacVLA learns unified tactile tokens inside a VLM so the policy can store task-relevant contact information with vision and language observations.
- It uses tactile chain-of-thought supervision to make the tactile latent describe contact stage, contact condition, and likely failure modes.
- It predicts future tactile latents in two steps: an MLP predicts a coarse future contact trend, then a DiT refines local tactile detail.
- A lightweight Transformer controller takes the planned action, predicted future tactile latent, and real-time tactile latent, then adds a bounded residual correction to the action.
- Training has two stages: joint action, semantic, and tactile prediction on clean demonstrations, then controller training on clean and disturbed recovery trajectories.

## Results
- On 8 real-robot subtasks with 50 trials per setting, UniTacVLA reached 64.0% average clean success and 53.5% average perturbed success.
- The strongest reproduced tactile baseline, pi0.5-TacVLA, reached 45.25% clean and 16.25% perturbed average success, so UniTacVLA improved average success by 18.75 points clean and 37.25 points perturbed.
- Against vision-only pi0.5, UniTacVLA improved average success from 26.0% to 64.0% clean and from 5.75% to 53.5% perturbed.
- On USB insertion without disturbance, the ablation rose from 18% success with no tactile components to 30% with tactile input, 36% with T-CoT, 44% with coarse prediction, 52% with fine prediction, and 62% with the controller.
- UniTacVLA without real tactile input at inference reached 48.0% clean and 17.0% perturbed average success, suggesting tactile-supervised training still improves the learned contact prior.
- The best reported prediction window for the USB ablation was 12 steps, according to the provided figure text.

## Link
- [https://arxiv.org/abs/2606.31723v1](https://arxiv.org/abs/2606.31723v1)
