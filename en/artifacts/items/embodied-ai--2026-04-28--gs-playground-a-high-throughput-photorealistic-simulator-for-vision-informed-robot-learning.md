---
source: arxiv
url: https://arxiv.org/abs/2604.25459v1
published_at: '2026-04-28T10:05:39'
authors:
- Yufei Jia
- Heng Zhang
- Ziheng Zhang
- Junzhe Wu
- Mingrui Yu
- Zifan Wang
- Dixuan Jiang
- Zheng Li
- Chenyu Cao
- Zhuoyuan Yu
- Xun Yang
- Haizhou Ge
- Yuchi Zhang
- Jiayuan Zhang
- Zhenbiao Huang
- Tianle Liu
- Shenyu Chen
- Jiacheng Wang
- Bin Xie
- Xuran Yao
- Xiwa Deng
- Guangyu Wang
- Jinzhi Zhang
- Lei Hao
- Zhixing Chen
- Yuxiang Chen
- Anqi Wang
- Hongyun Tian
- Yiyi Yan
- Zhanxiang Cao
- Yizhou Jiang
- Hanyang Shao
- Yue Li
- Lu Shi
- Bokui Chen
- Wei Sui
- Hanqing Cui
- Yusen Qin
- Ruqi Huang
- Lei Han
- Tiancai Wang
- Guyue Zhou
topics:
- robot-simulation
- vision-based-rl
- gaussian-splatting
- sim2real
- robot-data-scaling
- contact-rich-manipulation
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# GS-Playground: A High-Throughput Photorealistic Simulator for Vision-Informed Robot Learning

## Summary
GS-Playground is a simulator for training vision-based robot policies with photorealistic 3D Gaussian Splatting images at high speed. It targets visual RL, real-to-sim scene creation, contact-rich manipulation, navigation, and locomotion.

## Problem
- Vision-based robot RL needs many parallel simulation steps, but high-resolution photorealistic rendering can exhaust GPU memory and slow training.
- Building simulation-ready scenes from real captures still takes manual work because visual assets, collision geometry, pose, scale, and physical consistency must line up.
- The problem matters because contact-rich robot skills often need simulation scale, while visual policies need images close enough to real camera input for sim-to-real transfer.

## Approach
- The system combines a custom parallel physics engine with a batched 3D Gaussian Splatting renderer, so physics states and rendered images update together across many environments.
- The physics solver uses a velocity-impulse contact formulation, Projected Gauss-Seidel solving, constraint islands, and warm-starting to handle rigid contact and friction.
- The renderer prunes 3DGS points and batches many scenes, which reduces memory use while keeping visual quality close to the original reconstruction.
- Rigid-Link Gaussian Kinematics binds Gaussian clusters to simulated rigid bodies, so rendered objects move with the physics bodies during contacts and motion.
- The Real2Sim pipeline uses Grounding DINO, SAM/SAM2, LaMa, SAM-3D, AnySplat, and Speedy-splat to turn RGB captures into 3DGS assets, meshes, depth, pose, scale, and collision-ready scene elements.

## Results
- The paper claims about 10,000 FPS 3DGS rendering at 640×480 on an NVIDIA RTX 4090 and Intel i9-14900K; the comparison table lists DISCOVERSE at about 650 FPS and GS-Playground at about 10k FPS.
- The batch renderer supports up to 2048 scenes at 640×480 with total throughput up to 10,000 FPS.
- The 3DGS pruning step removes more than 90% of Gaussians while keeping PSNR loss below 0.05.
- The simulator supports up to 4096 3DGS environments in the comparison table, matching GaussGym on environment count while adding dynamic 3DGS scenes.
- Warm-starting reduces Projected Gauss-Seidel iterations from more than 50 to fewer than 10 in stable stacking tasks.
- The physics benchmark includes a 10 ms timestep Boston Dynamics Spot stability test and Newton’s Cradle contact tests, with claimed lower energy bleed than MuJoCo and better stability in the shown contact cases.

## Link
- [https://arxiv.org/abs/2604.25459v1](https://arxiv.org/abs/2604.25459v1)
