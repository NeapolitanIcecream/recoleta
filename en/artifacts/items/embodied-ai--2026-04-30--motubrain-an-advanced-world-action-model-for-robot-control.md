---
source: arxiv
url: https://arxiv.org/abs/2604.27792v2
published_at: '2026-04-30T12:34:44'
authors:
- MotuBrain Team
- Chendong Xiang
- Fan Bao
- Haitian Liu
- Hengkai Tan
- Hongzhe Bi
- James Li
- Jiabao Liu
- Jingrui Pang
- Kiro Jing
- Louis Liu
- Mengchen Cai
- Rongxu Cui
- Ruowen Zhao
- Runqing Wang
- Shuhe Huang
- Yao Feng
- Yinze Rong
- Zeyuan Wang
- Jun Zhu
topics:
- world-action-model
- vision-language-action
- robot-foundation-model
- real-time-robot-control
- multiview-manipulation
- robot-data-scaling
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# MotuBrain: An Advanced World Action Model for Robot Control

## Summary
MotuBrain is a unified world action model that predicts robot actions and future visual states with one diffusion-based model. It targets real-time robot control by combining video, action, and language streams with multiview support and a faster inference stack.

## Problem
- Vision-language-action policies often map images and instructions straight to actions, so they can miss fine-grained temporal dynamics needed for precise manipulation.
- Two-stage video-generation-plus-inverse-dynamics systems can accumulate video prediction errors before actions are inferred, which can lower control accuracy.
- Large world action models are slow at inference, which matters because robot controllers need low-latency action updates for long-horizon and dexterous tasks.

## Approach
- The core mechanism is a UniDiffuser-style joint model over two continuous outputs: future video latents and action tokens. The same model can run as a policy, world model, video generator, inverse dynamics model, or joint video-action predictor.
- MotuBrain uses three Transformer streams for text, video, and action. Video and action streams learn flow-matching objectives, while text conditions both streams through attention.
- It uses H-bridge attention: full video-action joint attention appears only in the middle 50% of Transformer layers, while the bottom 25% and top 25% use separate modality attention to reduce cost.
- Multiview inputs are encoded per camera with a Vidu VAE, then joined at the token level with view-dependent 3D RoPE spatial offsets. This supports different camera layouts without changing the backbone.
- Training moves through broad video data, ego-centric and robot data, then target-embodiment data. Actions use relative end-effector coordinates with 10 dimensions per end-effector action, including position, 6D rotation, and gripper state.

## Results
- On RoboTwin 2.0, MotuBrain reports 95.8% average success in the clean setting and 96.1% in the randomized setting.
- The randomized RoboTwin 2.0 score is above 95%, which the authors use as evidence that the model handles visual and task variation.
- On WorldArena, the paper claims the strongest reported EWMScore among its comparison set, but the excerpt does not provide the numeric EWMScore.
- The inference stack reduces end-to-end latency from 4.90 s to 0.09 s and raises frequency from 0.20 Hz to 11.11 Hz, a 54.4x speedup over the naive baseline.
- Step reduction lowers diffusion sampling from 50 steps to 30 steps; the authors report sub-percent success-rate changes on RoboTwin 2.0 after the optimization stack.
- The model is claimed to adapt to new humanoid embodiments with 50-100 same-embodiment trajectories and to solve long-horizon and dexterous manipulation tasks without an extra VLM planner, dual-system decomposition, external memory, or retry-specific data.

## Link
- [https://arxiv.org/abs/2604.27792v2](https://arxiv.org/abs/2604.27792v2)
