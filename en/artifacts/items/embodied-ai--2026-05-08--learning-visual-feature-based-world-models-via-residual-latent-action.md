---
source: arxiv
url: https://arxiv.org/abs/2605.07079v1
published_at: '2026-05-08T00:58:16'
authors:
- Xinyu Zhang
- Zhengtong Xu
- Yutian Tao
- Yeping Wang
- Yu She
- Abdeslam Boularias
topics:
- robot-world-model
- visual-feature-prediction
- latent-action
- flow-matching
- actionless-video-learning
- offline-robot-rl
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Learning Visual Feature-Based World Models via Residual Latent Action

## Summary
RLA-WM predicts future robot visual features by generating a compact residual latent action, then decoding it with the current DINO features. The paper claims better prediction accuracy than DINO-token regression, direct feature-space generation, and video diffusion, with much lower compute than video diffusion.

## Problem
- Robot world models often predict video pixels, which is expensive and can produce visually sharp but physically wrong futures.
- Feature-based world models such as DINO-WM are cheaper, but direct regression can blur or collapse predictions in complex 3D manipulation.
- The problem matters because a useful robot world model should support policy learning from offline robot videos, including videos without action labels.

## Approach
- The method encodes the residual between two DINO token states, `s_{t+h} - s_t`, into a compact latent vector called Residual Latent Action, or RLA.
- An RLA decoder reconstructs the future DINO tokens `s_{t+h}` from the current tokens `s_t` and the latent `z` in one forward pass.
- RLA-WM predicts `z` with flow matching, conditioned on the current DINO tokens and an action chunk, then decodes the predicted latent into future DINO tokens.
- The model runs the iterative generative step in the small RLA space instead of the much larger DINO token space. The paper gives a scale example: a 512×512 image has about 16k Stable Diffusion VAE latent dimensions, while DINOv3-L tokens have about 1M dimensions.
- The paper also uses RLA for two policy-learning settings: a lightweight world action model trained partly on actionless videos, and visual RL inside an offline-trained RLA-WM.

## Results
- On ManiSkill future-frame prediction, RLA-WM reports LPIPS 0.071, SSIM 0.931, and DINO L1 0.030. The strongest listed baselines are FM-WM at 0.127 LPIPS, 0.890 SSIM, 0.063 DINO L1, and DINO-WM at 0.156, 0.865, 0.078.
- On the real-world IWS dataset, RLA-WM reports LPIPS 0.196, SSIM 0.847, and DINO L1 0.053. DINO-WM reports 0.223, 0.825, 0.058, while FM-WM reports 0.360, 0.741, 0.119.
- Compute per inference is 3.5T FLOPs for RLA-WM, 2.1T for DINO-WM, 14.3T for RAE and FM-WM, and 1.1P for Vid2World.
- In actionless-video imitation learning, the RLA world action model reaches 35.6% average success across 5 ManiSkill tasks, compared with 27.2% for BC-ResNet, 27.4% for DINO CLS, 28.7% for UniVLA, and 33.7% for AdaWorld.
- On PushT in the same setting, RLA reaches 15.2% success, compared with 3.6% for BC-ResNet and 9.2% for AdaWorld.
- The training data described for prediction include 1,000 successful and 500 failed episodes per ManiSkill task, 3,000 play videos per robot, and over 600 human teleoperation demos per selected IWS task.

## Link
- [https://arxiv.org/abs/2605.07079v1](https://arxiv.org/abs/2605.07079v1)
