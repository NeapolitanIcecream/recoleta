---
source: arxiv
url: https://arxiv.org/abs/2606.23296v1
published_at: '2026-06-22T13:09:34'
authors:
- Chengyu Bai
- Peidong Jia
- Tiecheng Guo
- Yukai Wang
- Rui Ma
- Fangyuan Zhao
- Chunkai Fan
- Xiaobao Wei
- Jintao Chen
- Hao Wang
- Ying Li
- Xiaozhu Ju
- Jian Tang
- Shanghang Zhang
topics:
- interactive-world-model
- robot-world-model
- vision-language-action
- robot-data-scaling
- sim2real
- manipulation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# IOI: Decoupling Kinematics and Physics for Interactive World Models

## Summary
IOI is an interactive robot world model that uses exact robot kinematics to guide video generation, so the model has less burden to learn robot motion from pixels alone. It targets action-conditioned rollouts for robot policy training and evaluation.

## Problem
- Robot policies need simulated environments that respond to actions with realistic video and plausible contact dynamics.
- Purely learned action-to-video world models can drift away from commanded robot motion and can generate impossible object states, such as penetration, deformation, or lost object permanence.
- This matters because bad rollouts can mislead policy learning and make simulated policy evaluation unreliable.

## Approach
- IOI takes the robot URDF and future action sequence, converts actions into joint states with integration or inverse kinematics, then computes link poses with forward kinematics.
- It renders the computed robot geometry into front, side, and top orthographic views, which avoids extrinsic camera calibration for aligning rendered motion with observed scenes.
- The Multi-view Kinematic Aggregation and Injection module fuses the three rendered views into kinematic tokens, aligns them with video tokens, and injects them into a frozen diffusion transformer through trainable kinematic blocks.
- The video generator uses flow matching in latent space: history frames condition the scene, kinematic tokens condition robot motion, and the generator predicts future frames and scene interactions.

## Results
- On the RoboTwin table excerpt, IOI reports the best overall SSIM: 0.8637 versus 0.8198 for IRASim and 0.8192 for Ctrl-World.
- IOI reports the best overall LPIPS: 0.0695 versus 0.0803 for IRASim and 0.0867 for Ctrl-World. Lower is better.
- IOI reports the best overall FVD: 41.23 versus 126.20 for IRASim and 64.90 for Ctrl-World. Lower is better.
- Overall PSNR is mixed: IOI reports 25.73, below IRASim at 26.81 and above Ctrl-World at 25.50.
- On Move Can Pot, IOI reports 30.41 PSNR, 0.9288 SSIM, 0.0310 LPIPS, and 89.43 FVD, beating both listed baselines on all four metrics for that task.
- The excerpt also claims zero-shot OOD generalization, policy evaluation close to ground-truth physics simulators, and real-world policies trained on IOI-synthesized data matching teleoperation-trained policies, but it provides no quantitative values for those claims in the shown text.

## Link
- [https://arxiv.org/abs/2606.23296v1](https://arxiv.org/abs/2606.23296v1)
