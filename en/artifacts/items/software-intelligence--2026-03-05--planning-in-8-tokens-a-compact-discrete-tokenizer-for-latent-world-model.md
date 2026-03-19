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
- world-models
- discrete-tokenizer
- model-predictive-control
- visual-planning
- latent-representation
relevance_score: 0.35
run_id: materialize-outputs
language_code: en
---

# Planning in 8 Tokens: A Compact Discrete Tokenizer for Latent World Model

## Summary
CompACT proposes an extremely compressed discrete image tokenizer for planning with world models, compressing each frame observation to as few as 8 tokens to significantly reduce decision-time planning cost. The core claim is that planning does not need photo-level detail; it only needs semantic information related to actions and spatial relations.

## Problem
- Existing world models often encode a single image into hundreds of tokens, and attention computation grows approximately quadratically with the number of tokens, making planning too slow and unsuitable for real-time control.
- This matters because although world models can improve sample efficiency and support MPC/decision-time planning, if each planning step takes a long time, they are difficult to use in real systems such as robotics and navigation.
- The paper specifically notes that existing navigation world models can take **up to about 3 minutes** of planning per episode on a single RTX 6000 ADA, creating a deployment bottleneck.

## Approach
- **CompACT** compresses each image into **16 or 8 discrete tokens**; the 8-token version is about **128 bits/image** (8 16-bit tokens), dramatically shortening sequence length compared with the **784 tokens** of the SD-VAE used in NWM.
- On the encoding side, instead of training a standard encoder for pixel reconstruction, it uses a **frozen DINOv3 vision foundation model** to extract semantic features, then distills planning-critical semantics (objects, layout, spatial relations) through a small number of learnable queries with a **cross-attention resampler**.
- To avoid the difficulty of reconstructing pixels directly from so few tokens, the decoding side switches to **conditional generation**: it first predicts pretrained **VQGAN/MaskGIT** target tokens (typically **196 tokens @ 224×224**), and then its decoder generates the image, turning “decompression” into a more feasible semantic conditional generation task.
- The world model learns action-conditioned transitions directly in this **extremely small discrete latent space**, using **masked generative modeling** to predict next-step tokens, so MPC rollouts operate only at the 8/16-token level.
- Because it uses discrete tokens and MaskGIT-style parallel/non-autoregressive generation, future-state prediction avoids the hundreds of denoising steps common in diffusion models, further reducing planning latency.

## Results
- On **RECON** navigation planning, an action-conditioned world model trained with the CompACT tokenizer achieves **comparable planning accuracy** to a model using **784 continuous tokens**, while delivering about a **40× planning latency speedup**.
- The paper claims its **8-token model outperforms the previous 64-token tokenizer**, suggesting that “carefully designed extreme compression” is not only faster but may also yield better planning performance; however, the excerpt **does not provide specific ATE/RPE values**.
- On **RoboNet** action-conditioned video prediction, CompACT is reported to achieve **comparable action regression performance** to a previous tokenizer using **16× more tokens**, while maintaining strong action consistency; however, the excerpt **does not provide specific L1/R²/APE values**.
- At the representation-compression level, the paper gives the most intuitive scale comparison: **8 tokens vs 784 tokens**, with the intermediate target tokenizer typically using **196 tokens**; its core conclusion is that planning-critical semantics can be preserved in far fewer tokens than traditional methods.
- Its strongest concrete claim about real-time usability is that, compared with existing planning costs reaching **3 minutes/episode**, CompACT pushes world-model planning toward a speed range closer to practical deployment.

## Link
- [http://arxiv.org/abs/2603.05438v1](http://arxiv.org/abs/2603.05438v1)
