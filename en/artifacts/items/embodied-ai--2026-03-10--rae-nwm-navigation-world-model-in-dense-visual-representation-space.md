---
source: arxiv
url: http://arxiv.org/abs/2603.09241v1
published_at: '2026-03-10T06:16:23'
authors:
- Mingkun Zhang
- Wangtian Shen
- Fan Zhang
- Haijian Qin
- Zihao Pei
- Ziyang Meng
topics:
- world-model
- visual-navigation
- dinov2
- diffusion-transformer
- representation-learning
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# RAE-NWM: Navigation World Model in Dense Visual Representation Space

## Summary
RAE-NWM proposes learning a navigation world model in a **dense visual representation space** rather than a VAE-compressed latent space, to reduce structural collapse and action drift in long-horizon prediction. The core idea is to leverage DINOv2 features, which are easier to model with linear action-conditioned dynamics, and to use a diffusion Transformer to generate future states in that space.

## Problem
- Existing navigation world models mostly predict future observations in a VAE-compressed latent space, but compression loses fine-grained geometric structure, leading to structural degradation and kinematic drift in long rollout prediction.
- This directly weakens downstream planning and navigation, because a world model must not only “generate realistic images” but also maintain spatial stability and controllability of actions.
- The problem the authors aim to solve is: how to choose a visual state space better suited for action-conditioned dynamics modeling, and how to perform stable long-horizon navigation prediction within it.

## Approach
- First, they conduct a **linear dynamics probe**: freeze different visual encoders and train only a linear model to predict future states under action conditioning; the results show that dense DINOv2 features have stronger linear predictability than VAE, MAE, SigLIP, ResNet50, and others.
- Based on this, they propose **RAE-NWM**: use frozen DINOv2 to extract uncompressed patch tokens, and use a frozen RAE decoder to reconstruct images only when visualization or pixel-level evaluation is needed.
- They train a **Conditional Diffusion Transformer with Decoupled Head (CDiT-DH)** in representation space, directly modeling continuous visual state transitions with flow matching rather than discrete token autoregressive prediction.
- They introduce a **time-driven gating** dynamic conditioning module: it adjusts the injection strength of action and prediction-horizon conditions according to diffusion/flow time, emphasizing kinematic priors more in the early stage and relaxing later to preserve detail and reduce artifacts.
- Downstream planning is performed directly in representation space, avoiding geometric distortion and information loss caused by pixel decoding.

## Results
- On **direct long-horizon prediction** on the SACSoN dataset, RAE-NWM is significantly better than NWM: LPIPS drops from **0.407/0.470** to **0.303/0.349** (4s/16s), DreamSim from **0.229/0.281** to **0.145/0.171**, DINO Distance from **0.402/0.460** to **0.327/0.367**, and FID from **26.15/33.06** to **15.09/15.90**.
- The paper claims that in **16-second sequential rollout prediction**, RAE-NWM maintains stronger temporal stability and structural consistency; the figures show that the baseline NWM suffers obvious structural collapse in later stages, while RAE-NWM still preserves geometric integrity.
- On **trajectory prediction/planning-related evaluation**, RAE-NWM outperforms NWM on SACSoN and SCAND: on SACSoN, ATE/RPE improves from **4.12/0.96** to **2.91/0.70**, and on SCAND from **1.28/0.33** to **1.14/0.28**.
- On RECON, RAE-NWM achieves **ATE 1.36, RPE 0.37**, which is slightly worse than NWM’s **1.13, 0.35**, indicating that the improvement does not uniformly lead on every dataset.
- The quantitative values for the linear probe are not given in the excerpt, but the authors explicitly claim that the DINOv2 uncompressed token space shows higher global $R^2$ across the full prediction horizon, and that performance drops significantly after spatial shuffling, supporting the argument that “spatial structure itself helps action-conditioned dynamics modeling.”

## Link
- [http://arxiv.org/abs/2603.09241v1](http://arxiv.org/abs/2603.09241v1)
