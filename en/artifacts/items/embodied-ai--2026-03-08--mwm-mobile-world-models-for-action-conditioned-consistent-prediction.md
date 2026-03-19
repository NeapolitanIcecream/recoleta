---
source: arxiv
url: http://arxiv.org/abs/2603.07799v1
published_at: '2026-03-08T20:54:50'
authors:
- Han Yan
- Zishang Xiang
- Zeyu Zhang
- Hao Tang
topics:
- world-model
- mobile-robot-navigation
- diffusion-model
- model-predictive-control
- consistency-distillation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# MWM: Mobile World Models for Action-Conditioned Consistent Prediction

## Summary
MWM is a world model for mobile robot navigation that focuses on solving the problem that “predicted frames look plausible, but are inconsistent with the true trajectory induced by the actions.” Through consistency post-training and inference-oriented consistency distillation, it enables reliable planning even with few-step diffusion inference.

## Problem
- Existing navigation world models can generate realistic future images, but they are **not necessarily consistent with the true future corresponding to a given action sequence**; errors accumulate during multi-step rollout and mislead MPC planning.
- Online robot deployment requires **fast inference**, but common few-step diffusion/distillation methods mainly preserve distributional similarity and **do not explicitly preserve rollout consistency**, leading to a training–inference mismatch.
- This matters because navigation planning depends on imagined trajectories; if the predicted endpoint location is off, the robot may choose the wrong action, directly affecting success rate and safety.

## Approach
- Proposes a two-stage training scheme: **Stage I structural pretraining** first uses teacher forcing to learn scene structure, geometry, and appearance; **Stage II ACC post-training** then lets the model use its own predictions as context during autoregressive rollout to specifically reduce error accumulation.
- The core idea of ACC is simple: during training, instead of always feeding the real previous frame, the model is made to “look at its own generated history,” and a multi-frame **LPIPS perceptual loss** is used to pull the predicted trajectory closer to the real observation trajectory.
- To avoid damaging the high-fidelity generation learned in the first stage, the main **CDiT** backbone is **frozen** during post-training, and only the lightweight **AdaLN/LoRA** layers that inject action/time-step information are updated.
- Proposes **ICSD (Inference-Consistent State Distillation)**: it changes few-step diffusion distillation from “matching the output distribution” to “preserving action-conditioned consistency,” and reduces the training–inference gap caused by truncated denoising through a state more consistent with the inference endpoint.
- In the planning stage, it continues to use **CEM-based MPC**, searching for action sequences in the world-model rollout space and scoring them with LPIPS similarity between the final frame and the goal image.

## Results
- **Action-conditioned consistency (SCAND)**: MWM (DDIM 5) outperforms NWM at all rollout horizons. For example, **16s DreamSim 0.337 vs 0.373 (NWM DDIM 25) vs 0.568 (NWM DDIM 5)**; **16s LPIPS 0.495 vs 0.569 vs 0.734**. The authors summarize this as a **20.4% reduction** in DreamSim.
- **Visual quality (SCAND FID)**: MWM (DDIM 5) also outperforms the slower NWM (DDIM 25) at multiple horizons, e.g. **1s: 80.97 vs 96.68**, **8s: 85.80 vs 91.29**, **16s: 93.12 vs 93.63**; the overall claim relative to NWM is a **17.5% reduction** in FID.
- **Inference efficiency**: average rollout time is **2.3s** (MWM DDIM 5) vs **9.6s** (NWM DDIM 25) vs **2.6s** (NWM DDIM 5), i.e. at least a **4× speedup** relative to the main baseline, while reducing denoising steps from the 25/250 range down to **5 steps**.
- **Navigation performance (SCAND)**: MWM achieves **ATE 1.14, RPE 0.302**, outperforming **NWM’s 1.28 / 0.33**, as well as GNM, NoMaD, and others; the authors summarize this as **10.9% improvement** in ATE and **8.5% improvement** in RPE.
- **Real-robot deployment**: the paper claims a **50% relative improvement** in success rate over the baseline, as well as a **32.1% reduction** in navigation error.
- **Strongest concrete takeaway**: MWM shows that if few-step diffusion is trained explicitly around “action-conditioned rollout consistency,” rather than only preserving single-frame distribution realism, it can simultaneously improve planning reliability, visual fidelity, and real-time performance.

## Link
- [http://arxiv.org/abs/2603.07799v1](http://arxiv.org/abs/2603.07799v1)
