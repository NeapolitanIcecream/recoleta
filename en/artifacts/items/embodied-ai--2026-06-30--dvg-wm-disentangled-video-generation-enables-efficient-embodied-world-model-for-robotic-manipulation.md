---
source: arxiv
url: https://arxiv.org/abs/2606.32028v1
published_at: '2026-06-30T17:54:32'
authors:
- Ziyu Shan
- Zhenyu Wu
- Xiaofeng Wang
- Zheng Zhu
- Ziwei Wang
topics:
- embodied-world-model
- robotic-manipulation
- video-generation
- language-conditioned-planning
- imitation-learning
- contact-rich-manipulation
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# DVG-WM: Disentangled Video Generation Enables Efficient Embodied World Model for Robotic Manipulation

## Summary
DVG-WM is a two-stage video world model for robotic manipulation that separates low-resolution dynamics prediction from high-resolution video refinement. It claims better video fidelity, better object grounding, and faster inference than several video-planning baselines on LIBERO.

## Problem
- Video world models for robots need to predict contact, occlusion, and object motion while also producing clear high-resolution frames.
- Single-stage video generators spend many denoising steps on high-resolution synthesis, which slows repeated planning calls.
- Coarse or slow predictions hurt manipulation because small contact errors can change the action plan.

## Approach
- The model takes an initial observation and a language instruction, then predicts a 49-frame future video.
- A low-resolution preview stage uses CogVideoX-5B with LoRA to generate coarse latent dynamics at 256×384.
- A high-resolution refinement stage uses a smaller CogVideoX-2B model to produce 480×720 video latents.
- Flow matching maps the upsampled low-resolution latent sequence directly toward high-resolution latents, using 4 refinement steps at inference.
- A latent degradation training method perturbs preview latents so the refinement model learns to regenerate gripper-object contact details instead of only upscaling pixels.

## Results
- On LIBERO video prediction, DVG-WM reports PSNR 20.019, compared with CogVideoX-5B 19.286, Wan2.1-14B 18.964, LongScape 19.977, and LVP-14B 19.582.
- DVG-WM reports LPIPS 0.120 and FVD 152.36, compared with LongScape 0.123 LPIPS and 153.72 FVD, and CogVideoX-5B 0.138 LPIPS and 171.24 FVD.
- Object-level accuracy reaches 89%, compared with 80% for LVP-14B, 76% for CogVideoX-5B, and 68% for Wan2.1-14B.
- SSIM is 0.783, below LongScape at 0.788 but above CogVideoX-5B at 0.761, Wan2.1-14B at 0.732, and LVP-14B at 0.765.
- Inference time is 88.7 seconds, compared with 236.8 seconds for CogVideoX-5B, 312.0 seconds for Wan2.1-14B, and 354.2 seconds for LVP-14B, giving up to 3.97× speedup.
- The paper also reports tests on a 7K-trajectory real-world dataset with an action expert, but the provided excerpt does not include numeric real-world success rates.

## Link
- [https://arxiv.org/abs/2606.32028v1](https://arxiv.org/abs/2606.32028v1)
