---
source: arxiv
url: http://arxiv.org/abs/2603.03739v1
published_at: '2026-03-04T05:19:20'
authors:
- Zehua Fan
- Wenqi Lyu
- Wenxuan Song
- Linge Zhao
- Yifei Yang
- Xi Wang
- Junjie He
- Lida Huang
- Haiyan Liu
- Bingchuan Sun
- Guangjun Bao
- Xuanyao Mao
- Liang Xu
- Yan Wang
- Feng Gao
topics:
- vision-language-navigation
- streaming-vla
- 3d-spatial-encoder
- latent-prediction
- embodied-ai
relevance_score: 0.22
run_id: materialize-outputs
language_code: en
---

# PROSPECT: Unified Streaming Vision-Language Navigation via Semantic--Spatial Fusion and Latent Predictive Representation

## Summary
PROSPECT is a unified streaming model for vision-language navigation that places action decision-making, 2D semantic understanding, 3D spatial understanding, and “predicting the next-step latent representation” into a single framework. Its key idea is to use latent-space prediction to improve long-horizon navigation and real-robot robustness without increasing inference overhead.

## Problem
- Existing zero-shot/end-to-end VLN has strong semantic understanding, but usually lacks explicit modeling of **future states, environment dynamics, and spatial structure**, making long-horizon navigation more prone to failure.
- Relying only on 2D semantic encoders lacks stable spatial perception; meanwhile, some 3D encoders are expensive under long-context settings, require truncating history, or provide only relative-scale representations, which is unfavorable for streaming navigation.
- Directly predicting explicit modalities such as pixels or depth can easily overfit irrelevant details like texture and lighting, weakening robustness across scenes and under complex illumination.

## Approach
- Use a **streaming Vision-Language-Action** framework for navigation: input instructions and continuous RGB observations, and output discrete navigation actions.
- Use **SigLIP** to extract 2D semantic features, and **CUT3R** as a streaming 3D foundation spatial encoder to extract **absolute-scale** spatial features, then fuse them through **cross-attention** into a unified representation for the policy.
- During training, introduce learnable **stream query tokens** that “query back” into long-horizon streaming context to predict next-step **2D/3D latent features**. Supervision comes from frozen SigLIP/CUT3R teachers rather than pixel prediction.
- Design a dedicated **streaming causal attention mask**: ensuring queries can only see the present and past, not the future; queries from different time steps are isolated from each other; and 2D/3D queries are mutually masked to avoid information leakage and task interference.
- During inference, the **predictive branch is removed**, so predictive learning shapes internal representations only during training and **does not increase inference latency**.

## Results
- On **VLN-CE R2R val-unseen** (monocular RGB), PROSPECT(*) compared with **StreamVLN(*)** achieves **NE 5.31 vs 5.47**, **OSR 60.3 vs 57.8**, **SR 52.0 vs 50.8**, and **SPL 46.2 vs 45.7**.
- Under a stronger training setting on **R2R val-unseen**, PROSPECT(†) reaches **NE 4.92 / OSR 65.2 / SR 58.9 / SPL 54.0**, outperforming **StreamVLN(†)** at **5.10 / 64.0 / 55.7 / 50.9**; the relative gains are **NE -0.18, OSR +1.2, SR +3.2, SPL +3.1**, respectively.
- On the longer-horizon and more complex **RxR val-unseen**, PROSPECT(†) achieves **NE 5.70 / SR 54.6 / SPL 46.2 / nDTW 62.1**, outperforming **StreamVLN(†)** at **6.22 / 52.9 / 46.0 / 61.9**; this indicates greater robustness on complex instructions and long-horizon tasks.
- Ablation experiments (R2R val-unseen) show that from the **SigLIP-only baseline** to the full model **(+WM-2D + WM-3D)**: **SR 45.5 → 48.7**, **SPL 41.6 → 42.9**, **OSR 53.8 → 57.6**, and **NE 6.05 → 5.82**, indicating that both 3D fusion and latent representation prediction are effective.
- In the spatial encoder ablation, **VGGT** is **OOM** under this streaming long-context setting; **InfiniteVGGT** achieves **0.284s/step, SR 43.2, SPL 38.0, OSR 54.4, NE 6.61**; **CUT3R** achieves **0.245s/step, SR 48.7, SPL 42.9, OSR 57.6, NE 5.82**, showing it is faster and performs better.
- By task length, on **long-horizon tasks (≥100)** relative to the baseline, the full model achieves **SR +4.14 (20.18→24.32)**, **SPL +3.64 (10.61→14.25)**, **OSR +6.54 (34.21→40.75)**, and **NE -0.37 (9.11→8.74)**; real-robot deployment runs at about **0.25–0.27 s/step (about 4 Hz)** and claims robustness across indoor/outdoor settings and diverse lighting conditions.

## Link
- [http://arxiv.org/abs/2603.03739v1](http://arxiv.org/abs/2603.03739v1)
