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
- world-models
- robot-navigation
- diffusion-models
- model-predictive-control
- consistency-distillation
relevance_score: 0.31
run_id: materialize-outputs
language_code: en
---

# MWM: Mobile World Models for Action-Conditioned Consistent Prediction

## Summary
MWM is a mobile world model for robot navigation, designed to generate more consistent and more planning-usable future visual predictions given an action sequence. Through two-stage training and inference-oriented consistency distillation, it improves prediction quality, trajectory accuracy, and real-world deployment success rates while also enabling faster sampling.

## Problem
- Existing navigation world models can generate future frames that “look realistic,” but those frames are not necessarily consistent with what the same action sequence would produce in the real world, so long-horizon rollouts gradually drift.
- This action-conditioned inconsistency directly undermines MPC/CEM-based planning, because the planner can be misled by imagined trajectories that appear plausible but are actually wrong.
- Diffusion-model deployment also requires few-step inference acceleration, but existing distillation methods mainly preserve distributional similarity and do not explicitly preserve multi-step rollout consistency, leading to a training–inference mismatch.

## Approach
- Proposes **two-stage training**: first, structure pretraining uses teacher forcing to learn high-fidelity scene structure and appearance; then **ACC (Action-Conditioned Consistency) post-training** lets the model use its own generated historical predictions as context during training, reducing error accumulation at test time.
- The core idea of ACC is simple: train not only for “the next frame looks right,” but for “when these actions are executed continuously, the entire predicted trajectory stays closer to real observations.”
- During post-training, the backbone CDiT is frozen, and only lightweight AdaLN/LoRA modulation layers are updated, so as to preserve the image details learned in the first stage while correcting action-conditioned consistency.
- Proposes **ICSD (Inference-Consistent State Distillation)**: few-step diffusion distillation is formulated as consistency distillation aligned with real inference states, narrowing the gap between truncated states during training and the final states encountered in actual few-step inference.
- In the planning stage, it continues to use CEM-based MPC, searching for action sequences in the world-model rollout space and scoring them by perceptual similarity between the final frame and the goal image.

## Results
- On **SCAND**, MWM (DDIM 5) shows significantly better action-conditioned consistency than **NWM (DDIM 5)**: for example, **16s DreamSim 0.337 vs 0.568** and **16s LPIPS 0.495 vs 0.734**; relative to the overall statement in the paper abstract, DreamSim is reduced by up to **20.4%**.
- Even compared with the slower **NWM (DDIM 25)**, MWM (DDIM 5) still performs better: for example, **1s DreamSim 0.244 vs 0.309** and **8s LPIPS 0.459 vs 0.540**, indicating that it can maintain more consistent rollouts even with fewer sampling steps.
- In visual fidelity, on **SCAND FID**, MWM (DDIM 5) outperforms NWM: **1s 80.97 vs 96.68 (NWM DDIM 25)** and **8s 85.80 vs 91.29**; the abstract states an overall **17.5% reduction in FID**.
- In inference efficiency, the average rollout time is **2.3s**, about **4.2×** faster than **9.6s** for **NWM (DDIM 25)**, and also slightly faster than **2.6s** for **NWM (DDIM 5)**; the paper also describes this as at least a **4× speedup**, with denoising steps reduced from the default **250 to 5** (at least an **80%+** reduction in step count).
- In navigation performance, for goal-image navigation on **SCAND**, MWM reaches **ATE 1.14, RPE 0.302**, outperforming **NWM with ATE 1.28, RPE 0.33**, corresponding to the abstract’s claimed **10.9% improvement in ATE** and **8.5% improvement in RPE**.
- In real-world deployment, the abstract claims a **50% improvement in success rate** over the baseline and a **32.1% reduction in navigation error**; this is the paper’s strongest real-robot result claim.

## Link
- [http://arxiv.org/abs/2603.07799v1](http://arxiv.org/abs/2603.07799v1)
