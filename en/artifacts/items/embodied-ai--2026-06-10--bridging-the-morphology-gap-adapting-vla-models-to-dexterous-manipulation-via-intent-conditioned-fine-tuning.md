---
source: arxiv
url: https://arxiv.org/abs/2606.12109v1
published_at: '2026-06-10T14:03:52'
authors:
- Chuanke Pang
- Junyi Huang
- Zhijun Zhao
- Yaobing Wang
- Kun Xu
- Xilun Ding
topics:
- vision-language-action
- dexterous-manipulation
- robot-foundation-model
- policy-finetuning
- diffusion-policy
- cross-morphology-adaptation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Bridging the Morphology Gap: Adapting VLA Models to Dexterous Manipulation via Intent-Conditioned Fine-Tuning

## Summary
InDex adapts a pre-trained VLA policy to a high-DoF dexterous hand by keeping the VLA’s arm-level spatial skill and adding an intent-conditioned diffusion head for finger control. The paper claims large simulated gains on four dexterous manipulation tasks using 100 demonstrations per task.

## Problem
- Most pre-trained VLA robot policies target 1-DoF parallel grippers, so their action heads do not match multi-finger hands.
- Direct end-to-end fine-tuning on dexterous actions can erase useful VLA spatial behavior and can collapse under scarce high-DoF demonstrations.
- The problem matters because contact-rich tasks such as stacking and nut assembly need precise finger motion, not only object reaching.

## Approach
- The method converts the dexterous hand pose into a scalar grasp intent γ in [0,1], where 0 means open and 1 means closed, using the distance between the thumb tip and the centroid of the other fingertips.
- Stage 1 fine-tunes the π0.5 action expert with LoRA while freezing the VLM backbone. It predicts 6-DoF arm motion and coarse hand intent.
- Stage 2 freezes the VLA backbone and trains a denoising diffusion action head for 12-D actions, conditioned on VLA visual embeddings, proprioception, and γ.
- The diffusion head handles finger-level action generation, while the VLA keeps the higher-level reaching and visual-language behavior.

## Results
- On four robosuite simulation tasks, π0.5+InDex reports 85.8% average task success, compared with π0.5 at 50.3%, Diffusion Policy at 42.8%, UniVLA at 37.8%, OpenVLA at 31.8%, and ACT at 34.5%.
- Per-task task success for π0.5+InDex is 95% on Lift, 83% on Stack, 89% on Pick & Place, and 76% on Nut Assembly.
- Stage-wise average success for π0.5+InDex is 92.8% reach, 88.3% grasp, and 85.8% full task. The π0.5 baseline reports 76.0%, 56.0%, and 50.3% on the same metrics.
- On Nut Assembly, π0.5 drops from 57% reach to 25% task success, while π0.5+InDex reports 87% reach, 79% grasp, and 76% task success.
- The evaluation uses 100 successful demonstrations per task and 100 independent trials per task, with domain randomization over object poses and lighting.
- The ablation excerpt reports 4.0% average success for native π0.5 direct projection and 17.0% without intent conditioning, supporting the role of the γ intent signal, though the full ablation table is truncated in the provided text.

## Link
- [https://arxiv.org/abs/2606.12109v1](https://arxiv.org/abs/2606.12109v1)
