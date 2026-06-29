---
source: arxiv
url: http://arxiv.org/abs/2604.09330v1
published_at: '2026-04-10T13:59:54'
authors:
- Xiaolei Lang
- Yang Wang
- Yukun Zhou
- Chaojun Ni
- Kerui Li
- Jiagang Zhu
- Tianze Liu
- Jiajun Lv
- Xingxing Zuo
- Yun Ye
- Guan Huang
- Xiaofeng Wang
- Zheng Zhu
topics:
- embodied-data-synthesis
- vision-language-action
- world-action-model
- robot-data-scaling
- sim2real
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# VAG: Dual-Stream Video-Action Generation for Embodied Data Synthesis

## Summary
VAG is a joint video-and-action generator for robot data synthesis. It aims to make synthetic embodied data usable for policy learning by generating future video frames and matching action trajectories together.

## Problem
- Robot foundation models need large teleoperation datasets, but collecting new robot demonstrations for each task or setting is expensive and slow.
- Standard world models can generate future video, but they do not output the paired actions needed to train robot policies.
- Two-stage methods that generate video first and then infer actions often lose video-action consistency and accumulate errors over long horizons.

## Approach
- VAG uses a dual-stream architecture with one branch for video generation and one branch for action generation, both conditioned on the first frame and a language instruction.
- Both branches use flow matching and denoise in sync across the same generation steps, so video and action are produced together over a horizon of 93 frames, about 10 seconds at 10 Hz.
- The video branch is built on Cosmos-Predict2 and predicts future video latents; the action branch is a modified 1D U-Net that predicts the action sequence.
- At each denoising step, VAG takes the current clean video latent, compresses it with adaptive 3D pooling into a compact global embedding, and feeds that embedding to the action branch.
- Training uses paired robot video-action trajectories plus text instructions extracted with Qwen2.5-VL and encoded with T5-XXL.

## Results
- On the AgiBot dataset, VAG beats SVD, Wan2.2, and Cosmos-Predict2 on several video metrics: FVD 965 vs 988 for CP2, 1152 for Wan2.2, and 1311 for SVD; LPIPS 0.320 vs 0.352, 0.325, and 0.421; PSNR 15.1 vs 14.2, 14.5, and 12.7. Its FID is 130, close to CP2 at 135 and Wan2.2 at 129.
- On action generation for AgiBot, VAG reaches ED 0.81 and success rate 45%, compared with VAG-Video+AnyPos at ED 0.98 and 29%, and VAG-Video+ResNet at ED 1.54 and 8%.
- On LIBERO action generation, VAG reaches ED 0.38 and success rate 79%, compared with VAG-Video+AnyPos at ED 0.55 and 66%, and VAG-Video+ResNet at ED 0.87 and 37%.
- On LIBERO replay success, VAG gets 70% on Spatial, 72% on Object, 64% on Goal, 42% on Long, and 62% average. The AnyPos two-stage pipeline gets 54% average, and the ResNet pipeline gets 25% average.
- For downstream VLA training on a self-collected real-robot dataset, the paper reports that VAG synthetic pretraining raises success rate from 35% to 55%, a gain of 20 percentage points.
- The paper also claims the generated actions can be replayed on a real robot and can support executable trajectories, but the excerpt does not give fuller real-robot evaluation numbers beyond the 35% to 55% VLA improvement.

## Link
- [http://arxiv.org/abs/2604.09330v1](http://arxiv.org/abs/2604.09330v1)
