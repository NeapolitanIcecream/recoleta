---
source: arxiv
url: http://arxiv.org/abs/2603.05438v1
published_at: '2026-03-05T18:00:02'
authors:
- Dongwon Kim
- Gawon Seo
- Jinsung Lee
- Minsu Cho
- Suha Kwak
topics:
- world-model
- latent-tokenizer
- planning
- model-predictive-control
- robotics
- discrete-latents
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Planning in 8 Tokens: A Compact Discrete Tokenizer for Latent World Model

## Summary
This paper proposes CompACT, a compact tokenizer that compresses each image into only 8 discrete tokens to accelerate planning in latent world models. The core claim is that planning does not require high-fidelity pixel details, but only semantic and spatial information relevant to action decisions.

## Problem
- Existing world models often encode a single frame into hundreds of tokens, causing the computation of attention-based planning to grow quadratically with the number of tokens, making real-time control difficult.
- Many generative world models pursue photorealistic reconstruction, preserving high-frequency details such as texture and lighting that are not critical for planning, resulting in unnecessary representational redundancy.
- This matters because if planning latency is too high, then even a world model with strong predictive ability is hard to use for online decision-making in real robots or navigation systems.

## Approach
- Proposes **CompACT**: encoding each image into **16 or 8 discrete tokens**, with the 8-token setting corresponding to about **128 bits/image** (**8 tokens x 16 bits**).
- The encoder is no longer trained end-to-end for reconstruction, but is built on top of a **frozen DINOv3 vision encoder**; a small number of learnable queries extract object-level semantics and spatial relationships from its features through cross-attention, followed by discrete quantization to obtain compact tokens.
- The decoder does not reconstruct pixels directly from 8/16 tokens. Instead, it uses them as conditioning to **generate the high-dimensional target tokens of a pretrained VQGAN/MaskGIT**, after which the target decoder reconstructs the image. Put simply: the “compact tokens preserve semantics, while generative decoding fills in appearance details.”
- During world model training, the authors directly learn **action-conditioned next-step prediction** on this set of ultra-compact discrete tokens, using masked generative modeling; during planning, they combine MPC/CEM to search action sequences through latent-space rollouts.
- Because discrete tokens can be predicted quickly via MaskGIT-style unmasking, avoiding the multi-step diffusion denoising commonly required by continuous latents, inference cost is further reduced.

## Results
- In **RECON** navigation planning, the action-conditioned world model using CompACT achieves planning accuracy **comparable** to a model using **784 continuous tokens**, but with **about 40x faster planning latency**.
- The authors claim that their **8-token** model outperforms a previous tokenizer using **64 tokens**, suggesting that extreme compression, when carefully designed, can be not only faster but also potentially better for planning.
- The paper notes that existing methods in the **NWM** family can require **up to about 3 minutes** to plan a single episode (on a single RTX 6000 ADA GPU), whereas CompACT aims to bring this latency closer to a practically real-time level.
- In **RoboNet** action-conditioned video prediction, CompACT’s latent variables support **action regression performance comparable to prior tokenizers using 16x more tokens**, while maintaining strong action consistency.
- The excerpt does not provide more complete table values (such as specific absolute values for ATE/RPE, APE, or IDM), but the strongest quantitative takeaway is: **8 tokens vs. 784 tokens achieve similar planning performance, with about a 40x speedup in planning**.

## Link
- [http://arxiv.org/abs/2603.05438v1](http://arxiv.org/abs/2603.05438v1)
