---
source: arxiv
url: http://arxiv.org/abs/2604.03181v1
published_at: '2026-04-03T16:57:06'
authors:
- Peiyan Li
- Yixiang Chen
- Yuan Xu
- Jiabing Yang
- Xiangnan Wu
- Jun Guo
- Nan Sun
- Long Qian
- Xinghang Li
- Xin Xiao
- Jing Liu
- Nianfeng Liu
- Tao Kong
- Yan Huang
- Liang Wang
- Tieniu Tan
topics:
- robot-manipulation
- video-diffusion-policy
- multi-view-3d
- vision-language-action
- data-efficient-learning
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Multi-View Video Diffusion Policy: A 3D Spatio-Temporal-Aware Video Action Model

## Summary
MV-VDP is a robot manipulation policy that predicts both future multi-view videos and action heatmaps, so the model tracks 3D scene structure and how the scene will change after an action. The paper targets low-data manipulation and reports strong gains over video-action, 3D, and vision-language-action baselines in simulation and on real robots.

## Problem
- Many robot policies learn from 2D images while acting in 3D space, which creates a mismatch between observation and control and raises the amount of robot data needed.
- Many policies reuse image-text backbones trained on static images, so they do a poor job modeling scene dynamics and action consequences over time.
- This matters most in low-data manipulation: the paper focuses on settings with only 5 to 10 demonstrations per task, where common behavior cloning and VLA systems often fail.

## Approach
- The method projects cropped point clouds into three fixed orthographic views, producing multi-view RGB images and multi-view heatmaps for the robot end-effector pose.
- It uses the same representation type for pretraining-compatible video inputs and for action prediction: the model predicts future RGB videos and future heatmap videos together.
- The backbone is a 5B Wan2.2 video diffusion model, extended with cross-view attention so tokens from different camera views interact at each timestep.
- Predicted heatmap peaks from the views are back-projected into 3D end-effector positions. A separate 170M decoder uses denoised video latents to predict rotation and gripper state, then combines position, rotation, and gripper outputs into action chunks.
- Training uses diffusion loss on both video and heatmap sequences, plus LoRA fine-tuning and SE(3) augmentation. The paper says full fine-tuning did not improve performance.

## Results
- **Meta-World, 7 tasks, 5 demos per task, 25 trials per task:** MV-VDP reaches **89.1%** average success, ahead of **Track2Act 67.4%**, **DreamZero 61.1%**, **AVDC 58.9%**, **DP 37.7%**, **BC-R3M 35.4%**, **BC-Scratch 26.2%**, and **UniPi 11.4%**.
- **Meta-World per-task examples:** MV-VDP gets **25/25** on D-Open, D-Close, Btn, and Handle, **24/25** on Btn-Top and Fct-Open, and **8/25** on Fct-Cls.
- **Real world, about 10 demos per task, 10 trials per task:** on basic tasks MV-VDP reports **10/10** on Put Lion, **4/10** on Push-T, and **7/10** on Scoop Tortilla. Baselines shown in the excerpt are weaker: **BridgeVLA 9/10, 0/10, 4/10**; **UVA 2/10, 0/10, 0/10**; **DP3 0/10, 0/10, 0/10**; **π0.5 1/10, 0/10, 0/10**.
- **Real-world unseen variants:** the excerpt reports **5/10** on Put-B and **6/10** on Put-H for MV-VDP, showing some transfer to changed background and object height. The table is truncated, so the remaining unseen-task numbers and final average are not fully visible in the provided text.
- The paper also claims strong robustness to hyperparameters, including keeping good performance with only **1 diffusion step**, but the excerpt does not provide the supporting table or exact numbers.
- It claims realistic future-video prediction and interpretable action previews, but the excerpt does not include a quantitative video-prediction metric.

## Link
- [http://arxiv.org/abs/2604.03181v1](http://arxiv.org/abs/2604.03181v1)
