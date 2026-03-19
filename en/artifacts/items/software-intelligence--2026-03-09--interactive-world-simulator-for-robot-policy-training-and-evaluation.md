---
source: arxiv
url: http://arxiv.org/abs/2603.08546v1
published_at: '2026-03-09T16:13:32'
authors:
- Yixuan Wang
- Rhythm Syed
- Fangyu Wu
- Mengchao Zhang
- Aykut Onol
- Jose Barreiros
- Hooshang Nayyeri
- Tony Dear
- Huan Zhang
- Yunzhu Li
topics:
- world-models
- robot-learning
- video-prediction
- imitation-learning
- policy-evaluation
relevance_score: 0.46
run_id: materialize-outputs
language_code: en
---

# Interactive World Simulator for Robot Policy Training and Evaluation

## Summary
This paper proposes Interactive World Simulator (IWS), an interactive world model for robot policy training and evaluation, with an emphasis on achieving long-horizon, stable, physically consistent video-level simulation on a single consumer-grade GPU. Its core value is training an interactive surrogate environment from a moderately sized real interaction dataset, enabling low-cost demonstration generation and reproducible policy evaluation.

## Problem
- Existing action-conditioned video prediction/world models are often **too slow**, or **gradually drift and become unstable** during long-horizon rollouts, making them difficult to use for practical robot training and evaluation.
- This matters because robot imitation learning depends on large amounts of real demonstrations, which are expensive to collect; meanwhile, real-world evaluation is slow, hard to reproduce, and difficult to compare fairly.
- The goal is to build an interactive simulator trained only on **RGB images + actions** that is both fast and stable, while realistically reflecting real robot-object interactions.

## Approach
- It uses a **two-stage latent world model**: first compressing images into compact 2D latents, then predicting the future only in latent space, thereby reducing computational cost and improving long-horizon stability.
- In stage 1, an autoencoder is trained: a CNN encoder extracts latents, and a **consistency-model decoder** performs high-fidelity image reconstruction in a small number of steps.
- In stage 2, the autoencoder is frozen, and an **action-conditioned latent dynamics consistency model** is trained to predict the next-frame latent from past latents and actions; the model uses 3D convolutions, FiLM modulation, and spatiotemporal attention to model multimodal futures.
- At inference time, it uses an **autoregressive sliding window** to generate long-horizon video, while injecting small amounts of noise into the context so the model learns to tolerate the accumulated errors caused by “predicting from its own predictions.”
- At the application layer, the authors directly collect human teleoperation demonstrations inside the world model, and seamlessly use the generated data to train imitation learning policies such as DP, ACT, π0, and π0.5, while also enabling closed-loop, reproducible evaluation of policies in the simulator.

## Results
- **Long-horizon stability and speed**: the model can sustain interactive simulation for **more than 10 minutes** at **15 FPS** on a **single RTX 4090**; the paper also states that for the mug grasping task the model size is only **176.02 MB**, and training takes about **6 hours (stage 1) + 12 hours (stage 2)**, all on a single H200.
- **Video prediction metrics outperform baselines across the board**: under a 7-task aggregate, **192-step long-horizon prediction** setting, IWS achieves better metrics than DINO-WM/UVA/Dreamer4/Cosmos: **MSE 0.005** (vs 0.028/0.023/0.012/0.019), **LPIPS 0.051** (vs 0.270/0.272/0.163/0.224), **FID 63.50** (vs 200.77/142.55/239.97/200.74), **PSNR 25.82** (vs 17.79/17.87/20.81/18.91), **SSIM 0.831** (vs 0.652/0.650/0.693/0.647), **UIQI 0.960** (vs 0.875/0.884/0.919/0.883), **FVD 243.20** (vs 1752.57/2213.29/1747.26/799.34).
- **Data generation for imitation learning**: the authors train DP, ACT, π0, and π0.5 under different mixture ratios ranging from **100% simulated data to 100% real data**, and claim that **policy performance is comparable across all ratios**, suggesting that world-model-generated demonstrations are close in quality to real demonstrations of the same scale; however, the excerpt **does not provide specific success-rate numbers**.
- **Validity for policy evaluation**: the authors report a **strong correlation** between simulator performance and real-world performance across multiple tasks and training checkpoints, indicating that it can be used for scalable, reproducible policy evaluation; however, the excerpt **does not provide concrete values such as correlation coefficients**.
- **Data scale and task coverage**: experiments cover **1 MuJoCo task + 6 real robot tasks**; each real-world task contains about **600 episodes × 200 steps**, involving rigid objects, deformable objects, articulated objects, object piles, and multi-object interactions, suggesting broad applicability of the method.

## Link
- [http://arxiv.org/abs/2603.08546v1](http://arxiv.org/abs/2603.08546v1)
